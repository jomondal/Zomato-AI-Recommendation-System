import json

from sqlalchemy import func, select

from phase1.etl.ingest import rows_to_restaurants
from shared.db.models import Restaurant


def test_rows_to_restaurants_deduplicates_by_url(sample_rows):
    restaurants = rows_to_restaurants(sample_rows)
    assert len(restaurants) == 3
    names = {restaurant.name for restaurant in restaurants}
    assert "Jalsa Duplicate" not in names


def test_populated_session_inserts_expected_records(populated_session):
    count = populated_session.scalar(select(func.count()).select_from(Restaurant))
    assert count == 3

    onesta = populated_session.scalar(select(Restaurant).where(Restaurant.name == "Onesta"))
    assert onesta is not None
    assert onesta.rating == 4.6
    assert onesta.cost_for_two == 600
    assert onesta.city == "Banashankari"
    assert json.loads(onesta.cuisine_tags) == ["Pizza", "Cafe", "Italian"]


def test_cities_and_cuisines_are_queryable(populated_session):
    cities = populated_session.scalars(
        select(Restaurant.city).where(Restaurant.city.is_not(None)).distinct()
    ).all()
    assert "Banashankari" in cities

    italian_restaurants = [
        restaurant
        for restaurant in populated_session.scalars(select(Restaurant)).all()
        if "Italian" in json.loads(restaurant.cuisine_tags or "[]")
    ]
    assert len(italian_restaurants) == 1
    assert italian_restaurants[0].name == "Onesta"
