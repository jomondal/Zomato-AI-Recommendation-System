# Phase 4 — Dashboard UI

Zomato-style React dashboard wired to the Phase 2/3 FastAPI backend.

## Stack

- React 18 + Vite + TypeScript
- Tailwind CSS (Zomato red `#E23744`)
- Recharts (Top Cities bar chart)
- TanStack Query (API state)

## Run

```bash
# Terminal 1 — API
cd backend
uvicorn phase2.app.main:app --reload --port 8000

# Terminal 2 — Dashboard
cd frontend/phase4
npm install
npm run dev
```

Open http://localhost:5173

## Tests

```bash
npm test
npm run build
```

## Features

- Sidebar + header with city search
- KPI cards from `/api/v1/stats/overview`
- Preference form → `POST /api/v1/recommend` (Groq AI)
- Recommendation cards with match score and reasons
- Top cuisines cards + Top 10 cities chart
