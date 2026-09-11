from fastapi import APIRouter

from phase5.cache.redis_backend import get_redis_client
from shared.config import settings

router = APIRouter(tags=["health"])


@router.get("/api/health")
def health_check() -> dict:
    redis_connected = get_redis_client() is not None if settings.redis_url else False
    return {
        "status": "ok",
        "phase": "5",
        "llm": "groq",
        "model": settings.groq_model,
        "redis_enabled": bool(settings.redis_url),
        "redis_connected": redis_connected,
        "rate_limit": f"{settings.rate_limit_requests}/{settings.rate_limit_window_seconds}s",
        "api_key_required": bool(settings.api_key),
    }
