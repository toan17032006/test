#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT/docker-compose.yml"
PROJECT="vulnshop"
BUILD=1
FOREGROUND=0

for arg in "$@"; do
  case "$arg" in
    --no-build) BUILD=0 ;;
    --foreground) FOREGROUND=1 ;;
    -h|--help)
      echo "Usage: scripts/docker-up.sh [--no-build] [--foreground]"
      exit 0
      ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker CLI not found. Install Docker Engine + Compose v2, start it, then rerun this script." >&2
  exit 1
fi

lan_ip() {
  if command -v ip >/dev/null 2>&1; then
    ip -4 route get 1.1.1.1 2>/dev/null | awk '{print $7; exit}'
  elif command -v powershell >/dev/null 2>&1; then
    powershell -NoProfile -Command '$r = Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Sort-Object RouteMetric | Select-Object -First 1; Get-NetIPAddress -AddressFamily IPv4 -InterfaceIndex $r.ifIndex | Where-Object { $_.IPAddress -ne "127.0.0.1" } | Select-Object -First 1 -ExpandProperty IPAddress' 2>/dev/null | tr -d '\r'
  elif command -v ipconfig >/dev/null 2>&1; then
    ipconfig 2>/dev/null | awk '/IPv4/ {print $NF; exit}' | tr -d '\r'
  fi
}

wait_url() {
  local url="$1" deadline=$(( $(date +%s) + 180 ))
  while [ "$(date +%s)" -lt "$deadline" ]; do
    if curl -fsS -o /dev/null --max-time 3 "$url"; then
      return 0
    fi
    sleep 2
  done
  return 1
}

echo "Building the VulnShop Docker images..."
if [ "$BUILD" -eq 1 ]; then
  docker compose -f "$COMPOSE_FILE" -p "$PROJECT" build
fi

if [ "$FOREGROUND" -eq 1 ]; then
  echo "Starting the stack in the foreground. Press Ctrl+C to stop."
  exec docker compose -f "$COMPOSE_FILE" -p "$PROJECT" up
fi

echo "Starting the VulnShop stack..."
docker compose -f "$COMPOSE_FILE" -p "$PROJECT" up -d

echo "Waiting for the backend and storefront to answer..."
if ! wait_url "http://127.0.0.1:18000/health" || ! wait_url "http://127.0.0.1:13000/"; then
  docker compose -f "$COMPOSE_FILE" -p "$PROJECT" ps || true
  docker compose -f "$COMPOSE_FILE" -p "$PROJECT" logs --tail=80 || true
  echo "Services did not become ready in time. See the logs above." >&2
  exit 1
fi

lan="$(lan_ip || true)"
echo ""
echo "VulnShop is running."
echo "  Storefront (this machine): http://127.0.0.1:13000"
if [ -n "$lan" ]; then echo "  Storefront (LAN browser):  http://${lan}:13000"; fi
echo "  Nginx entry point:         http://127.0.0.1:9080"
if [ -n "$lan" ]; then echo "  Nginx (LAN browser):       http://${lan}:9080"; fi
echo "  Backend API:               http://127.0.0.1:18000/health"
echo "  OpenAPI docs:              http://127.0.0.1:18000/docs"
echo "  GraphQL:                   http://127.0.0.1:14000/graphql"
echo "  MailHog inbox:             http://127.0.0.1:18025"
echo ""
echo "Stop with: scripts/start-app.sh --stop"
