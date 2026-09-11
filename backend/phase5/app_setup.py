import logging

from fastapi import FastAPI

from phase5.middleware.api_key import ApiKeyMiddleware
from phase5.middleware.rate_limit import RateLimitMiddleware
from phase5.middleware.request_logging import RequestLoggingMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)


def configure_production_app(app: FastAPI) -> None:
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(ApiKeyMiddleware)
