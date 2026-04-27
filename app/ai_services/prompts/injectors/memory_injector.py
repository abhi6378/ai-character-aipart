from __future__ import annotations

from app.ai_services.contracts import MemoryContext


class MemoryInjector:
    """Renders selected memory and recent messages into a prompt section."""

    def render(self, memory: MemoryContext) -> str:
        sections: list[str] = []

        if memory.summary:
            sections.append("Conversation Summary:")
            sections.append(memory.summary)

        if memory.selected_memories:
            sections.append("\nImportant Memories:")
            for item in memory.selected_memories:
                pin_marker = "pinned" if item.is_pinned else "normal"
                sections.append(
                    f"- [{pin_marker}] ({item.memory_type}) {item.content}"
                )

        if memory.recent_messages:
            sections.append("\nRecent Messages:")
            for message in memory.recent_messages:
                sections.append(f"- {message.role}: {message.content}")

        if not sections:
            return "No prior memory available."

        return "\n".join(sections)
