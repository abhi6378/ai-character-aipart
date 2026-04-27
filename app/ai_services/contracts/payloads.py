from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class VoicePayload(BaseModel):
    """Payload prepared by AI service for VoxCPM TTS."""

    text_for_tts: str
    display_text: str
    voice_id: str | None = None
    voice_profile_id: str | None = None
    emotion: str = "neutral"
    speed: float = 1.0
    reference_audio_id: str | None = None
    provider: str = "voxcpm"
    inference_config: dict[str, Any] = Field(default_factory=dict)


class MemoryUpdateProposal(BaseModel):
    """AI-proposed memory updates. Backend decides how to persist them."""

    memory_type: str
    content: str
    salience_score: float = 0.5
    should_pin: bool = False
    source: str = "chat_turn"


class ContinuityUpdateProposal(BaseModel):
    """AI-proposed user-character continuity update."""

    tone_state: str | None = None
    relationship_label: str | None = None
    relationship_delta: float = 0.0
    last_context_summary: str | None = None
    language_mode: str | None = None


class TraceMetadata(BaseModel):
    """Safe tracing metadata for LangSmith/logging."""

    prompt_version: str | None = None
    model_name: str | None = None
    character_version_id: str | None = None
    language_mode: str | None = None
    memory_count: int = 0
    tokens_input: int = 0
    tokens_output: int = 0
    fallback_used: bool = False
