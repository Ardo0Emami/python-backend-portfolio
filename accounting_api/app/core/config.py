from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Accounting API"
    environment: str = "dev"  # dev | test | prod
    debug: bool = True
    database_url: str = "sqlite:///./dev.db"
    echo_sql: bool = False
    api_key: str = "dev-secret-key"
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
