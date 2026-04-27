from __future__ import annotations

from typing import Protocol

from app.ai_services.contracts import UserPersonaContext


class UserPersonaStore(Protocol):
    """
    Port/interface for loading user persona data.

    This helps the character address the user naturally.
    Example: preferred name, preferred language, persona summary.
    """

    async def get_user_persona(self, user_id: str) -> UserPersonaContext:
        """Return user persona information for AI personalization."""
        ...
