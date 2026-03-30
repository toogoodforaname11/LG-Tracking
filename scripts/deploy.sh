#!/bin/bash
# scripts/deploy.sh — deploy (or redeploy) the LG-Tracking application
#
# Works for both fresh installs and updates:
#   1. Install Python deps into a venv
#   2. Run alembic migrations
#   3. Seed reference data (municipalities + sources)
#   4. Build the frontend
#   5. Restart the systemd service
#
# Usage:
#   bash scripts/deploy.sh              # from the repo root
#   bash /var/www/lg-tracking/scripts/deploy.sh   # absolute path on VPS
#
# Prerequisites:
#   - Python 3.11+ available as python3.11 (or python3)
#   - Node.js 20+ and npm
#   - PostgreSQL running with credentials in backend/.env
#   - backend/.env exists (copy from backend/.env.example and fill in values)

set -euo pipefail

# --- Resolve paths ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$REPO_DIR/backend"
FRONTEND_DIR="$REPO_DIR/frontend"
VENV_DIR="$REPO_DIR/venv"
SERVICE_NAME="bc-hearing-watch"

# Prefer python3.11 if available, fall back to python3
PYTHON="python3"
if command -v python3.11 &> /dev/null; then
    PYTHON="python3.11"
fi

echo "=== LG-Tracking Deploy ==="
echo "Repo:     $REPO_DIR"
echo "Python:   $($PYTHON --version 2>&1)"
echo ""

# --- Check .env exists ---
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo "ERROR: $BACKEND_DIR/.env not found."
    echo "Copy the example and fill in your values:"
    echo "  cp $BACKEND_DIR/.env.example $BACKEND_DIR/.env"
    echo "  nano $BACKEND_DIR/.env"
    exit 1
fi

# --- Pull latest code (if this is a git repo with a remote) ---
if [ -d "$REPO_DIR/.git" ] && git -C "$REPO_DIR" remote get-url origin &> /dev/null; then
    echo "[1/5] Pulling latest code..."
    git -C "$REPO_DIR" pull || echo "Warning: git pull failed (offline or no remote). Continuing with local code."
else
    echo "[1/5] Skipping git pull (no remote configured)."
fi

# --- Python virtual environment + dependencies ---
echo "[2/5] Installing Python dependencies..."
if [ ! -d "$VENV_DIR" ]; then
    echo "  Creating virtual environment..."
    $PYTHON -m venv "$VENV_DIR"
fi
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r "$BACKEND_DIR/requirements.txt"

# --- Run alembic migrations ---
echo "[3/5] Running database migrations..."
cd "$BACKEND_DIR"
"$VENV_DIR/bin/alembic" upgrade head
cd "$REPO_DIR"

# --- Seed reference data ---
echo "[4/5] Seeding reference data..."
"$VENV_DIR/bin/python" "$REPO_DIR/scripts/seed.py"

# --- Build frontend ---
echo "[5/5] Building frontend..."
if [ -f "$FRONTEND_DIR/package.json" ]; then
    cd "$FRONTEND_DIR"
    npm install --silent
    STATIC_EXPORT=true npm run build
    cd "$REPO_DIR"
    echo "  Frontend built → $FRONTEND_DIR/out/"
else
    echo "  No frontend/package.json found — skipping frontend build."
fi

# --- Restart systemd service (if it exists) ---
if systemctl list-unit-files "$SERVICE_NAME.service" &> /dev/null 2>&1; then
    echo ""
    echo "Restarting $SERVICE_NAME service..."
    systemctl restart "$SERVICE_NAME"
    sleep 2
    systemctl status "$SERVICE_NAME" --no-pager || true
else
    echo ""
    echo "No systemd service '$SERVICE_NAME' found — skipping restart."
    echo "Start the backend manually with:"
    echo "  $VENV_DIR/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000"
fi

echo ""
echo "=== Deploy complete ==="
