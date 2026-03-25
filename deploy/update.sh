#!/bin/bash
# update.sh — pull latest code and restart the backend service
# Run from anywhere on the server: bash /var/www/lg-tracking/deploy/update.sh

set -euo pipefail

APP_DIR="/var/www/lg-tracking"

echo "=== Updating BC Local Government Council Tracker ==="

# Pull latest code
sudo -u www-data git -C "$APP_DIR" pull

# Install any new/updated dependencies
sudo -u www-data "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt"

# Restart service
systemctl restart bc-hearing-watch
sleep 2
systemctl status bc-hearing-watch --no-pager

echo ""
echo "Update complete. Testing health endpoint..."
curl -s http://127.0.0.1:8000/health | python3 -m json.tool
