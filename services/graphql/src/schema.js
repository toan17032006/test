
const { gql } = require('graphql-tag');

const typeDefs = gql`
  type User {
    id: ID!
    username: String!
    email: String!
    password: String!
    phone: String
    address: String
    role: String            # admin, user, moderator
    creditCard: String
    ssn: String
    bankAccount: String
    orders: [Order]
    cart: Cart
    wishlist: [Product]
    loyaltyPoints: Int
    refreshToken: String
    resetToken: String
    createdAt: String
    lastLogin: String
    isActive: Boolean
    failedLoginAttempts: Int
    internalNotes: String
  }

  type Product {
    id: ID!
    name: String!
    description: String!
    price: Float!
    cost: Float
    stock: Int!
    sku: String
    category: Category
    reviews: [Review]
    variants: [ProductVariant]
    supplier: Supplier
    supplierCost: Float
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
    contractTerms: String
  }

  type Order {
    id: ID!
    user: User
    items: [OrderItem]
    total: Float!
    status: String!
    paymentInfo: PaymentInfo
    shippingAddress: String
    trackingNumber: String
    notes: String
    couponUsed: String
    createdAt: String
    updatedAt: String
    internalStatus: String
  }

  type OrderItem {
    id: ID!
    product: Product
    quantity: Int!
    price: Float!
    discount: Float
  }

  type PaymentInfo {
    id: ID!
    cardNumber: String
    cardHolder: String
    cvv: String
    expiryDate: String
    amount: Float
    status: String
    transactionId: String
    gatewayResponse: String
  }

  type Payment {
    id: ID!
    orderId: ID
    userId: ID
    amount: Float!
    method: String
    cardNumber: String
    cvv: String
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
    discount: Float!
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
    adminNote: String
    createdAt: String
  }

  type AdminData {
    totalUsers: Int
    totalOrders: Int
    totalRevenue: Float
    systemConfig: String
    secretKeys: [String]
    databaseConfig: String
    internalLogs: String
    activeUsers: [User]
    adminUsers: [User]
  }

  type SystemInfo {
    version: String
    nodeVersion: String
    osInfo: String
    databaseVersion: String
    env: String
    uptime: Float
    memoryUsage: String
    dependencies: String
  }

  type Alert {
    id: ID!
    type: String!
    message: String!
    severity: String
    userId: ID
    metadata: String
    createdAt: String
  }

  type SearchResult {
    users: [User]
    products: [Product]
    orders: [Order]
  }

  input UserInput {
    username: String
    email: String
    password: String
    phone: String
    address: String
    role: String
    creditCard: String
    ssn: String
    isActive: Boolean
    loyaltyPoints: Int
    internalNotes: String
    refreshToken: String
  }

  input ProductInput {
    name: String
    description: String
    price: Float
    cost: Float
    stock: Int
    categoryId: ID
    sku: String
    discountPercentage: Float
    supplierCost: Float
  }

  input OrderInput {
    userId: ID
    items: [OrderItemInput]
    total: Float
    couponCode: String
    shippingAddress: String
    paymentInfo: PaymentInput
    discount: Float
    status: String
  }

  input OrderItemInput {
    productId: ID!
    quantity: Int!
    price: Float
    discount: Float
  }

  input PaymentInput {
    cardNumber: String
    cardHolder: String
    cvv: String
    expiryDate: String
    amount: Float
  }

  input ProductFilter {
    category: String
    minPrice: Float
    maxPrice: Float
    search: String
    sortBy: String
    sortOrder: String
    includeDeleted: Boolean
  }

  type Query {
    users(role: String, limit: Int, offset: Int): [User]
    user(id: ID!): User
    userByEmail(email: String!): User
    userByUsername(username: String!): User
    me: User
    searchUsers(query: String!): [User]

    products(filter: ProductFilter, limit: Int, offset: Int): [Product]
    product(id: ID!): Product
    productBySku(sku: String!): Product
    productsByCategory(categoryId: ID!): [Product]

    orders(userId: ID, status: String, limit: Int): [Order]
    order(id: ID!): Order
    ordersByUser(userId: ID!): [Order]

    cart(userId: ID): Cart

    payments(userId: ID, limit: Int): [Payment]
    payment(id: ID!): Payment

    coupons: [Coupon]
    coupon(code: String!): Coupon

    adminData: AdminData
    systemInfo: SystemInfo
    dumpDatabase: String
    exportAllUsers: String

    reviews(productId: ID, userId: ID): [Review]

    search(query: String!, types: [String]): SearchResult

    categories: [Category]
    category(id: ID!): Category

    debugInfo: String
    rawQuery(sql: String!): String
  }

  type Mutation {
    register(input: UserInput!): AuthPayload
    login(email: String!, password: String!): AuthPayload
    logout: Boolean

    createUser(input: UserInput!): User
    updateUser(id: ID!, input: UserInput!): User
    updateUserRole(id: ID!, role: String!): User
    deleteUser(id: ID!): Boolean
    adminUpdateUser(id: ID!, input: UserInput!): User

    createProduct(input: ProductInput!): Product
    updateProduct(id: ID!, input: ProductInput!): Product
    deleteProduct(id: ID!): Boolean

    createOrder(input: OrderInput!): Order
    updateOrderStatus(id: ID!, status: String!): Order
    cancelOrder(id: ID!): Order

    processPayment(orderId: ID!, amount: Float!, cardData: PaymentInput): Payment
    refundPayment(paymentId: ID!, amount: Float!): Payment

    addToCart(userId: ID, productId: ID!, quantity: Int!, price: Float): Cart
    removeFromCart(cartItemId: ID!): Cart
    clearCart(userId: ID): Boolean

    applyDiscount(cartId: ID!, code: String!, discount: Float!): Cart
    createCoupon(code: String!, discount: Float!, maxUses: Int): Coupon

    executeSql(query: String!): String
    updateSystemConfig(config: String!): Boolean
    resetAllPasswords: Boolean
  }

  type Subscription {
    orderUpdated(userId: ID): Order
    paymentProcessed: Payment
    adminAlerts: Alert
    userLoggedIn: User
    newOrder: Order
    priceChanged: Product                                      # Legitimate but exposes cost field
  }

  type AuthPayload {
    token: String!
    refreshToken: String!
    user: User!
  }
`;

module.exports = { typeDefs };
