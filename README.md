# BC Hearing Watch

Track BC local government council hearing updates — agendas, videos, and minutes — with AI-powered matching and summaries.

**Personal experimental prototype. Public data only. FIPPA-safe by design.**

## Architecture

- **Backend**: FastAPI + SQLAlchemy (async) + Neon Postgres
- **Frontend**: Next.js 15 + Tailwind CSS
- **AI**: Gemini 1.5 Flash (matching + summaries) + Embedding-2 (vectors)
- **Verification**: Perplexity Search API
- **Vector DB**: Pinecone (free tier)
- **Deploy**: Vercel (free tier)

## Quick Start

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -e .
cp .env.example .env  # Edit with your credentials
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Seed Registry

```bash
curl -X POST http://localhost:8000/api/v1/seed
```

## Coverage

Starting with Capital Regional District (CRD) — 13 municipalities + CRD board:
- 8 with CivicWeb portals (Colwood, Victoria, Central Saanich, North Saanich, Oak Bay, Metchosin, Sooke + more)
- 6 with custom websites (Saanich, Sidney, Esquimalt, View Royal, Langford, Highlands)

## Disclaimer

AI-generated summaries may contain errors. Always verify with original government sources. Not official government communication.
