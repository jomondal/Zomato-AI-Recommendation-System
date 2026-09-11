import logging
import time

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from phase2.schemas.recommendation import RecommendRequest, RecommendationItem, RecommendResponse
from phase2.services.filter_service import filter_restaurants
from phase2.services.ranking_service import build_highlights, compute_rank_score
from phase2.services.recommend_service import recommend_restaurants as rule_based_recommend
from phase3.services.cache_service import get_cached, make_cache_key, set_cached
from phase3.services.llm_service import rank_with_groq
from shared.db.models import Restaurant

SOURCE_GROQ = "groq"
SOURCE_RULE_BASED = "rule_based"
SOURCE_CACHE = "cache"


def _candidate_map(candidates: list[Restaurant]) -> dict[int, Restaurant]:
    return {restaurant.id: restaurant for restaurant in candidates}


def _merge_llm_with_restaurants(
    llm_response,
    candidates_by_id: dict[int, Restaurant],
) -> list[RecommendationItem]:
    recommendations: list[RecommendationItem] = []
    for item in llm_response.recommendations:
        restaurant = candidates_by_id.get(item.restaurant_id)
        if restaurant is None:
            continue
        highlights = item.highlights or build_highlights(restaurant)
        recommendations.append(
            RecommendationItem(
                rank=item.rank,
                restaurant_id=restaurant.id,
                name=restaurant.name,
                rating=restaurant.rating,
                votes=restaurant.votes,
                cost_for_two=restaurant.cost_for_two,
                location=restaurant.location,
                city=restaurant.city,
                cuisines=restaurant.cuisines,
                match_score=item.match_score,
                reason=item.reason,
                highlights=highlights,
                url=restaurant.url,
                online_order=restaurant.online_order,
                book_table=restaurant.book_table,
            )
        )
    return recommendations


def recommend_with_groq(session: Session, request: RecommendRequest) -> RecommendResponse:
    started = time.perf_counter()
    cache_key = make_cache_key(request.model_dump())

    cached = get_cached(cache_key)
    if cached is not None:
        return cached.model_copy(
            update={
                "source": SOURCE_CACHE,
                "latency_ms": int((time.perf_counter() - started) * 1000),
            }
        )

    candidates = filter_restaurants(session, request)
    total_candidates = len(candidates)

    if total_candidates == 0:
        return RecommendResponse(
            summary="No restaurants matched your filters.",
            total_candidates=0,
            recommendations=[],
            latency_ms=int((time.perf_counter() - started) * 1000),
            source=SOURCE_RULE_BASED,
            llm_latency_ms=None,
        )

    if not request.use_llm:
        response = rule_based_recommend(session, request)
        response.source = SOURCE_RULE_BASED
        set_cached(cache_key, response)
        return response

    llm_started = time.perf_counter()
    try:
        ranked_for_llm = sorted(candidates, key=compute_rank_score, reverse=True)
        llm_response = rank_with_groq(request, ranked_for_llm)
        llm_latency_ms = int((time.perf_counter() - llm_started) * 1000)

        recommendations = _merge_llm_with_restaurants(
            llm_response,
            _candidate_map(candidates),
        )

        response = RecommendResponse(
            summary=llm_response.summary,
            total_candidates=total_candidates,
            recommendations=recommendations,
            latency_ms=int((time.perf_counter() - started) * 1000),
            source=SOURCE_GROQ,
            llm_latency_ms=llm_latency_ms,
        )
        set_cached(cache_key, response)
        return response

    except Exception as exc:
        logger.exception("Groq recommendation failed, using rule-based fallback: %s", exc)
        fallback = rule_based_recommend(session, request)
        fallback.source = SOURCE_RULE_BASED
        fallback.latency_ms = int((time.perf_counter() - started) * 1000)
        fallback.llm_latency_ms = None
        return fallback
