# BC Local Government Council Tracker

A civic-technology tool that tracks British Columbia municipal council activity — agendas, minutes, bylaws, notices, and meeting videos — and notifies subscribers about housing, zoning, transit-oriented development, and related policy updates across many municipalities at once.

The application is publicly available at <https://lg-tracker.ca>.

> **Disclaimer:** This is an experimental, work-in-progress tool that consumes public data published by BC municipalities. AI-generated summaries may contain errors and should always be verified against the original municipal source. This repository is not official government communication.
>
> **Reuse:** This repository is published as-is for transparency. No public reuse is intended, no license is granted, and external contributions are not currently being invited.

## What it does

Local government agendas, minutes, videos, and bylaw updates are spread across many municipal websites and meeting platforms (CivicWeb, Granicus, eScribe, YouTube, custom CMSes). Manually checking each one is slow and easy to miss.

LG-Tracker runs the following workflow:

1. Maintains a registry of BC municipalities and their public meeting sources.
2. Polls agenda, minutes, bylaw, notice, and video sources on a schedule.
3. Stores discovered documents and meeting metadata in PostgreSQL.
4. Matches new documents against each subscriber's selected municipalities, topics, and keywords (with optional AI-assisted matching/summarization).
5. Sends immediate alerts and weekly digest emails for relevant updates.

Subscribers can:

- Pick municipalities to monitor.
- Choose topics such as transit-oriented development, OCP updates, zoning density, SSMUH, housing legislation, development permits, and development cost charges.
- Add custom keywords (bylaw numbers, bill names, specific phrases).
- Opt into immediate alerts in addition to the weekly digest.
- Confirm or update preferences via emailed magic links and unsubscribe at any time.

## Tech stack

- **Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS 4
- **Backend:** FastAPI, Pydantic, SQLAlchemy (async), Uvicorn
- **Database:** PostgreSQL with Alembic migrations
- **Scraping/parsing:** httpx, BeautifulSoup, lxml, PyYAML
- **AI (optional):** Google Gemini for matching and summarization; Perplexity for claim-verification notes
- **Email:** SMTP (defaults shown for Hostinger)
- **Tests:** pytest, pytest-asyncio
- **Deployment assets:** Nginx, systemd, cron, Vercel cron (`vercel.json`)

## Repository structure

```text
.
├── README.md
├── backend/
│   ├── app/
│   │   ├── ai/              # Gemini, Perplexity, prompts, document processing
│   │   ├── api/             # FastAPI routers (subscriptions, registry, cron, search, etc.)
│   │   ├── db/              # SQLAlchemy database setup
│   │   ├── discovery/       # Source scrapers and polling orchestration
│   │   ├── models/          # SQLAlchemy models
│   │   └── services/        # Email, alerts, digests, seeding, cost tracking
│   ├── alembic/             # Database migrations
│   ├── tests/               # Backend test suite and scraper fixtures
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── .env.example
├── frontend/
│   ├── src/app/             # Next.js app routes and subscription UI
│   ├── src/lib/             # Frontend API helpers
│   ├── package.json
│   └── next.config.ts
├── deploy/
│   ├── bc-hearing-watch.service
│   ├── crontab
│   ├── deploy.sh
│   ├── nginx.conf
│   └── update.sh
├── scripts/
│   ├── deploy.sh
│   └── seed.py
└── vercel.json              # Cron route schedule for Vercel
```

## Architecture overview

```text
            ┌──────────────────────┐
            │  Next.js frontend    │  (subscription form, magic-link
            │  (lg-tracker.ca)     │   confirmation, unsubscribe)
            └──────────┬───────────┘
                       │  HTTPS / /api/v1/*
                       ▼
            ┌──────────────────────┐
            │  FastAPI backend     │
            │  - subscriptions     │
            │  - registry / search │
            │  - cron / admin API  │  ← X-Cron-Secret header
            │  - AI processor      │
            └──────────┬───────────┘
                       │
        ┌──────────────┼──────────────────────────────┐
        ▼              ▼                              ▼
 ┌─────────────┐  ┌──────────────────────┐   ┌──────────────────┐
 │ PostgreSQL  │  │ Scrapers             │   │ SMTP (alerts,    │
 │ (registry,  │  │ - CivicWeb           │   │  confirmations,  │
 │  documents, │  │ - Granicus           │   │  weekly digests) │
 │  matches,   │  │ - eScribe            │   └──────────────────┘
 │  subs)      │  │ - YouTube RSS        │
 └─────────────┘  │ - Custom municipal   │   ┌──────────────────┐
                  │   websites           │   │ Optional AI:     │
                  └──────────────────────┘   │ Gemini, Perplexity│
                       ▲                     └──────────────────┘
                       │
                  ┌────┴────────────────┐
                  │ Scheduled jobs:     │
                  │ - cron (VPS) /      │
                  │ - vercel.json crons │
                  │ Trigger /api/v1/cron│
                  └─────────────────────┘
```

