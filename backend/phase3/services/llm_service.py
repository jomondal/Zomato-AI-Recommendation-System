import json
import logging
from typing import Any

from groq import Groq

from phase2.schemas.recommendation import RecommendRequest
from phase3.schemas.llm import LlmRecommendResponse
from shared.config import settings
from shared.db.models import Restaurant

logger = logging.getLogger(__name__)

MAX_LLM_CANDIDATES = 20

SYSTEM_PROMPT = """You are a Zomato restaurant recommendation assistant.
You must ONLY recommend restaurants from the provided candidate list.
Never invent restaurant names or IDs.
Return valid JSON matching the required schema exactly."""

USER_PROMPT_TEMPLATE = """User preferences:
{preferences_json}

Candidate restaurants (ONLY choose from these):
{candidates_json}

Return JSON with this exact structure:
{{
  "summary": "One paragraph explaining why these restaurants fit the user",
  "recommendations": [
    {{
      "restaurant_id": <id from candidate list>,
      "rank": 1,
      "match_score": 95,
      "reason": "2-3 sentences citing rating, cuisine, price, and reviews",
      "highlights": ["4.6★", "₹600 for two", "North Indian"],
      "best_for": "family dinner"
    }}
  ]
}}

Rules:
- Return at most {limit} recommendations, ranked best first
- restaurant_id MUST exist in the candidate list
- match_score is 0-100 based on fit to preferences
- reason must reference real data from the candidate (rating, price, cuisine, reviews)"""


def restaurant_to_candidate(restaurant: Restaurant) -> dict[str, Any]:
    return {
        "restaurant_id": restaurant.id,
        "name": restaurant.name,
        "rating": restaurant.rating,
        "votes": restaurant.votes,
        "cost_for_two": restaurant.cost_for_two,
        "location": restaurant.location,
        "city": restaurant.city,
        "cuisines": restaurant.cuisines,
        "dish_liked": restaurant.dish_liked,
        "review_snippet": (restaurant.review_snippet or "")[:250],
        "online_order": restaurant.online_order,
        "book_table": restaurant.book_table,
    }


def build_preferences_payload(request: RecommendRequest) -> dict[str, Any]:
    return {
        "city": request.city,
        "location": request.location,
        "min_rating": request.min_rating,
        "max_rating": request.max_rating,
        "min_price": request.min_price,
        "max_price": request.max_price,
        "cuisines": request.cuisines,
        "free_text": request.free_text,
        "limit": request.limit,
    }


def build_user_prompt(request: RecommendRequest, candidates: list[Restaurant]) -> str:
    preferences_json = json.dumps(build_preferences_payload(request), indent=2)
    candidates_json = json.dumps(
        [restaurant_to_candidate(restaurant) for restaurant in candidates],
        indent=2,
    )
    return USER_PROMPT_TEMPLATE.format(
        preferences_json=preferences_json,
        candidates_json=candidates_json,
        limit=request.limit,
    )


def parse_llm_response(raw_content: str) -> LlmRecommendResponse:
    data = json.loads(raw_content)
    return LlmRecommendResponse.model_validate(data)


def validate_llm_recommendations(
    llm_response: LlmRecommendResponse,
    candidates: list[Restaurant],
    limit: int,
) -> LlmRecommendResponse:
    allowed_ids = {restaurant.id for restaurant in candidates}
    valid_items = [
        item for item in llm_response.recommendations if item.restaurant_id in allowed_ids
    ]

    if not valid_items:
        raise ValueError("Groq returned no valid restaurant IDs from candidate list")

    valid_items.sort(key=lambda item: item.rank)
    return LlmRecommendResponse(
        summary=llm_response.summary,
        recommendations=valid_items[:limit],
    )


def rank_with_groq(request: RecommendRequest, candidates: list[Restaurant]) -> LlmRecommendResponse:
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is not configured")

    if not candidates:
        return LlmRecommendResponse(summary="No restaurants matched your filters.", recommendations=[])

    llm_candidates = candidates[:MAX_LLM_CANDIDATES]
    client = Groq(api_key=settings.groq_api_key)

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(request, llm_candidates)},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    raw_content = response.choices[0].message.content or "{}"
    logger.info("Groq response received for model=%s", settings.groq_model)
    parsed = parse_llm_response(raw_content)
    return validate_llm_recommendations(parsed, llm_candidates, request.limit)
