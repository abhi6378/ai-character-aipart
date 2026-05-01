from __future__ import annotations

from typing import Protocol

from app.ai_services.contracts import CharacterContext


class CharacterStore(Protocol):
    """
    Port/interface for loading character data.

    Backend will later implement this using PostgreSQL.
    AI tests can implement this using fake data.
    """

    async def get_active_character_version(self, character_id: str) -> CharacterContext:
        """Return the active character version used for chat generation."""
        ...
