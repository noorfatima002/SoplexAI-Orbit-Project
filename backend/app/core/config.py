"""Application settings, loaded from environment variables / .env (never hard-code secrets)."""
from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # "../.env" = repo root when running from backend/; ".env" = current folder.
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "SoplexAI Orbit API"
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg://orbit:orbit@localhost:5432/orbit"
    api_key: str = ""
    secret_key: str = ""
    n8n_url: str = "http://localhost:5678"
    llm_api_key: str = ""
    cors_origins: str = "http://localhost:3000"

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @model_validator(mode="after")
    def _require_real_secrets_in_production(self) -> "Settings":
        if self.is_production:
            for name in ("api_key", "secret_key"):
                value = getattr(self, name)
                if not value or value.startswith("change_me"):
                    raise ValueError(
                        f"{name.upper()} must be set to a real secret when APP_ENV=production"
                    )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
