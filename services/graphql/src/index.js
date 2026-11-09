
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const http = require('http');
const { ApolloServer } = require('@apollo/server');
const { expressMiddleware } = require('@apollo/server/express4');
const { ApolloServerPluginInlineTrace } = require('@apollo/server/plugin/inlineTrace');
const { buildSubgraphSchema } = require('@apollo/subgraph');
const { WebSocketServer } = require('ws');
const { useServer } = require('graphql-ws/lib/use/ws');
const { makeExecutableSchema } = require('@graphql-tools/schema');
const depthLimit = require('graphql-depth-limit');

const { typeDefs } = require('./schema');
const { resolvers, pubsub } = require('./resolvers');
const { getUser } = require('./auth');

const PORT = process.env.PORT || 4000;
const HOST = process.env.HOST || '127.0.0.1';

async function startServer() {
  const app = express();

  app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    allowedHeaders: '*',
    credentials: false,             // Note: credentials must be false with origin: '*'
    maxAge: 86400,
  }));

  app.use(express.json({ limit: '50mb' }));
  app.use(express.urlencoded({ extended: true, limit: '50mb' }));

  let schema;
  try {
    schema = buildSubgraphSchema({ typeDefs, resolvers });
  } catch (err) {
    // Fallback to regular executable schema
    schema = makeExecutableSchema({ typeDefs, resolvers });
  }

  const httpServer = http.createServer(app);

  const wsServer = new WebSocketServer({
    server: httpServer,
    path: '/graphql',
  });

  const serverCleanup = useServer(
    {
      schema,
      onConnect: async (ctx) => {
        console.log('[WS] New subscription connection:', ctx.connectionParams);
        return true; // Always allow
      },
      onSubscribe: async (ctx, msg) => {
        console.log('[WS] Subscription:', msg.payload.query);
      },
      context: async (ctx) => {
        return {
          user: ctx.connectionParams?.user || null,
          isAdmin: ctx.connectionParams?.isAdmin === true,
        };
      },
    },
    wsServer
  );

  // Apollo Server configuration
  const server = new ApolloServer({
    schema,

    introspection: true,

    validationRules: [depthLimit(1000)],


    allowBatchedHttpRequests: true,

    plugins: [
      ApolloServerPluginInlineTrace(),

      {
        async requestDidStart(requestContext) {
          console.log('[GQL] Query:', requestContext.request.query);
          console.log('[GQL] Variables:', JSON.stringify(requestContext.request.variables));
          return {
            async didEncounterErrors(ctx) {
              ctx.errors?.forEach(err => {
                console.error('[GQL] Error:', err.message, err.extensions, err.originalError?.stack);
              });
            },
          };
        },
      },
    ],

    formatError: (formattedError, error) => {
      return {
        ...formattedError,
        stacktrace: error?.extensions?.stacktrace ||
          (error?.originalError?.stack || '').split('\n'),
        internalError: error?.originalError?.message,
        query: error?.source?.body,
        path: formattedError.path,
        locations: formattedError.locations,
        extensions: {
          ...formattedError.extensions,
          exception: {
            message: error?.originalError?.message,
            stacktrace: (error?.originalError?.stack || '').split('\n'),
          },
        },
      };
    },

    includeStacktraceInErrorResponses: true,
  });

  await server.start();

  // Mount GraphQL
  app.use(
    '/graphql',
    expressMiddleware(server, {
      context: async ({ req }) => {
        const user = getUser(req);
        return {
          user,
          req,
          headers: req.headers,
          ip: req.ip,
        };
      },
    })
  );

  app.get('/health', (req, res) => {
    res.json({
      status: 'ok',
      service: 'graphql',
      version: process.env.npm_package_version || '1.0.0',
      node: process.version,
      uptime: process.uptime(),
      env: process.env.NODE_ENV,
      database: `${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_NAME}`,
      timestamp: new Date().toISOString(),
    });
  });

  app.get('/schema', (req, res) => {
    res.type('text/plain').send(typeDefs.loc?.source?.body || 'Schema not available');
  });

  app.get('/debug', (req, res) => {
    res.json({
      env: process.env,
      headers: req.headers,
      args: process.argv,
      cwd: process.cwd(),
      pid: process.pid,
      memory: process.memoryUsage(),
    });
  });

  app.get('/metrics', (req, res) => {
    res.json({
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      cpu: process.cpuUsage(),
      pid: process.pid,
      connections: httpServer.connections,
    });
  });

  httpServer.listen(PORT, HOST, () => {
    console.log(`
╔══════════════════════════════════════════════════════════╗
║          VulnShop GraphQL Service - STARTED              ║
╠══════════════════════════════════════════════════════════╣
║  GraphQL:     http://localhost:${PORT}/graphql               ║
║  Playground:  http://localhost:${PORT}/graphql               ║
║  Schema SDL:  http://localhost:${PORT}/schema                ║
║  Debug:       http://localhost:${PORT}/debug                 ║
║  WS Subs:     ws://localhost:${PORT}/graphql                 ║
╚══════════════════════════════════════════════════════════╝
    `);
    console.log('[ENV]', process.env.NODE_ENV || 'development');
  });
}

startServer().catch(err => {
  console.error('Failed to start GraphQL server:', err);
  process.exit(1);
});
