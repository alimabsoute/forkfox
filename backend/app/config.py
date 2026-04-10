from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_secret_key: str = "dev-secret-change-in-prod"
    app_debug: bool = False

    jwt_secret: str = "dev-jwt-secret-change-in-prod"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    database_url: str = "sqlite:///./forkfox.db"
    redis_url: str = ""

    rate_limit_default: str = "100/minute"
    rate_limit_scoring: str = "30/minute"
    rate_limit_auth: str = "10/minute"

    openai_api_key: str = ""
    scoring_model: str = "gpt-4o-mini"

    allowed_origins: str = "http://localhost:3000,https://forkfox.ai"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
