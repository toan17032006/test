#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$ROOT/.run"
LOG_DIR="$RUN_DIR/logs"
API_PORT=18000
WEB_PORT=13000
STOP=0
NO_INSTALL=0

for arg in "$@"; do
  case "$arg" in
    --stop) STOP=1 ;;
    --no-install) NO_INSTALL=1 ;;
    -h|--help)
      echo "Usage: scripts/dev-up.sh [--stop] [--no-install]"
      exit 0
      ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

stop_tracked() {
  local name="$1"
  local pid_file="$RUN_DIR/$name.pid"
  if [ -f "$pid_file" ]; then
    local pid
    pid="$(head -n 1 "$pid_file" || true)"
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
    fi
    rm -f "$pid_file"
  fi
}

if [ "$STOP" -eq 1 ]; then
  stop_tracked api
  stop_tracked frontend
  echo "Native VulnShop processes stopped."
  exit 0
fi

mkdir -p "$LOG_DIR"
stop_tracked api
stop_tracked frontend

if ! command -v python >/dev/null 2>&1; then
  echo "Python not found on PATH. Install Python 3.12 and add it to PATH." >&2
  exit 1
fi

if ! python -c 'import fastapi, uvicorn' >/dev/null 2>&1; then
  echo "Backend dependencies are missing. Run: python -m pip install -r backend/requirements.txt" >&2
  exit 1
fi

if [ ! -d "$ROOT/frontend/node_modules/express" ]; then
  if [ "$NO_INSTALL" -eq 1 ]; then
    echo "Frontend dependencies are missing and --no-install was set. Run: npm --prefix frontend ci" >&2
    exit 1
  fi
  echo "Installing frontend dependencies..."
  (cd "$ROOT/frontend" && npm ci)
fi

export PYTHONUNBUFFERED=1
export DATABASE_URL='postgresql://postgres:postgres123@127.0.0.1:15432/vulnshop'
export MYSQL_URL='mysql+pymysql://mysql_user:mysql_pass@127.0.0.1:13306/vulnshop_legacy'
export MONGODB_URL='mongodb://127.0.0.1:27017/vulnshop'
export REDIS_URL='redis://127.0.0.1:16379/0'
export ELASTICSEARCH_URL='http://127.0.0.1:19200'
export NEO4J_URL='bolt://127.0.0.1:17687'
export SMTP_HOST='127.0.0.1'
export SMTP_PORT='11025'
export SECRET_KEY='local-dev-secret'
export JWT_SECRET='jwt-secret-weak'
export ADMIN_PASSWORD='admin123'
export DEBUG='true'

(
  cd "$ROOT/backend"
  python -m uvicorn main:app --host 0.0.0.0 --port "$API_PORT" >"$LOG_DIR/api.log" 2>&1 &
  echo $! >"$RUN_DIR/api.pid"
)

export API_URL="http://127.0.0.1:$API_PORT"
export GRAPHQL_URL='http://127.0.0.1:14000/graphql'
export HOST='0.0.0.0'
export PORT="$WEB_PORT"
export NODE_ENV='development'
export SESSION_SECRET='session-secret-weak'

(
  cd "$ROOT/frontend"
  node server.js >"$LOG_DIR/frontend.log" 2>&1 &
  echo $! >"$RUN_DIR/frontend.pid"
)

wait_url() {
  local url="$1" deadline=$(( $(date +%s) + 60 ))
  while [ "$(date +%s)" -lt "$deadline" ]; do
    if curl -fsS -o /dev/null --max-time 2 "$url"; then
      return 0
    fi
    sleep 1
  done
  return 1
}

echo "Waiting for the backend and storefront to answer..."
if ! wait_url "http://127.0.0.1:$API_PORT/health" || ! wait_url "http://127.0.0.1:$WEB_PORT/"; then
  stop_tracked api
  stop_tracked frontend
  tail -n 40 "$LOG_DIR/api.log" "$LOG_DIR/frontend.log" 2>/dev/null || true
  echo "Native services did not become ready in time. See the logs above." >&2
  exit 1
fi

lan=""
if command -v ip >/dev/null 2>&1; then
  lan="$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{print $7; exit}' || true)"
elif command -v powershell >/dev/null 2>&1; then
  lan="$(powershell -NoProfile -Command '$r = Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Sort-Object RouteMetric | Select-Object -First 1; Get-NetIPAddress -AddressFamily IPv4 -InterfaceIndex $r.ifIndex | Where-Object { $_.IPAddress -ne "127.0.0.1" } | Select-Object -First 1 -ExpandProperty IPAddress' 2>/dev/null | tr -d '\r' || true)"
elif command -v ipconfig >/dev/null 2>&1; then
  lan="$(ipconfig 2>/dev/null | awk '/IPv4/ {print $NF; exit}' | tr -d '\r')"
fi

echo ""
echo "VulnShop is running natively."
echo "  Storefront (this machine): http://127.0.0.1:$WEB_PORT"
if [ -n "$lan" ]; then echo "  Storefront (LAN browser):  http://${lan}:$WEB_PORT"; fi
echo "  Backend API:               http://127.0.0.1:$API_PORT/health"
echo "  Logs:                      $LOG_DIR"
echo ""
echo "Stop with: scripts/start-app.sh --stop"
