import asyncio

from app.ai_services.memory import FactExtractor, MemorySelector, MemoryService
from tests.ai.fixtures.fake_memory_data import FAKE_MEMORY_CONTEXT
from tests.ai.fixtures.fake_stores import FakeMemoryStore


def test_memory_selector_prioritizes_pinned_memory():
    selector = MemorySelector()

    selected = selector.select(FAKE_MEMORY_CONTEXT)

    assert selected.selected_memories
    assert selected.selected_memories[0].is_pinned is True


def test_fact_extractor_extracts_preferred_name():
    extractor = FactExtractor()

    updates = extractor.extract_from_user_message("Please call me Mahendra.")

    assert len(updates) == 1
    assert updates[0].memory_type == "user_preference"
    assert "Mahendra" in updates[0].content
    assert updates[0].should_pin is True


def test_fact_extractor_extracts_hinglish_preference():
    extractor = FactExtractor()

    updates = extractor.extract_from_user_message("I prefer Hinglish replies.")

    assert updates
    assert updates[0].memory_type == "language_preference"
    assert updates[0].should_pin is True


def test_memory_service_loads_prompt_memory_with_fake_store():
    async def run():
        service = MemoryService(memory_store=FakeMemoryStore())

        memory = await service.load_prompt_memory(
            user_id="user_001",
            character_id="char_001",
            thread_id="thread_001",
        )

        assert memory.summary is not None
        assert len(memory.selected_memories) > 0

    asyncio.run(run())


def test_memory_service_proposes_and_saves_updates():
    async def run():
        store = FakeMemoryStore()
        service = MemoryService(memory_store=store)

        updates = service.propose_memory_updates(
            user_message="Please call me Mahendra."
        )

        await service.save_memory_updates(
            user_id="user_001",
            character_id="char_001",
            updates=updates,
        )

        assert len(store.saved_updates) == 1
        assert "Mahendra" in store.saved_updates[0].content

    asyncio.run(run())


def test_memory_service_summarizes_recent_messages():
    service = MemoryService()

    summary = service.summarize_recent_messages(FAKE_MEMORY_CONTEXT)

    assert "Recent conversation summary" in summary
    assert "user:" in summary
