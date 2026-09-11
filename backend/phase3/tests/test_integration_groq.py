"""Live Groq integration test — runs only when GROQ_API_KEY is set."""

import pytest
from fastapi.testclient import TestClient

from phase2.app.main import app
from phase3.services.cache_service import clear_cache
from shared.config import settings


@pytest.mark.integration
def test_live_groq_recommendation():
    if not settings.groq_api_key:
        pytest.skip("GROQ_API_KEY not configured")

    clear_cache()

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/recommend",
            json={
                "city": "Banashankari",
                "min_rating": 4.0,
                "max_price": 700,
                "cuisines": ["Italian"],
                "free_text": "family dinner, good pizza",
                "limit": 3,
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "groq"
    assert body["total_candidates"] > 0
    assert len(body["recommendations"]) > 0
    assert body["summary"]
    assert body["llm_latency_ms"] is not None
    assert body["llm_latency_ms"] < 10000
    assert body["latency_ms"] < 15000

    for item in body["recommendations"]:
        assert item["reason"]
        assert 0 <= item["match_score"] <= 100
        assert item["name"]