A diagram image can be dropped at `docs/architecture.png` to replace the ASCII version above.

## Getting started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 14+ (local or hosted)
- SMTP credentials *only if* you want to test real email delivery
- Gemini and/or Perplexity API keys *only if* you want AI-assisted matching and summaries

### Minimum viable local setup (no email, no AI)

If you just want to see the app running against a local database, without email or AI integrations:

1. Create a Postgres database and user.
2. Configure `backend/.env` with `DEBUG=true` and the database URLs (see below). Leave `SMTP_*`, `GEMINI_API_KEY`, and `PERPLEXITY_API_KEY` blank.
3. Run migrations and seed:
   ```bash
   cd backend
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   pip install -e ".[dev]"
   alembic upgrade head
   cd ..
   python3 scripts/seed.py
   ```
4. Start the backend: `cd backend && uvicorn app.main:app --reload`
5. Start the frontend: `cd frontend && npm install && npm run dev`
6. Open <http://localhost:3000>.

In this mode:

- Subscribing will create a row in the database but **no confirmation email will actually be sent** (SMTP is unconfigured).
- AI matching/summarization falls back to keyword-based matching.
- Cron/admin endpoints are accessible without `X-Cron-Secret` because `DEBUG=true`.

### Full local setup (email + AI)

The minimum-viable steps above plus:

1. Set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, and `SMTP_FROM_EMAIL` in `backend/.env` to enable confirmation, alert, and digest email delivery.
2. Set `APP_BASE_URL` to the URL the frontend is served from (e.g. `http://localhost:3000`) so confirmation/unsubscribe links work.
3. Set `GEMINI_API_KEY` (and optionally `PERPLEXITY_API_KEY`) to enable AI-assisted matching and summaries.

### 1. Clone the repository

```bash
git clone https://github.com/toogoodforaname11/LG-Tracking.git
cd LG-Tracking
```

### 2. Configure the backend environment

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` for your local database and runtime settings.

For local development, set either:

- `DEBUG=true`, or
- a non-empty `APP_BASE_URL`.

The backend validates production-like configuration at startup. If `DEBUG=false` and `APP_BASE_URL` is empty, the server will refuse to start (email-dependent features would otherwise silently fail). Similarly, if `DEBUG=false` and `CRON_SECRET` is empty, all cron/admin endpoints return 503.

### 3. Install backend dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"
```

### 4. Prepare the database

Create a PostgreSQL database and set `DATABASE_URL` and `DATABASE_URL_SYNC` in `backend/.env`:

```env
DATABASE_URL=postgresql+asyncpg://lg_user:CHANGE_ME@localhost:5432/lg_tracking
DATABASE_URL_SYNC=postgresql://lg_user:CHANGE_ME@localhost:5432/lg_tracking
```

Then run migrations:

```bash
cd backend
alembic upgrade head
```

Seed the municipality registry from the repository root:

```bash
cd ..
python3 scripts/seed.py
```

The seed step is idempotent: existing municipalities are skipped, new sources are added.

### 5. Run the backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

By default, the API runs at `http://localhost:8000`.

### 6. Install and run the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:3000>.

The Next.js development configuration rewrites `/api/*` requests to `http://localhost:8000` unless `NEXT_PUBLIC_API_URL` is set.

### 7. Test and build

Backend tests:

```bash
cd backend
source venv/bin/activate
python -m pytest
```

Backend tests cover models, the subscription lifecycle, scraper modules (CivicWeb, Granicus, custom municipal scrapers, BC municipal scraper, batch-2 scrapers, YouTube), the digest pipeline, the poll pipeline, the AI pipeline (with Gemini doubles), security/auth behavior, and seed logic. There is no CI configured in this repository, so test status should be re-verified locally before drawing conclusions about coverage or pass rate.

Frontend build:

```bash
cd frontend
npm run build
```

There is no dedicated frontend test runner configured beyond `next build` and `next lint`.

