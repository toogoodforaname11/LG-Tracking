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
- **Backend**: FastAPI + SQLAlchemy (async) + Neon Postgres
- **Email**: Resend SDK for transactional emails (alerts + digests)
- **AI**: Gemini 1.5 Flash (matching + summaries) with keyword fallback
- **Verification**: Perplexity Search API (optional fact-checking)
- **Discovery**: CivicWeb, Granicus, eScribe, YouTube RSS, and custom HTML scrapers
- **Polling**: Every 30 minutes via cron
- **Deploy**: Hostinger VPS (Ubuntu 22.04) or Vercel

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

## Quick Start

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -e ".[ai]"
cp .env.example .env  # Edit with your credentials
uvicorn app.main:app --reload
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
curl -X POST http://localhost:8000/api/v1/seed
```

### Test Immediate Alerts

```bash
# 1. Poll sources for new documents
curl -X POST http://localhost:8000/api/v1/cron/poll

# 2. Trigger a test alert email
curl "http://localhost:8000/api/v1/cron/trigger-alerts?email=you@example.com"
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | Neon Postgres async connection string (`postgresql+asyncpg://...`) |
| `APP_BASE_URL` | **Yes** | Your public domain (e.g. `https://yourdomain.com`). **All email features are disabled if this is empty.** |
| `CRON_SECRET` | **Yes** (prod) | Random string protecting cron/admin endpoints. Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `RESEND_API_KEY` | Yes | Resend API key for sending emails |
| `RESEND_FROM_EMAIL` | No | Sender address (default: `BC Hearing Watch <noreply@bchearingwatch.ca>`) |
| `GEMINI_API_KEY` | No | Google Gemini for AI matching/summaries (falls back to keyword matching) |
| `PERPLEXITY_API_KEY` | No | Perplexity for fact verification |
| `ALLOWED_ORIGINS` | No | Comma-separated CORS origins (default: `http://localhost:3000`) |
| `REQUEST_DELAY_SECONDS` | No | Delay between source polls (default: `2.0`) |

### Resend Setup

1. Create an account at [resend.com](https://resend.com)
2. Add and verify your sending domain
3. Generate an API key
4. Set `RESEND_API_KEY` in `.env`

## Email Schedule

| Type | Frequency | Trigger |
|---|---|---|
| **Immediate Alert** | Within minutes of detection | Opt-in checkbox; sources polled every 30 min |
| **Weekly Digest** | Sundays at 8 PM Pacific | Always sent to all active subscribers |
| **Confirmation** | On subscribe/update | Sent via Resend after form submission |

### Adding a New Municipality

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

### Cron Jobs (Vercel Cron or manual)
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

## Hostinger VPS Deployment

Deploy the full stack (frontend + backend) on a single Hostinger VPS running Ubuntu 22.04.

### Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |
| **RAM** | 2 GB | 4 GB |
| **CPU** | 1 vCPU | 2 vCPU |
| **Storage** | 20 GB SSD | 40 GB SSD |
| **Hostinger Plan** | KVM 2 | KVM 4 |

### Prerequisites

- A **domain name** with an A record pointing to your VPS IP
- SSH root access to your VPS
- API keys ready (see [Environment Variables](#environment-variables))

### One-Command Deploy

```bash
# 1. SSH into your VPS
ssh root@your-vps-ip

# 2. Download and edit the deploy script
curl -O https://raw.githubusercontent.com/toogoodforaname11/lg-tracking/main/deploy/deploy.sh

# 3. Set your domain at the top of deploy.sh
nano deploy.sh   # change DOMAIN="" to DOMAIN="yourdomain.com"

# 4. Run it
bash deploy.sh
```

This installs everything: Python 3.11, Node.js 20, Nginx, Certbot (SSL), clones the repo, builds the frontend as static files, and sets up the systemd service.

### Post-Deploy Setup

```bash
# 1. Configure your secrets
cp /var/www/lg-tracking/backend/.env.example /var/www/lg-tracking/backend/.env
nano /var/www/lg-tracking/backend/.env

# 2. Set up cron jobs (replace <YOUR_CRON_SECRET> first)
nano /var/www/lg-tracking/deploy/crontab
crontab -u www-data /var/www/lg-tracking/deploy/crontab

# 3. Start the backend
systemctl start bc-hearing-watch

# 4. Seed the municipality database
curl -X POST http://127.0.0.1:8000/api/v1/seed

# 5. Verify everything works
curl http://127.0.0.1:8000/health
# Then visit https://yourdomain.com in your browser
```

### Updating

```bash
bash /var/www/lg-tracking/deploy/update.sh
```

This pulls the latest code, rebuilds the frontend, reinstalls dependencies, and restarts the backend.

### What Gets Deployed

| Component | How it runs |
|-----------|-------------|
| **Frontend** | Static HTML/CSS/JS served by Nginx from `/var/www/lg-tracking/frontend/out/` |
| **Backend** | Uvicorn (FastAPI) on port 8000, managed by systemd |
| **Nginx** | Reverse proxy on ports 80/443 — serves frontend, proxies `/api/*` to backend |
| **SSL** | Free Let's Encrypt certificate via Certbot (auto-renews) |
| **Cron** | Linux crontab polls sources every 30 min, sends weekly digest on Sundays |
| **Database** | Neon serverless Postgres (external, configured via `DATABASE_URL`) |

### Useful Commands

```bash
# Service management
systemctl status bc-hearing-watch      # Check backend status
systemctl restart bc-hearing-watch     # Restart backend
journalctl -u bc-hearing-watch -f      # Stream backend logs

# Nginx
nginx -t                               # Test config
systemctl reload nginx                 # Reload after config changes

# Cron logs
tail -f /var/log/lg-tracking-poll.log
tail -f /var/log/lg-tracking-digest.log

# SSL renewal (auto, but you can test)
certbot renew --dry-run
```

## Disclaimer

This is an experimental personal tool using public data. AI summaries may contain errors. Always verify with original municipal sources. Not official government communication. This tool tracks publicly available council meeting agendas, minutes, and videos from BC municipalities.
