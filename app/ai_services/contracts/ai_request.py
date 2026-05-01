from __future__ import annotations

from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    """
    Request sent by backend to AI service.

    Backend is responsible for auth, DB lookup, and persistence.
    AI service is responsible for response generation and update proposals.
    """

    user_id: str
    character_id: str
    thread_id: str
    message: str = Field(min_length=1)
    request_audio: bool = False
    language_mode: str | None = None
    request_id: str | None = None
