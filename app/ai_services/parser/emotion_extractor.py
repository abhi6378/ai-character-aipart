from __future__ import annotations

import re

from app.ai_services.config.emotion_taxonomy import normalize_emotion


class EmotionExtractor:
    """Extracts and normalizes emotion from structured or text output."""

    _BRACKET_PATTERN = re.compile(r"^\s*\[([a-zA-Z_ -]+)\]\s*")

    def extract(self, *, emotion: str | None = None, text: str | None = None) -> str:
        if emotion:
            return normalize_emotion(emotion)

        if not text:
            return normalize_emotion(None)

        match = self._BRACKET_PATTERN.match(text)
        if match:
            return normalize_emotion(match.group(1))

        return normalize_emotion(None)
