from __future__ import annotations

from app.ai_services.contracts import MemoryContext, MemoryUpdateProposal
from app.ai_services.memory.fact_extractor import FactExtractor
from app.ai_services.memory.memory_pinner import MemoryPinner
from app.ai_services.memory.memory_selector import MemorySelector
from app.ai_services.memory.memory_summarizer import MemorySummarizer
from app.ai_services.ports import MemoryStore


class MemoryService:
    """
    Main memory service used by the AI orchestrator.

    Responsibilities:
    - load memory context through MemoryStore
    - select best memories for prompt
    - propose memory updates from user messages
    - optionally save memory updates through store
    """

    def __init__(
        self,
        memory_store: MemoryStore | None = None,
        selector: MemorySelector | None = None,
        fact_extractor: FactExtractor | None = None,
        pinner: MemoryPinner | None = None,
        summarizer: MemorySummarizer | None = None,
    ) -> None:
        self._memory_store = memory_store
        self._selector = selector or MemorySelector()
        self._fact_extractor = fact_extractor or FactExtractor()
        self._pinner = pinner or MemoryPinner()
        self._summarizer = summarizer or MemorySummarizer()

    async def load_prompt_memory(
        self,
        *,
        user_id: str,
        character_id: str,
        thread_id: str,
    ) -> MemoryContext:
        if self._memory_store is None:
            return MemoryContext()

        raw_memory = await self._memory_store.get_memory_context(
            user_id=user_id,
            character_id=character_id,
            thread_id=thread_id,
        )

        return self._selector.select(raw_memory)

    def propose_memory_updates(
        self,
        *,
        user_message: str,
    ) -> list[MemoryUpdateProposal]:
        raw_updates = self._fact_extractor.extract_from_user_message(user_message)
        return self._pinner.apply_pinning_rules(raw_updates)

    async def save_memory_updates(
        self,
        *,
        user_id: str,
        character_id: str,
        updates: list[MemoryUpdateProposal],
    ) -> None:
        if not updates:
            return

        if self._memory_store is None:
            return

        await self._memory_store.save_memory_updates(
            user_id=user_id,
            character_id=character_id,
            updates=updates,
        )

    def summarize_recent_messages(self, memory: MemoryContext) -> str:
        return self._summarizer.summarize_messages(memory.recent_messages)
