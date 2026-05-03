#!/bin/bash
# update.sh — pull latest code, rebuild frontend, and restart the backend service
# Run from anywhere on the server: bash /var/www/lg-tracking/deploy/update.sh

set -euo pipefail

APP_DIR="/var/www/lg-tracking"

echo "=== Updating BC Local Government Council Tracker ==="

# Pull latest code
sudo -u www-data git -C "$APP_DIR" pull

# Install any new/updated Python dependencies
sudo -u www-data "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt"

# Apply any new database migrations BEFORE restarting the service so the
# running process never sees a stale schema. Idempotent — does nothing if
# the database is already at head.
echo "Applying database migrations..."
sudo -u www-data bash -c "cd '$APP_DIR/backend' && '$APP_DIR/venv/bin/alembic' upgrade head"

# Rebuild frontend (static export)
echo "Rebuilding frontend..."
cd "$APP_DIR/frontend"
sudo -u www-data npm install
sudo -u www-data STATIC_EXPORT=true npm run build
cd -
echo "Frontend rebuilt → $APP_DIR/frontend/out/"

# Restart backend service
systemctl restart bc-hearing-watch
sleep 2
systemctl status bc-hearing-watch --no-pager

echo ""
echo "Update complete. Testing health endpoint..."
curl -s http://127.0.0.1:8000/health | python3 -m json.tool
