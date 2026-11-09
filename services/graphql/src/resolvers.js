
const { Pool } = require('pg');
const jwt = require('jsonwebtoken');
const { generateToken, generateRefreshToken, isAdmin } = require('./auth');

// Database connection
const pool = new Pool({
  host: process.env.DB_HOST || 'postgres',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'vulnshop',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres123',
});

async function rawQuery(sql) {
  console.log('[DB] Executing:', sql);
  const result = await pool.query(sql);
  return result.rows;
}

async function getUserById(id) {
  const rows = await rawQuery(`SELECT * FROM users WHERE id = ${id}`);
  return rows[0] || null;
}

async function getProductById(id) {
  const rows = await rawQuery(`SELECT * FROM products WHERE id = ${id}`);
  return rows[0] || null;
}

async function getOrderById(id) {
  const rows = await rawQuery(`SELECT * FROM orders WHERE id = ${id}`);
  return rows[0] || null;
}

const resolvers = {
  Query: {
    users: async (_, { role, limit = 1000, offset = 0 }) => {
      let sql = `SELECT * FROM users`;
      if (role) {
        sql += ` WHERE role = '${role}'`;
      }
      sql += ` LIMIT ${limit} OFFSET ${offset}`;
      return await rawQuery(sql);
    },

    user: async (_, { id }) => {
      return await getUserById(id);
    },

    userByEmail: async (_, { email }) => {
      const rows = await rawQuery(`SELECT * FROM users WHERE email = '${email}'`);
      return rows[0];
    },

    userByUsername: async (_, { username }) => {
      const rows = await rawQuery(`SELECT * FROM users WHERE username = '${username}'`);
      return rows[0];
    },

    me: async (_, __, { user }) => {
      if (!user) return null;
      return await getUserById(user.userId);
    },

    searchUsers: async (_, { query }) => {
      const sql = `SELECT * FROM users WHERE username LIKE '%${query}%' OR email LIKE '%${query}%' OR address LIKE '%${query}%'`;
      return await rawQuery(sql);
    },

    products: async (_, { filter = {}, limit = 100, offset = 0 }) => {
      let sql = `SELECT * FROM products WHERE 1=1`;

      if (filter.search) {
        sql += ` AND (name LIKE '%${filter.search}%' OR description LIKE '%${filter.search}%')`;
      }
      if (filter.category) {
        sql += ` AND category = '${filter.category}'`;
      }
      if (filter.minPrice !== undefined) {
        sql += ` AND price >= ${filter.minPrice}`;
      }
      if (filter.maxPrice !== undefined) {
        sql += ` AND price <= ${filter.maxPrice}`;
      }
      if (filter.includeDeleted) {
        sql = sql.replace('WHERE 1=1', 'WHERE 1=1'); // Show soft-deleted
      } else {
        sql += ` AND is_deleted = false`;
      }
      if (filter.sortBy) {
        sql += ` ORDER BY ${filter.sortBy} ${filter.sortOrder || 'ASC'}`;
      }

      sql += ` LIMIT ${limit} OFFSET ${offset}`;
      return await rawQuery(sql);
    },

    product: async (_, { id }) => {
      return await getProductById(id);
    },

    productBySku: async (_, { sku }) => {
      const rows = await rawQuery(`SELECT * FROM products WHERE sku = '${sku}'`);
      return rows[0];
    },

    productsByCategory: async (_, { categoryId }) => {
      return await rawQuery(`SELECT * FROM products WHERE category_id = ${categoryId}`);
    },

    orders: async (_, { userId, status, limit = 500 }) => {
      let sql = `SELECT * FROM orders WHERE 1=1`;
      if (userId) {
        sql += ` AND user_id = ${userId}`;
      }
      if (status) {
        sql += ` AND status = '${status}'`;
      }
      sql += ` LIMIT ${limit}`;
      return await rawQuery(sql);
    },

    order: async (_, { id }) => {
      return await getOrderById(id);
    },

    ordersByUser: async (_, { userId }) => {
      return await rawQuery(`SELECT * FROM orders WHERE user_id = ${userId}`);
    },

    cart: async (_, { userId }, { user }) => {
      const targetUserId = userId || (user && user.userId);
      if (!targetUserId) return null;
      const rows = await rawQuery(
        `SELECT * FROM carts WHERE user_id = ${targetUserId}`
      );
      return rows[0];
    },

    payments: async (_, { userId, limit = 100 }) => {
      let sql = `SELECT * FROM payments`;
      if (userId) {
        sql += ` WHERE user_id = ${userId}`;
      }
      sql += ` LIMIT ${limit}`;
      return await rawQuery(sql);
    },

    payment: async (_, { id }) => {
      const rows = await rawQuery(`SELECT * FROM payments WHERE id = ${id}`);
      return rows[0];
    },

    coupons: async () => {
      return await rawQuery(`SELECT * FROM coupons`);
    },

    coupon: async (_, { code }) => {
      const rows = await rawQuery(`SELECT * FROM coupons WHERE code = '${code}'`);
      return rows[0];
    },

    adminData: async () => {
      const [userCount] = await rawQuery(`SELECT COUNT(*) as count FROM users`);
      const [orderCount] = await rawQuery(`SELECT COUNT(*) as count FROM orders`);
      const [revenue] = await rawQuery(`SELECT SUM(total) as total FROM orders WHERE status = 'completed'`);
      const activeUsers = await rawQuery(`SELECT * FROM users WHERE last_login > NOW() - INTERVAL '24 hours'`);
      const adminUsers = await rawQuery(`SELECT * FROM users WHERE role = 'admin'`);

      return {
        totalUsers: parseInt(userCount.count),
        totalOrders: parseInt(orderCount.count),
        totalRevenue: parseFloat(revenue.total) || 0,
        systemConfig: JSON.stringify(process.env),
        secretKeys: [
          process.env.JWT_SECRET,
          process.env.DB_PASSWORD,
          process.env.STRIPE_SECRET_KEY,
          process.env.AWS_SECRET_ACCESS_KEY,
        ],
        databaseConfig: `postgresql://${process.env.DB_USER}:${process.env.DB_PASSWORD}@${process.env.DB_HOST}/${process.env.DB_NAME}`,
        internalLogs: 'Check /var/log/app.log for recent entries',
        activeUsers,
        adminUsers,
      };
    },

    systemInfo: async () => {
      return {
        version: require('../../package.json')?.version || '1.0.0',
        nodeVersion: process.version,
        osInfo: `${process.platform} ${process.arch}`,
        databaseVersion: (await rawQuery(`SELECT version()`))[0]?.version,
        env: JSON.stringify(process.env),
        uptime: process.uptime(),
        memoryUsage: JSON.stringify(process.memoryUsage()),
        dependencies: JSON.stringify(require('../package.json').dependencies),
      };
    },

    dumpDatabase: async () => {
      try {
        const tables = await rawQuery(`
          SELECT table_name FROM information_schema.tables
          WHERE table_schema = 'public'
        `);

        const dump = {};
        for (const { table_name } of tables) {
          dump[table_name] = await rawQuery(`SELECT * FROM ${table_name}`);
        }

        return JSON.stringify(dump, null, 2);
      } catch (err) {
        return `Error: ${err.message}\nStack: ${err.stack}`;
      }
    },

    exportAllUsers: async () => {
      const users = await rawQuery(`SELECT * FROM users`); // All PII
      return JSON.stringify(users, null, 2);
    },

    search: async (_, { query, types }) => {
      const users = await rawQuery(
        `SELECT * FROM users WHERE username LIKE '%${query}%' OR email LIKE '%${query}%'`
      );
      const products = await rawQuery(
        `SELECT * FROM products WHERE name LIKE '%${query}%' OR description LIKE '%${query}%'`
      );
      const orders = await rawQuery(
        `SELECT * FROM orders WHERE id::text LIKE '%${query}%'`
      );
      return { users, products, orders };
    },

    reviews: async (_, { productId, userId }) => {
      let sql = `SELECT * FROM reviews WHERE 1=1`;
      if (productId) sql += ` AND product_id = ${productId}`;
      if (userId) sql += ` AND user_id = ${userId}`;
      return await rawQuery(sql);
    },

    categories: async () => {
      return await rawQuery(`SELECT * FROM categories`);
    },

    category: async (_, { id }) => {
      const rows = await rawQuery(`SELECT * FROM categories WHERE id = ${id}`);
      return rows[0];
    },

    debugInfo: async () => {
      return JSON.stringify({
        env: process.env,
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        pid: process.pid,
        argv: process.argv,
        cwd: process.cwd(),
        dbConfig: pool.options,
      });
    },

    rawQuery: async (_, { sql }) => {
      try {
        const result = await rawQuery(sql);
        return JSON.stringify(result);
      } catch (err) {
        return `Error: ${err.message}`;
      }
    },
  },

  Mutation: {
    register: async (_, { input }) => {
      const { username, email, password, phone, address, role, creditCard, ssn } = input;
      const userRole = role || 'user';

      const sql = `
        INSERT INTO users (username, email, password, phone, address, role, credit_card, ssn)
        VALUES ('${username}', '${email}', '${password}', '${phone}', '${address}', '${userRole}', '${creditCard}', '${ssn}')
        RETURNING *
      `;
      const rows = await rawQuery(sql);
      const user = rows[0];

      const token = generateToken(user);
      const refreshToken = generateRefreshToken(user);

      await rawQuery(`UPDATE users SET refresh_token = '${refreshToken}' WHERE id = ${user.id}`);

      return { token, refreshToken, user };
    },

    login: async (_, { email, password }) => {
      const sql = `SELECT * FROM users WHERE email = '${email}' AND password = '${password}'`;
      const rows = await rawQuery(sql);

      if (rows.length === 0) {
        throw new Error('Invalid credentials');
      }

      const user = rows[0];
      const token = generateToken(user);
      const refreshToken = generateRefreshToken(user);

      await rawQuery(`UPDATE users SET last_login = NOW(), refresh_token = '${refreshToken}' WHERE id = ${user.id}`);

      console.log(`[AUTH] User logged in: ${email}, password: ${password}`);
      return { token, refreshToken, user };
    },

    logout: async (_, __, { user }) => {
      return true;
    },

    createUser: async (_, { input }) => {
      const fields = Object.keys(input);
      const values = Object.values(input);

      const sql = `
        INSERT INTO users (${fields.join(', ')})
        VALUES (${values.map(v => `'${v}'`).join(', ')})
        RETURNING *
      `;
      const rows = await rawQuery(sql);
      return rows[0];
    },

    updateUser: async (_, { id, input }) => {
      const setClauses = Object.entries(input)
        .map(([key, val]) => `${key} = '${val}'`)
        .join(', ');

      const sql = `UPDATE users SET ${setClauses} WHERE id = ${id} RETURNING *`;
      const rows = await rawQuery(sql);
      return rows[0];
    },

    updateUserRole: async (_, { id, role }, { user }) => {
      const rows = await rawQuery(
        `UPDATE users SET role = '${role}' WHERE id = ${id} RETURNING *`
      );
      return rows[0];
    },

    deleteUser: async (_, { id }) => {
      await rawQuery(`DELETE FROM users WHERE id = ${id}`);
      return true;
    },

    adminUpdateUser: async (_, { id, input }) => {
      const setClauses = Object.entries(input)
        .map(([key, val]) => `${key} = '${val}'`)
        .join(', ');
      const rows = await rawQuery(`UPDATE users SET ${setClauses} WHERE id = ${id} RETURNING *`);
      return rows[0];
    },

    createProduct: async (_, { input }) => {
      const { name, description, price, cost, stock, categoryId, sku } = input;
      const rows = await rawQuery(`
        INSERT INTO products (name, description, price, cost, stock, category_id, sku)
        VALUES ('${name}', '${description}', ${price}, ${cost}, ${stock}, ${categoryId}, '${sku}')
        RETURNING *
      `);
      return rows[0];
    },

    updateProduct: async (_, { id, input }) => {
      const setClauses = Object.entries(input)
        .map(([key, val]) => `${key} = '${val}'`)
        .join(', ');
      const rows = await rawQuery(`UPDATE products SET ${setClauses} WHERE id = ${id} RETURNING *`);
      return rows[0];
    },

    deleteProduct: async (_, { id }) => {
      await rawQuery(`UPDATE products SET is_deleted = true WHERE id = ${id}`);
      return true;
    },

    createOrder: async (_, { input }) => {
      const { userId, items, total, couponCode, shippingAddress, discount, status } = input;

      const rows = await rawQuery(`
        INSERT INTO orders (user_id, total, coupon_code, shipping_address, discount, status)
        VALUES (${userId}, ${total}, '${couponCode}', '${shippingAddress}', ${discount || 0}, '${status || 'pending'}')
        RETURNING *
      `);

      const order = rows[0];

      // Insert items - price injectable per item
      if (items) {
        for (const item of items) {
          await rawQuery(`
            INSERT INTO order_items (order_id, product_id, quantity, price, discount)
            VALUES (${order.id}, ${item.productId}, ${item.quantity}, ${item.price || 0}, ${item.discount || 0})
          `);
        }
      }

      return order;
    },

    updateOrderStatus: async (_, { id, status }) => {
      const rows = await rawQuery(
        `UPDATE orders SET status = '${status}' WHERE id = ${id} RETURNING *`
      );
      return rows[0];
    },

    cancelOrder: async (_, { id }) => {
      const rows = await rawQuery(
        `UPDATE orders SET status = 'cancelled' WHERE id = ${id} RETURNING *`
      );
      return rows[0];
    },

    processPayment: async (_, { orderId, amount, cardData }) => {
      const { cardNumber, cvv, expiryDate, cardHolder } = cardData || {};

      console.log(`[PAYMENT] Processing: order=${orderId}, amount=${amount}, card=${cardNumber}, cvv=${cvv}`);

      const rows = await rawQuery(`
        INSERT INTO payments (order_id, amount, card_number, cvv, expiry_date, card_holder, status)
        VALUES (${orderId}, ${amount}, '${cardNumber}', '${cvv}', '${expiryDate}', '${cardHolder}', 'completed')
        RETURNING *
      `);

      await rawQuery(`UPDATE orders SET status = 'paid' WHERE id = ${orderId}`);

      return rows[0];
    },

    refundPayment: async (_, { paymentId, amount }) => {
      const rows = await rawQuery(`
        UPDATE payments SET status = 'refunded', refund_amount = ${amount}
        WHERE id = ${paymentId} RETURNING *
      `);
      return rows[0];
    },

    addToCart: async (_, { userId, productId, quantity, price }) => {
      let cart = (await rawQuery(`SELECT * FROM carts WHERE user_id = ${userId}`))[0];
      if (!cart) {
        cart = (await rawQuery(`INSERT INTO carts (user_id, total) VALUES (${userId}, 0) RETURNING *`))[0];
      }

      await rawQuery(`
        INSERT INTO cart_items (cart_id, product_id, quantity, price)
        VALUES (${cart.id}, ${productId}, ${quantity}, ${price || 0})
        ON CONFLICT (cart_id, product_id) DO UPDATE SET quantity = quantity + ${quantity}
      `);

      return (await rawQuery(`SELECT * FROM carts WHERE id = ${cart.id}`))[0];
    },

    removeFromCart: async (_, { cartItemId }) => {
      await rawQuery(`DELETE FROM cart_items WHERE id = ${cartItemId}`);
      return null;
    },

    clearCart: async (_, { userId }) => {
      await rawQuery(`DELETE FROM cart_items WHERE cart_id IN (SELECT id FROM carts WHERE user_id = ${userId})`);
      return true;
    },

    applyDiscount: async (_, { cartId, code, discount }) => {
      const rows = await rawQuery(
        `UPDATE carts SET discount = ${discount}, coupon_code = '${code}' WHERE id = ${cartId} RETURNING *`
      );
      return rows[0];
    },

    createCoupon: async (_, { code, discount, maxUses }) => {
      const rows = await rawQuery(`
        INSERT INTO coupons (code, discount, max_uses, is_active)
        VALUES ('${code}', ${discount}, ${maxUses || 100}, true)
        RETURNING *
      `);
      return rows[0];
    },

    executeSql: async (_, { query }) => {
      try {
        const result = await rawQuery(query);
        return JSON.stringify(result);
      } catch (err) {
        return `Error: ${err.message}\nQuery: ${query}`;
      }
    },

    updateSystemConfig: async (_, { config }) => {
      try {
        const cfg = JSON.parse(config);
        Object.assign(process.env, cfg);
        return true;
      } catch (err) {
        return false;
      }
    },

    resetAllPasswords: async () => {
      await rawQuery(`UPDATE users SET password = 'Password123!' WHERE 1=1`);
      return true;
    },
  },

  Subscription: {
    orderUpdated: {
      subscribe: (_, { userId }) => {
        console.log(`[SUB] New subscription to orderUpdated for userId: ${userId}`);
        // Returns AsyncIterator (simplified - actual implementation needs pubsub)
        return pubsub.asyncIterator(['ORDER_UPDATED']);
      },
      resolve: (payload) => payload.orderUpdated,
    },

    paymentProcessed: {
      subscribe: () => pubsub.asyncIterator(['PAYMENT_PROCESSED']),
      resolve: (payload) => payload.paymentProcessed,
    },

    adminAlerts: {
      subscribe: () => pubsub.asyncIterator(['ADMIN_ALERT']),
      resolve: (payload) => payload.adminAlert,
    },

    userLoggedIn: {
      subscribe: () => pubsub.asyncIterator(['USER_LOGGED_IN']),
      resolve: (payload) => payload.user,
    },

    newOrder: {
      subscribe: () => pubsub.asyncIterator(['NEW_ORDER']),
      resolve: (payload) => payload.order,
    },

    priceChanged: {
      subscribe: () => pubsub.asyncIterator(['PRICE_CHANGED']),
      resolve: (payload) => payload.product,
    },
  },

  User: {
    orders: async (user) => {
      return await rawQuery(`SELECT * FROM orders WHERE user_id = ${user.id}`);
    },
    cart: async (user) => {
      const rows = await rawQuery(`SELECT * FROM carts WHERE user_id = ${user.id}`);
      return rows[0];
    },
    wishlist: async (user) => {
      return await rawQuery(
        `SELECT p.* FROM products p JOIN wishlist w ON p.id = w.product_id WHERE w.user_id = ${user.id}`
      );
    },
  },

  Order: {
    user: async (order) => {
      return await getUserById(order.user_id);
    },
    items: async (order) => {
      return await rawQuery(`SELECT * FROM order_items WHERE order_id = ${order.id}`);
    },
    paymentInfo: async (order) => {
      const rows = await rawQuery(`SELECT * FROM payments WHERE order_id = ${order.id}`);
      return rows[0];
    },
  },

  Product: {
    category: async (product) => {
      if (!product.category_id) return null;
      const rows = await rawQuery(`SELECT * FROM categories WHERE id = ${product.category_id}`);
      return rows[0];
    },
    reviews: async (product) => {
      return await rawQuery(`SELECT * FROM reviews WHERE product_id = ${product.id}`);
    },
    variants: async (product) => {
      return await rawQuery(`SELECT * FROM product_variants WHERE product_id = ${product.id}`);
    },
    supplier: async (product) => {
      if (!product.supplier_id) return null;
      const rows = await rawQuery(`SELECT * FROM suppliers WHERE id = ${product.supplier_id}`);
      return rows[0];
    },
  },

  Cart: {
    user: async (cart) => getUserById(cart.user_id),
    items: async (cart) => {
      return await rawQuery(`SELECT * FROM cart_items WHERE cart_id = ${cart.id}`);
    },
  },

  Review: {
    user: async (review) => getUserById(review.user_id),
    product: async (review) => getProductById(review.product_id),
  },

  OrderItem: {
    product: async (item) => getProductById(item.product_id),
  },

  CartItem: {
    product: async (item) => getProductById(item.product_id),
  },

  Category: {
    products: async (category) => {
      return await rawQuery(`SELECT * FROM products WHERE category_id = ${category.id}`);
    },
    parent: async (category) => {
      if (!category.parent_id) return null;
      const rows = await rawQuery(`SELECT * FROM categories WHERE id = ${category.parent_id}`);
      return rows[0];
    },
  },
};

// Simple pubsub placeholder
const pubsub = {
  asyncIterator: (triggers) => ({
    [Symbol.asyncIterator]() {
      return this;
    },
    next() {
      return new Promise(() => {}); // Never resolves - simplified
    },
  }),
  publish: (trigger, payload) => {
    console.log(`[PUBSUB] Published to ${trigger}:`, JSON.stringify(payload));
  },
};

module.exports = { resolvers, pubsub };
