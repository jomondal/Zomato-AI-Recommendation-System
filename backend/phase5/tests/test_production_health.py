from fastapi.testclient import TestClient

from phase2.app.main import app


def test_health_reports_phase5_metadata():
    client = TestClient(app)
    response = client.get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["phase"] == "5"
    assert body["llm"] == "groq"
    assert "rate_limit" in body
    assert "redis_enabled" in body
