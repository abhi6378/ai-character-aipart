from __future__ import annotations

from typing import Protocol

from app.ai_services.contracts import MemoryContext, MemoryUpdateProposal


class MemoryStore(Protocol):
    """
    Port/interface for loading and saving memory data.

    AI service proposes memory updates.
    Backend decides how to persist them.
    """

    async def get_memory_context(
        self,
        user_id: str,
        character_id: str,
        thread_id: str,
    ) -> MemoryContext:
        """Return selected memory context for this user-character chat."""
        ...

    async def save_memory_updates(
        self,
        user_id: str,
        character_id: str,
        updates: list[MemoryUpdateProposal],
    ) -> None:
        """Persist AI-proposed memory updates."""
        ...
