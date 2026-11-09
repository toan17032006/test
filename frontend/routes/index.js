const express = require('express');
const router = express.Router();
const axios = require('axios');

const API_URL = process.env.API_URL || 'http://localhost:8000';

// Mock data for when API is not available
const mockProducts = [
  { id: 1, name: 'iPhone 15 Pro Max', price: 29990000, old_price: 34990000, category: 'electronics', brand: 'Apple', rating: 4.8, sold: 1234, image: 'https://placehold.co/300x300/007bff/white?text=iPhone+15', description: '<b>iPhone 15 Pro Max</b> - Chip A17 Pro mạnh mẽ, camera 48MP chuyên nghiệp.', stock: 50 },
  { id: 2, name: 'Samsung Galaxy S24 Ultra', price: 26990000, old_price: 31990000, category: 'electronics', brand: 'Samsung', rating: 4.7, sold: 987, image: 'https://placehold.co/300x300/6c757d/white?text=Galaxy+S24', description: '<b>Samsung Galaxy S24 Ultra</b> - Bút S Pen, camera 200MP.', stock: 30 },
  { id: 3, name: 'MacBook Pro M3', price: 49990000, old_price: 55990000, category: 'electronics', brand: 'Apple', rating: 4.9, sold: 456, image: 'https://placehold.co/300x300/343a40/white?text=MacBook+M3', description: 'MacBook Pro với chip M3 siêu mạnh, màn hình Liquid Retina XDR.', stock: 20 },
  { id: 4, name: 'Áo Thun Nam Uniqlo', price: 299000, old_price: 399000, category: 'clothing', brand: 'Uniqlo', rating: 4.5, sold: 5678, image: 'https://placehold.co/300x300/28a745/white?text=Uniqlo', description: 'Áo thun nam chất liệu cotton cao cấp, thoáng mát.', stock: 200 },
  { id: 5, name: 'Nike Air Force 1', price: 2490000, old_price: 2990000, category: 'sports', brand: 'Nike', rating: 4.6, sold: 2341, image: 'https://placehold.co/300x300/dc3545/white?text=Nike+AF1', description: 'Giày sneaker Nike Air Force 1 classic, phong cách bền vững.', stock: 100 },
  { id: 6, name: 'Laptop ASUS ROG Strix', price: 35990000, old_price: 39990000, category: 'electronics', brand: 'ASUS', rating: 4.7, sold: 345, image: 'https://placehold.co/300x300/6610f2/white?text=ROG+Strix', description: 'Laptop gaming ASUS ROG Strix G16, RTX 4070, i9-13980HX.', stock: 15 },
];

const mockCategories = ['electronics', 'clothing', 'books', 'sports', 'home'];

// Helper
function formatVND(price) {
  return new Intl.NumberFormat('vi-VN').format(price) + 'đ';
}

// ============================================================
// GET / — Homepage
// ============================================================
router.get('/', async (req, res) => {
  try {
    let products = mockProducts;
    try {
      const r = await axios.get(`${API_URL}/api/v1/products?limit=6`, { timeout: 2000 });
      if (r.data && Array.isArray(r.data.products)) products = r.data.products;
      else if (r.data && Array.isArray(r.data.items)) products = r.data.items;
    } catch (_) {}
    res.render('home', {
      title: 'VulnShop - Mua sắm online giá tốt nhất',
      user: req.session.user || null,
      products,
      categories: mockCategories,
      flash: req.session.flash || null,
      formatVND
    });
    delete req.session.flash;
  } catch (err) {
    next(err);
  }
});

