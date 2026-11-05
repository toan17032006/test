require('dotenv').config();
const express = require('express');
const session = require('express-session');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const morgan = require('morgan');
const fileUpload = require('express-fileupload');
const path = require('path');
const http = require('http');
const { Server } = require('socket.io');
const fs = require('fs');

const app = express();
const server = http.createServer(app);

// =====================================================
// INTENTIONAL VULN: Socket.io with NO authentication
// vuln #271 - WebSocket without auth
// =====================================================
const io = new Server(server, {
  cors: { origin: '*', methods: ['GET', 'POST'] }
});

io.on('connection', (socket) => {
  console.log('[WS] New connection:', socket.id, 'IP:', socket.handshake.address);
  // No auth check at all
  socket.on('join_room', (room) => {
    // No validation, anyone can join any room
    socket.join(room);
    socket.emit('joined', { room, userId: socket.handshake.query.userId });
  });
  socket.on('admin_broadcast', (msg) => {
    // No admin check - anyone can broadcast
    io.emit('notification', msg);
  });
  socket.on('get_user_data', (userId) => {
    // IDOR - returns any user data without auth
    socket.emit('user_data', { userId, token: 'fake-token-' + userId });
  });
});

// =====================================================
// INTENTIONAL VULN: CORS allows all origins
// =====================================================
app.use(cors());

// INTENTIONAL: Helmet DISABLED
// app.use(helmet()); // Disabled intentionally - no security headers

// Template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// =====================================================
// INTENTIONAL VULN: Session with weak config
// - Weak secret
// - No secure flag (works over HTTP)
// - No httpOnly (accessible to JS)
// - No sameSite (CSRF possible)
// =====================================================
app.use(session({
  secret: process.env.SESSION_SECRET || 'weak-secret-123',
  resave: true,
  saveUninitialized: true,
  cookie: {
    secure: false,      // VULN: works over HTTP
    httpOnly: false,    // VULN: JS can read session cookie
    sameSite: false,    // VULN: CSRF possible
    maxAge: 30 * 24 * 60 * 60 * 1000
  },
  name: 'sessionId'
}));

// Cookie parser
app.use(cookieParser());

// Body parsers
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// File upload
app.use(fileUpload({
  useTempFiles: true,
  tempFileDir: '/tmp/',
  limits: { fileSize: 50 * 1024 * 1024 }
  // No file type validation - intentional
}));

// =====================================================
// INTENTIONAL VULN: Request logging with sensitive data
// Logs passwords, tokens, card numbers etc.
// =====================================================
morgan.token('body', (req) => JSON.stringify(req.body));
morgan.token('cookies', (req) => JSON.stringify(req.cookies));
app.use(morgan(':method :url :status :response-time ms - body: :body - cookies: :cookies'));

// =====================================================
// INTENTIONAL VULN: Static file serving
// - Exposes source maps
// - Exposes .env
// - Exposes .git
// =====================================================
app.use(express.static(path.join(__dirname, 'public')));
app.use('/.git', express.static(path.join(__dirname, '.git')));

// Pentest inventory viewer. Progress is stored in the visitor's browser only.
const vulnDbDir = process.env.VULNDB_DIR || path.join(__dirname, '..', 'vulndb');
app.get('/admin/vulns', (req, res) => {
  res.sendFile(path.join(vulnDbDir, 'index.html'));
});
app.get('/api/vuln-catalog', (req, res) => {
  res.sendFile(path.join(vulnDbDir, 'catalog.json'));
});

// Serve .env directly
app.get('/.env', (req, res) => {
  res.type('text/plain');
  try {
    res.send(fs.readFileSync(path.join(__dirname, '.env'), 'utf8'));
  } catch (e) {
    res.send('API_URL=http://api:8000\nSESSION_SECRET=session-secret-weak\nJWT_SECRET=jwt-secret-weak');
  }
});

// robots.txt
app.get('/robots.txt', (req, res) => {
  res.sendFile(path.join(__dirname, 'robots.txt'));
});

// Debug endpoint (intentional)
app.get('/debug', (req, res) => {
  res.json({
    env: process.env,
    session: req.session,
    headers: req.headers,
    cookies: req.cookies
  });
});

// Source map (intentional exposure)
app.get('/js/app.js.map', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'js', 'app.js.map'));
});

// Routes
const indexRouter = require('./routes/index');
const apiRouter = require('./routes/api');
const webhookRouter = require('./routes/webhook');

app.use('/', indexRouter);
app.use('/api', apiRouter);
app.use('/webhook', webhookRouter);

// Admin redirect (no auth)
app.get('/admin', (req, res) => {
  // INTENTIONAL: No auth check before redirect
  res.redirect('/admin/vulns');
});
app.get('/admin/dashboard', (req, res) => {
  res.redirect('/admin/vulns');
});

// =====================================================
// INTENTIONAL VULN: Error handler exposes stack traces
// =====================================================
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: err.message,
    stack: err.stack,         // VULN: stack trace exposed
    env: process.env.NODE_ENV,
    file: err.fileName,
    line: err.lineNumber
  });
});

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '127.0.0.1';
server.listen(PORT, HOST, () => {
  console.log(`VulnShop frontend running on http://${HOST}:${PORT}`);
  console.log(`[WARNING] This app is intentionally vulnerable!`);
});

module.exports = app;
