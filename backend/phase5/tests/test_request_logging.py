from fastapi import FastAPI
from fastapi.testclient import TestClient

from phase5.middleware.request_logging import RequestLoggingMiddleware


def test_request_logging_adds_request_id_header():
    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    client = TestClient(app)
    response = client.get("/api/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 0
