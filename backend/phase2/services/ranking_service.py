import math

from shared.db.models import Restaurant


def compute_rank_score(restaurant: Restaurant) -> float:
    rating = restaurant.rating or 0.0
    votes = restaurant.votes or 0
    return rating * math.log10(votes + 1)


def to_match_score(rank_score: float, max_score: float) -> int:
    if max_score <= 0:
        return 0
    return min(100, max(1, int((rank_score / max_score) * 100)))


def build_reason(restaurant: Restaurant) -> str:
    rating_text = f"{restaurant.rating:.1f}★" if restaurant.rating is not None else "unrated"
    cost_text = f"₹{restaurant.cost_for_two} for two" if restaurant.cost_for_two else "price unavailable"
    cuisine_text = restaurant.cuisines or "varied cuisines"
    location_text = restaurant.location or restaurant.city or "your area"
    return (
        f"Rated {rating_text} with {restaurant.votes} votes in {location_text}. "
        f"Serves {cuisine_text}. Approx {cost_text}."
    )


def build_highlights(restaurant: Restaurant) -> list[str]:
    highlights: list[str] = []
    if restaurant.rating is not None:
        highlights.append(f"{restaurant.rating:.1f}★")
    if restaurant.cost_for_two is not None:
        highlights.append(f"₹{restaurant.cost_for_two} for two")
    if restaurant.cuisine_tag_list:
        highlights.append(restaurant.cuisine_tag_list[0])
    if restaurant.online_order:
        highlights.append("Online order")
    return highlights[:4]
