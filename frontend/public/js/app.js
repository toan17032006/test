(() => {
  const readCart = () => { try { return JSON.parse(localStorage.getItem('cart') || '[]'); } catch (_) { return []; } };
  const saveCart = items => { localStorage.setItem('cart', JSON.stringify(items)); document.querySelectorAll('.cart-badge').forEach(node => { node.textContent = items.reduce((sum, row) => sum + (Number(row.qty) || 1), 0); }); };
  const post = async (url, payload) => {
    const response = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (!response.ok) throw new Error('Request failed');
    return response.json();
  };
  const addToCart = async item => {
    const items = readCart();
    const productId = String(item.productId);
    const existing = items.find(row => String(row.productId) === productId);
    if (existing) existing.qty = (Number(existing.qty) || 1) + (Number(item.qty) || 1);
    else items.push({ ...item, qty: Number(item.qty) || 1 });
    saveCart(items);
    try { await post('/cart/add', { ...item, qty: Number(item.qty) || 1 }); } catch (_) {}
    const button = document.querySelector('.button-row .button.primary');
    if (button) { const label = button.textContent; button.textContent = 'Đã thêm vào giỏ'; setTimeout(() => { button.textContent = label; }, 1300); }
  };
  const updateCart = async (productId, qty, price) => {
    const items = readCart().map(row => String(row.productId) === String(productId) ? { ...row, qty: Number(qty), price: Number(price) } : row);
    saveCart(items);
    try { await post('/cart/update', { productId, qty, price }); } finally { location.reload(); }
  };
  const removeFromCart = async productId => {
    saveCart(readCart().filter(row => String(row.productId) !== String(productId)));
    try { await post('/cart/remove', { productId }); } finally { location.reload(); }
  };
  window.VulnShop = { addToCart, updateCart, removeFromCart };
  window.addToCart = (productId, name, price, image) => addToCart({ productId, name, price, qty: 1, image });
  window.toggleWishlist = id => {
    let items = [];
    try { items = JSON.parse(localStorage.getItem('wishlist') || '[]'); } catch (_) {}
    const index = items.indexOf(id);
    if (index < 0) items.push(id); else items.splice(index, 1);
    localStorage.setItem('wishlist', JSON.stringify(items));
  };
  window.addToWishlist = window.toggleWishlist;
  document.addEventListener('DOMContentLoaded', () => saveCart(readCart()));
})();
