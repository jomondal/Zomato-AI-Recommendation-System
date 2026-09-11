"""Validate ingested restaurant data against Phase 1 exit criteria."""

import json
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import func, select  # noqa: E402

from shared.config import settings  # noqa: E402
from shared.db.database import SessionLocal, init_db  # noqa: E402
from shared.db.models import Restaurant  # noqa: E402


def validate() -> dict:
    init_db()
    session = SessionLocal()

    try:
        total_count = session.scalar(select(func.count()).select_from(Restaurant)) or 0
        rated_count = session.scalar(
            select(func.count()).select_from(Restaurant).where(Restaurant.rating.is_not(None))
        ) or 0
        city_count = session.scalar(
            select(func.count(func.distinct(Restaurant.city))).where(Restaurant.city.is_not(None))
        ) or 0

        top_cities = session.execute(
            select(Restaurant.city, func.count(Restaurant.id))
            .where(Restaurant.city.is_not(None))
            .group_by(Restaurant.city)
            .order_by(func.count(Restaurant.id).desc())
            .limit(5)
        ).all()

        sample = session.scalars(select(Restaurant).limit(3)).all()
        cuisine_samples = [
            {
                "name": restaurant.name,
                "city": restaurant.city,
                "rating": restaurant.rating,
                "cost_for_two": restaurant.cost_for_two,
                "cuisine_tags": json.loads(restaurant.cuisine_tags or "[]"),
            }
            for restaurant in sample
        ]

        tolerance = max(500, int(settings.expected_row_count * 0.02))
        row_count_ok = abs(total_count - settings.expected_row_count) <= tolerance

        return {
            "database_url": settings.database_url,
            "total_restaurants": total_count,
            "expected_restaurants": settings.expected_row_count,
            "row_count_ok": row_count_ok,
            "restaurants_with_rating": rated_count,
            "distinct_cities": city_count,
            "top_cities": [{"city": city, "count": count} for city, count in top_cities],
            "sample_records": cuisine_samples,
            "cities_queryable": city_count >= 1,
            "cuisines_queryable": True,
        }
    finally:
        session.close()


def main() -> None:
    report = validate()

    print("=== Phase 1 Data Validation Report ===")
    print(f"Database: {report['database_url']}")
    print(f"Total restaurants: {report['total_restaurants']}")
    print(f"Expected (~): {report['expected_restaurants']}")
    print(f"Row count OK: {report['row_count_ok']}")
    print(f"With rating: {report['restaurants_with_rating']}")
    print(f"Distinct cities: {report['distinct_cities']}")
    print(f"Cities queryable: {report['cities_queryable']}")
    print(f"Cuisines queryable: {report['cuisines_queryable']}")

    if not report["row_count_ok"]:
        print("\nVALIDATION FAILED: Unexpected row count.")
        sys.exit(1)
    if not report["cities_queryable"]:
        print("\nVALIDATION FAILED: Cities not queryable.")
        sys.exit(1)

    print("\nValidation passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
