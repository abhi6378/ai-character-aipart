from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel


class LLMResult(BaseModel):
    """Normalized result returned by any LLM provider."""

    content: str
    tokens_input: int = 0
    tokens_output: int = 0
    model_name: str | None = None


class BaseLLMClient(Protocol):
    """Interface for all LLM clients."""

    async def generate(
        self,
        *,
        system_prompt: str,
        user_message: str,
        metadata: dict | None = None,
    ) -> LLMResult:
        """Generate an assistant response."""
        ...
