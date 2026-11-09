#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_DIR="$ROOT/scripts"
COMPOSE_FILE="$ROOT/docker-compose.yml"
LOCAL=0
STOP=0
NO_BUILD=0
FOREGROUND=0

for arg in "$@"; do
  case "$arg" in
    --local) LOCAL=1 ;;
    --stop) STOP=1 ;;
    --no-build) NO_BUILD=1 ;;
    --foreground) FOREGROUND=1 ;;
    -h|--help)
      echo "Usage: scripts/start-app.sh [--local] [--stop] [--no-build] [--foreground]"
      echo "  (no flags)     build images and start the Docker stack"
      echo "  --local        start backend and frontend natively"
      echo "  --stop         stop Docker and native processes"
      exit 0
      ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

if [ "$STOP" -eq 1 ]; then
  bash "$SCRIPT_DIR/dev-up.sh" --stop
  if command -v docker >/dev/null 2>&1; then
    docker compose -f "$COMPOSE_FILE" -p vulnshop down
  fi
  echo "VulnShop stopped."
  exit 0
fi

if [ "$LOCAL" -eq 1 ]; then
  bash "$SCRIPT_DIR/dev-up.sh"
else
  args=()
  [ "$NO_BUILD" -eq 1 ] && args+=(--no-build)
  [ "$FOREGROUND" -eq 1 ] && args+=(--foreground)
  bash "$SCRIPT_DIR/docker-up.sh" ${args[@]+"${args[@]}"}
fi
