# BC Local Government Council Tracker

BC Local Government Council Tracker is a full-stack civic technology project for monitoring British Columbia municipal council activity related to housing, zoning, transit-oriented development, bylaws, and related policy topics. It combines public meeting-source discovery, structured subscription preferences, optional AI-assisted matching and summaries, and email alerts/digests.

The project is designed as a portfolio-ready prototype for local government, planning, public policy, civic data, and workflow automation use cases. It demonstrates how public civic information can be collected, normalized, searched, and delivered to users who need to track policy changes across many municipalities.

> **Important disclaimer:** This is an experimental personal tool using public data. AI-generated summaries may contain errors and should be verified against original municipal sources. This repository is not official government communication.

## Purpose / Problem Statement

Local government agendas, minutes, videos, and bylaw updates are often spread across many municipal websites and meeting platforms. For planners, policy analysts, advocates, researchers, and civic technology teams, manually checking each source is time-consuming and easy to miss.

This project explores a structured tracking workflow:

1. Maintain a registry of municipalities and public meeting sources.
2. Poll agenda, minutes, bylaw, notice, and video sources.
3. Store discovered documents and meeting metadata.
4. Match new documents against user-selected municipalities, topics, and keywords.
5. Send email alerts or weekly digests for relevant updates.

## Key Features

- Subscription form for selecting municipalities, policy topics, custom keywords, and immediate-alert preferences.
- Backend API for subscription creation, email confirmation, magic-link preference updates, and unsubscribe links.
- Seeded registry for 166 British Columbia municipalities with 229 public source entries.
- Scraper modules for CivicWeb, Granicus, eScribe, YouTube RSS, and custom municipal website sources.
- Topic and keyword matching for housing, zoning, transit-oriented development, OCP updates, housing legislation, development permits, and related planning terms.
- Optional Gemini integration for AI-assisted matching and summaries.
- Optional Perplexity integration for claim verification notes.
- PostgreSQL data model for municipalities, sources, meetings, documents, subscriptions, tracks, track matches, scrape runs, API cost logs, and magic-link tokens.
- Search endpoint for keyword search across discovered documents and match summaries.
- Cron endpoints for polling sources, processing new documents, and sending weekly digests.
- Backend tests covering models, subscriptions, scraping components, digest processing, security behavior, and AI pipeline behavior.
- Deployment assets for a VPS-style setup with Nginx, systemd, cron, PostgreSQL, and static frontend export.

## Technical Highlights

- **Full-stack architecture:** Next.js frontend paired with a FastAPI backend.
- **Civic data ingestion:** Modular scraper architecture for multiple public-sector meeting platforms and custom municipal websites.
- **Structured persistence:** SQLAlchemy models and Alembic migrations for relational civic-data records.
- **User preference workflow:** Double opt-in subscription flow, magic-link updates, and tokenized unsubscribe handling.
- **Background processing:** Cron-triggered polling, document processing, immediate alerts, and weekly digest workflows.
- **AI-assisted processing:** Optional Gemini-based matching/summarization with keyword fallback paths in the backend.
- **Operational awareness:** Environment-based configuration, CORS configuration, structured logging option, deployment scripts, and service files.
- **Testing discipline:** Pytest-based backend test coverage is present for several core workflows and scraper modules.

## Tech Stack

- **Frontend:** Next.js 15, React 19, TypeScript
- **Styling:** Tailwind CSS 4
- **Backend:** FastAPI, Pydantic, SQLAlchemy async, Uvicorn
- **Database:** PostgreSQL, Alembic migrations
- **Scraping / parsing:** httpx, BeautifulSoup, lxml, PyYAML
- **AI integrations:** Google Gemini API optional; Perplexity API optional
- **Email:** SMTP configuration, with Hostinger defaults in the example environment file
- **Testing:** pytest, pytest-asyncio
- **Deployment tooling:** Nginx config, systemd service file, cron file, shell deployment/update scripts, Vercel cron configuration

## Repository Structure

