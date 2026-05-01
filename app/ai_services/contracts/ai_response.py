from __future__ import annotations

from pydantic import BaseModel, Field

from app.ai_services.contracts.payloads import (
    ContinuityUpdateProposal,
    MemoryUpdateProposal,
    TraceMetadata,
    VoicePayload,
)


class ParsedAssistantMessage(BaseModel):
    """Clean assistant output after parsing raw LLM response."""

    display_text: str
    action_text: str | None = None
    emotion: str = "neutral"
    raw_text: str | None = None


class AIChatResponse(BaseModel):
    """
    Final structured response returned by AI service to backend.

    Backend should save messages, apply memory/state updates,
    and trigger voice generation if needed.
    """

    display_text: str
    action_text: str | None = None
    emotion: str = "neutral"
    character_version_id: str | None = None

    memory_updates: list[MemoryUpdateProposal] = Field(default_factory=list)
    continuity_update: ContinuityUpdateProposal | None = None
    voice_payload: VoicePayload | None = None
    trace: TraceMetadata = Field(default_factory=TraceMetadata)
