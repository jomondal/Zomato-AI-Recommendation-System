from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from phase2.schemas.recommendation import RecommendRequest
from phase2.schemas.restaurant import RestaurantFilters
from shared.db.models import Restaurant


def _apply_filters(query, filters: RecommendRequest | RestaurantFilters):
    if filters.city:
        query = query.where(Restaurant.city.ilike(filters.city.strip()))

    if filters.location:
        query = query.where(Restaurant.location.ilike(f"%{filters.location.strip()}%"))

    if filters.min_rating is not None:
        query = query.where(Restaurant.rating >= filters.min_rating)

    if filters.max_rating is not None:
        query = query.where(Restaurant.rating <= filters.max_rating)

    if filters.min_price is not None:
        query = query.where(Restaurant.cost_for_two >= filters.min_price)

    if filters.max_price is not None:
        query = query.where(Restaurant.cost_for_two <= filters.max_price)

    if filters.cuisines:
        cuisine_conditions = [
            Restaurant.cuisines.ilike(f"%{cuisine.strip()}%") for cuisine in filters.cuisines if cuisine.strip()
        ]
        if cuisine_conditions:
            query = query.where(or_(*cuisine_conditions))

    return query


def filter_restaurants(session: Session, filters: RecommendRequest | RestaurantFilters) -> list[Restaurant]:
    query = select(Restaurant)
    query = _apply_filters(query, filters)
    return list(session.scalars(query).all())


def count_restaurants(session: Session, filters: RestaurantFilters) -> int:
    from sqlalchemy import func

    query = select(func.count()).select_from(Restaurant)
    query = _apply_filters(query, filters)
    return session.scalar(query) or 0


def paginate_restaurants(session: Session, filters: RestaurantFilters) -> list[Restaurant]:
    query = select(Restaurant)
    query = _apply_filters(query, filters)
    query = query.order_by(Restaurant.rating.desc().nullslast(), Restaurant.votes.desc())
    offset = (filters.page - 1) * filters.page_size
    query = query.offset(offset).limit(filters.page_size)
    return list(session.scalars(query).all())


def get_restaurant_by_id(session: Session, restaurant_id: int) -> Restaurant | None:
    return session.get(Restaurant, restaurant_id)
