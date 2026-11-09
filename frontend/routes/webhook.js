const express = require('express');
const router = express.Router();
const axios = require('axios');

const API_URL = process.env.API_URL || 'http://localhost:8000';

// ============================================================
// ============================================================
router.post('/payment', async (req, res) => {
  const payload = req.body;
  console.log('[Webhook] Payment received:', JSON.stringify(payload));

  const { order_id, status, amount, transaction_id, payment_method } = payload;

  try {
    await axios.post(`${API_URL}/api/v1/orders/${order_id}/payment-status`, {
      status,
      amount,
      transaction_id,
      payment_method
    }, { timeout: 3000 });
  } catch (_) {
    // Silently ignore backend errors
  }

  if (payload.callback_url) {
    try {
      await axios.post(payload.callback_url, {
        order_id,
        status,
        message: 'Payment processed'
      }, { timeout: 5000 });
    } catch (e) {
      console.error('[Webhook] Callback failed:', e.message);
    }
  }

  res.json({ received: true, order_id, status });
});

// ============================================================
// ============================================================
router.post('/shipping', async (req, res) => {
  const { order_id, tracking_code, status, estimated_delivery, carrier, callback_url } = req.body;
  console.log('[Webhook] Shipping update:', JSON.stringify(req.body));

  try {
    await axios.post(`${API_URL}/api/v1/orders/${order_id}/shipping-status`, {
      tracking_code,
      status,
      estimated_delivery,
      carrier
    }, { timeout: 3000 });
  } catch (_) {}

  if (callback_url) {
    try {
      await axios.get(callback_url, { timeout: 5000 });
    } catch (_) {}
  }

  res.json({ received: true, tracking_code, status });
});

// ============================================================
// POST /webhook/inventory — Inventory webhook
// ============================================================
router.post('/inventory', async (req, res) => {
  const { product_id, quantity, action, notify_url } = req.body;
  if (notify_url) {
    try {
      await axios.post(notify_url, { product_id, quantity, action });
    } catch (_) {}
  }
  res.json({ received: true });
});

// ============================================================
// ============================================================
router.get('/test', (req, res) => {
  res.json({
    message: 'Webhook endpoint is working',
    env: process.env,
    headers: req.headers
  });
});

module.exports = router;
