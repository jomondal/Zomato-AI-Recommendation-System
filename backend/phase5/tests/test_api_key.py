from fastapi import FastAPI
from fastapi.testclient import TestClient

from phase5.middleware.api_key import ApiKeyMiddleware
from shared.config import settings


def test_api_key_middleware_blocks_without_key(monkeypatch):
    monkeypatch.setattr(settings, "api_key", "secret-key")
    app = FastAPI()
    app.add_middleware(ApiKeyMiddleware)

    @app.get("/api/v1/stats/overview")
    def protected():
        return {"ok": True}

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    client = TestClient(app)

    health = client.get("/api/health")
    assert health.status_code == 200

    blocked = client.get("/api/v1/stats/overview")
    assert blocked.status_code == 401

    allowed = client.get("/api/v1/stats/overview", headers={"X-API-Key": "secret-key"})
    assert allowed.status_code == 200


def test_api_key_middleware_disabled_when_not_configured(monkeypatch):
    monkeypatch.setattr(settings, "api_key", "")
    app = FastAPI()
    app.add_middleware(ApiKeyMiddleware)

    @app.get("/api/v1/stats/overview")
    def protected():
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/api/v1/stats/overview")
    assert response.status_code == 200