```text
.
|-- README.md
|-- backend/
|   |-- app/
|   |   |-- ai/              # Gemini, Perplexity, prompts, and document processing
|   |   |-- api/             # FastAPI routers for subscriptions, registry, cron, search, etc.
|   |   |-- db/              # SQLAlchemy database setup
|   |   |-- discovery/       # Source scrapers and polling orchestration
|   |   |-- models/          # SQLAlchemy models
|   |   `-- services/        # Email, alerts, digests, seeding, and cost tracking
|   |-- alembic/             # Database migrations
|   |-- tests/               # Backend test suite and scraper fixtures
|   |-- requirements.txt
|   |-- pyproject.toml
|   `-- .env.example
|-- frontend/
|   |-- src/app/             # Next.js app routes and subscription UI
|   |-- src/lib/             # Frontend API helpers
|   |-- package.json
|   `-- next.config.ts
|-- deploy/
|   |-- bc-hearing-watch.service
|   |-- crontab
|   |-- deploy.sh
|   |-- nginx.conf
|   `-- update.sh
|-- scripts/
|   |-- deploy.sh
|   `-- seed.py
`-- vercel.json             # Cron route schedule configuration
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 14+ or compatible PostgreSQL service
- SMTP credentials if you want to test real email delivery
- Optional Gemini and Perplexity API keys for AI-assisted features

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
- a non-empty `APP_BASE_URL`

The backend validates production-like configuration at startup. If `DEBUG=false` and `APP_BASE_URL` is empty, email-dependent features are intentionally disabled by raising a startup error.

### 3. Install backend dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"
```

### 4. Prepare the database

Create a PostgreSQL database and set `DATABASE_URL` and `DATABASE_URL_SYNC` in `backend/.env`.

Example local values:

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

### 5. Run the backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

By default, the API runs at:

```text
http://localhost:8000
```

### 6. Install and run the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

The Next.js development configuration rewrites `/api/*` requests to `http://localhost:8000` unless `NEXT_PUBLIC_API_URL` is set.

### 7. Build and test

Backend tests:

```bash
cd backend
source venv/bin/activate
python -m pytest
```

Frontend build:

```bash
cd frontend
npm run build
```

No dedicated frontend test runner was identified beyond the existing build and lint-related package scripts.

## Environment Variables

Variables identified from `backend/.env.example`, backend settings, and frontend API configuration:

| Variable | Required? | Description |
|---|---:|---|
| `DATABASE_URL` | Yes | Async PostgreSQL connection string used by the FastAPI application. |
| `DATABASE_URL_SYNC` | Yes | Sync PostgreSQL connection string used by Alembic and database utilities. |
| `GEMINI_API_KEY` | Optional | Enables Gemini-based matching and summarization when configured. |
| `GEMINI_MODEL` | Optional | Gemini model name. Defaults to `gemini-2.5-flash`. |
| `PERPLEXITY_API_KEY` | Optional | Enables optional claim verification notes when configured. |
| `SMTP_HOST` | Email features | SMTP host. Example default is `smtp.hostinger.com`. |
| `SMTP_PORT` | Email features | SMTP port. Example default is `465`. |
| `SMTP_USERNAME` | Email features | SMTP username for sending alerts, confirmations, and digests. |
| `SMTP_PASSWORD` | Email features | SMTP password for email delivery. |
| `SMTP_FROM_EMAIL` | Email features | Sender address/display name used in outgoing emails. |
| `APP_BASE_URL` | Production / email links | Public app URL used to build confirmation and unsubscribe links. |
| `ALLOWED_ORIGINS` | Yes | Comma-separated list of allowed frontend origins for CORS. |
| `CRON_SECRET` | Production cron/admin routes | Protects cron and admin endpoints with the `X-Cron-Secret` header. |
| `DEBUG` | Recommended | Enables development behavior such as table auto-creation and relaxed startup validation. Use `false` in production. |
| `LOG_FORMAT` | Optional | Supports text or JSON-style logging through backend settings. |
| `REQUEST_DELAY_SECONDS` | Optional | Scraper request delay setting. |
| `SCRAPE_TIMEOUT_SECONDS` | Optional | Scraper timeout setting. |
| `USER_AGENT` | Optional | User agent string used by scraping requests. |
| `NEXT_PUBLIC_API_URL` | Optional frontend setting | Overrides the frontend API base URL. Useful when the backend is hosted separately. |

## Usage

