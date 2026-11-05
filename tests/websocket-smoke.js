'use strict';

const WebSocket = require('../services/graphql/node_modules/ws');

function withTimeout(promise, timer, label) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error(`${label} timed out`)), timer);
    promise.then(
      (value) => { clearTimeout(timeout); resolve(value); },
      (error) => { clearTimeout(timeout); reject(error); },
    );
  });
}

function probeSocketIo(baseUrl) {
  return withTimeout(new Promise((resolve, reject) => {
    const url = `${baseUrl.replace(/^http/, 'ws')}/socket.io/?EIO=4&transport=websocket`;
    const socket = new WebSocket(url, { headers: { Origin: 'https://attacker.invalid' } });
    let settled = false;
    let receivedUserData = false;
    let probeTimer;

    const finish = (error, value) => {
      if (settled) return;
      settled = true;
      clearTimeout(probeTimer);
      if (socket.readyState === WebSocket.OPEN) socket.close();
      else if (socket.readyState === WebSocket.CONNECTING) socket.terminate();
      if (error) reject(error);
      else resolve(value);
    };
    probeTimer = setTimeout(() => finish(new Error('Socket.IO probe timed out')), 4000);

    socket.on('message', (raw) => {
      const packet = raw.toString();
      if (packet.startsWith('0')) {
        socket.send('40');
        return;
      }
      if (packet.startsWith('40')) {
        socket.send('42["get_user_data",3]');
        return;
      }
      if (packet.startsWith('44')) {
        finish(new Error(`Socket.IO rejected the unauthenticated test client: ${packet}`));
        return;
      }
      if (packet.startsWith('42')) {
        try {
          const [event, data] = JSON.parse(packet.slice(2));
          if (event === 'user_data') {
            if (String(data.userId) !== '3' || data.token !== 'fake-token-3') {
              finish(new Error('Socket.IO returned unexpected data for the synthetic user probe.'));
              return;
            }
            receivedUserData = true;
            socket.send('42["admin_broadcast","LAB_ONLY_BROADCAST"]');
            return;
          }
          if (event === 'notification' && receivedUserData && data === 'LAB_ONLY_BROADCAST') {
            finish(null, 'An unauthenticated attacker-origin Socket.IO client read the fake user token and broadcast a lab marker.');
          }
        } catch (error) {
          finish(error);
        }
      }
    });
    socket.on('error', (error) => finish(error));
  }), 5000, 'Socket.IO probe');
}

function probeGraphqlSubscription(baseUrl) {
  return withTimeout(new Promise((resolve, reject) => {
    const url = `${baseUrl.replace(/^http/, 'ws')}/graphql`;
    const socket = new WebSocket(url, 'graphql-transport-ws');
    let subscribed = false;
    let settled = false;
    let probeTimer;
    let observationTimer;

    const finish = (error, value) => {
      if (settled) return;
      settled = true;
      clearTimeout(probeTimer);
      clearTimeout(observationTimer);
      if (socket.readyState === WebSocket.OPEN) socket.close();
      else if (socket.readyState === WebSocket.CONNECTING) socket.terminate();
      if (error) reject(error);
      else resolve(value);
    };
    probeTimer = setTimeout(() => finish(new Error('GraphQL subscription probe timed out')), 4000);

    socket.on('open', () => socket.send(JSON.stringify({ type: 'connection_init' })));
    socket.on('message', (raw) => {
      let message;
      try {
        message = JSON.parse(raw.toString());
      } catch (error) {
        finish(error);
        return;
      }
      if (message.type === 'connection_ack' && !subscribed) {
        subscribed = true;
        socket.send(JSON.stringify({
          id: 'synthetic-admin-alert-subscription',
          type: 'subscribe',
          payload: { query: 'subscription { adminAlerts { id } }' },
        }));
      } else if (message.type === 'error') {
        finish(new Error(`Unauthenticated GraphQL subscription was rejected: ${JSON.stringify(message.payload)}`));
      }
    });
    socket.on('error', (error) => finish(error));

    observationTimer = setTimeout(() => {
      if (!subscribed || socket.readyState !== WebSocket.OPEN) {
        finish(new Error('GraphQL service did not keep the unauthenticated subscription open.'));
        return;
      }
      finish(null, 'Unauthenticated GraphQL adminAlerts subscription was accepted; the lab emitted no event data.');
    }, 350);
  }), 5000, 'GraphQL subscription probe');
}

async function main() {
  if (process.argv.length !== 4) throw new Error('Expected storefront and GraphQL base URLs.');
  console.log(await probeSocketIo(process.argv[2]));
  console.log(await probeGraphqlSubscription(process.argv[3]));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
