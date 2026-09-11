from phase2.schemas.recommendation import RecommendRequest
from phase2.schemas.restaurant import RestaurantFilters
from phase2.services.filter_service import count_restaurants, filter_restaurants, get_restaurant_by_id


def test_filter_by_city_rating_price_and_cuisine(db_session):
    request = RecommendRequest(
        city="Banashankari",
        min_rating=4.0,
        max_price=700,
        cuisines=["Italian"],
    )
    results = filter_restaurants(db_session, request)
    assert len(results) == 1
    assert results[0].name == "Onesta"


def test_filter_empty_cuisine_returns_multiple_matches(db_session):
    request = RecommendRequest(city="Banashankari")
    results = filter_restaurants(db_session, request)
    assert len(results) == 3


def test_count_and_get_by_id(db_session):
    filters = RestaurantFilters(city="Banashankari", cuisines=["Italian"])
    assert count_restaurants(db_session, filters) == 1

    from sqlalchemy import select

    from shared.db.models import Restaurant

    onesta = db_session.scalar(select(Restaurant).where(Restaurant.name == "Onesta"))
    assert onesta is not None
    assert get_restaurant_by_id(db_session, onesta.id) is not None


def test_min_rating_boundary_excludes_lower_rated(db_session):
    request = RecommendRequest(city="Banashankari", min_rating=4.0)
    results = filter_restaurants(db_session, request)
    names = {restaurant.name for restaurant in results}
    assert "Onesta" in names
    assert "Addhuri Udupi Bhojana" not in names
