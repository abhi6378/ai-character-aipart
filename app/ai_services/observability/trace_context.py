from __future__ import annotations

from app.ai_services.contracts import CharacterContext, ContinuityContext, MemoryContext


def build_trace_metadata(
    *,
    user_id: str,
    thread_id: str,
    character: CharacterContext,
    memory: MemoryContext,
    continuity: ContinuityContext,
    prompt_version: str,
    model_name: str,
) -> dict:
    """
    Build safe metadata for LangSmith/logging.

    Do not include secrets or full private user messages here.
    """

    return {
        "user_id": user_id,
        "thread_id": thread_id,
        "character_id": character.character_id,
        "character_version_id": character.character_version_id,
        "prompt_version": prompt_version,
        "model_name": model_name,
        "memory_count": len(memory.selected_memories),
        "recent_message_count": len(memory.recent_messages),
        "language_mode": continuity.language_mode,
    }
