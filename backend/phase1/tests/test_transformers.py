import json

from phase1.etl.transformers import (
    extract_review_snippet,
    parse_cost,
    parse_cuisine_tags,
    parse_rating,
    parse_yes_no,
    transform_row,
)


def test_parse_rating_from_fraction():
    assert parse_rating("4.1/5") == 4.1


def test_parse_rating_handles_new_and_missing():
    assert parse_rating("NEW") is None
    assert parse_rating(None) is None
    assert parse_rating("-") is None


def test_parse_cost_strips_non_digits():
    assert parse_cost("800") == 800
    assert parse_cost("1,200") == 1200
    assert parse_cost(None) is None


def test_parse_cuisine_tags_splits_and_trims():
    assert parse_cuisine_tags("North Indian, Mughlai, Chinese") == [
        "North Indian",
        "Mughlai",
        "Chinese",
    ]
    assert parse_cuisine_tags("") == []


def test_parse_yes_no():
    assert parse_yes_no("Yes") is True
    assert parse_yes_no("No") is False


def test_extract_review_snippet_from_list_literal():
    reviews = "[('Rated 4.0', 'RATED\\n A beautiful place to dine in.')]"
    snippet = extract_review_snippet(reviews, max_length=100)
    assert snippet is not None
    assert "beautiful place" in snippet


def test_transform_row_maps_hf_columns():
    row = {
        "name": "Onesta",
        "url": "https://example.com/onesta",
        "address": "Banashankari",
        "location": "Banashankari",
        "listed_in(city)": "Banashankari",
        "rest_type": "Cafe",
        "cuisines": "Pizza, Cafe, Italian",
        "rate": "4.6/5",
        "votes": 2556,
        "approx_cost(for two people)": "600",
        "dish_liked": "Pizza",
        "online_order": "Yes",
        "book_table": "Yes",
        "listed_in(type)": "Cafes",
        "reviews_list": "[('Rated 5.0', 'RATED\\n Great pizza.')]",
    }

    result = transform_row(row)
    assert result["name"] == "Onesta"
    assert result["rating"] == 4.6
    assert result["cost_for_two"] == 600
    assert result["online_order"] is True
    assert json.loads(result["cuisine_tags"]) == ["Pizza", "Cafe", "Italian"]
