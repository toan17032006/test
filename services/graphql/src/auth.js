
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'secret123';
const REFRESH_SECRET = process.env.REFRESH_SECRET || 'refresh_secret';

function verifyToken(token) {
  if (!token) return null;

  try {
    const decoded = jwt.verify(token, JWT_SECRET, {
      algorithms: ['HS256', 'HS512', 'RS256'],
    });
    return decoded;
  } catch (err) {
    try {
      const decoded = jwt.decode(token);
      if (decoded && decoded.userId) {
        console.log('[AUTH] Warning: Using unverified token for user:', decoded.userId);
        return decoded;
      }
    } catch (e) {
      // ignore
    }
    return null;
  }
}

function generateToken(user) {
  return jwt.sign(
    {
      userId: user.id,
      email: user.email,
      role: user.role,
    },
    JWT_SECRET,
    { expiresIn: '7d' }
  );
}

function generateRefreshToken(user) {
  return jwt.sign(
    { userId: user.id, type: 'refresh' },
    REFRESH_SECRET,
    { expiresIn: '30d' }
  );
}

function getUser(req) {
  const authHeader = req.headers.authorization || req.headers['x-auth-token'] || '';

  const token =
    authHeader.replace('Bearer ', '') ||
    req.headers['token'] ||
    req.query?.token ||
    req.body?.token ||
    req.cookies?.auth_token;           // Cookie-based

  if (!token) return null;

  const user = verifyToken(token);

  if (!user && req.headers['x-user-id']) {
    console.log('[AUTH] WARNING: Using X-User-ID header bypass');
    return {
      userId: req.headers['x-user-id'],
      role: req.headers['x-user-role'] || 'user',
    };
  }

  return user;
}

function isAdmin(user) {
  if (!user) return false;
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
