import json

import pytest

from phase2.schemas.recommendation import RecommendRequest
from phase3.schemas.llm import LlmRecommendResponse, LlmRecommendationItem
from phase3.services.llm_service import (
    build_user_prompt,
    parse_llm_response,
    rank_with_groq,
    validate_llm_recommendations,
)
from shared.db.models import Restaurant


def test_build_user_prompt_includes_preferences_and_candidates():
    request = RecommendRequest(city="Banashankari", cuisines=["Italian"], limit=3)
    candidates = [
        Restaurant(
            id=2,
            name="Onesta",
            rating=4.6,
            votes=2556,
            cuisines="Pizza, Cafe, Italian",
            cost_for_two=600,
            city="Banashankari",
        )
    ]
    prompt = build_user_prompt(request, candidates)
    assert "Banashankari" in prompt
    assert "Onesta" in prompt
    assert "Italian" in prompt


def test_parse_llm_response_validates_schema():
    payload = {
        "summary": "Great picks for Italian food.",
        "recommendations": [
            {
                "restaurant_id": 2,
                "rank": 1,
                "match_score": 90,
                "reason": "Highly rated Italian cafe.",
                "highlights": ["4.6★"],
            }
        ],
    }
    parsed = parse_llm_response(json.dumps(payload))
    assert parsed.summary.startswith("Great picks")
    assert parsed.recommendations[0].restaurant_id == 2


def test_validate_llm_recommendations_rejects_hallucinated_ids():
    llm_response = LlmRecommendResponse(
        summary="Test",
        recommendations=[
            LlmRecommendationItem(
                restaurant_id=999,
                rank=1,
                match_score=90,
                reason="Fake restaurant",
                highlights=[],
            ),
            LlmRecommendationItem(
                restaurant_id=2,
                rank=2,
                match_score=85,
                reason="Real restaurant",
                highlights=[],
            ),
        ],
    )
    candidates = [Restaurant(id=2, name="Onesta", votes=100)]
    validated = validate_llm_recommendations(llm_response, candidates, limit=5)
    assert len(validated.recommendations) == 1
    assert validated.recommendations[0].restaurant_id == 2


def test_validate_llm_recommendations_raises_when_all_ids_invalid():
    llm_response = LlmRecommendResponse(
        summary="Test",
        recommendations=[
            LlmRecommendationItem(
                restaurant_id=999,
                rank=1,
                match_score=90,
                reason="Fake",
                highlights=[],
            )
        ],
    )
    with pytest.raises(ValueError, match="no valid restaurant IDs"):
        validate_llm_recommendations(llm_response, [Restaurant(id=2, name="Onesta")], limit=5)


def test_rank_with_groq_uses_client(mock_groq_client, mock_groq_response, monkeypatch):
    monkeypatch.setattr("phase3.services.llm_service.settings.groq_api_key", "test-key")
    monkeypatch.setattr("phase3.services.llm_service.Groq", lambda api_key: mock_groq_client)

    request = RecommendRequest(city="Banashankari", cuisines=["Italian"], limit=1)
    candidates = [
        Restaurant(
            id=2,
            name="Onesta",
            rating=4.6,
            votes=2556,
            cuisines="Pizza, Cafe, Italian",
            cost_for_two=600,
            city="Banashankari",
        )
    ]

    result = rank_with_groq(request, candidates)
    assert result.summary == mock_groq_response.summary
    assert result.recommendations[0].restaurant_id == 2
    mock_groq_client.chat.completions.create.assert_called_once()
