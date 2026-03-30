# BC Hearing Watch — Housing & Bylaw Tracking

Subscribe to **immediate alerts** and **weekly AI-summarized digests** of BC municipal council meetings — focused on **housing policy, transit-oriented development, zoning, and specific bylaws**.

**This is an experimental personal tool using public data. AI summaries may contain errors. Always verify with original municipal sources. Not official government communication.**

## Coverage

**166 BC municipalities** tracked across 5 scraper platforms:

| Platform | Municipalities | Discovery Method |
|----------|---------------|-----------------|
| CivicWeb | ~60 | Multi-strategy HTML scraping (schedule, type list, detail pages) |
| Custom | ~103 | Per-municipality HTML scrapers via `BCMunicipalScraper` base class |
| Granicus | ~11 | Multi-path HTML scraping |
| YouTube | ~10 | RSS feed + timestamp extraction (no API key needed) |
| eScribe | ~3 | Multi-path HTML scraping |

### CRD Municipalities (14)

| Municipality | Platform | Status |
|---|---|---|
| Colwood | CivicWeb + YouTube | Active |
| Victoria | CivicWeb + eScribe | Active |
| Central Saanich | CivicWeb + Granicus | Active |
| North Saanich | CivicWeb | Active |
| Oak Bay | CivicWeb | Active |
| Metchosin | CivicWeb | Active |
| Sooke | CivicWeb | Active |
| Saanich | Custom + Granicus | Active |
| Sidney | Custom + CivicWeb | Active |
| Esquimalt | Custom + CivicWeb | Active |
| View Royal | Custom + CivicWeb | Active |
| Langford | Custom + CivicWeb | Active |
| Highlands | Custom + CivicWeb | Active |
| CRD Board | Custom | Active |

### BC-Wide Coverage

An additional 150+ municipalities across Metro Vancouver, Fraser Valley, Vancouver Island, Interior, Kootenays, and Northern BC. The full list is available via the `GET /api/v1/municipalities` endpoint or in the frontend subscription form.

## Topics Tracked

- **Transit Oriented Development (TOD)** — TOD designations, density near transit
- **Transit Oriented Areas (TOA) / Bill 47** — increased density near rapid transit stations
- **Small-Scale Multi-Unit Housing (SSMUH)** — duplex, triplex, fourplex, missing middle
- **Housing Statutes Amendment Bills** — Bill 44, Bill 46, Bill 47, Bill 16, Bill 25
- **Official Community Plan (OCP)** — housing-related OCP amendments and updates
- **Zoning / Rezoning for Housing Density** — upzoning, density bonuses, zoning bylaw changes
- **Development Permits Affecting Housing** — residential DP applications and variances
- **Area Plans** — local area or neighbourhood plans
- **BRT / Bus Rapid Transit** — bus priority infrastructure
- **Multimodal Transport & Active Transportation**
- **Provincial Housing Targets / Housing Needs Reports**
- **Development Cost Charges / Affordability Incentives**
- **Transportation Plans / Studies**

### Specific Bylaw Tracking

You can track specific bylaws by name or number (e.g. "Bylaw 1700" or "Housing Statutes Amendment Act") in the keywords field. The system will alert you every time that exact bylaw is mentioned in any hearing, regardless of topic.

## How It Works

1. **Subscribe**: Visit the form at `/`, enter your email, pick municipalities, housing topics, and optionally enable immediate alerts
2. **Edit**: Submit the same form with the same email — a magic link is sent to confirm changes
3. **Immediate Alerts** (opt-in): Sources are polled every 30 minutes. When a new matching council item is detected, you get an email right away
4. **Weekly Digest** (always): Every Sunday at 8 PM Pacific, you receive a full summary of the week's matching council updates
5. **Unsubscribe**: One-click link in every email

## Architecture

- **Frontend**: Next.js 15 + Tailwind CSS — single subscription form page
- **Backend**: FastAPI + SQLAlchemy (async) + PostgreSQL
- **Email**: Hostinger SMTP (your existing email — no third-party service needed)
- **AI**: Gemini 2.5 Flash (matching + summaries) with keyword fallback
- **Verification**: Perplexity Search API (optional fact-checking)
- **Discovery**: CivicWeb, Granicus, eScribe, YouTube RSS, and custom HTML scrapers
- **Polling**: Every 30 minutes via cron
- **Deploy**: Hostinger VPS (Ubuntu 22.04) — everything runs on one server

