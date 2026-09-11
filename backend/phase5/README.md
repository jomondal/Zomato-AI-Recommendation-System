# Phase 5 — Production Hardening

Production-ready infrastructure for the Zomato AI Recommendation System.

## Features

| Feature | Implementation |
|---------|----------------|
| Docker Compose | `redis` + `backend` + `frontend` one-command startup |
| Redis cache | Hot recommend queries cached (falls back to in-memory) |
| Rate limiting | 30 req/min per IP on `POST /api/v1/recommend` |
| API key auth | Optional `X-API-Key` header when `API_KEY` is set |
| Request tracing | `X-Request-ID` header + structured logs |
| CI/CD | GitHub Actions (`.github/workflows/ci.yml`) |

## Run with Docker

```bash
# From project root (requires GROQ_API_KEY in .env)
docker compose up --build
```

- API: http://localhost:8000/docs
- Dashboard: http://localhost:5173

## Environment variables

```env
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=3600
API_KEY=your_optional_api_key
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW_SECONDS=60
```

## Tests

```bash
cd backend
pytest phase5/tests
```