Once the app is running locally, a user can:

1. Enter an email address.
2. Select municipalities to monitor.
3. Choose policy topics such as transit-oriented development, OCP updates, zoning density, SSMUH, housing legislation, development permits, and development cost charges.
4. Add custom keywords such as bylaw numbers, bill names, or policy phrases.
5. Opt into immediate alerts.
6. Submit the form and confirm the subscription by email.

Administrators or scheduled jobs can use protected API endpoints to seed municipality data, poll sources, process new documents, send immediate alerts, and trigger weekly digests.

Selected API routes include:

- `GET /health`
- `GET /api/v1/municipalities`
- `POST /api/v1/seed`
- `POST /api/v1/subscribe`
- `GET /api/v1/unsubscribe?token=...`
- `GET /api/v1/auth/confirm?token=...`
- `GET /api/v1/search?q=...`
- `POST /api/v1/cron/poll`
- `POST /api/v1/cron/weekly-digest`
- `POST /api/v1/cron/poll-and-digest`

## Screenshots / Demo

Screenshots can be added here to show the dashboard, tracking workflow, subscription form, and key UI screens.

Suggested additions:

- Subscription form with municipality selection.
- Topic and keyword selection workflow.
- Confirmation or magic-link update state.
- Example digest or alert email with sensitive information removed.

## Deployment Notes

The repository includes deployment assets for a single-server VPS style deployment:

- `deploy/deploy.sh` for initial provisioning.
- `deploy/update.sh` for updates.
- `deploy/nginx.conf` for reverse proxy and static frontend serving.
- `deploy/bc-hearing-watch.service` for systemd backend process management.
- `deploy/crontab` for scheduled polling and digest jobs.
- `vercel.json` with cron route schedules.

No live deployment URL was verified from the repository alone. Treat deployment status as **to verify** unless a current public URL and environment configuration are provided.

## Project Status

This repository appears to be a **portfolio project / work-in-progress prototype** with substantial backend implementation, a working subscription-oriented frontend, database migrations, scraper modules, tests, and deployment scripts.

Evidence supporting this status:

- Core application code, models, migrations, APIs, scraper modules, and tests are present.
- Deployment assets exist, but a live production deployment was not verified.
- README screenshots and demo artifacts are not currently present.
- No license file was identified.
- Some operational details, such as current test pass status in a clean environment and live deployment status, should be verified before presenting the project as production-ready.

## Roadmap

Practical next steps to make the project stronger for technical reviewers:

- Add screenshots or a short demo GIF of the subscription flow.
- Add sample anonymized digest and alert email outputs.
- Add a concise architecture diagram showing frontend, backend, database, scrapers, cron jobs, and email delivery.
- Verify and document the current backend test status in a clean environment.
- Add CI/CD for linting, backend tests, and frontend builds.
- Add frontend tests for the subscription workflow.
- Add sample seed data or a lightweight local development fixture for faster reviewer evaluation.
- Clarify deployment options: local-only, VPS, Vercel cron, or another hosted environment.
- Add API documentation examples for the main endpoints.
- Add validation and observability notes for scraper failures and source health.
- Add a license file if the project is intended for public reuse.

## Skills Demonstrated

This project demonstrates skills relevant to software engineering, data, planning, policy, and civic technology roles:

- Full-stack web application development.
- FastAPI backend design and API routing.
- React/Next.js frontend implementation.
- Relational data modelling with SQLAlchemy and PostgreSQL.
- Database migration management with Alembic.
- Public data ingestion from heterogeneous civic information sources.
- Modular scraper design for CivicWeb, Granicus, eScribe, YouTube RSS, and custom HTML pages.
- Subscription, confirmation, magic-link, and unsubscribe workflows.
- Email alert and digest workflow design.
- Search and filtering over structured civic records.
- Optional AI integration for document matching and summarization.
- Policy-domain modelling for housing, zoning, transit, bylaws, and local government workflows.
- Test organization for backend services, models, scrapers, and pipelines.
- Deployment-oriented thinking with Nginx, systemd, cron, and environment-based configuration.
- Technical documentation for both recruiters and engineering reviewers.

## License

No license file was identified in the repository. Add a license before encouraging reuse or external contributions.
