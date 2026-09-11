import time

from sqlalchemy.orm import Session

from phase2.schemas.recommendation import RecommendRequest, RecommendationItem, RecommendResponse
from phase2.services.filter_service import filter_restaurants
from phase2.services.ranking_service import (
    build_highlights,
    build_reason,
    compute_rank_score,
    to_match_score,
)


def build_summary(request: RecommendRequest, total: int) -> str:
    parts: list[str] = []
    if request.city:
        parts.append(f"in {request.city}")
    if request.cuisines:
        parts.append(f"serving {', '.join(request.cuisines)}")
    if request.min_rating is not None:
        parts.append(f"rated {request.min_rating}+")
    if request.max_price is not None:
        parts.append(f"under ₹{request.max_price} for two")

    criteria = ", ".join(parts) if parts else "your preferences"
    return f"Found {total} restaurants matching {criteria} (rule-based ranking, no LLM)."


def recommend_restaurants(session: Session, request: RecommendRequest) -> RecommendResponse:
    started = time.perf_counter()
    candidates = filter_restaurants(session, request)
    total_candidates = len(candidates)

    ranked = sorted(candidates, key=compute_rank_score, reverse=True)
    top = ranked[: request.limit]

    scores = [compute_rank_score(restaurant) for restaurant in top]
    max_score = max(scores) if scores else 0.0

    recommendations: list[RecommendationItem] = []
    for index, restaurant in enumerate(top, start=1):
        rank_score = compute_rank_score(restaurant)
        recommendations.append(
            RecommendationItem(
                rank=index,
                restaurant_id=restaurant.id,
                name=restaurant.name,
                rating=restaurant.rating,
                votes=restaurant.votes,
                cost_for_two=restaurant.cost_for_two,
                location=restaurant.location,
                city=restaurant.city,
                cuisines=restaurant.cuisines,
                match_score=to_match_score(rank_score, max_score),
                reason=build_reason(restaurant),
                highlights=build_highlights(restaurant),
                url=restaurant.url,
                online_order=restaurant.online_order,
                book_table=restaurant.book_table,
            )
        )

    latency_ms = int((time.perf_counter() - started) * 1000)
    return RecommendResponse(
        summary=build_summary(request, total_candidates),
        total_candidates=total_candidates,
        recommendations=recommendations,
        latency_ms=latency_ms,
        source="rule_based",
        llm_latency_ms=None,
    )
