from collections.abc import Iterable
from typing import Any

from sqlalchemy.orm import Session

from phase1.etl.transformers import transform_row
from shared.db.models import Restaurant


def rows_to_restaurants(rows: Iterable[dict[str, Any]]) -> list[Restaurant]:
    restaurants: list[Restaurant] = []
    seen_urls: set[str] = set()

    for row in rows:
        data = transform_row(row)
        url = data.get("url")
        if url:
            if url in seen_urls:
                continue
            seen_urls.add(url)

        restaurants.append(Restaurant(**data))

    return restaurants


def bulk_insert_restaurants(session: Session, restaurants: list[Restaurant], batch_size: int = 500) -> int:
    inserted = 0
    for index in range(0, len(restaurants), batch_size):
        batch = restaurants[index : index + batch_size]
        session.add_all(batch)
        session.commit()
        inserted += len(batch)
    return inserted


def clear_restaurants(session: Session) -> None:
    session.query(Restaurant).delete()
    session.commit()