### Scraper Architecture

All scrapers live in `backend/app/discovery/`:

| File | Purpose |
|------|---------|
| `base.py` | Abstract base class with HTTP client, retries, and `DiscoveredItem` dataclass |
| `civicweb.py` | CivicWeb/Diligent portal scraper (multi-strategy) |
| `granicus.py` | Granicus meeting management scraper |
| `escribe.py` | eScribe meeting portal scraper |
| `youtube.py` | YouTube RSS feed + timestamp extraction |
| `custom_bc_municipal.py` | Base class for custom municipal website scrapers |
| `custom_*.py` | Per-municipality scrapers extending `BCMunicipalScraper` |
| `poller.py` | Orchestrator — polls all active sources, stores results, triggers alerts |

## Quick Start (Local Development)

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your credentials

# Create database tables
alembic upgrade head

# Seed municipalities and sources
cd .. && python scripts/seed.py

# Start the backend
cd backend && uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` — you'll see the subscription form.

### Seed the Municipality Registry

```bash
# Standalone script (idempotent — safe to run multiple times)
python scripts/seed.py

# Or via the API (requires X-Cron-Secret header if CRON_SECRET is set)
curl -X POST http://localhost:8000/api/v1/seed
```

## Deployment

### Prerequisites

1. **PostgreSQL 14+** — create a database and user:

   ```bash
   sudo -u postgres psql
   CREATE USER lg_user WITH PASSWORD 'your-secure-password';
   CREATE DATABASE lg_tracking OWNER lg_user;
   \q
   ```

2. **Python 3.11+** and **Node.js 20+**

3. **Environment config** — copy and edit the example:

   ```bash
   cp backend/.env.example backend/.env
   nano backend/.env
   ```

   Required variables (all documented in `.env.example`):
   - `DATABASE_URL` / `DATABASE_URL_SYNC` — async and sync PostgreSQL URLs
   - `GEMINI_API_KEY` — for AI matching/summarization (optional)
   - `PERPLEXITY_API_KEY` — for fact verification (optional)
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM_EMAIL` — email delivery
   - `APP_BASE_URL` — e.g. `https://lg-tracker.ca`
   - `ALLOWED_ORIGINS` — CORS origins (comma-separated)
   - `CRON_SECRET` — protects cron/admin endpoints
   - `DEBUG` — `false` in production

### Deploy Script

The `scripts/deploy.sh` script handles a full fresh deployment **or** redeployment:

```bash
bash scripts/deploy.sh
```

It runs these steps in order:
1. `git pull` (if a remote is configured)
2. Create/update Python venv and install deps from `backend/requirements.txt`
3. `alembic upgrade head` — create or migrate all database tables
4. `python scripts/seed.py` — populate municipalities and sources (idempotent)
5. `npm install && npm run build` — build the Next.js frontend
6. `systemctl restart bc-hearing-watch` — restart the backend service

For initial VPS provisioning (installs PostgreSQL, Nginx, Certbot, Node.js, etc.), use `deploy/deploy.sh` instead.

### Nginx Reverse Proxy with SSL

An nginx config is provided in `deploy/nginx.conf`. To set it up:

