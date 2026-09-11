from phase2.schemas.recommendation import RecommendRequest
from phase3.services.cache_service import get_cached, make_cache_key
from phase3.services.recommend_service import SOURCE_CACHE, SOURCE_GROQ, SOURCE_RULE_BASED, recommend_with_groq


def test_recommend_with_groq_returns_ai_ranking(db_session, mock_groq_client, monkeypatch):
    monkeypatch.setattr("phase3.services.llm_service.settings.groq_api_key", "test-key")
    monkeypatch.setattr("phase3.services.llm_service.Groq", lambda api_key: mock_groq_client)

    request = RecommendRequest(
        city="Banashankari",
        min_rating=4.0,
        max_price=700,
        cuisines=["Italian"],
        limit=1,
    )
    response = recommend_with_groq(db_session, request)

    assert response.source == SOURCE_GROQ
    assert response.total_candidates == 1
    assert len(response.recommendations) == 1
    assert response.recommendations[0].name == "Onesta"
    assert response.recommendations[0].match_score == 96
    assert "4.6" in response.recommendations[0].reason or "Onesta" in response.recommendations[0].reason
    assert response.llm_latency_ms is not None


def test_recommend_falls_back_when_groq_fails(db_session, monkeypatch):
    monkeypatch.setattr("phase3.services.llm_service.settings.groq_api_key", "test-key")

    def raise_error(*_args, **_kwargs):
        raise RuntimeError("Groq unavailable")

    monkeypatch.setattr("phase3.services.recommend_service.rank_with_groq", raise_error)

    request = RecommendRequest(city="Banashankari", use_llm=True, limit=3)
    response = recommend_with_groq(db_session, request)

    assert response.source == SOURCE_RULE_BASED
    assert response.total_candidates == 3
    assert len(response.recommendations) == 3


def test_recommend_rule_based_when_use_llm_false(db_session):
    request = RecommendRequest(city="Banashankari", use_llm=False, limit=2)
    response = recommend_with_groq(db_session, request)

    assert response.source == SOURCE_RULE_BASED
    assert len(response.recommendations) == 2


def test_recommend_uses_cache_on_repeat_request(db_session, mock_groq_client, monkeypatch):
    monkeypatch.setattr("phase3.services.llm_service.settings.groq_api_key", "test-key")
    monkeypatch.setattr("phase3.services.llm_service.Groq", lambda api_key: mock_groq_client)

    request = RecommendRequest(city="Banashankari", cuisines=["Italian"], limit=1)

    first = recommend_with_groq(db_session, request)
    second = recommend_with_groq(db_session, request)

    assert first.source == SOURCE_GROQ
    assert second.source == SOURCE_CACHE
    assert mock_groq_client.chat.completions.create.call_count == 1

    cache_key = make_cache_key(request.model_dump())
    assert get_cached(cache_key) is not None
