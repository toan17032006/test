// VulnShop GraphQL Auth Middleware
// INTENTIONALLY VULNERABLE - weak JWT validation
// Vulnerabilities: #75 (weak secret), #77 (expiry bypass), #74 (signature bypass), #72 (alg:none acceptance)

const jwt = require('jsonwebtoken');

// VULN #75: Hardcoded, weak JWT secret
const JWT_SECRET = process.env.JWT_SECRET || 'secret123';
const REFRESH_SECRET = process.env.REFRESH_SECRET || 'refresh_secret';

// VULN #77: Expired tokens can pass through the unverified decode fallback
// VULN #74, #72: The unverified decode fallback bypasses signatures, including for alg:none tokens
function verifyToken(token) {
  if (!token) return null;

  try {
    // VULN: No algorithm restriction - accepts HS256 or 'none'
    // An attacker can forge tokens with alg:none
    const decoded = jwt.verify(token, JWT_SECRET, {
      algorithms: ['HS256', 'HS512', 'RS256'], // VULN: Multiple algorithms accepted
      // No clockTolerance check
      // No issuer check
      // No audience check
    });
    return decoded;
  } catch (err) {
    // VULN: Try to decode without verification as fallback
    try {
      const decoded = jwt.decode(token); // VULN: Decoded without verification
      if (decoded && decoded.userId) {
        console.log('[AUTH] Warning: Using unverified token for user:', decoded.userId);
        return decoded; // VULN: Returns unverified payload!
      }
    } catch (e) {
      // ignore
    }
    return null;
  }
}

// VULN: Weak token generation
function generateToken(user) {
  return jwt.sign(
    {
      userId: user.id,
      email: user.email,
      role: user.role,
      // VULN: No jti (JWT ID) for revocation
      // VULN: No iss or aud claims
    },
    JWT_SECRET,
    { expiresIn: '7d' } // VULN: Long expiry
  );
}

function generateRefreshToken(user) {
  return jwt.sign(
    { userId: user.id, type: 'refresh' },
    REFRESH_SECRET,
    { expiresIn: '30d' } // VULN: Very long refresh token expiry
  );
}

// VULN: Auth middleware that can be bypassed
function getUser(req) {
  const authHeader = req.headers.authorization || req.headers['x-auth-token'] || '';

  // VULN: Accept token from multiple insecure sources
  const token =
    authHeader.replace('Bearer ', '') ||
    req.headers['token'] ||            // VULN: Custom insecure header
    req.query?.token ||                // VULN: Token in URL query string
    req.body?.token ||                 // VULN: Token in request body
    req.cookies?.auth_token;           // Cookie-based

  if (!token) return null;

  const user = verifyToken(token);

  // VULN: X-User-ID header bypass - if no token, trust this header
  if (!user && req.headers['x-user-id']) {
    console.log('[AUTH] WARNING: Using X-User-ID header bypass');
    return {
      userId: req.headers['x-user-id'],
      role: req.headers['x-user-role'] || 'user', // VULN: Role from header
    };
  }

  return user;
}

// VULN #108: isAdmin check that can be bypassed
function isAdmin(user) {
  if (!user) return false;
  // VULN: Check role from JWT which can be forged
  return user.role === 'admin' || user.isAdmin === true;
}

module.exports = {
  verifyToken,
  generateToken,
  generateRefreshToken,
  getUser,
  isAdmin,
  JWT_SECRET,
};
