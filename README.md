# Zomato AI Restaurant Recommendation System

AI-powered restaurant discovery for Bangalore — filter by city, cuisine, rating, and budget, then get personalised picks ranked by **Groq LLM** across **51,717 restaurants**.

## Live Demo

| Service | URL |
|---------|-----|
| **Dashboard (Vercel)** | [**zomato-ai-recommender.vercel.app**](https://zomato-ai-recommender.vercel.app) |
| **API (Render)** | [zomato-ai-recommender-api.onrender.com](https://zomato-ai-recommender-api.onrender.com) |
| **API Docs** | [zomato-ai-recommender-api.onrender.com/docs](https://zomato-ai-recommender-api.onrender.com/docs) |

> **Note:** The API runs on Render's free tier — the first request after idle may take ~30–60 seconds (cold start).

## Features

- **Smart filters** — city, area search, multi-cuisine, rating slider, price range
- **AI recommendations** — Groq LLM explains why each restaurant fits your preferences
- **51K+ restaurants** — sourced from the [Zomato Hugging Face dataset](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- **Responsive UI** — works on mobile, tablet, and desktop
- **Production-ready** — Redis caching, rate limiting, Docker, and CI/CD

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, Vite, TypeScript, Tailwind CSS, TanStack Query |
| Backend | FastAPI, SQLAlchemy, SQLite |
| AI | Groq (`groq/compound-mini`) |
| Cache | Redis (optional) |
| Hosting | Vercel (UI) + Render (API) |

## Project Structure

```
backend/
├── shared/          # Config + database models
├── phase1/          # Data ingestion & validation
├── phase2/          # Filter API & stats endpoints
├── phase3/          # Groq LLM recommendations
├── phase5/          # Production middleware (cache, rate limit)
├── docker/          # Pre-built SQLite for cloud deploy
└── data/            # Local SQLite database (gitignored)
frontend/phase4/     # React dashboard
.github/workflows/   # CI pipeline
render.yaml          # Render one-click backend deploy
docker-compose.yml   # Local full stack (API + UI + Redis)
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full phased development plan.

## Quick Start (Local)

### 1. Backend

```bash
cd backend
pip install -r requirements.txt

# First-time only: ingest dataset (~51K restaurants)
python phase1/scripts/ingest_hf_dataset.py --clear
python phase1/scripts/validate_data.py

# Start API
py -3.13 -m uvicorn phase2.app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend/phase4
npm install
npm run dev
```

Open http://localhost:5173

### 3. Environment

Copy `.env.example` to `.env` and set your Groq key:

```
GROQ_API_KEY=your_key_here
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/v1/filters/options` | Cities, cuisines, price/rating ranges |
| `POST` | `/api/v1/recommend` | AI-powered recommendations |
| `GET` | `/api/v1/restaurants` | Browse restaurants |
| `GET` | `/api/v1/stats/overview` | Dashboard KPIs |

## Deployment

| Component | Platform | Config |
|-----------|----------|--------|
| Frontend | [Vercel](https://vercel.com) | `frontend/phase4/` — see `vercel.json` |
| Backend | [Render](https://render.com) | `render.yaml` blueprint |

**Render env vars:** `GROQ_API_KEY`, `CORS_ORIGINS=https://zomato-ai-recommender.vercel.app`

## Tests

```bash
# Backend (all phases)
cd backend && pytest

# Frontend
cd frontend/phase4 && npm test
```

## Docker (full stack)

```bash
docker compose up --build
```

- Dashboard: http://localhost:5173
- API: http://localhost:8000/docs

## License

This project uses the Zomato restaurant dataset for educational purposes. Zomato branding is used for demonstration only.
