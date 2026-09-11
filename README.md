# Zomato AI Restaurant Recommendation System

AI-powered restaurant recommendations using the [Zomato Hugging Face dataset](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) and **Groq LLM**.

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full phased plan.

## Project Structure (by phase)

```
backend/
├── shared/          # Config + DB models (used by all phases)
├── phase1/          # Data foundation (ETL, ingestion, validation)
├── phase2/          # Filter API & stats (FastAPI)
├── phase3/          # Groq LLM recommendations
├── data/            # SQLite database
frontend/
└── phase4/          # Dashboard UI (React)
.github/workflows/     # CI/CD pipeline
docker-compose.yml   # Redis + API + UI
└── requirements.txt
```

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Phase 1 — Data Foundation

```bash
python phase1/scripts/ingest_hf_dataset.py --clear
python phase1/scripts/validate_data.py
pytest phase1/tests
```

## Phase 2 — Filter API & Stats

```bash
uvicorn phase2.app.main:app --reload --port 8000
pytest phase2/tests
```

API docs: http://localhost:8000/docs

## Phase 3 — Groq LLM Integration

Add `GROQ_API_KEY` to `.env` (see `.env.example`), then:

```bash
pytest phase3/tests
pytest phase3/tests/test_integration_groq.py  # live Groq test
```

`POST /api/v1/recommend` uses Groq for AI ranking; set `"use_llm": false` for rule-based mode.

## Phase 4 — Dashboard UI

```bash
cd frontend/phase4
npm install
npm run dev
```

Requires the API running on port 8000. Tests: `npm test`

## Phase 5 — Production (Docker + Redis + CI)

```bash
docker compose up --build
```

- Dashboard: http://localhost:5173
- API docs: http://localhost:8000/docs

```bash
cd backend && pytest phase5/tests
```

## Run all tests

```bash
pytest
```
