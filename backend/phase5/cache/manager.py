import hashlib
import json
from typing import Any

from phase2.schemas.recommendation import RecommendResponse
from phase5.cache.memory_backend import memory_clear, memory_get, memory_set
from phase5.cache.redis_backend import redis_clear, redis_get, redis_set
from shared.config import settings


def make_cache_key(payload: dict[str, Any]) -> str:
    normalized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(normalized.encode()).hexdigest()


def get_cached(key: str) -> RecommendResponse | None:
    raw = redis_get(key)
    if raw is None:
        raw = memory_get(key)
    if raw is None:
        return None
    if isinstance(raw, RecommendResponse):
        return raw
    return RecommendResponse.model_validate(raw)


def set_cached(key: str, value: RecommendResponse) -> None:
    payload = value.model_dump()
    memory_set(key, payload)
    redis_set(key, payload, settings.cache_ttl_seconds)


def clear_cache() -> None:
    memory_clear()
    redis_clear()