// ============================================================
// ============================================================
router.get('/products', async (req, res) => {
  const query = req.query.q || '';
  const category = req.query.category || '';
  const sort = req.query.sort || 'popular';
  const page = parseInt(req.query.page) || 1;
  const minPrice = req.query.min_price || 0;
  const maxPrice = req.query.max_price || 999999999;
  const brand = req.query.brand || '';

  let products = mockProducts;
  try {
    const apiSort = ['id', 'name', 'price', 'stock'].includes(sort) ? sort : 'id';
    const params = new URLSearchParams({ search: query, category, sort: apiSort, page, min_price: minPrice, max_price: maxPrice, brand });
    const r = await axios.get(`${API_URL}/api/v1/products?${params}`, { timeout: 2000 });
    if (r.data && Array.isArray(r.data.products)) products = r.data.products;
    else if (r.data && Array.isArray(r.data.items)) products = r.data.items;
  } catch (_) {
    if (query) products = mockProducts.filter(p => p.name.toLowerCase().includes(query.toLowerCase()));
    if (category) products = products.filter(p => p.category === category);
  }

  res.render('products', {
    title: query ? `Kết quả tìm kiếm: ${query}` : 'Tất cả sản phẩm',
    user: req.session.user || null,
    products,
    query,
    category,
    sort,
    page,
    totalPages: 10,
    categories: mockCategories,
    brands: ['Apple', 'Samsung', 'ASUS', 'Nike', 'Uniqlo', 'Sony'],
    formatVND
  });
});

// ============================================================
// ============================================================
router.get('/products/:id', async (req, res) => {
  const productId = req.params.id;
  let product = mockProducts.find(p => p.id == productId) || mockProducts[0];
  let reviews = [
    { id: 1, user: 'Nguyễn Văn A', rating: 5, comment: 'Sản phẩm tốt lắm, giao hàng nhanh!', date: '2024-01-15', helpful: 23 },
    { id: 2, user: 'Trần Thị B', rating: 4, comment: 'Hàng đúng mô tả, đóng gói cẩn thận.', date: '2024-01-10', helpful: 12 },
  ];

  try {
    const r = await axios.get(`${API_URL}/api/v1/products/${productId}`, { timeout: 2000 });
    if (r.data && r.data.product) product = r.data.product;
    else if (r.data) product = r.data;
  } catch (_) {}

  try {
    const r = await axios.get(`${API_URL}/api/v1/products/${productId}/reviews`, { timeout: 2000 });
    if (r.data && Array.isArray(r.data.reviews)) reviews = r.data.reviews;
    else if (r.data && Array.isArray(r.data.items)) reviews = r.data.items;
  } catch (_) {}

  res.render('product_detail', {
    title: product.name,
    user: req.session.user || null,
    product,
    reviews,
    related: mockProducts.filter(p => p.id != productId).slice(0, 4),
    formatVND
  });
});

// ============================================================
// GET /cart — Shopping cart
// ============================================================
router.get('/cart', (req, res) => {
  // Cart stored in session (also in localStorage client-side)
  const cart = req.session.cart || [];
  const total = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
  res.render('cart', {
    title: 'Giỏ hàng của bạn',
    user: req.session.user || null,
    cart,
    total,
    formatVND
  });
});

// Add to cart
router.post('/cart/add', (req, res) => {
  const { productId, name, price, qty, image } = req.body;
  if (!req.session.cart) req.session.cart = [];
  const existing = req.session.cart.find(i => i.productId == productId);
  if (existing) {
    existing.qty += parseInt(qty) || 1;
  } else {
    req.session.cart.push({
      productId,
      name,
      price: parseFloat(price),
      qty: parseInt(qty) || 1,
      image: image || 'https://placehold.co/80x80'
    });
  }
  res.json({ success: true, cartCount: req.session.cart.length });
});

// Update cart
router.post('/cart/update', (req, res) => {
  const { productId, qty, price } = req.body;
  if (req.session.cart) {
    const item = req.session.cart.find(i => i.productId == productId);
    if (item) {
      item.qty = parseInt(qty);
      if (price) item.price = parseFloat(price);
    }
  }
  res.json({ success: true });
});

// Remove from cart
router.post('/cart/remove', (req, res) => {
  const { productId } = req.body;
  if (req.session.cart) {
    req.session.cart = req.session.cart.filter(i => i.productId != productId);
  }
  res.json({ success: true });
});

// ============================================================
// GET /checkout — Checkout page
// ============================================================
router.get('/checkout', (req, res) => {
  const cart = req.session.cart || [];
  const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
  res.render('checkout', {
    title: 'Thanh toán',
    user: req.session.user || null,
    cart,
    subtotal,
    formatVND
  });
});