```bash
# Copy and customize the server_name
sudo cp deploy/nginx.conf /etc/nginx/sites-available/lg-tracking
sudo sed -i 's/lg-tracker.ca/your-domain.com/g' /etc/nginx/sites-available/lg-tracking
sudo ln -sf /etc/nginx/sites-available/lg-tracking /etc/nginx/sites-enabled/lg-tracking
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# SSL via Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

The config serves the static frontend from `frontend/out/` and proxies `/api/*` to the FastAPI backend on port 8000.

### DNS Setup

Point an **A record** for your domain to your VPS IP address:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | `@` | `your.vps.ip.address` | 3600 |
| A | `www` | `your.vps.ip.address` | 3600 |

Allow 5–30 minutes for DNS propagation before running Certbot.

### Test Immediate Alerts

```bash
# 1. Poll sources for new documents
curl -X POST http://localhost:8000/api/v1/cron/poll

# 2. Trigger a test alert email
curl "http://localhost:8000/api/v1/cron/trigger-alerts?email=you@example.com"
```

## Hostinger VPS Deployment

Everything runs on a single Hostinger VPS — PostgreSQL, backend, frontend, email. The deploy script handles all the infrastructure automatically. You just need to add your email credentials and (optionally) AI API keys.

### What You Need Before Starting

1. A **Hostinger VPS** (KVM 2 minimum, KVM 4 recommended)
2. A **domain name** with an A record pointing to your VPS IP
3. A **Hostinger email address** (e.g. `noreply@lg-tracker.ca`) — create one in Hostinger's email panel
4. (Optional) A **Gemini API key** from [Google AI Studio](https://aistudio.google.com/apikey) — free tier works
5. (Optional) A **Perplexity API key** for fact verification

### VPS Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |
| **RAM** | 2 GB | 4 GB |
| **CPU** | 1 vCPU | 2 vCPU |
| **Storage** | 20 GB SSD | 40 GB SSD |

### Deploy (One Command)

```bash
# 1. SSH into your VPS
ssh root@your-vps-ip

# 2. Download the deploy script
curl -O https://raw.githubusercontent.com/toogoodforaname11/lg-tracking/main/deploy/deploy.sh

# 3. Run it (DOMAIN is pre-set to lg-tracker.ca)
bash deploy.sh
```

The script automatically:
- Installs Python 3.11, Node.js 20, Nginx, Certbot
- **Installs and configures PostgreSQL** with a local database and auto-generated credentials
- Clones the repo, builds the frontend, sets up systemd
- **Generates your `.env`** with database credentials and cron secret pre-filled
- Configures SSL via Let's Encrypt
- Installs cron jobs (poll every 30 min, weekly digest)
- Starts the backend

### After Deploy — Add Your Credentials

The only thing left is to add your email and (optionally) AI API keys:

```bash
nano /var/www/lg-tracking/backend/.env
```

Fill in these lines:

```env
# Your Hostinger email (required for sending alerts/digests)
SMTP_USERNAME=noreply@lg-tracker.ca
SMTP_PASSWORD=your-hostinger-email-password

# Optional — enables AI matching and summarization (free tier available)
GEMINI_API_KEY=your-gemini-api-key

# Optional — enables fact verification
PERPLEXITY_API_KEY=your-perplexity-api-key
```

Then restart and seed the database:

```bash
systemctl restart bc-hearing-watch
curl -X POST http://127.0.0.1:8000/api/v1/seed
curl http://127.0.0.1:8000/health
```

Visit `https://lg-tracker.ca` — you're live.

### What Gets Deployed

| Component | Details |
|-----------|---------|
| **PostgreSQL** | Local database on the VPS (auto-configured, no external service needed) |
| **Frontend** | Static HTML/CSS/JS served by Nginx from `/var/www/lg-tracking/frontend/out/` |
| **Backend** | Uvicorn (FastAPI) on port 8000, managed by systemd |
| **Nginx** | Reverse proxy on ports 80/443 — serves frontend, proxies `/api/*` to backend |
| **SSL** | Free Let's Encrypt certificate via Certbot (auto-renews) |
| **Email** | Sent via your Hostinger email over SMTP (port 465 SSL) |
| **Cron** | Linux crontab polls sources every 30 min, sends weekly digest on Sundays |

### Environment Variables

| Variable | Auto-configured? | Description |
|---|---|---|
| `DATABASE_URL` | Yes | Local PostgreSQL connection (set by deploy script) |
| `DATABASE_URL_SYNC` | Yes | Sync version of the above |
| `CRON_SECRET` | Yes | Random string protecting cron endpoints (auto-generated) |
| `APP_BASE_URL` | Yes | Your domain URL (set from DOMAIN in deploy script) |
| `ALLOWED_ORIGINS` | Yes | CORS origins (auto-set) |
| `SMTP_USERNAME` | **You fill in** | Your Hostinger email address |
| `SMTP_PASSWORD` | **You fill in** | Your Hostinger email password |
| `GEMINI_API_KEY` | **You fill in** (optional) | Google Gemini API key for AI features |
| `PERPLEXITY_API_KEY` | **You fill in** (optional) | Perplexity API key for fact verification |
| `SMTP_HOST` | Pre-set | `smtp.hostinger.com` (default) |
| `SMTP_PORT` | Pre-set | `465` (SSL, default) |
| `SMTP_FROM_EMAIL` | Pre-set | Sender display name |
| `GEMINI_MODEL` | Pre-set | `gemini-2.5-flash` (default) |

### Updating

```bash
bash /var/www/lg-tracking/deploy/update.sh
```

This pulls the latest code, rebuilds the frontend, reinstalls dependencies, and restarts the backend.

### Troubleshooting

**"Load failed" on the subscription form**

This means the frontend cannot reach the backend API. Check in order:

```bash
# 1. Is the backend running?
systemctl status bc-hearing-watch
journalctl -u bc-hearing-watch -n 50    # check for startup errors

# 2. Can the backend reach the database?
curl http://127.0.0.1:8000/health

# 3. Is CORS configured? (must include your domain)
grep ALLOWED_ORIGINS /var/www/lg-tracking/backend/.env
# Should contain: https://lg-tracker.ca

# 4. Is APP_BASE_URL set? (required for email features)
grep APP_BASE_URL /var/www/lg-tracking/backend/.env
# Should be: https://lg-tracker.ca

# 5. Run the database migration (required after updates)
cd /var/www/lg-tracking/backend
../venv/bin/alembic upgrade head
systemctl restart bc-hearing-watch

# 6. Seed the municipality database (required on first deploy)
curl -X POST http://127.0.0.1:8000/api/v1/seed
```

**Emails not sending**

```bash
# Check SMTP credentials are set
grep SMTP_ /var/www/lg-tracking/backend/.env

# Test by subscribing and checking logs
journalctl -u bc-hearing-watch -n 20 | grep -i "email\|smtp"
```

### Useful Commands

```bash
# Service management
systemctl status bc-hearing-watch      # Check backend status
systemctl restart bc-hearing-watch     # Restart backend
journalctl -u bc-hearing-watch -f      # Stream backend logs

# PostgreSQL
sudo -u postgres psql -d lg_tracking   # Connect to database
systemctl status postgresql            # Check Postgres status

# Nginx
nginx -t                               # Test config
systemctl reload nginx                 # Reload after config changes

# Cron logs
tail -f /var/log/lg-tracking-poll.log
tail -f /var/log/lg-tracking-digest.log

# SSL renewal (auto, but you can test)
certbot renew --dry-run
```

## Email Schedule

| Type | Frequency | Trigger |
|---|---|---|
| **Immediate Alert** | Within minutes of detection | Opt-in checkbox; sources polled every 30 min |
| **Weekly Digest** | Sundays at 8 PM Pacific | Always sent to all active subscribers |
| **Confirmation** | On subscribe/update | Sent after form submission |

## Adding a New Municipality

1. Add an entry to `backend/app/services/seed_registry.py` in the appropriate batch list
2. If the municipality uses a custom website (not CivicWeb/Granicus/eScribe), create a scraper file `backend/app/discovery/custom_<name>.py` extending `BCMunicipalScraper`
3. If custom: add the scraper to `CUSTOM_SCRAPER_MAP` in `backend/app/discovery/poller.py`
4. Add the `short_name` to the `MUNICIPALITIES` array in `frontend/src/app/page.tsx`
5. Re-run the seed endpoint: `curl -X POST http://localhost:8000/api/v1/seed`

## API Endpoints

### Subscription
- `POST /api/v1/subscribe` — Create/update subscription (email = primary key)
- `GET /api/v1/unsubscribe?token=...` — One-click unsubscribe (token-based)
- `GET /api/v1/auth/confirm?token=...` — Confirm preference changes via magic link

### Cron Jobs (auto-installed by deploy script)
- `POST /api/v1/cron/poll` — Poll sources + send immediate alerts (every 30 min)
- `POST /api/v1/cron/weekly-digest` — Send weekly digest (Sundays 8 PM Pacific)
- `POST /api/v1/cron/poll-and-digest` — Full pipeline (poll + digest)
- `GET /api/v1/cron/trigger-alerts?email=...` — Manual test for alert emails

### Registry & Discovery
- `POST /api/v1/seed` — Seed municipality registry (requires `X-Cron-Secret`)
- `GET /api/v1/municipalities` — List municipalities (optional `?region=CRD`)
- `POST /api/v1/discovery/poll` — Manual discovery poll

### AI Processing
- `POST /api/v1/ai/process` — Trigger document matching and summarization

## Disclaimer

This is an experimental personal tool using public data. AI summaries may contain errors. Always verify with original municipal sources. Not official government communication. This tool tracks publicly available council meeting agendas, minutes, and videos from BC municipalities.
