from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    """Central AI settings loaded from environment variables."""

    app_env: str = "local"

    openai_api_key: str | None = None
    llm_model_name: str = "gpt-4o-mini"

    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str = "ai-character-dev"

    voxcpm_tts_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",
    )


ai_settings = AISettings()
