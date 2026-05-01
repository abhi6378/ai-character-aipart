from app.ai_services.contracts import ContinuityContext


FAKE_CONTINUITY = ContinuityContext(
    user_id="user_001",
    character_id="char_001",
    tone_state="playful",
    relationship_label="friendly",
    relationship_score=0.35,
    last_interaction_at="2026-04-20T10:00:00",
    last_context_summary="User came late because of work. Aisha responded warmly.",
    language_mode="hinglish",
)
