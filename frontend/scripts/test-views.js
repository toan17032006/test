const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const ejs = require('ejs');

const viewsDir = path.join(__dirname, '..', 'views');
const formatVND = value => `${Number(value || 0).toLocaleString('vi-VN')}đ`;
const product = {
  id: 1,
  name: 'iPhone 15 Pro Max',
  description: 'Synthetic lab product',
  image: 'https://placehold.co/320x240?text=Lab',
  price: 29990000,
  old_price: 34990000,
  stock: 50,
  category: 'electronics',
  brand: 'Apple',
  rating: 4.8,
  sold: 1234
};
const shared = {
  title: 'VulnShop test',
  user: { id: 2, name: 'Lab User', email: 'user@vulnshop.com', phone: '0900000000', role: 'user' },
  formatVND,
  products: [product],
  related: [product],
  reviews: [{ id: 1, user: 'Lab User', rating: 5, comment: 'Synthetic review', date: '2026-01-01' }],
  categories: ['electronics', 'clothing'],
  brands: ['Apple'],
  query: '',
  category: '',
  sort: 'popular',
  page: 1,
  totalPages: 1,
  cart: [{ productId: 1, name: product.name, price: product.price, qty: 1, image: product.image }],
  total: product.price,
  subtotal: product.price,
  orders: [{ id: 1001, status: 'pending', total: product.price, items: [product] }],
  activeTab: 'profile',
  successMessage: null,
  orderId: null,
  wishlist: [product],
  error: null,
  redirect: '/',
  token: null,
  email: null
};

async function main() {
  const expected = ['home', 'products', 'product_detail', 'cart', 'checkout', 'profile', 'login', 'register'];
  for (const name of expected) {
    const filename = path.join(viewsDir, `${name}.ejs`);
    assert.ok(fs.existsSync(filename), `Missing view ${name}.ejs`);
    const html = await ejs.renderFile(filename, { ...shared, product }, { async: false });
    assert.match(html, /<html lang="vi">/, `${name}.ejs did not render a Vietnamese HTML document`);
    assert.match(html, /VulnShop/i, `${name}.ejs did not render the store branding`);
  }
  for (const view of ['forgot', 'forgot_sent', 'reset']) {
    const html = await ejs.renderFile(path.join(viewsDir, 'login.ejs'), { ...shared, view, email: 'lab@example.test', token: 'synthetic-token' });
    assert.match(html, /auth-wrap/, `login.ejs did not render the ${view} state`);
  }
  const emptyCheckout = await ejs.renderFile(path.join(viewsDir, 'checkout.ejs'), { ...shared, cart: [] });
  assert.match(emptyCheckout, /giỏ hàng của bạn đang trống/i);
  process.stdout.write(`Rendered ${expected.length} storefront views with fixture data.\n`);
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
