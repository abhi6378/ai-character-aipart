from __future__ import annotations

from app.ai_services.config.default_limits import (
    MAX_PINNED_MEMORIES,
    MAX_SELECTED_MEMORIES,
)
from app.ai_services.contracts import MemoryContext, MemoryItemContext


class MemorySelector:
    """
    Selects the best memory items for prompt context.

    Rule:
    - pinned memories first
    - then high salience memories
    - keep limit small to avoid prompt bloat
    """

    def select(self, memory: MemoryContext) -> MemoryContext:
        pinned = [item for item in memory.selected_memories if item.is_pinned]
        normal = [item for item in memory.selected_memories if not item.is_pinned]

        pinned_sorted = sorted(
            pinned,
            key=lambda item: item.salience_score,
            reverse=True,
        )[:MAX_PINNED_MEMORIES]

        normal_sorted = sorted(
            normal,
            key=lambda item: item.salience_score,
            reverse=True,
        )

        selected_items: list[MemoryItemContext] = (
            pinned_sorted + normal_sorted
        )[:MAX_SELECTED_MEMORIES]

        return MemoryContext(
            recent_messages=memory.recent_messages,
            selected_memories=selected_items,
            summary=memory.summary,
        )
