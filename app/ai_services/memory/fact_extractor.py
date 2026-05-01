from __future__ import annotations

import re

from app.ai_services.config.default_limits import DEFAULT_MEMORY_SALIENCE
from app.ai_services.contracts import MemoryUpdateProposal


class FactExtractor:
    """
    Extracts simple durable memory candidates from user messages.

    This is a lightweight first version.
    Later, LangChain fact extraction can improve this.
    """

    _NAME_PATTERNS = [
        re.compile(r"\bmy name is\s+([a-zA-Z ]+)", re.IGNORECASE),
        re.compile(r"\bcall me\s+([a-zA-Z ]+)", re.IGNORECASE),
        re.compile(r"\bmujhe\s+([a-zA-Z ]+)\s+bolo", re.IGNORECASE),
    ]

    def extract_from_user_message(self, message: str) -> list[MemoryUpdateProposal]:
        text = message.strip()
        if not text:
            return []

        updates: list[MemoryUpdateProposal] = []

        preferred_name = self._extract_preferred_name(text)
        if preferred_name:
            updates.append(
                MemoryUpdateProposal(
                    memory_type="user_preference",
                    content=f"User prefers to be called {preferred_name}.",
                    salience_score=0.95,
                    should_pin=True,
                )
            )

        lowered = text.lower()

        if "hinglish" in lowered:
            updates.append(
                MemoryUpdateProposal(
                    memory_type="language_preference",
                    content="User prefers Hinglish conversation.",
                    salience_score=0.9,
                    should_pin=True,
                )
            )

        if "i like" in lowered or "mujhe" in lowered and "pasand" in lowered:
            updates.append(
                MemoryUpdateProposal(
                    memory_type="preference",
                    content=f"User preference mentioned: {text}",
                    salience_score=DEFAULT_MEMORY_SALIENCE,
                    should_pin=False,
                )
            )

        return updates

    def _extract_preferred_name(self, text: str) -> str | None:
        for pattern in self._NAME_PATTERNS:
            match = pattern.search(text)
            if match:
                return match.group(1).strip().split(".")[0]

        return None
