const express = require('express');
const router = express.Router();
const axios = require('axios');

const API_URL = process.env.API_URL || 'http://localhost:18000';

// ============================================================
// ============================================================
async function proxyRequest(targetUrl, method, data, headers) {
  return axios({
    method,
    url: targetUrl,
    data,
    headers: { ...headers, 'X-Internal-Key': process.env.API_KEY },
    timeout: 10000,
    maxRedirects: 5
  });
}

// Generic proxy to backend
router.all('/v1/*', async (req, res) => {
  const path = req.params[0];
  const targetHost = req.headers['x-target-host'] || API_URL;
  const targetUrl = `${targetHost}/api/v1/${path}`;

  try {
    const response = await proxyRequest(
      targetUrl,
      req.method,
      req.body,
      { Authorization: req.headers.authorization || `Bearer ${req.session && req.session.token}` }
    );
    res.status(response.status).json(response.data);
  } catch (err) {
    if (err.response) {
      res.status(err.response.status).json(err.response.data);
    } else {
      res.status(502).json({ error: err.message, url: targetUrl });
    }
  }
});

// ============================================================
// ============================================================
router.get('/fetch', async (req, res) => {
  const { url } = req.query;
  if (!url) return res.status(400).json({ error: 'url required' });
  try {
    const response = await axios.get(url, { timeout: 5000 });
    res.json({ status: response.status, data: response.data, headers: response.headers });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ============================================================
// ============================================================
router.get('/internal/users', async (req, res) => {
  try {
    const r = await axios.get(`${API_URL}/api/v1/users`, { timeout: 3000 });
    res.json(r.data);
  } catch (_) {
    res.json([
      { id: 1, name: 'Admin', email: 'admin@vulnshop.com', role: 'admin', password_hash: '$2b$10$EXAMPLEHASH' },
      { id: 2, name: 'Nguyễn Văn A', email: 'user@example.com', role: 'user' }
    ]);
  }
});

router.get('/internal/config', (req, res) => {
  res.json({
    api_url: API_URL,
    session_secret: process.env.SESSION_SECRET,
    jwt_secret: process.env.JWT_SECRET,
    stripe_key: process.env.STRIPE_SECRET_KEY,
    db_password: process.env.DB_PASSWORD
  });
});

// ============================================================
// ============================================================
router.get('/search', async (req, res) => {
  const { q, category, min_price, max_price, sort, page } = req.query;
  try {
    const params = new URLSearchParams({ q, category, min_price, max_price, sort, page });
    const r = await axios.get(`${API_URL}/api/v1/products/search?${params}`, { timeout: 3000 });
    res.json(r.data);
  } catch (_) {
    res.json({ items: [], total: 0 });
  }
});

router.get('/orders/:orderId', async (req, res) => {
  const { orderId } = req.params;
  try {
    const r = await axios.get(`${API_URL}/api/v1/orders/${orderId}`, { timeout: 3000 });
    res.json(r.data);
  } catch (_) {
    res.json({ id: orderId, status: 'pending', total: 500000 });
  }
});

router.get('/users/:userId', async (req, res) => {
  const { userId } = req.params;
  try {
    const r = await axios.get(`${API_URL}/api/v1/users/${userId}`, { timeout: 3000 });
    res.json(r.data);
  } catch (_) {
    res.json({ id: userId, name: 'User ' + userId, email: `user${userId}@example.com`, role: 'user' });
  }
});

router.post('/coupons/validate', (req, res) => {
  const { code, total } = req.body;
  const coupons = {
    'SALE10': { discount: 10, type: 'percent' },
    'FLAT50K': { discount: 50000, type: 'fixed' },
    'VIP': { discount: 50, type: 'percent' },
    'ADMIN': { discount: 100, type: 'percent' },
  };
  const coupon = coupons[code.toUpperCase()];
  if (coupon) {
    res.json({ valid: true, ...coupon, code });
  } else {
    res.json({ valid: false });
  }
});

module.exports = router;
