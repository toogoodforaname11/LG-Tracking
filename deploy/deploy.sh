#!/bin/bash
# deploy.sh — initial Hostinger VPS setup for BC Local Government Council Tracker
# Run once as root on a fresh Ubuntu 22.04 VPS:
#   bash deploy/deploy.sh
#
# Prerequisites:
#   - Ubuntu 22.04 VPS with SSH access
#   - A domain pointed at the server's IP (for SSL)
#   - Your GitHub repo accessible (public or SSH key configured)

set -euo pipefail

REPO_URL="https://github.com/toogoodforaname11/lg-tracking.git"
APP_DIR="/var/www/lg-tracking"
PYTHON="python3.11"
DOMAIN=""   # Set this before running, e.g. "bchearingwatch.ca"

echo "=== BC Local Government Council Tracker — Hostinger VPS Deploy ==="

# --- System packages ---
apt-get update -q
apt-get install -y python3.11 python3.11-venv python3.11-dev \
    nginx certbot python3-certbot-nginx \
    git curl build-essential libpq-dev

# --- Node.js 20.x (for frontend build) ---
if ! command -v node &> /dev/null; then
    echo "Installing Node.js 20.x..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
fi
echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

# --- App directory ---
mkdir -p "$APP_DIR"
chown www-data:www-data "$APP_DIR"

# --- Clone / pull repo ---
if [ -d "$APP_DIR/.git" ]; then
    echo "Repo exists — pulling latest..."
    sudo -u www-data git -C "$APP_DIR" pull
else
    echo "Cloning repo..."
    sudo -u www-data git clone "$REPO_URL" "$APP_DIR"
fi

# --- Python virtual environment ---
if [ ! -d "$APP_DIR/venv" ]; then
    echo "Creating virtual environment..."
    sudo -u www-data $PYTHON -m venv "$APP_DIR/venv"
fi

echo "Installing Python dependencies..."
sudo -u www-data "$APP_DIR/venv/bin/pip" install --upgrade pip
sudo -u www-data "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt"

# --- Frontend build (static export) ---
echo "Building frontend..."
cd "$APP_DIR/frontend"
sudo -u www-data npm install
sudo -u www-data STATIC_EXPORT=true npm run build
cd -
echo "Frontend built → $APP_DIR/frontend/out/"

# --- Environment file ---
if [ ! -f "$APP_DIR/backend/.env" ]; then
    echo ""
    echo "IMPORTANT: Create $APP_DIR/backend/.env before starting the service."
    echo "  cp $APP_DIR/backend/.env.example $APP_DIR/backend/.env"
    echo "  nano $APP_DIR/backend/.env"
    echo ""
fi

# --- systemd service ---
cp "$APP_DIR/deploy/bc-hearing-watch.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable bc-hearing-watch

# --- nginx ---
if [ -n "$DOMAIN" ]; then
    sed "s/yourdomain.com/$DOMAIN/g" "$APP_DIR/deploy/nginx.conf" \
        > /etc/nginx/sites-available/lg-tracking
    ln -sf /etc/nginx/sites-available/lg-tracking /etc/nginx/sites-enabled/lg-tracking
    rm -f /etc/nginx/sites-enabled/default
    nginx -t && systemctl reload nginx

    echo "Setting up SSL with Certbot for $DOMAIN..."
    certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "admin@$DOMAIN"
else
    echo "DOMAIN not set — skipping nginx and SSL config."
    echo "Edit DOMAIN= at the top of this script and re-run, or configure nginx manually."
fi

# --- Cron jobs ---
echo "Installing cron jobs..."
echo "NOTE: Edit deploy/crontab and replace <YOUR_CRON_SECRET> before installing."
# crontab -u www-data "$APP_DIR/deploy/crontab"   # uncomment after editing crontab

# --- Log files ---
touch /var/log/lg-tracking-poll.log /var/log/lg-tracking-digest.log
chown www-data:www-data /var/log/lg-tracking-poll.log /var/log/lg-tracking-digest.log

echo ""
echo "=== Deploy complete ==="
echo ""
echo "Next steps:"
echo "  1. Edit $APP_DIR/backend/.env with your secrets"
echo "  2. Edit deploy/crontab and replace <YOUR_CRON_SECRET>"
echo "  3. Install crontab: crontab -u www-data $APP_DIR/deploy/crontab"
echo "  4. Start the service: systemctl start bc-hearing-watch"
echo "  5. Check status:      systemctl status bc-hearing-watch"
echo "  6. View logs:         journalctl -u bc-hearing-watch -f"
echo "  7. Test health:       curl http://127.0.0.1:8000/health"
echo "  8. Visit your site:   https://$DOMAIN"
