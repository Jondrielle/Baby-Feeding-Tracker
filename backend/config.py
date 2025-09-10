# backend/config.py
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    model_config = ConfigDict(
        # Use .env for local dev; CI injects variables directly
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
