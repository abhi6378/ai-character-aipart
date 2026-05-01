from __future__ import annotations

from app.ai_services.config.default_limits import PINNED_MEMORY_MIN_SALIENCE
from app.ai_services.contracts import MemoryUpdateProposal


class MemoryPinner:
    """Applies pinning rules to memory update proposals."""

    def apply_pinning_rules(
        self,
        updates: list[MemoryUpdateProposal],
    ) -> list[MemoryUpdateProposal]:
        pinned_types = {
            "user_preference",
            "language_preference",
            "safety_preference",
        }

        final_updates: list[MemoryUpdateProposal] = []

        for update in updates:
            should_pin = (
                update.should_pin
                or update.memory_type in pinned_types
                or update.salience_score >= PINNED_MEMORY_MIN_SALIENCE
            )

            final_updates.append(
                update.model_copy(update={"should_pin": should_pin})
            )

        return final_updates
