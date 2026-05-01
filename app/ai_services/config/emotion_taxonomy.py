from __future__ import annotations

DEFAULT_EMOTION = "neutral"

VALID_EMOTIONS = {
    "neutral",
    "playful",
    "happy",
    "sad",
    "angry",
    "romantic",
    "caring",
    "excited",
    "shy",
    "serious",
    "whisper",
}


def normalize_emotion(emotion: str | None) -> str:
    """Return a safe emotion value supported by the app."""

    if not emotion:
        return DEFAULT_EMOTION

    normalized = emotion.strip().lower()

    if normalized in VALID_EMOTIONS:
        return normalized

    return DEFAULT_EMOTION
