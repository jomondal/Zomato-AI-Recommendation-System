from sqlalchemy import inspect

from shared.db.database import Base
from shared.db.models import Restaurant


def test_restaurants_table_has_expected_columns(db_session):
    table_names = inspect(db_session.bind).get_table_names()
    assert "restaurants" in table_names

    columns = {column["name"] for column in inspect(db_session.bind).get_columns("restaurants")}
    expected = {
        "id",
        "name",
        "url",
        "address",
        "location",
        "city",
        "rest_type",
        "cuisines",
        "cuisine_tags",
        "rating",
        "votes",
        "cost_for_two",
        "dish_liked",
        "online_order",
        "book_table",
        "listed_in_type",
        "review_snippet",
        "created_at",
    }
    assert expected.issubset(columns)


def test_restaurant_model_registered_with_metadata():
    assert Restaurant.__tablename__ in Base.metadata.tables
