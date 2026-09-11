# Phase 3 — Groq LLM Integration

AI-powered restaurant ranking and explanations via **Groq** (`groq/compound-mini`), with rule-based fallback and in-memory caching.

## Setup

Add to project root `.env`:

```env
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=groq/compound-mini
```

## How it works

1. Filter restaurants (Phase 2) by price, place, rating, cuisine
2. Send top 20 candidates + user preferences to Groq
3. Groq returns ranked picks with `reason`, `match_score`, and `summary`
4. Validate all `restaurant_id` values exist in the candidate list (no hallucinations)
5. Cache identical requests in memory
6. Fall back to rule-based ranking if Groq fails

## Tests

```bash
pytest phase3/tests -m "not integration"   # unit tests (mocked Groq)
pytest phase3/tests/test_integration_groq.py  # live Groq call
```

## API

`POST /api/v1/recommend` now returns:

```json
{
  "summary": "AI-generated overview...",
  "source": "groq",
  "llm_latency_ms": 850,
  "recommendations": [...]
}
```

Set `"use_llm": false` to force rule-based mode.