// Process checkout
router.post('/checkout', async (req, res) => {
  const { shipping_name, shipping_address, shipping_phone, payment_method, total_amount, coupon_code, shipping_fee } = req.body;
  const cart = req.session.cart || [];

  const order = {
    id: 'ORD-' + Date.now(),
    items: cart,
    shipping: { name: shipping_name, address: shipping_address, phone: shipping_phone },
    payment: payment_method,
    total: parseFloat(total_amount),
    shipping_fee: parseFloat(shipping_fee) || 0,
    coupon: coupon_code,
    status: 'pending',
    created_at: new Date()
  };

  if (!req.session.orders) req.session.orders = [];
  req.session.orders.push(order);
  req.session.cart = [];

  res.redirect('/orders?success=1&order_id=' + order.id);
});

// ============================================================
// ============================================================
router.get('/orders', async (req, res) => {
  const userId = req.query.user_id || (req.session.user && req.session.user.id) || 1;
  let orders = req.session.orders || [];

  try {
    const r = await axios.get(`${API_URL}/api/v1/orders?user_id=${userId}`, { timeout: 2000 });
    if (r.data && r.data.items) orders = r.data.items;
  } catch (_) {}

  res.render('profile', {
    title: 'Đơn hàng của tôi',
    user: req.session.user || null,
    orders,
    activeTab: 'orders',
    successMessage: req.query.success ? 'Đặt hàng thành công!' : null,
    orderId: req.query.order_id,
    formatVND
  });
});

// ============================================================
// ============================================================
router.get('/profile', (req, res) => {
  res.render('profile', {
    title: 'Tài khoản của tôi',
    user: req.session.user || { id: 1, name: 'Guest User', email: 'guest@example.com', phone: '0987654321', role: 'user', loyalty_points: 1500 },
    orders: req.session.orders || [],
    activeTab: 'profile',
    successMessage: null,
    orderId: null,
    formatVND
  });
});

router.post('/profile', (req, res) => {
  if (req.session.user) {
    Object.assign(req.session.user, req.body);
  }
  req.session.flash = { type: 'success', message: 'Cập nhật thông tin thành công!' };
  res.redirect('/profile');
});

router.post('/profile/change-password', (req, res) => {
  const { new_password, confirm_password } = req.body;
  if (new_password === confirm_password) {
    req.session.flash = { type: 'success', message: 'Đổi mật khẩu thành công!' };
  }
  res.redirect('/profile');
});

// ============================================================
// GET /wishlist — Wishlist
// ============================================================
router.get('/wishlist', (req, res) => {
  const wishlist = req.session.wishlist || mockProducts.slice(0, 3);
  res.render('profile', {
    title: 'Danh sách yêu thích',
    user: req.session.user || null,
    orders: [],
    wishlist,
    activeTab: 'wishlist',
    successMessage: null,
    orderId: null,
    formatVND
  });
});

// ============================================================
// ============================================================
router.get('/login', (req, res) => {
  if (req.session.user) return res.redirect('/');
  res.render('login', {
    title: 'Đăng nhập',
    user: null,
    error: req.query.error || null,
    redirect: req.query.redirect || '/',
  });
});

router.post('/login', async (req, res) => {
  const { email, password, remember } = req.body;
  try {
    const r = await axios.post(`${API_URL}/api/v1/auth/login`, { email, password }, { timeout: 3000 });
    const userData = r.data;
    const profile = userData.user || userData;
    req.session.user = { ...profile, name: profile.name || profile.username || profile.email };
    req.session.token = userData.access_token || profile.access_token;
    if (remember) {
      res.cookie('remember_email', email, { maxAge: 30 * 24 * 60 * 60 * 1000, httpOnly: false });
      res.cookie('remember_token', Buffer.from(`${email}:${password}`).toString('base64'), { maxAge: 30 * 24 * 60 * 60 * 1000, httpOnly: false });
    }
    res.redirect(req.query.redirect || '/');
  } catch (err) {
    const status = err.response && err.response.status;
    let error = 'Đăng nhập thất bại.';
    if (status === 404) error = 'Email không tồn tại trong hệ thống.';
    if (status === 401) error = 'Mật khẩu không đúng.';
    if (email === 'admin@vulnshop.com' && password === 'admin123') {
      req.session.user = { id: 1, name: 'Admin', email, role: 'admin', loyalty_points: 9999 };
      return res.redirect('/');
    }
    res.render('login', { title: 'Đăng nhập', user: null, error, redirect: req.query.redirect || '/' });
  }
});

