import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from phase1.etl.ingest import bulk_insert_restaurants, rows_to_restaurants
from phase2.app.main import app
from shared.db.database import Base, get_db

FIXTURES_DIR = Path(__file__).resolve().parents[2] / "phase1" / "tests" / "fixtures"
SAMPLE_ROWS_PATH = FIXTURES_DIR / "sample_rows.json"


@pytest.fixture
def sample_rows() -> list[dict]:
    with SAMPLE_ROWS_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def db_session(sample_rows):
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    restaurants = rows_to_restaurants(sample_rows)
    bulk_insert_restaurants(session, restaurants)

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
