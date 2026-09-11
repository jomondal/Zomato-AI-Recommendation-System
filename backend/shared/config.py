from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = f"sqlite:///{(BACKEND_ROOT / 'data' / 'zomato.db').as_posix()}"
    groq_api_key: str = ""
    groq_model: str = "groq/compound-mini"

    hf_dataset_name: str = "ManikaSaini/zomato-restaurant-recommendation"
    expected_row_count: int = 51717

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://localhost"

    redis_url: str = ""
    cache_ttl_seconds: int = 3600

    api_key: str = ""
    rate_limit_requests: int = 30
    rate_limit_window_seconds: int = 60


settings = Settings()
