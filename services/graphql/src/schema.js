// VulnShop GraphQL Schema
// INTENTIONALLY VULNERABLE - For educational/pentesting purposes only
// Vulnerabilities: #20, #97, #102, #104, #108, #113, #115, #250, #260, #264, #265, #266, #267, #268, #309

const { gql } = require('graphql-tag');

const typeDefs = gql`
  # VULN #251: Password field exposed in schema - excessive data exposure
  # VULN #643, #648: PII and payment fields exposed in schema
  type User {
    id: ID!
    username: String!
    email: String!
    password: String!       # VULN: Password hash directly accessible
    phone: String
    address: String
    role: String            # admin, user, moderator
    creditCard: String      # VULN #648: Payment data exposed
    ssn: String             # VULN #643: SSN directly in schema
    bankAccount: String     # VULN #643: Bank info exposed
    orders: [Order]
    cart: Cart
    wishlist: [Product]
    loyaltyPoints: Int
    refreshToken: String    # VULN: Token exposed in schema
    resetToken: String      # VULN #51: Password reset token exposed
    createdAt: String
    lastLogin: String
    isActive: Boolean
    failedLoginAttempts: Int
    internalNotes: String   # VULN: Internal admin notes accessible
  }

  type Product {
    id: ID!
    name: String!
    description: String!
    price: Float!
    cost: Float             # VULN: Internal cost/margin data exposed
    stock: Int!
    sku: String
    category: Category
    reviews: [Review]
    variants: [ProductVariant]
    supplier: Supplier      # VULN: Supplier info exposed
    supplierCost: Float     # VULN: Business-sensitive pricing
    discountPercentage: Float
    tags: [String]
    images: [String]
    weight: Float
    isDeleted: Boolean      # Soft-deleted products still queryable
  }

  type Category {
    id: ID!
    name: String!
    description: String
    products: [Product]
    parent: Category
  }

  type ProductVariant {
    id: ID!
    product: Product
    name: String!
    price: Float!
    stock: Int!
    sku: String
  }

  type Supplier {
    id: ID!
    name: String!
    email: String!
    phone: String
    address: String
    contractTerms: String   # VULN: Sensitive contract data exposed
  }

  # VULN #97, #113: Order accessible without ownership check (IDOR)
  type Order {
    id: ID!
    user: User              # VULN: Can access any user's data via order
    items: [OrderItem]
    total: Float!
    status: String!
    paymentInfo: PaymentInfo  # VULN: Sensitive payment data returned
    shippingAddress: String
    trackingNumber: String
    notes: String           # VULN: Internal order notes
    couponUsed: String
    createdAt: String
    updatedAt: String
    internalStatus: String  # VULN: Internal fulfillment status
  }

  type OrderItem {
    id: ID!
    product: Product
    quantity: Int!
    price: Float!
    discount: Float
  }

  # VULN #648: Payment card data exposed in API responses
  type PaymentInfo {
    id: ID!
    cardNumber: String      # VULN: Full card number exposed
    cardHolder: String
    cvv: String             # VULN: CVV exposed (PCI DSS violation)
    expiryDate: String
    amount: Float
    status: String
    transactionId: String
    gatewayResponse: String # VULN: Raw gateway response with internals
  }

  type Payment {
    id: ID!
    orderId: ID
    userId: ID
    amount: Float!
    method: String
    cardNumber: String      # VULN: Full card data
    cvv: String             # VULN: CVV stored and exposed
    status: String!
    transactionId: String
    gatewayResponse: String
    createdAt: String
  }

  type Cart {
    id: ID!
    user: User
    items: [CartItem]
    total: Float
    discount: Float
    couponCode: String
    createdAt: String
  }

  type CartItem {
    id: ID!
    product: Product
    quantity: Int!
    price: Float!
  }

  type Coupon {
    id: ID!
    code: String!
    discount: Float!        # VULN: Discount percentage exposed
    maxUses: Int
    currentUses: Int
    isActive: Boolean
    expiresAt: String
    createdBy: String
  }

  type Review {
    id: ID!
    user: User
    product: Product
    rating: Int!
    comment: String!
    isApproved: Boolean
    adminNote: String       # VULN: Admin notes exposed to all
    createdAt: String
  }

  # VULN #108: Admin data accessible without auth
  type AdminData {
    totalUsers: Int
    totalOrders: Int
    totalRevenue: Float
    systemConfig: String    # VULN: System config exposed
    secretKeys: [String]    # VULN: API keys and secrets in response
    databaseConfig: String  # VULN: DB connection string exposed
    internalLogs: String    # VULN: Log data exposed
    activeUsers: [User]     # VULN: All active user data
    adminUsers: [User]      # VULN: Admin accounts exposed
  }

  type SystemInfo {
    version: String
    nodeVersion: String     # VULN: Version fingerprinting
    osInfo: String          # VULN: OS info exposed
    databaseVersion: String # VULN: DB version exposed
    env: String             # VULN: Environment variables exposed
    uptime: Float
    memoryUsage: String     # VULN: Memory stats exposed
    dependencies: String    # VULN: Package list exposed
  }

  type Alert {
    id: ID!
    type: String!
    message: String!
    severity: String
    userId: ID
    metadata: String        # VULN: Raw metadata in alerts
    createdAt: String
  }

  type SearchResult {
    users: [User]           # VULN: User data in search results
    products: [Product]
    orders: [Order]
  }

  # VULN #250: Permissive input types allow mass assignment
  input UserInput {
    username: String
    email: String
    password: String
    phone: String
    address: String
    role: String            # VULN #102: Role directly settable in input
    creditCard: String
    ssn: String
    isActive: Boolean
    loyaltyPoints: Int
    internalNotes: String   # VULN: Internal field settable by users
    refreshToken: String    # VULN: Token settable by users
  }

  input ProductInput {
    name: String
    description: String
    price: Float
    cost: Float             # VULN: Internal cost field settable
    stock: Int
    categoryId: ID
    sku: String
    discountPercentage: Float
    supplierCost: Float     # VULN: Business data settable
  }

  input OrderInput {
    userId: ID              # VULN: User ID settable = IDOR
    items: [OrderItemInput]
    total: Float            # VULN #309: Total price settable by client
    couponCode: String
    shippingAddress: String
    paymentInfo: PaymentInput
    discount: Float         # VULN: Discount settable directly
    status: String          # VULN: Status settable on creation
  }

  input OrderItemInput {
    productId: ID!
    quantity: Int!
    price: Float            # VULN #309: Price settable by client
    discount: Float         # VULN: Discount settable per item
  }

  input PaymentInput {
    cardNumber: String
    cardHolder: String
    cvv: String
    expiryDate: String
    amount: Float           # VULN #309: Amount client-controlled
  }

  input ProductFilter {
    category: String
    minPrice: Float
    maxPrice: Float
    search: String          # VULN: SQL injectable via raw query
    sortBy: String          # VULN: SQL injectable field name
    sortOrder: String       # VULN: SQL injectable order direction
    includeDeleted: Boolean # VULN: Soft-deleted items accessible
  }

  # VULN #104, #108, #113, #115: Many queries lack auth checks
  type Query {
    # User queries - no auth checks
    users(role: String, limit: Int, offset: Int): [User]      # VULN #104: Admin only but no check
    user(id: ID!): User                                        # VULN #97: IDOR - any user data
    userByEmail(email: String!): User                          # VULN: User enumeration
    userByUsername(username: String!): User                    # VULN: User enumeration
    me: User                                                   # Returns current user (checks token)
    searchUsers(query: String!): [User]                        # VULN: SQL injectable, returns PII

    # Product queries
    products(filter: ProductFilter, limit: Int, offset: Int): [Product]
    product(id: ID!): Product
    productBySku(sku: String!): Product
    productsByCategory(categoryId: ID!): [Product]

    # Order queries - IDOR and auth bypass
    orders(userId: ID, status: String, limit: Int): [Order]    # VULN #113: Returns ALL orders
    order(id: ID!): Order                                      # VULN: IDOR
    ordersByUser(userId: ID!): [Order]                         # VULN: IDOR

    # Cart - IDOR
    cart(userId: ID): Cart                                     # VULN: Access any user's cart

    # Payment data - highly sensitive
    payments(userId: ID, limit: Int): [Payment]                # VULN #115: Payment data, no auth
    payment(id: ID!): Payment                                  # VULN: IDOR on payments

    # Coupons - business logic abuse
    coupons: [Coupon]                                          # VULN: All coupon codes exposed
    coupon(code: String!): Coupon                              # VULN: Coupon detail including discount

    # Admin endpoints - no auth checks
    adminData: AdminData                                       # VULN #108: No auth
    systemInfo: SystemInfo                                     # VULN: Internal system info exposed
    dumpDatabase: String                                       # VULN (extreme): Full DB dump
    exportAllUsers: String                                     # VULN: All user PII exported

    # Reviews
    reviews(productId: ID, userId: ID): [Review]

    # Search - injectable
    search(query: String!, types: [String]): SearchResult      # VULN: SQL/NoSQL injectable

    # Categories
    categories: [Category]
    category(id: ID!): Category

    # Debug endpoints that should not exist in production
    debugInfo: String                                          # VULN: Debug info
    rawQuery(sql: String!): String                             # VULN (extreme): Direct SQL execution
  }

  # VULN #102, #250, #309: Mutations without auth or input validation
  type Mutation {
    # User mutations
    register(input: UserInput!): AuthPayload
    login(email: String!, password: String!): AuthPayload
    logout: Boolean

    createUser(input: UserInput!): User                        # VULN #250: Mass assignment
    updateUser(id: ID!, input: UserInput!): User               # VULN: No ownership check; mass assign
    updateUserRole(id: ID!, role: String!): User               # VULN #102: Privilege escalation
    deleteUser(id: ID!): Boolean                               # VULN: No auth check
    adminUpdateUser(id: ID!, input: UserInput!): User          # VULN #108: No admin check

    # Product mutations - no auth
    createProduct(input: ProductInput!): Product               # VULN: No admin check
    updateProduct(id: ID!, input: ProductInput!): Product      # VULN: No auth
    deleteProduct(id: ID!): Boolean                            # VULN: No auth

    # Order mutations
    createOrder(input: OrderInput!): Order                     # VULN #309: Total/price injectable
    updateOrderStatus(id: ID!, status: String!): Order         # VULN: No auth check
    cancelOrder(id: ID!): Order                                # VULN: Can cancel anyone's order

    # Payment mutations
    processPayment(orderId: ID!, amount: Float!, cardData: PaymentInput): Payment  # VULN #309: Amount client-controlled
    refundPayment(paymentId: ID!, amount: Float!): Payment     # VULN: Refund amount client-controlled

    # Cart mutations
    addToCart(userId: ID, productId: ID!, quantity: Int!, price: Float): Cart  # VULN: Price injectable
    removeFromCart(cartItemId: ID!): Cart
    clearCart(userId: ID): Boolean                             # VULN: Can clear anyone's cart

    # Coupon mutations
    applyDiscount(cartId: ID!, code: String!, discount: Float!): Cart  # VULN: Discount injectable
    createCoupon(code: String!, discount: Float!, maxUses: Int): Coupon  # VULN: No auth

    # Admin mutations
    executeSql(query: String!): String                         # VULN (extreme): Direct SQL execution
    updateSystemConfig(config: String!): Boolean               # VULN: No auth
    resetAllPasswords: Boolean                                 # VULN: Extreme admin action no check
  }

  # VULN #267: Subscriptions without authentication
  type Subscription {
    orderUpdated(userId: ID): Order                            # VULN: Anyone can subscribe to any user's orders
    paymentProcessed: Payment                                  # VULN: Leaks all payment events globally
    adminAlerts: Alert                                         # VULN: Admin alerts exposed to all subscribers
    userLoggedIn: User                                         # VULN: Login events expose user data
    newOrder: Order                                            # VULN: All new orders visible
    priceChanged: Product                                      # Legitimate but exposes cost field
  }

  type AuthPayload {
    token: String!
    refreshToken: String!
    user: User!
  }
`;

module.exports = { typeDefs };
