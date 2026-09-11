import json
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from phase1.etl.ingest import bulk_insert_restaurants, rows_to_restaurants
from shared.db.database import Base

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_ROWS_PATH = FIXTURES_DIR / "sample_rows.json"


@pytest.fixture
def sample_rows() -> list[dict]:
    with SAMPLE_ROWS_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def test_db_url(tmp_path) -> str:
    return f"sqlite:///{tmp_path / 'test_zomato.db'}"


@pytest.fixture
def db_session(test_db_url):
    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def populated_session(db_session, sample_rows):
    restaurants = rows_to_restaurants(sample_rows)
    bulk_insert_restaurants(db_session, restaurants)
    return db_session
