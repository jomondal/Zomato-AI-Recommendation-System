import pytest
from fastapi.testclient import TestClient

from phase2.app.main import app
from shared.db.database import get_db


@pytest.fixture
def groq_client(db_session, mock_groq_client, monkeypatch):
    monkeypatch.setattr("phase3.services.llm_service.settings.groq_api_key", "test-key")
    monkeypatch.setattr("phase3.services.llm_service.Groq", lambda api_key: mock_groq_client)

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_recommend_api_with_groq(groq_client):
    response = groq_client.post(
        "/api/v1/recommend",
        json={
            "city": "Banashankari",
            "min_rating": 4.0,
            "max_price": 700,
            "cuisines": ["Italian"],
            "free_text": "good pizza and rooftop ambience",
            "limit": 1,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "groq"
    assert body["total_candidates"] == 1
    assert body["recommendations"][0]["name"] == "Onesta"
    assert body["llm_latency_ms"] is not None
    assert body["latency_ms"] < 2000
