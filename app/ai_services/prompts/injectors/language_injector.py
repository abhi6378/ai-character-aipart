from __future__ import annotations

from app.ai_services.contracts import LanguageContext


class LanguageInjector:
    """Renders language guidance into a prompt section."""

    def render(self, language: LanguageContext | None) -> str:
        if language is None:
            return (
                "Language Guidance: Detect the user's language naturally. "
                "Prefer the user's current style."
            )

        if language.response_language == "hinglish":
            return (
                "Language Guidance: Reply in natural Roman Hinglish. "
                "Keep English words in English and Hindi words in casual Roman style."
            )

        if language.response_language == "hindi":
            return "Language Guidance: Reply naturally in Hindi."

        if language.response_language == "english":
            return "Language Guidance: Reply naturally in English."

        return (
            "Language Guidance: Detect the user's language naturally. "
            "Prefer the user's current style."
        )
