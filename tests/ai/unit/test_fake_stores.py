import asyncio

from app.ai_services.contracts import (
    ContinuityUpdateProposal,
    MemoryUpdateProposal,
    VoicePayload,
)

from tests.ai.fixtures.fake_stores import (
    FakeAudioStore,
    FakeCharacterStore,
    FakeContinuityStore,
    FakeMemoryStore,
    FakeUserPersonaStore,
    FakeVoiceStore,
)


def test_fake_character_store():
    async def run():
        store = FakeCharacterStore()
        character = await store.get_active_character_version("char_001")
        assert character.character_id == "char_001"
        assert character.character_version_id == "char_ver_001"
        assert character.name == "Aisha"

    asyncio.run(run())


def test_fake_user_persona_store():
    async def run():
        store = FakeUserPersonaStore()
        persona = await store.get_user_persona("user_001")
        assert persona.user_id == "user_001"
        assert persona.preferred_name == "Mahendra"

    asyncio.run(run())


def test_fake_memory_store_read_and_write():
    async def run():
        store = FakeMemoryStore()

        memory = await store.get_memory_context(
            user_id="user_001",
            character_id="char_001",
            thread_id="thread_001",
        )

        assert memory.summary is not None
        assert len(memory.selected_memories) == 2

        update = MemoryUpdateProposal(
            memory_type="preference",
            content="User likes short Hinglish replies.",
            salience_score=0.8,
            should_pin=True,
        )

        await store.save_memory_updates(
            user_id="user_001",
            character_id="char_001",
            updates=[update],
        )

        assert len(store.saved_updates) == 1
        assert store.saved_updates[0].content == "User likes short Hinglish replies."

    asyncio.run(run())


def test_fake_continuity_store_read_and_write():
    async def run():
        store = FakeContinuityStore()

        state = await store.get_continuity_state(
            user_id="user_001",
            character_id="char_001",
        )

        assert state.user_id == "user_001"
        assert state.character_id == "char_001"
        assert state.language_mode == "hinglish"

        update = ContinuityUpdateProposal(
            tone_state="playful",
            relationship_label="friendly",
            relationship_delta=0.1,
            last_context_summary="User returned after a gap and conversation resumed naturally.",
            language_mode="hinglish",
        )

        await store.save_continuity_update(
            user_id="user_001",
            character_id="char_001",
            update=update,
        )

        assert store.saved_update is not None
        assert store.saved_update.relationship_delta == 0.1

    asyncio.run(run())


def test_fake_voice_store():
    async def run():
        store = FakeVoiceStore()
        voice = await store.get_voice_context("char_001")

        assert voice.voice_id == "aisha_default_voice"
        assert voice.voice_style == "warm_playful_female"

    asyncio.run(run())


def test_fake_audio_store():
    async def run():
        store = FakeAudioStore()

        payload = VoicePayload(
            text_for_tts="??? ??? ???, ??? ?????",
            display_text="Main theek hoon, tum batao?",
            voice_id="aisha_default_voice",
            emotion="playful",
        )

        audio_asset_id = await store.create_pending_audio_asset(
            thread_id="thread_001",
            message_id="msg_001",
            voice_payload=payload,
        )

        assert audio_asset_id == "audio_001"
        assert len(store.created_assets) == 1

    asyncio.run(run())
