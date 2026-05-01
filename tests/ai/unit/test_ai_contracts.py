from app.ai_services.contracts import (
    AIChatRequest,
    AIChatResponse,
    ContinuityUpdateProposal,
    MemoryUpdateProposal,
    TraceMetadata,
    VoicePayload,
)


def test_ai_chat_request_contract():
    request = AIChatRequest(
        user_id="user_001",
        character_id="char_001",
        thread_id="thread_001",
        message="Hey, kaise ho?",
        request_audio=True,
    )

    assert request.user_id == "user_001"
    assert request.character_id == "char_001"
    assert request.request_audio is True


def test_ai_chat_response_contract():
    response = AIChatResponse(
        display_text="Main theek hoon, tum batao?",
        action_text="She smiles softly.",
        emotion="playful",
        character_version_id="char_ver_001",
        memory_updates=[
            MemoryUpdateProposal(
                memory_type="preference",
                content="User prefers Hinglish conversation.",
                salience_score=0.8,
                should_pin=True,
            )
        ],
        continuity_update=ContinuityUpdateProposal(
            tone_state="playful",
            relationship_label="friendly",
            relationship_delta=0.1,
            language_mode="hinglish",
        ),
        voice_payload=VoicePayload(
            text_for_tts="??? ??? ???, ??? ?????",
            display_text="Main theek hoon, tum batao?",
            voice_id="aisha_default",
            emotion="playful",
        ),
        trace=TraceMetadata(
            prompt_version="chat_v1",
            model_name="openai",
            character_version_id="char_ver_001",
            memory_count=1,
        ),
    )

    assert response.display_text
    assert response.emotion == "playful"
    assert len(response.memory_updates) == 1
    assert response.voice_payload is not None
