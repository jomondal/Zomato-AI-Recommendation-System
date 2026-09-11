import json
import logging
from typing import Any

import redis

from shared.config import settings

logger = logging.getLogger(__name__)

_client: redis.Redis | None = None
_redis_available = False


def get_redis_client() -> redis.Redis | None:
    global _client, _redis_available
    if not settings.redis_url:
        return None
    if _client is None:
        try:
            _client = redis.from_url(settings.redis_url, decode_responses=True)
            _client.ping()
            _redis_available = True
            logger.info("Redis cache connected: %s", settings.redis_url)
        except redis.RedisError as exc:
            logger.warning("Redis unavailable, using in-memory cache: %s", exc)
            _redis_available = False
            _client = None
    return _client if _redis_available else None


def redis_get(key: str) -> Any | None:
    client = get_redis_client()
    if client is None:
        return None
    try:
        raw = client.get(f"zomato:rec:{key}")
        if raw is None:
            return None
        return json.loads(raw)
    except (redis.RedisError, json.JSONDecodeError) as exc:
        logger.warning("Redis get failed: %s", exc)
        return None


def redis_set(key: str, value: dict[str, Any], ttl_seconds: int) -> bool:
    client = get_redis_client()
    if client is None:
        return False
    try:
        client.setex(f"zomato:rec:{key}", ttl_seconds, json.dumps(value))
        return True
    except redis.RedisError as exc:
        logger.warning("Redis set failed: %s", exc)
        return False


def redis_clear() -> None:
    client = get_redis_client()
    if client is None:
        return
    try:
        for key in client.scan_iter("zomato:rec:*"):
            client.delete(key)
    except redis.RedisError as exc:
        logger.warning("Redis clear failed: %s", exc)


def reset_redis_client() -> None:
    global _client, _redis_available
    _client = None
    _redis_available = False
