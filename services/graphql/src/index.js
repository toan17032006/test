// VulnShop GraphQL Service - Main Entry Point
// INTENTIONALLY VULNERABLE - For educational/pentesting purposes only
// Vulnerabilities: #20, #187, #260, #264, #265, #266, #267, #268

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

  // VULN #187: CORS allows ALL origins - no restriction
  app.use(cors({
    origin: '*',                    // VULN: Wildcard CORS
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    allowedHeaders: '*',            // VULN: All headers allowed
    credentials: false,             // Note: credentials must be false with origin: '*'
    maxAge: 86400,
  }));

  app.use(express.json({ limit: '50mb' })); // VULN: Large payload limit (DoS risk)
  app.use(express.urlencoded({ extended: true, limit: '50mb' }));

  // Build schema - using buildSubgraphSchema for federation (vuln #268)
  let schema;
  try {
    // VULN #268: Federation enabled - exposes _service, _entities, _sdl
    schema = buildSubgraphSchema({ typeDefs, resolvers });
  } catch (err) {
    // Fallback to regular executable schema
    schema = makeExecutableSchema({ typeDefs, resolvers });
  }

  const httpServer = http.createServer(app);

  // VULN #267: WebSocket server for subscriptions - NO AUTH
  const wsServer = new WebSocketServer({
    server: httpServer,
    path: '/graphql',
  });

  // Setup GraphQL over WebSocket (subscriptions) - no auth
  const serverCleanup = useServer(
    {
      schema,
      // VULN #267: No authentication on websocket connection
      onConnect: async (ctx) => {
        console.log('[WS] New subscription connection:', ctx.connectionParams);
        // VULN: Accept all connections, log params (may contain tokens)
        return true; // Always allow
      },
      onSubscribe: async (ctx, msg) => {
        console.log('[WS] Subscription:', msg.payload.query);
        // VULN: No auth check on subscriptions
      },
      context: async (ctx) => {
        // VULN: Extract user from connection params without validation
        return {
          user: ctx.connectionParams?.user || null,
          // VULN: Trust user role from client
          isAdmin: ctx.connectionParams?.isAdmin === true,
        };
      },
    },
    wsServer
  );

  // Apollo Server configuration
  const server = new ApolloServer({
    schema,

    // VULN #20, #260: Introspection ALWAYS enabled regardless of environment
    introspection: true,

    // VULN #264: Effectively no depth limit (1000 is functionally unlimited)
    // Real protection would be depthLimit(5) or depthLimit(7)
    validationRules: [depthLimit(1000)],

    // VULN #265: No query complexity limit configured
    // No complexity plugin installed

    // VULN #266: Batching enabled (allows batch GraphQL attacks)
    allowBatchedHttpRequests: true,

    // VULN: Inline tracing exposes query execution details
    plugins: [
      ApolloServerPluginInlineTrace(),

      // Custom plugin to log all queries (may log sensitive data)
      {
        async requestDidStart(requestContext) {
          console.log('[GQL] Query:', requestContext.request.query);
          console.log('[GQL] Variables:', JSON.stringify(requestContext.request.variables));
          return {
            async didEncounterErrors(ctx) {
              // VULN: Full error details including stack traces
              ctx.errors?.forEach(err => {
                console.error('[GQL] Error:', err.message, err.extensions, err.originalError?.stack);
              });
            },
          };
        },
      },
    ],

    // VULN: Detailed error formatting - exposes stack traces
    formatError: (formattedError, error) => {
      return {
        ...formattedError,
        // VULN: Expose internal error details
        stacktrace: error?.extensions?.stacktrace ||
          (error?.originalError?.stack || '').split('\n'),
        internalError: error?.originalError?.message,
        query: error?.source?.body,        // VULN: Echo the query back
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

    // VULN: Include suggestions in errors (helps attackers enumerate schema)
    includeStacktraceInErrorResponses: true,
  });

  await server.start();

  // Mount GraphQL
  app.use(
    '/graphql',
    expressMiddleware(server, {
      context: async ({ req }) => {
        // VULN: User extracted from token without strict validation
        const user = getUser(req);
        return {
          user,
          req,
          // VULN: Pass raw headers to context (accessible in resolvers)
          headers: req.headers,
          ip: req.ip,
        };
      },
    })
  );

  // VULN: Health check endpoint leaks environment info
  app.get('/health', (req, res) => {
    res.json({
      status: 'ok',
      service: 'graphql',
      version: process.env.npm_package_version || '1.0.0',
      node: process.version,
      uptime: process.uptime(),
      env: process.env.NODE_ENV,
      // VULN: DB info in health check
      database: `${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_NAME}`,
      timestamp: new Date().toISOString(),
    });
  });

  // VULN: SDL/Schema endpoint exposed (federation)
  app.get('/schema', (req, res) => {
    res.type('text/plain').send(typeDefs.loc?.source?.body || 'Schema not available');
  });

  // VULN: Debug endpoint exposes all env vars
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

  // VULN: Metrics endpoint without auth
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
║   ** INTENTIONALLY VULNERABLE - PENTESTING ONLY **       ║
╠══════════════════════════════════════════════════════════╣
║  GraphQL:     http://localhost:${PORT}/graphql               ║
║  Playground:  http://localhost:${PORT}/graphql               ║
║  Schema SDL:  http://localhost:${PORT}/schema                ║
║  Debug:       http://localhost:${PORT}/debug                 ║
║  WS Subs:     ws://localhost:${PORT}/graphql                 ║
╚══════════════════════════════════════════════════════════╝
    `);
    console.log('[CONFIG] Introspection: ALWAYS ENABLED (vuln #20, #260)');
    console.log('[CONFIG] Depth limit: 1000 (effectively none, vuln #264)');
    console.log('[CONFIG] Complexity limit: NONE (vuln #265)');
    console.log('[CONFIG] Batching: ENABLED (vuln #266)');
    console.log('[CONFIG] Subscriptions auth: NONE (vuln #267)');
    console.log('[CONFIG] Federation: ENABLED (vuln #268)');
    console.log('[CONFIG] CORS: ALL ORIGINS (vuln #187)');
    console.log('[ENV]', process.env.NODE_ENV || 'development');
  });
}

startServer().catch(err => {
  console.error('Failed to start GraphQL server:', err);
  process.exit(1);
});
