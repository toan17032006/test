// VulnShop GraphQL Resolvers
// INTENTIONALLY VULNERABLE - For educational/pentesting purposes only
// Vulnerabilities: #97, #102, #104, #108, #113, #115, #250, #264, #265, #266, #309

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

// VULN: Helper that runs raw SQL without parameterization (SQL Injection)
async function rawQuery(sql) {
  console.log('[DB] Executing:', sql); // VULN #559: SQL logged
  const result = await pool.query(sql);
  return result.rows;
}

// N+1 query helper - intentionally not batched
async function getUserById(id) {
  // VULN: No caching, N+1 problem
  const rows = await rawQuery(`SELECT * FROM users WHERE id = ${id}`); // VULN: SQLi
  return rows[0] || null;
}

async function getProductById(id) {
  const rows = await rawQuery(`SELECT * FROM products WHERE id = ${id}`); // VULN: SQLi
  return rows[0] || null;
}

async function getOrderById(id) {
  const rows = await rawQuery(`SELECT * FROM orders WHERE id = ${id}`); // VULN: SQLi
  return rows[0] || null;
}

const resolvers = {
  Query: {
    // VULN #104: Returns all users including passwords, no auth check
    users: async (_, { role, limit = 1000, offset = 0 }) => {
      let sql = `SELECT * FROM users`; // VULN: Returns password column
      if (role) {
        sql += ` WHERE role = '${role}'`; // VULN: SQL injection via role param
      }
      sql += ` LIMIT ${limit} OFFSET ${offset}`; // VULN: SQLi via limit/offset
      return await rawQuery(sql);
    },

    // VULN #97: IDOR - returns any user's data including password
    user: async (_, { id }) => {
      // VULN: No auth check, no ownership verification
      return await getUserById(id);
    },

    // VULN: User enumeration
    userByEmail: async (_, { email }) => {
      const rows = await rawQuery(`SELECT * FROM users WHERE email = '${email}'`); // VULN: SQLi
      return rows[0];
    },

    userByUsername: async (_, { username }) => {
      const rows = await rawQuery(`SELECT * FROM users WHERE username = '${username}'`); // VULN: SQLi
      return rows[0];
    },

    // VULN: Returns current user including sensitive fields
    me: async (_, __, { user }) => {
      if (!user) return null;
      return await getUserById(user.userId);
    },

    // VULN: SQL injectable search returning PII
    searchUsers: async (_, { query }) => {
      // VULN: Direct SQL injection
      const sql = `SELECT * FROM users WHERE username LIKE '%${query}%' OR email LIKE '%${query}%' OR address LIKE '%${query}%'`;
      return await rawQuery(sql);
    },

    // VULN: Filter with SQL injectable fields
    products: async (_, { filter = {}, limit = 100, offset = 0 }) => {
      let sql = `SELECT * FROM products WHERE 1=1`;

      if (filter.search) {
        // VULN: SQL injection via search
        sql += ` AND (name LIKE '%${filter.search}%' OR description LIKE '%${filter.search}%')`;
      }
      if (filter.category) {
        sql += ` AND category = '${filter.category}'`; // VULN: SQLi
      }
      if (filter.minPrice !== undefined) {
        sql += ` AND price >= ${filter.minPrice}`; // VULN: SQLi
      }
      if (filter.maxPrice !== undefined) {
        sql += ` AND price <= ${filter.maxPrice}`; // VULN: SQLi
      }
      if (filter.includeDeleted) {
        sql = sql.replace('WHERE 1=1', 'WHERE 1=1'); // Show soft-deleted
      } else {
        sql += ` AND is_deleted = false`;
      }
      if (filter.sortBy) {
        // VULN: SQL injection via ORDER BY field name
        sql += ` ORDER BY ${filter.sortBy} ${filter.sortOrder || 'ASC'}`;
      }

      sql += ` LIMIT ${limit} OFFSET ${offset}`; // VULN: SQLi
      return await rawQuery(sql);
    },

    product: async (_, { id }) => {
      return await getProductById(id);
    },

    productBySku: async (_, { sku }) => {
      const rows = await rawQuery(`SELECT * FROM products WHERE sku = '${sku}'`); // VULN: SQLi
      return rows[0];
    },

    productsByCategory: async (_, { categoryId }) => {
      return await rawQuery(`SELECT * FROM products WHERE category_id = ${categoryId}`); // VULN: SQLi
    },

    // VULN #113: Returns ALL orders regardless of auth or ownership
    orders: async (_, { userId, status, limit = 500 }) => {
      let sql = `SELECT * FROM orders WHERE 1=1`;
      if (userId) {
        sql += ` AND user_id = ${userId}`; // VULN: SQLi
      }
      if (status) {
        sql += ` AND status = '${status}'`; // VULN: SQLi
      }
      sql += ` LIMIT ${limit}`;
      // VULN: No auth check - returns all orders
      return await rawQuery(sql);
    },

    // VULN: IDOR on order
    order: async (_, { id }) => {
      // VULN: No auth check, no ownership check
      return await getOrderById(id);
    },

    ordersByUser: async (_, { userId }) => {
      // VULN: IDOR - no check if current user owns these orders
      return await rawQuery(`SELECT * FROM orders WHERE user_id = ${userId}`); // VULN: SQLi
    },

    // VULN: IDOR on cart
    cart: async (_, { userId }, { user }) => {
      const targetUserId = userId || (user && user.userId);
      if (!targetUserId) return null;
      // VULN: No ownership check
      const rows = await rawQuery(
        `SELECT * FROM carts WHERE user_id = ${targetUserId}`  // VULN: SQLi
      );
      return rows[0];
    },

    // VULN #115: Payment data accessible without auth
    payments: async (_, { userId, limit = 100 }) => {
      let sql = `SELECT * FROM payments`;
      if (userId) {
        sql += ` WHERE user_id = ${userId}`; // VULN: SQLi
      }
      sql += ` LIMIT ${limit}`;
      // VULN: No auth check - returns card numbers, CVVs
      return await rawQuery(sql);
    },

    payment: async (_, { id }) => {
      // VULN: IDOR - returns payment with card details
      const rows = await rawQuery(`SELECT * FROM payments WHERE id = ${id}`); // VULN: SQLi
      return rows[0];
    },

    // VULN: All coupons exposed
    coupons: async () => {
      return await rawQuery(`SELECT * FROM coupons`);
    },

    coupon: async (_, { code }) => {
      const rows = await rawQuery(`SELECT * FROM coupons WHERE code = '${code}'`); // VULN: SQLi
      return rows[0];
    },

    // VULN #108: Admin data without auth check
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
        // VULN: Expose sensitive system configuration
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

    // VULN: System info exposed
    systemInfo: async () => {
      return {
        version: require('../../package.json')?.version || '1.0.0',
        nodeVersion: process.version,
        osInfo: `${process.platform} ${process.arch}`,
        databaseVersion: (await rawQuery(`SELECT version()`))[0]?.version,
        env: JSON.stringify(process.env), // VULN: ALL env vars exposed
        uptime: process.uptime(),
        memoryUsage: JSON.stringify(process.memoryUsage()),
        dependencies: JSON.stringify(require('../package.json').dependencies),
      };
    },

    // VULN (EXTREME): Direct database dump endpoint
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
        return `Error: ${err.message}\nStack: ${err.stack}`; // VULN: Error details exposed
      }
    },

    exportAllUsers: async () => {
      const users = await rawQuery(`SELECT * FROM users`); // All PII
      return JSON.stringify(users, null, 2);
    },

    // VULN: SQL injectable search
    search: async (_, { query, types }) => {
      // VULN: Direct SQL injection in query
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
      const rows = await rawQuery(`SELECT * FROM categories WHERE id = ${id}`); // VULN: SQLi
      return rows[0];
    },

    // VULN: Debug endpoint
    debugInfo: async () => {
      return JSON.stringify({
        env: process.env,
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        pid: process.pid,
        argv: process.argv,
        cwd: process.cwd(),
        // VULN: DB connection details in debug
        dbConfig: pool.options,
      });
    },

    // VULN (EXTREME): Direct SQL execution
    rawQuery: async (_, { sql }) => {
      try {
        const result = await rawQuery(sql);
        return JSON.stringify(result);
      } catch (err) {
        return `Error: ${err.message}`; // VULN: DB error messages exposed
      }
    },
  },

  Mutation: {
    // Register with mass assignment
    register: async (_, { input }) => {
      const { username, email, password, phone, address, role, creditCard, ssn } = input;
      // VULN #250: role directly from input - privilege escalation
      const userRole = role || 'user';

      // VULN: Password stored in plaintext if no hashing
      // VULN: SQL injection in registration
      const sql = `
        INSERT INTO users (username, email, password, phone, address, role, credit_card, ssn)
        VALUES ('${username}', '${email}', '${password}', '${phone}', '${address}', '${userRole}', '${creditCard}', '${ssn}')
        RETURNING *
      `;
      const rows = await rawQuery(sql);
      const user = rows[0];

      const token = generateToken(user);
      const refreshToken = generateRefreshToken(user);

      // VULN: Store refresh token in DB
      await rawQuery(`UPDATE users SET refresh_token = '${refreshToken}' WHERE id = ${user.id}`);

      return { token, refreshToken, user };
    },

    login: async (_, { email, password }) => {
      // VULN: SQL injection in login
      const sql = `SELECT * FROM users WHERE email = '${email}' AND password = '${password}'`;
      const rows = await rawQuery(sql);

      if (rows.length === 0) {
        // VULN: Timing-based user enumeration possible
        throw new Error('Invalid credentials');
      }

      const user = rows[0];
      const token = generateToken(user);
      const refreshToken = generateRefreshToken(user);

      await rawQuery(`UPDATE users SET last_login = NOW(), refresh_token = '${refreshToken}' WHERE id = ${user.id}`);

      console.log(`[AUTH] User logged in: ${email}, password: ${password}`); // VULN: Logging password
      return { token, refreshToken, user };
    },

    logout: async (_, __, { user }) => {
      // VULN: Tokens not actually invalidated server-side
      return true;
    },

    // VULN #250: Mass assignment - all fields settable including role
    createUser: async (_, { input }) => {
      const fields = Object.keys(input);
      const values = Object.values(input);

      // VULN: SQL injection via field names and values
      const sql = `
        INSERT INTO users (${fields.join(', ')})
        VALUES (${values.map(v => `'${v}'`).join(', ')})
        RETURNING *
      `;
      const rows = await rawQuery(sql);
      return rows[0];
    },

    // VULN: No ownership check - can update any user
    updateUser: async (_, { id, input }) => {
      // VULN: No auth check, no ownership verification
      const setClauses = Object.entries(input)
        .map(([key, val]) => `${key} = '${val}'`) // VULN: SQL injection in key names and values
        .join(', ');

      const sql = `UPDATE users SET ${setClauses} WHERE id = ${id} RETURNING *`;
      const rows = await rawQuery(sql);
      return rows[0];
    },

    // VULN #102: Privilege escalation - change any user's role
    updateUserRole: async (_, { id, role }, { user }) => {
      // VULN: No auth check - any user can escalate any other user's role
      const rows = await rawQuery(
        `UPDATE users SET role = '${role}' WHERE id = ${id} RETURNING *` // VULN: SQLi
      );
      return rows[0];
    },

    // VULN: Delete any user without auth
    deleteUser: async (_, { id }) => {
      await rawQuery(`DELETE FROM users WHERE id = ${id}`); // VULN: SQLi, no auth
      return true;
    },

    // VULN #108: Admin update without admin check
    adminUpdateUser: async (_, { id, input }) => {
      // VULN: Same as updateUser but labeled "admin" - no actual check
      const setClauses = Object.entries(input)
        .map(([key, val]) => `${key} = '${val}'`)
        .join(', ');
      const rows = await rawQuery(`UPDATE users SET ${setClauses} WHERE id = ${id} RETURNING *`);
      return rows[0];
    },

    createProduct: async (_, { input }) => {
      const { name, description, price, cost, stock, categoryId, sku } = input;
      // VULN: No auth check - anyone can create products
      const rows = await rawQuery(`
        INSERT INTO products (name, description, price, cost, stock, category_id, sku)
        VALUES ('${name}', '${description}', ${price}, ${cost}, ${stock}, ${categoryId}, '${sku}')
        RETURNING *
      `); // VULN: SQLi
      return rows[0];
    },

    updateProduct: async (_, { id, input }) => {
      // VULN: No auth check
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

    // VULN #309: Price/total injectable by client
    createOrder: async (_, { input }) => {
      const { userId, items, total, couponCode, shippingAddress, discount, status } = input;

      // VULN: Total comes from client - no server-side calculation
      // VULN: Status settable on creation
      const rows = await rawQuery(`
        INSERT INTO orders (user_id, total, coupon_code, shipping_address, discount, status)
        VALUES (${userId}, ${total}, '${couponCode}', '${shippingAddress}', ${discount || 0}, '${status || 'pending'}')
        RETURNING *
      `); // VULN: SQLi

      const order = rows[0];

      // Insert items - price injectable per item
      if (items) {
        for (const item of items) {
          await rawQuery(`
            INSERT INTO order_items (order_id, product_id, quantity, price, discount)
            VALUES (${order.id}, ${item.productId}, ${item.quantity}, ${item.price || 0}, ${item.discount || 0})
          `); // VULN: SQLi, price injectable
        }
      }

      return order;
    },

    // VULN: No auth on status change
    updateOrderStatus: async (_, { id, status }) => {
      const rows = await rawQuery(
        `UPDATE orders SET status = '${status}' WHERE id = ${id} RETURNING *` // VULN: SQLi
      );
      return rows[0];
    },

    cancelOrder: async (_, { id }) => {
      // VULN: No ownership check
      const rows = await rawQuery(
        `UPDATE orders SET status = 'cancelled' WHERE id = ${id} RETURNING *`
      );
      return rows[0];
    },

    // VULN #309: Payment amount injectable
    processPayment: async (_, { orderId, amount, cardData }) => {
      // VULN: Amount comes from client - no validation against order total
      // VULN: Arbitrary amount can be passed (send $0.01 for a $1000 order)
      const { cardNumber, cvv, expiryDate, cardHolder } = cardData || {};

      console.log(`[PAYMENT] Processing: order=${orderId}, amount=${amount}, card=${cardNumber}, cvv=${cvv}`); // VULN: Logging PCI data

      const rows = await rawQuery(`
        INSERT INTO payments (order_id, amount, card_number, cvv, expiry_date, card_holder, status)
        VALUES (${orderId}, ${amount}, '${cardNumber}', '${cvv}', '${expiryDate}', '${cardHolder}', 'completed')
        RETURNING *
      `); // VULN: SQLi; CVV stored (PCI violation)

      // VULN: Update order without validating amount
      await rawQuery(`UPDATE orders SET status = 'paid' WHERE id = ${orderId}`);

      return rows[0];
    },

    // VULN: Refund amount injectable
    refundPayment: async (_, { paymentId, amount }) => {
      // VULN: No check if refund amount <= original payment amount
      const rows = await rawQuery(`
        UPDATE payments SET status = 'refunded', refund_amount = ${amount}
        WHERE id = ${paymentId} RETURNING *
      `);
      return rows[0];
    },

    // VULN: Price injectable; can add to any user's cart
    addToCart: async (_, { userId, productId, quantity, price }) => {
      // VULN: price comes from client
      let cart = (await rawQuery(`SELECT * FROM carts WHERE user_id = ${userId}`))[0];
      if (!cart) {
        cart = (await rawQuery(`INSERT INTO carts (user_id, total) VALUES (${userId}, 0) RETURNING *`))[0];
      }

      await rawQuery(`
        INSERT INTO cart_items (cart_id, product_id, quantity, price)
        VALUES (${cart.id}, ${productId}, ${quantity}, ${price || 0})
        ON CONFLICT (cart_id, product_id) DO UPDATE SET quantity = quantity + ${quantity}
      `); // VULN: SQLi

      return (await rawQuery(`SELECT * FROM carts WHERE id = ${cart.id}`))[0];
    },

    removeFromCart: async (_, { cartItemId }) => {
      await rawQuery(`DELETE FROM cart_items WHERE id = ${cartItemId}`); // VULN: SQLi, no auth
      return null;
    },

    clearCart: async (_, { userId }) => {
      // VULN: Can clear any user's cart - no ownership check
      await rawQuery(`DELETE FROM cart_items WHERE cart_id IN (SELECT id FROM carts WHERE user_id = ${userId})`);
      return true;
    },

    // VULN: Discount amount injected by client
    applyDiscount: async (_, { cartId, code, discount }) => {
      // VULN: discount value comes from client - no validation against coupon table
      const rows = await rawQuery(
        `UPDATE carts SET discount = ${discount}, coupon_code = '${code}' WHERE id = ${cartId} RETURNING *`
      ); // VULN: SQLi
      return rows[0];
    },

    // VULN: Create coupon without auth
    createCoupon: async (_, { code, discount, maxUses }) => {
      const rows = await rawQuery(`
        INSERT INTO coupons (code, discount, max_uses, is_active)
        VALUES ('${code}', ${discount}, ${maxUses || 100}, true)
        RETURNING *
      `); // VULN: SQLi, no auth
      return rows[0];
    },

    // VULN (EXTREME): Direct SQL execution - no auth
    executeSql: async (_, { query }) => {
      try {
        const result = await rawQuery(query); // VULN: Arbitrary SQL execution
        return JSON.stringify(result);
      } catch (err) {
        return `Error: ${err.message}\nQuery: ${query}`; // VULN: Error + query in response
      }
    },

    // VULN: System config update without auth
    updateSystemConfig: async (_, { config }) => {
      try {
        const cfg = JSON.parse(config);
        Object.assign(process.env, cfg); // VULN: Directly modifying process environment
        return true;
      } catch (err) {
        return false;
      }
    },

    // VULN: Reset ALL passwords without auth
    resetAllPasswords: async () => {
      // VULN: No auth check on destructive admin operation
      await rawQuery(`UPDATE users SET password = 'Password123!' WHERE 1=1`);
      return true;
    },
  },

  // VULN #267: Subscriptions without auth
  Subscription: {
    orderUpdated: {
      subscribe: (_, { userId }) => {
        // VULN: No auth check - anyone can subscribe to any user's order updates
        console.log(`[SUB] New subscription to orderUpdated for userId: ${userId}`);
        // Returns AsyncIterator (simplified - actual implementation needs pubsub)
        return pubsub.asyncIterator(['ORDER_UPDATED']);
      },
      resolve: (payload) => payload.orderUpdated,
    },

    paymentProcessed: {
      // VULN: ALL payment events broadcast to all subscribers
      subscribe: () => pubsub.asyncIterator(['PAYMENT_PROCESSED']),
      resolve: (payload) => payload.paymentProcessed,
    },

    adminAlerts: {
      // VULN: Admin alerts accessible to any subscriber
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

  // Type resolvers for relations (N+1 problem - vuln for DoS)
  User: {
    orders: async (user) => {
      // VULN: N+1 query - no DataLoader
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
      // VULN: Accessing any user via order - IDOR
      return await getUserById(order.user_id);
    },
    items: async (order) => {
      return await rawQuery(`SELECT * FROM order_items WHERE order_id = ${order.id}`); // VULN: N+1
    },
    paymentInfo: async (order) => {
      const rows = await rawQuery(`SELECT * FROM payments WHERE order_id = ${order.id}`);
      return rows[0]; // VULN: Returns card number, CVV
    },
  },

  Product: {
    category: async (product) => {
      if (!product.category_id) return null;
      const rows = await rawQuery(`SELECT * FROM categories WHERE id = ${product.category_id}`);
      return rows[0];
    },
    reviews: async (product) => {
      // VULN: N+1 - no batching
      return await rawQuery(`SELECT * FROM reviews WHERE product_id = ${product.id}`);
    },
    variants: async (product) => {
      return await rawQuery(`SELECT * FROM product_variants WHERE product_id = ${product.id}`);
    },
    supplier: async (product) => {
      if (!product.supplier_id) return null;
      const rows = await rawQuery(`SELECT * FROM suppliers WHERE id = ${product.supplier_id}`);
      return rows[0]; // VULN: Returns contract terms and sensitive supplier data
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
