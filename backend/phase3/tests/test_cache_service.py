from phase2.schemas.recommendation import RecommendResponse
from phase3.services.cache_service import get_cached, make_cache_key, set_cached


def test_cache_stores_and_retrieves_values():
    key = make_cache_key({"city": "Banashankari", "min_rating": 4.0})
    assert get_cached(key) is None

    response = RecommendResponse(
        summary="cached",
        total_candidates=1,
        recommendations=[],
        latency_ms=10,
        source="groq",
    )
    set_cached(key, response)
    cached = get_cached(key)
    assert cached is not None
    assert cached.summary == "cached"


def test_cache_key_is_stable_for_same_payload():
    payload = {"city": "BTM", "cuisines": ["Italian"]}
    assert make_cache_key(payload) == make_cache_key(payload)
