from __future__ import annotations

from typing import Protocol

from app.ai_services.contracts import ContinuityContext, ContinuityUpdateProposal


class ContinuityStore(Protocol):
    """
    Port/interface for user-character continuity state.

    This is what makes the character feel like the same character
    when the user returns after several days.
    """

    async def get_continuity_state(
        self,
        user_id: str,
        character_id: str,
    ) -> ContinuityContext:
        """Return persistent continuity state for user + character."""
        ...

    async def save_continuity_update(
        self,
        user_id: str,
        character_id: str,
        update: ContinuityUpdateProposal,
    ) -> None:
        """Persist AI-proposed continuity update."""
        ...
