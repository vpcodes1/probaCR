"""Application configuration."""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "YUSEARCH"
    app_version: str = "1.0.0"
    debug: bool = False

    # AI Configuration
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    default_ai_model: str = "claude-3-5-sonnet-20241022"

    # Search Configuration
    serper_api_key: str = ""

    # Database
    database_url: str = "sqlite+aiosqlite:///./yusearch.db"

    # Security
    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    allowed_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # Rate Limiting
    rate_limit_per_minute: int = 10

    # Report Settings
    max_report_generation_time: int = 300  # 5 minutes

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