## Environment variables

Variables are read from `backend/.env` (and the OS environment). The table notes when each is required.

| Variable | When required | Description |
|---|---|---|
| `DATABASE_URL` | Always | Async PostgreSQL connection string used by the FastAPI application. |
| `DATABASE_URL_SYNC` | Always | Sync PostgreSQL connection string used by Alembic and the seed script. |
| `APP_BASE_URL` | Production (and any flow that emails links) | Public URL used to build confirmation and unsubscribe links. Required if `DEBUG=false`. |
| `ALLOWED_ORIGINS` | Always | Comma-separated CORS allow-list. Must include the frontend origin(s) exactly. |
| `CRON_SECRET` | Production | Required if `DEBUG=false`. Protects cron/admin endpoints via `X-Cron-Secret`. If unset in production, those endpoints return 503. |
| `DEBUG` | Recommended local only | `true` enables auto table creation, relaxed startup checks, and unauthenticated access to cron/admin endpoints. Use `false` in production. |
| `SMTP_HOST` / `SMTP_PORT` | If sending email | Defaults to `smtp.hostinger.com:465`. |
| `SMTP_USERNAME` / `SMTP_PASSWORD` | If sending email | SMTP credentials. Without these, email sending fails at runtime. |
| `SMTP_FROM_EMAIL` | If sending email | Display name and sender address. |
| `GEMINI_API_KEY` | Optional | Enables Gemini-based matching and summarization. Without it, the AI pipeline falls back to keyword-only matching. |
| `GEMINI_MODEL` | Optional | Gemini model name (default `gemini-2.5-flash`). |
| `PERPLEXITY_API_KEY` | Optional | Enables Perplexity-based claim verification notes. |
| `LOG_FORMAT` | Optional | `text` (default) or `json` for structured logs. |
| `REQUEST_DELAY_SECONDS` | Optional | Delay between scraper requests. Default `2.0`. |
| `SCRAPE_TIMEOUT_SECONDS` | Optional | Per-request scraper timeout. Default `30`. |
| `USER_AGENT` | Optional | User agent string for outbound scrape requests. |
| `NEXT_PUBLIC_API_URL` | Optional (frontend) | Overrides the frontend's API base URL. Useful when the backend is hosted separately from the frontend. |

## API endpoints

Selected routes (full set is visible in `backend/app/api/`):

Public:

- `GET /health`
- `GET /api/v1/municipalities`
- `GET /api/v1/municipalities/{id}`
- `GET /api/v1/sources`
- `GET /api/v1/topics`
- `GET /api/v1/search?q=...`
- `POST /api/v1/subscribe`
- `GET /api/v1/auth/confirm?token=...`
- `GET /api/v1/unsubscribe?token=...`

Protected (require `X-Cron-Secret` when `CRON_SECRET` is configured):

- `POST /api/v1/seed`
- `POST /api/v1/sources` and `PATCH /api/v1/sources/{id}/status`
- `POST /api/v1/cron/poll`
- `POST /api/v1/cron/weekly-digest`
- `POST /api/v1/cron/poll-and-digest`
- `GET /api/v1/cron/trigger-alerts`
- `POST /api/v1/ai/process`
- `POST /api/v1/alerts/notify`
- `GET /api/v1/alerts/digest/{track_id}` and `/html`

### Calling protected endpoints

Set `CRON_SECRET` to a long random value in `backend/.env` (e.g. `python -c "import secrets; print(secrets.token_urlsafe(32))"`) and pass it back as a header:

```bash
curl -X POST https://lg-tracker.ca/api/v1/cron/poll \
  -H "X-Cron-Secret: $CRON_SECRET"

curl -X POST https://lg-tracker.ca/api/v1/cron/weekly-digest \
  -H "X-Cron-Secret: $CRON_SECRET"
```

In `DEBUG=true` mode the header is not required, which is convenient for local testing but must not be relied on in production.

## Screenshots and example email

Suggested artifacts to add to a `docs/` folder so this README can render them:

- `docs/subscription-form.png` — subscription form with municipality selection.
- `docs/topics-keywords.png` — topic and keyword selection.
- `docs/confirm-state.png` — confirmation / magic-link update screen.
- `docs/sample-digest.png` or `docs/sample-digest.eml` — anonymized example weekly digest.
- `docs/architecture.png` — architecture diagram (frontend, backend, DB, scrapers, cron jobs, email, optional AI).

