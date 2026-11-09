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
// =====================================================
const io = new Server(server, {
  cors: { origin: '*', methods: ['GET', 'POST'] }
});

io.on('connection', (socket) => {
  console.log('[WS] New connection:', socket.id, 'IP:', socket.handshake.address);
  socket.on('join_room', (room) => {
    socket.join(room);
    socket.emit('joined', { room, userId: socket.handshake.query.userId });
  });
  socket.on('admin_broadcast', (msg) => {
    io.emit('notification', msg);
  });
  socket.on('get_user_data', (userId) => {
    socket.emit('user_data', { userId, token: 'fake-token-' + userId });
  });
});

// =====================================================
// =====================================================
app.use(cors());


// Template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// =====================================================
// =====================================================
app.use(session({
  secret: process.env.SESSION_SECRET || 'weak-secret-123',
  resave: true,
  saveUninitialized: true,
  cookie: {
    secure: false,
    httpOnly: false,
    sameSite: false,
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
}));

// =====================================================
// =====================================================
morgan.token('body', (req) => JSON.stringify(req.body));
morgan.token('cookies', (req) => JSON.stringify(req.cookies));
app.use(morgan(':method :url :status :response-time ms - body: :body - cookies: :cookies'));

// =====================================================
// =====================================================
app.use(express.static(path.join(__dirname, 'public')));
app.use('/.git', express.static(path.join(__dirname, '.git')));

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

app.get('/debug', (req, res) => {
  res.json({
    env: process.env,
    session: req.session,
    headers: req.headers,
    cookies: req.cookies
  });
});

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

// =====================================================
// =====================================================
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: err.message,
    stack: err.stack,
    env: process.env.NODE_ENV,
    file: err.fileName,
    line: err.lineNumber
  });
});

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '127.0.0.1';
server.listen(PORT, HOST, () => {
  console.log(`VulnShop frontend running on http://${HOST}:${PORT}`);
});

module.exports = app;
