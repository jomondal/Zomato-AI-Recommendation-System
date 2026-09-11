import ast
import json
import re
from typing import Any

NULL_VALUES = {"", "null", "none", "-", "nan", "NEW"}


def _clean_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if text.lower() in NULL_VALUES:
        return None
    return text


def parse_rating(rate_value: Any) -> float | None:
    text = _clean_string(rate_value)
    if not text:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    if not match:
        return None
    rating = float(match.group(1))
    if rating > 5:
        return None
    return rating


def parse_cost(cost_value: Any) -> int | None:
    text = _clean_string(cost_value)
    if not text:
        return None
    digits = re.sub(r"[^\d]", "", text)
    if not digits:
        return None
    return int(digits)


def parse_cuisine_tags(cuisines_value: Any) -> list[str]:
    text = _clean_string(cuisines_value)
    if not text:
        return []
    return [part.strip() for part in text.split(",") if part.strip()]


def parse_yes_no(value: Any) -> bool:
    text = _clean_string(value)
    return text is not None and text.lower() == "yes"


def extract_review_snippet(reviews_value: Any, max_length: int = 500) -> str | None:
    if reviews_value is None:
        return None

    text = str(reviews_value).strip()
    if not text or text.lower() in NULL_VALUES:
        return None

    if text.startswith("[") and text.endswith("]"):
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list) and parsed:
                first = parsed[0]
                if isinstance(first, (list, tuple)) and len(first) > 1:
                    text = str(first[1])
                else:
                    text = str(first)
        except (SyntaxError, ValueError):
            pass

    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."


def transform_row(row: dict[str, Any]) -> dict[str, Any]:
    cuisine_tags = parse_cuisine_tags(row.get("cuisines"))
    return {
        "name": _clean_string(row.get("name")) or "Unknown",
        "url": _clean_string(row.get("url")),
        "address": _clean_string(row.get("address")),
        "location": _clean_string(row.get("location")),
        "city": _clean_string(row.get("listed_in(city)")),
        "rest_type": _clean_string(row.get("rest_type")),
        "cuisines": _clean_string(row.get("cuisines")),
        "cuisine_tags": json.dumps(cuisine_tags),
        "rating": parse_rating(row.get("rate")),
        "votes": int(row.get("votes") or 0),
        "cost_for_two": parse_cost(row.get("approx_cost(for two people)")),
        "dish_liked": _clean_string(row.get("dish_liked")),
        "online_order": parse_yes_no(row.get("online_order")),
        "book_table": parse_yes_no(row.get("book_table")),
        "listed_in_type": _clean_string(row.get("listed_in(type)")),
        "review_snippet": extract_review_snippet(row.get("reviews_list")),
    }