These placeholders are intentionally not committed; add real artifacts when they are available.

## Deployment

The application is currently deployed at <https://lg-tracker.ca>. The repository supports several deployment shapes:

1. **Local development** — backend on `localhost:8000`, frontend on `localhost:3000`, optional Postgres, no email or AI required.
2. **Single VPS (Nginx + systemd + cron + Postgres)** — provisioning scripts in `deploy/`:
   - `deploy/deploy.sh` — initial Ubuntu 22.04 provisioning (installs Postgres, Node, Python, builds the frontend as a static export, writes `.env`, installs the systemd unit, configures Nginx + Let's Encrypt, installs cron jobs).
   - `deploy/update.sh` — pull latest, reinstall deps, rebuild frontend, restart service.
   - `deploy/nginx.conf` — reverse proxy + static frontend serving.
   - `deploy/bc-hearing-watch.service` — systemd unit for the FastAPI process.
   - `deploy/crontab` — cron entries calling the protected `/api/v1/cron/poll` and `/api/v1/cron/weekly-digest` endpoints with `X-Cron-Secret`.
3. **Static frontend export** — `STATIC_EXPORT=true npm run build` produces `frontend/out/` for serving as static files (used by the VPS Nginx configuration).
4. **Vercel-style scheduled cron** — `vercel.json` declares `/api/v1/cron/poll` every 30 minutes and `/api/v1/cron/weekly-digest` weekly. Either deployment shape (VPS cron or Vercel cron) can drive the scheduler — only one should be active at a time.

The `deploy/` scripts assume Hostinger-style VPS conventions (e.g. `smtp.hostinger.com`, `lg-tracker.ca`); adjust them for other hosts.

## Troubleshooting

- **Backend refuses to start with "APP\_BASE\_URL is not set"** — set `APP_BASE_URL` in `backend/.env`, or set `DEBUG=true` for local development.
- **Cron endpoints return 503 ("CRON\_SECRET is not set")** — set `CRON_SECRET` in `backend/.env`, or set `DEBUG=true` for local development.
- **Cron endpoints return 401** — the `X-Cron-Secret` header is missing or does not match the configured `CRON_SECRET`.
- **Frontend "Load failed" when submitting the form** — the frontend cannot reach the backend. In dev, check that `uvicorn` is running on `localhost:8000`. In production, check `NEXT_PUBLIC_API_URL` and that `ALLOWED_ORIGINS` includes the frontend origin.
- **Subscription succeeds but no confirmation email arrives** — `SMTP_USERNAME` / `SMTP_PASSWORD` are missing, or the SMTP server rejected the connection. Check backend logs for the SMTP error.
- **`alembic upgrade head` fails to connect** — confirm `DATABASE_URL_SYNC` is correct and the Postgres user has access to the database.
- **`python3 scripts/seed.py` reports import errors** — run it from the repository root (it adjusts `sys.path` and `cwd` to find `backend/.env`).

## Project status

This repository is a **work-in-progress prototype** that is publicly deployed at <https://lg-tracker.ca>. It is operated by a single maintainer for civic-tracking purposes.

What is in the repository:

- Backend application code, models, Alembic migrations, scraper modules, cron endpoints, subscription/auth flows, and a pytest suite.
- A subscription-oriented frontend.
- A seed script and seeded registry of BC municipalities and known public meeting sources.
- Deployment assets for a single-VPS Nginx + systemd + cron setup, plus a Vercel cron configuration.

What is intentionally **not** claimed:

- No SLA, uptime guarantee, or production-grade reliability.
- No verified test coverage percentage; tests should be re-run locally to confirm pass status.
- No CI is configured in this repository.
- No license file is provided; external reuse and contributions are not invited.

## Future development

Neutral list of improvements that would strengthen the project; not commitments:

- Add screenshots and an anonymized example digest to a `docs/` folder.
- Replace the ASCII architecture diagram with a rendered image.
- Add CI for backend tests, frontend builds, and linting.
- Add frontend tests for the subscription form and confirmation flow.
- Add tests for environment/configuration validation.
- Document scraper failure handling and source health more thoroughly.
- Add observability notes for polling, email delivery, and AI-processing failures.
- If the README grows further, move long deployment details into `docs/deployment.md`.

## License

No license is granted. The repository is published as-is for transparency around the public service running at <https://lg-tracker.ca>. Public reuse, redistribution, or external contributions are not invited at this time.
