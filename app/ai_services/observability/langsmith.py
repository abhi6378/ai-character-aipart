from __future__ import annotations

import os

from app.ai_services.config.ai_settings import ai_settings


def configure_langsmith() -> None:
    """
    Configure LangSmith tracing through environment variables.

    This function is safe to call at startup.
    If tracing is disabled, it will not send traces.
    """

    os.environ["LANGSMITH_TRACING"] = "true" if ai_settings.langsmith_tracing else "false"

    if ai_settings.langsmith_api_key:
        os.environ["LANGSMITH_API_KEY"] = ai_settings.langsmith_api_key

    if ai_settings.langsmith_project:
        os.environ["LANGSMITH_PROJECT"] = ai_settings.langsmith_project
