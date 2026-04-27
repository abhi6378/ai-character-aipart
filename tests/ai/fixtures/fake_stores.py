from __future__ import annotations

from app.ai_services.contracts import (
    CharacterContext,
    ContinuityContext,
    ContinuityUpdateProposal,
    MemoryContext,
    MemoryUpdateProposal,
    VoiceContext,
    VoicePayload,
    UserPersonaContext,
)

from tests.ai.fixtures.fake_character_data import FAKE_CHARACTER
from tests.ai.fixtures.fake_continuity_data import FAKE_CONTINUITY
from tests.ai.fixtures.fake_memory_data import FAKE_MEMORY_CONTEXT
from tests.ai.fixtures.fake_user_persona_data import FAKE_USER_PERSONA
from tests.ai.fixtures.fake_voice_data import FAKE_VOICE_CONTEXT


class FakeCharacterStore:
    async def get_active_character_version(self, character_id: str) -> CharacterContext:
        return FAKE_CHARACTER


class FakeUserPersonaStore:
    async def get_user_persona(self, user_id: str) -> UserPersonaContext:
        return FAKE_USER_PERSONA


class FakeMemoryStore:
    def __init__(self) -> None:
        self.saved_updates: list[MemoryUpdateProposal] = []

    async def get_memory_context(
        self,
        user_id: str,
        character_id: str,
        thread_id: str,
    ) -> MemoryContext:
        return FAKE_MEMORY_CONTEXT

    async def save_memory_updates(
        self,
        user_id: str,
        character_id: str,
        updates: list[MemoryUpdateProposal],
    ) -> None:
        self.saved_updates.extend(updates)


class FakeContinuityStore:
    def __init__(self) -> None:
        self.saved_update: ContinuityUpdateProposal | None = None

    async def get_continuity_state(
        self,
        user_id: str,
        character_id: str,
    ) -> ContinuityContext:
        return FAKE_CONTINUITY

    async def save_continuity_update(
        self,
        user_id: str,
        character_id: str,
        update: ContinuityUpdateProposal,
    ) -> None:
        self.saved_update = update


class FakeVoiceStore:
    async def get_voice_context(self, character_id: str) -> VoiceContext:
        return FAKE_VOICE_CONTEXT


class FakeAudioStore:
    def __init__(self) -> None:
        self.created_assets: list[dict] = []

    async def create_pending_audio_asset(
        self,
        thread_id: str,
        message_id: str,
        voice_payload: VoicePayload,
    ) -> str:
        audio_asset_id = f"audio_{len(self.created_assets) + 1:03d}"
        self.created_assets.append(
            {
                "audio_asset_id": audio_asset_id,
                "thread_id": thread_id,
                "message_id": message_id,
                "voice_payload": voice_payload,
            }
        )
        return audio_asset_id
