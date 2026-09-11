import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from phase1.etl.ingest import bulk_insert_restaurants, rows_to_restaurants
from phase3.schemas.llm import LlmRecommendResponse, LlmRecommendationItem
from phase3.services.cache_service import clear_cache
from shared.db.database import Base

FIXTURES_DIR = Path(__file__).resolve().parents[2] / "phase1" / "tests" / "fixtures"
SAMPLE_ROWS_PATH = FIXTURES_DIR / "sample_rows.json"


@pytest.fixture(autouse=True)
def reset_cache():
    clear_cache()
    yield
    clear_cache()


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
def mock_groq_response():
    return LlmRecommendResponse(
        summary="Top Italian cafe pick in Banashankari based on rating and reviews.",
        recommendations=[
            LlmRecommendationItem(
                restaurant_id=2,
                rank=1,
                match_score=96,
                reason="Onesta has 4.6★ with 2,556 votes and affordable Italian pizzas.",
                highlights=["4.6★", "₹600 for two", "Italian"],
                best_for="pizza lovers",
            )
        ],
    )


@pytest.fixture
def mock_groq_client(mock_groq_response):
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = mock_groq_response.model_dump_json()
    mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])
    return mock_client