// ============================================================
// ============================================================
router.get('/register', (req, res) => {
  if (req.session.user) return res.redirect('/');
  res.render('register', { title: 'Đăng ký tài khoản', user: null, error: null });
});

router.post('/register', async (req, res) => {
  const { name, email, phone, password, confirm_password } = req.body;
  if (password !== confirm_password) {
    return res.render('register', { title: 'Đăng ký', user: null, error: 'Mật khẩu xác nhận không khớp.' });
  }
  try {
    const r = await axios.post(`${API_URL}/api/v1/auth/register`, { name, email, phone, password }, { timeout: 3000 });
    const profile = r.data.user || r.data;
    req.session.user = { ...profile, id: profile.id || r.data.user_id || Date.now(), name: profile.name || name, email: profile.email || email, role: profile.role || 'user' };
    req.session.token = r.data.access_token || profile.access_token;
    res.redirect('/');
  } catch (err) {
    req.session.user = { id: Date.now(), name, email, phone, role: 'user', loyalty_points: 0 };
    res.redirect('/');
  }
});

// Logout
router.get('/logout', (req, res) => {
  req.session.destroy();
  res.clearCookie('sessionId');
  res.redirect('/');
});

// ============================================================
// GET /forgot-password
// ============================================================
router.get('/forgot-password', (req, res) => {
  res.render('login', {
    title: 'Quên mật khẩu',
    user: null,
    error: null,
    view: 'forgot',
    redirect: '/'
  });
});

router.post('/forgot-password', async (req, res) => {
  const { email } = req.body;
  try {
    await axios.post(`${API_URL}/api/v1/auth/forgot-password`, { email }, { timeout: 2000 });
  } catch (_) {}
  res.render('login', {
    title: 'Quên mật khẩu',
    user: null,
    error: null,
    view: 'forgot_sent',
    email,
    redirect: '/'
  });
});

// ============================================================
// ============================================================
router.get('/reset-password', (req, res) => {
  const { token, email } = req.query;
  res.render('login', {
    title: 'Đặt lại mật khẩu',
    user: null,
    error: null,
    view: 'reset',
    token,
    email,
    redirect: '/'
  });
});

router.post('/reset-password', async (req, res) => {
  const { token, email, new_password } = req.body;
  try {
    await axios.post(`${API_URL}/api/v1/auth/reset-password`, { token, email, new_password }, { timeout: 2000 });
  } catch (_) {}
  res.redirect('/login?success=password_reset');
});

// ============================================================
// ============================================================
router.get('/track/:orderId', async (req, res) => {
  const { orderId } = req.params;
  let order = null;
  try {
    const r = await axios.get(`${API_URL}/api/v1/orders/${orderId}`, { timeout: 2000 });
    order = r.data;
  } catch (_) {
    order = {
      id: orderId,
      status: 'shipping',
      items: [{ name: 'iPhone 15 Pro Max', qty: 1, price: 29990000 }],
      shipping: { name: 'Nguyễn Văn A', address: '123 Lê Lợi, Q1, TP.HCM', phone: '0987654321' },
      total: 29990000,
      tracking_code: 'GHN-' + orderId,
      estimated_delivery: '2024-02-01'
    };
  }
  res.render('profile', {
    title: `Theo dõi đơn hàng ${orderId}`,
    user: req.session.user || null,
    orders: [order],
    activeTab: 'tracking',
    order,
    orderId,
    successMessage: null,
    formatVND
  });
});

// ============================================================
// ============================================================
router.get('/addresses/:userId', async (req, res) => {
  const { userId } = req.params;
  let addresses = [];
  try {
    const r = await axios.get(`${API_URL}/api/v1/users/${userId}/addresses`, { timeout: 2000 });
    addresses = r.data;
  } catch (_) {
    addresses = [{ id: 1, label: 'Nhà', address: '123 Nguyễn Trãi, Q5, TP.HCM', is_default: true }];
  }
  res.json(addresses);
});

module.exports = router;
