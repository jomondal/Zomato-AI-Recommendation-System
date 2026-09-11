import json
from collections import Counter

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from phase2.schemas.restaurant import RestaurantFilters
from phase2.schemas.stats import CityStat, CuisineStat, FilteredStats, OverviewStats
from phase2.services.filter_service import _apply_filters
from shared.db.models import Restaurant


def get_overview_stats(session: Session) -> OverviewStats:
    total_restaurants = session.scalar(select(func.count()).select_from(Restaurant)) or 0
    restaurants_with_rating = session.scalar(
        select(func.count()).select_from(Restaurant).where(Restaurant.rating.is_not(None))
    ) or 0
    average_rating = session.scalar(select(func.avg(Restaurant.rating)).where(Restaurant.rating.is_not(None)))
    average_cost = session.scalar(
        select(func.avg(Restaurant.cost_for_two)).where(Restaurant.cost_for_two.is_not(None))
    )
    total_cities = session.scalar(
        select(func.count(func.distinct(Restaurant.city))).where(Restaurant.city.is_not(None))
    ) or 0

    cuisine_counter: Counter[str] = Counter()
    for tags_json in session.scalars(select(Restaurant.cuisine_tags).where(Restaurant.cuisine_tags.is_not(None))):
        cuisine_counter.update(json.loads(tags_json))

    return OverviewStats(
        total_restaurants=total_restaurants,
        restaurants_with_rating=restaurants_with_rating,
        average_rating=round(average_rating, 2) if average_rating is not None else None,
        average_cost_for_two=round(average_cost, 2) if average_cost is not None else None,
        total_cities=total_cities,
        total_cuisines=len(cuisine_counter),
    )


def get_filtered_stats(session: Session, filters: RestaurantFilters) -> FilteredStats:
    filtered = _apply_filters(select(Restaurant), filters).subquery()

    total_restaurants = session.scalar(select(func.count()).select_from(filtered)) or 0
    average_rating = session.scalar(
        select(func.avg(filtered.c.rating)).where(filtered.c.rating.is_not(None))
    )
    average_cost = session.scalar(
        select(func.avg(filtered.c.cost_for_two)).where(filtered.c.cost_for_two.is_not(None))
    )
    total_cities = (
        session.scalar(
            select(func.count(func.distinct(filtered.c.city))).where(filtered.c.city.is_not(None))
        )
        or 0
    )

    return FilteredStats(
        total_restaurants=total_restaurants,
        average_rating=round(average_rating, 2) if average_rating is not None else None,
        average_cost_for_two=round(average_cost, 2) if average_cost is not None else None,
        total_cities=total_cities,
    )


def get_top_cities(session: Session, limit: int = 10) -> list[CityStat]:
    rows = session.execute(
        select(Restaurant.city, func.count(Restaurant.id))
        .where(Restaurant.city.is_not(None))
        .group_by(Restaurant.city)
        .order_by(func.count(Restaurant.id).desc())
        .limit(limit)
    ).all()
    return [CityStat(city=city, count=count) for city, count in rows]


def get_top_cuisines(session: Session, limit: int = 10) -> list[CuisineStat]:
    cuisine_counter: Counter[str] = Counter()
    for tags_json in session.scalars(select(Restaurant.cuisine_tags).where(Restaurant.cuisine_tags.is_not(None))):
        cuisine_counter.update(json.loads(tags_json))

    return [CuisineStat(cuisine=name, count=count) for name, count in cuisine_counter.most_common(limit)]


def get_filter_options(session: Session) -> dict:
    cities = session.scalars(
        select(Restaurant.city).where(Restaurant.city.is_not(None)).distinct().order_by(Restaurant.city)
    ).all()
    locations = session.scalars(
        select(Restaurant.location).where(Restaurant.location.is_not(None)).distinct().order_by(Restaurant.location)
    ).all()

    cuisine_counter: Counter[str] = Counter()
    for tags_json in session.scalars(select(Restaurant.cuisine_tags).where(Restaurant.cuisine_tags.is_not(None))):
        cuisine_counter.update(json.loads(tags_json))

    min_price = session.scalar(select(func.min(Restaurant.cost_for_two)).where(Restaurant.cost_for_two.is_not(None)))
    max_price = session.scalar(select(func.max(Restaurant.cost_for_two)).where(Restaurant.cost_for_two.is_not(None)))
    min_rating = session.scalar(select(func.min(Restaurant.rating)).where(Restaurant.rating.is_not(None)))
    max_rating = session.scalar(select(func.max(Restaurant.rating)).where(Restaurant.rating.is_not(None)))

    price_ranges = [
        {"label": "Budget", "min": 0, "max": 400},
        {"label": "Mid-range", "min": 401, "max": 800},
        {"label": "Premium", "min": 801, "max": int(max_price or 2000)},
    ]

    return {
        "cities": list(cities),
        "locations": list(locations),
        "cuisines": sorted(cuisine_counter.keys()),
        "price_ranges": price_ranges,
        "rating_range": {
            "min": float(min_rating or 0),
            "max": float(max_rating or 5),
        },
    }
