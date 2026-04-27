from app.ai_services.contracts import VoiceContext


FAKE_VOICE_CONTEXT = VoiceContext(
    voice_profile_id="voice_profile_001",
    voice_id="aisha_default_voice",
    voice_style="warm_playful_female",
    speed=1.0,
    pitch=None,
    reference_audio_id=None,
    inference_config={
        "provider": "voxcpm",
        "emotion_strength": 0.7,
    },
)
