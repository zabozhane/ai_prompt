from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AI_CONTEXT_",
        extra="ignore",
    )

    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"
    temperature: float = 0.2


@lru_cache
def get_settings() -> Settings:
    return Settings()
