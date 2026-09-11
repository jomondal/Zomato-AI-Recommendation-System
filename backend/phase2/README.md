# Phase 2 — Filter API & Stats

Rule-based FastAPI endpoints (no Groq LLM yet).

## Run API

```bash
cd backend
.venv\Scripts\activate
uvicorn phase2.app.main:app --reload --host 0.0.0.0 --port 8000
```

Open docs: http://localhost:8000/docs

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/v1/recommend` | Rule-based recommendations |
| GET | `/api/v1/restaurants` | Paginated browse |
| GET | `/api/v1/restaurants/{id}` | Restaurant detail |
| GET | `/api/v1/stats/overview` | Dashboard KPIs |
| GET | `/api/v1/stats/cities` | Top cities |
| GET | `/api/v1/stats/cuisines` | Top cuisines |
| GET | `/api/v1/filters/options` | UI dropdown values |

## Tests

```bash
pytest phase2/tests
```

## Exit criteria

- API returns ranked restaurants for valid preference combos in < 200ms
- Stats and filter options endpoints return live DB data
