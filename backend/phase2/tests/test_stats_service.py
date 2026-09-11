from phase2.schemas.restaurant import RestaurantFilters
from phase2.services.stats_service import (
    get_filter_options,
    get_filtered_stats,
    get_overview_stats,
    get_top_cities,
    get_top_cuisines,
)


def test_overview_stats(db_session):
    stats = get_overview_stats(db_session)
    assert stats.total_restaurants == 3
    assert stats.total_cities == 1
    assert stats.average_rating is not None


def test_top_cities_and_cuisines(db_session):
    cities = get_top_cities(db_session, limit=5)
    cuisines = get_top_cuisines(db_session, limit=10)
    cuisine_names = {item.cuisine for item in cuisines}

    assert cities[0].city == "Banashankari"
    assert cities[0].count == 3
    assert "Italian" in cuisine_names


def test_filtered_stats(db_session):
    stats = get_filtered_stats(
        db_session,
        RestaurantFilters(city="Banashankari", min_rating=4.0, max_price=700, cuisines=["Italian"]),
    )
    assert stats.total_restaurants == 1
    assert stats.average_rating is not None
    assert stats.total_cities == 1


def test_filter_options(db_session):
    options = get_filter_options(db_session)
    assert "Banashankari" in options["cities"]
    assert "Italian" in options["cuisines"]
    assert options["rating_range"]["max"] >= options["rating_range"]["min"]
