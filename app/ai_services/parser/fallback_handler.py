from __future__ import annotations

from app.ai_services.contracts import ParsedAssistantMessage
from app.ai_services.config.emotion_taxonomy import DEFAULT_EMOTION


class FallbackHandler:
    """Creates safe fallback responses when parsing fails."""

    def build_fallback(self, *, raw_text: str | None = None) -> ParsedAssistantMessage:
        return ParsedAssistantMessage(
            display_text="Sorry, mujhe thoda clearly samajh nahi aaya. Ek baar phir se bolna?",
            action_text=None,
            emotion=DEFAULT_EMOTION,
            raw_text=raw_text,
        )
