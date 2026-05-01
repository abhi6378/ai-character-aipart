from __future__ import annotations

from typing import Protocol

from app.ai_services.contracts import VoiceContext


class VoiceStore(Protocol):
    """
    Port/interface for loading character voice config.

    This config is used to prepare VoxCPM TTS payloads.
    """

    async def get_voice_context(self, character_id: str) -> VoiceContext:
        """Return voice configuration for the selected character."""
        ...
