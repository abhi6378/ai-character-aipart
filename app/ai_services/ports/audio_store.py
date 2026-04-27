from __future__ import annotations

from typing import Protocol

from app.ai_services.contracts import VoicePayload


class AudioStore(Protocol):
    """
    Port/interface for audio asset persistence.

    In most cases backend will own actual audio storage.
    This port exists for future flexibility.
    """

    async def create_pending_audio_asset(
        self,
        thread_id: str,
        message_id: str,
        voice_payload: VoicePayload,
    ) -> str:
        """
        Create a pending audio asset record and return audio_asset_id.

        Backend may implement this later using PostgreSQL + GCS.
        """
        ...
