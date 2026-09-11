"""
Ingest the Zomato restaurant dataset from Hugging Face into the local database.

Usage:
    python phase1/scripts/ingest_hf_dataset.py
    python phase1/scripts/ingest_hf_dataset.py --limit 1000
    python phase1/scripts/ingest_hf_dataset.py --clear
"""

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BACKEND_ROOT))

from datasets import load_dataset  # noqa: E402

from phase1.etl.ingest import bulk_insert_restaurants, clear_restaurants, rows_to_restaurants  # noqa: E402
from shared.config import settings  # noqa: E402
from shared.db.database import SessionLocal, init_db  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest Zomato dataset from Hugging Face")
    parser.add_argument("--limit", type=int, default=None, help="Optional row limit for testing")
    parser.add_argument("--clear", action="store_true", help="Clear existing restaurants before ingestion")
    parser.add_argument("--batch-size", type=int, default=500, help="Batch size for database inserts")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    data_dir = BACKEND_ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading dataset: {settings.hf_dataset_name}")
    dataset = load_dataset(settings.hf_dataset_name, split="train")
    rows = dataset
    if args.limit:
        rows = dataset.select(range(min(args.limit, len(dataset))))
        print(f"Limiting ingestion to {len(rows)} rows")

    print("Transforming rows...")
    restaurants = rows_to_restaurants(rows)

    init_db()
    session = SessionLocal()
    try:
        if args.clear:
            print("Clearing existing restaurants...")
            clear_restaurants(session)

        print(f"Inserting {len(restaurants)} restaurants...")
        inserted = bulk_insert_restaurants(session, restaurants, batch_size=args.batch_size)
        print(f"Done. Inserted {inserted} restaurants into {settings.database_url}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
