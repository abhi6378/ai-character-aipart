from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


LanguageMode = Literal["english", "hindi", "hinglish", "auto"]
MessageRole = Literal["user", "assistant", "system"]
EmotionTag = Literal[
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
]


class UserPersonaContext(BaseModel):
    """User-level persona data used by AI to address the user naturally."""

    user_id: str
    display_name: str | None = None
    preferred_name: str | None = None
    preferred_language: LanguageMode = "auto"
    persona_summary: str | None = None


class CharacterContext(BaseModel):
    """Active character version/config loaded from backend database."""

    character_id: str
    character_version_id: str
    name: str
    description: str
    personality: str
    speaking_style: str | None = None
    greeting_message: str | None = None
    system_prompt: str | None = None
    inference_config: dict[str, Any] = Field(default_factory=dict)


class ChatMessageContext(BaseModel):
    """Recent message context used for prompt building."""

    role: MessageRole
    content: str
    created_at: str | None = None


class MemoryItemContext(BaseModel):
    """Long-term memory item for user-character continuity."""

    memory_id: str | None = None
    memory_type: str
    content: str
    salience_score: float = 0.5
    is_pinned: bool = False


class MemoryContext(BaseModel):
    """Selected memory context passed into prompt."""

    recent_messages: list[ChatMessageContext] = Field(default_factory=list)
    selected_memories: list[MemoryItemContext] = Field(default_factory=list)
    summary: str | None = None


class ContinuityContext(BaseModel):
    """Persistent user-character state loaded from backend."""

    user_id: str
    character_id: str
    tone_state: str | None = None
    relationship_label: str | None = None
    relationship_score: float = 0.0
    last_interaction_at: str | None = None
    last_context_summary: str | None = None
    language_mode: LanguageMode = "auto"


class LanguageContext(BaseModel):
    """Language processing result."""

    detected_language: LanguageMode
    response_language: LanguageMode
    tts_preprocessing_required: bool = False


class VoiceContext(BaseModel):
    """Character voice config used for VoxCPM payload preparation."""

    voice_profile_id: str | None = None
    voice_id: str | None = None
    voice_style: str | None = None
    speed: float = 1.0
    pitch: float | None = None
    reference_audio_id: str | None = None
    inference_config: dict[str, Any] = Field(default_factory=dict)
