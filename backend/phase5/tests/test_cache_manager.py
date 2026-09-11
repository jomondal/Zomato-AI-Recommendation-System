import fakeredis

from phase2.schemas.recommendation import RecommendResponse
from phase5.cache.manager import clear_cache, get_cached, make_cache_key, set_cached
from phase5.cache.redis_backend import reset_redis_client
from shared.config import settings


def test_cache_roundtrip_in_memory(monkeypatch):
    monkeypatch.setattr(settings, "redis_url", "")
    reset_redis_client()
    clear_cache()

    response = RecommendResponse(
        summary="Test summary",
        total_candidates=1,
        recommendations=[],
        latency_ms=50,
        source="groq",
        llm_latency_ms=40,
    )
    key = make_cache_key({"city": "BTM"})
    set_cached(key, response)

    cached = get_cached(key)
    assert cached is not None
    assert cached.summary == "Test summary"
    assert cached.source == "groq"


def test_cache_uses_redis_when_configured(monkeypatch):
    fake = fakeredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(settings, "redis_url", "redis://localhost:6379/0")
    monkeypatch.setattr(settings, "cache_ttl_seconds", 60)
    reset_redis_client()
    clear_cache()

    import phase5.cache.redis_backend as redis_backend

    monkeypatch.setattr(redis_backend, "_client", fake)
    monkeypatch.setattr(redis_backend, "_redis_available", True)

    response = RecommendResponse(
        summary="Redis cached",
        total_candidates=2,
        recommendations=[],
        latency_ms=30,
        source="groq",
    )
    key = make_cache_key({"city": "Banashankari", "cuisine": "Italian"})
    set_cached(key, response)

    cached = get_cached(key)
    assert cached is not None
    assert cached.summary == "Redis cached"
