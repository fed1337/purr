#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="/opt/lemur"
APP_DIR="/opt/lemur/lemur"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

source /opt/lemur/.venv/bin/activate


log_info() {
    echo -e "${BLUE}[supervisor]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[supervisor]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[supervisor]${NC} $*"
}

log_error() {
    echo -e "${RED}[supervisor]${NC} $*" >&2
}

init() {
    log_info "Initializing lemur database..."
    cd "$APP_DIR"
    lemur init -p "$LEMUR_PASSWORD" || log_error "Initialization failed"
    log_success "Lemur initialized"
}

migrate() {
    log_info "Running database migrations..."
    cd "$APP_DIR"
    lemur db upgrade || {
        log_error "Migration failed; refusing to start app"
        exit 1
  }
    log_success "Database migrations completed"
}

start() {
    local workers="${LEMUR_WORKERS:-4}"
    local bind="${LEMUR_BIND:-0.0.0.0:8000}"
    log_info "Starting Lemur server (workers=$workers, bind=$bind)..."
    cd "$ROOT_DIR"
    lemur start -w "$workers" -b "$bind" &
    LEMUR_PID=$!
    trap 'echo "[supervisor] Caught stop signal"; kill "$LEMUR_PID" 2>/dev/null || true' SIGTERM SIGINT
    echo "[supervisor] Starting Caddy (foreground)..."
    exec caddy run --config /opt/lemur/docker/Caddyfile
}

cli() {
    cd "$APP_DIR"
    log_info "Running Lemur CLI: $*"
    lemur "$@"
}

tests() {
    log_info "Running tests..."
    cd "$ROOT_DIR"
    pytest --cov=lemur --cov-report=html
    # doesn't work as no test deps are installed
}

drop_db() {
    log_info "Dropping database in 10 seconds"
    sleep 10
    cd "$APP_DIR"
    lemur db drop_all || log_error "Database hasn't been dropped"
    log_success "The database has been dropped"
}

main() {
    case "${1:-start}" in
        start)
            migrate
            start
            ;;
        migrate)
            migrate
            ;;
        init)
            init
            ;;
        drop)
            drop_db
            ;;
        lemur)
            shift
            cli "$@"
            ;;
        *)
            log_error "Unknown command: $command"
             exit  1
            ;;
  esac
}

main "$@"
