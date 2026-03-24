# BC Hearing Watch — Email-Only Prototype

Subscribe to weekly AI-summarized digests of BC municipal council meetings. One form, one email per week.

**This is an experimental personal tool using public data. AI summaries may contain errors. Always verify with original municipal sources. Not official government communication.**

## How It Works

1. **Subscribe**: Visit the form at `/`, enter your email, pick municipalities and topics
2. **Edit**: Submit the same form with the same email — your preferences are overwritten instantly
3. **Weekly Digest**: Every Sunday at 8 PM Pacific, you receive an email with AI-summarized council updates
4. **Unsubscribe**: One-click link in every email

## Architecture

- **Frontend**: Next.js 15 + Tailwind CSS — single subscription form page
- **Backend**: FastAPI + SQLAlchemy (async) + Neon Postgres
- **Email**: Resend SDK for transactional emails
- **AI**: Gemini 1.5 Flash (matching + summaries)
- **Verification**: Perplexity Search API (fact-checking)
- **Discovery**: CivicWeb scraper + YouTube RSS (agendas, minutes, videos)
- **Deploy**: Vercel (free tier)

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

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | Neon Postgres async connection string |
| `RESEND_API_KEY` | Yes | Resend API key for sending emails |
| `RESEND_FROM_EMAIL` | No | Sender address (default: `BC Hearing Watch <noreply@bchearingwatch.ca>`) |
| `GEMINI_API_KEY` | No | Google Gemini for AI matching/summaries |
| `PERPLEXITY_API_KEY` | No | Perplexity for fact verification |
| `PINECONE_API_KEY` | No | Pinecone for vector search (future) |

### Resend Setup

1. Create an account at [resend.com](https://resend.com)
2. Add and verify your sending domain
3. Generate an API key
4. Set `RESEND_API_KEY` in `.env`

## Coverage

Starting with Capital Regional District (CRD) — 14 municipalities:

| Municipality | Platform | Status |
|---|---|---|
| Colwood | CivicWeb + YouTube | Active |
| Victoria | CivicWeb | Active |
| Central Saanich | CivicWeb | Active |
| North Saanich | CivicWeb | Active |
| Oak Bay | CivicWeb | Active |
| Metchosin | CivicWeb | Active |
| Sooke | CivicWeb | Active |
| Saanich | Custom | Pending |
| Sidney | Custom | Pending |
| Esquimalt | Custom | Pending |
| View Royal | Custom | Pending |
| Langford | Custom | Pending |
| Highlands | Custom | Pending |
| CRD Board | Custom | Pending |

### Adding a New Municipality

Add an entry to `backend/app/services/seed_registry.py` in the `CRD_MUNICIPALITIES` list and re-run the seed endpoint. Then add the short_name to the `MUNICIPALITIES` array in `frontend/src/app/page.tsx`.

## Weekly Digest Timing

- **When**: Every Sunday at 8 PM Pacific Time
- **What**: AI-summarized council meeting updates matching your topics and keywords
- **From**: Configurable via `RESEND_FROM_EMAIL`

## Disclaimer

This is an experimental personal tool using public data. AI summaries may contain errors. Always verify with original municipal sources. Not official government communication. This tool tracks publicly available council meeting agendas, minutes, and videos from BC municipalities.
