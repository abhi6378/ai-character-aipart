from __future__ import annotations

from app.ai_services.contracts import ChatMessageContext


class MemorySummarizer:
    """
    Creates a compact summary from recent messages.

    This lightweight version avoids LLM calls.
    Later this can use memory_summary_chain.py.
    """

    def summarize_messages(self, messages: list[ChatMessageContext]) -> str:
        if not messages:
            return ""

        compact_lines = [
            f"{message.role}: {message.content}"
            for message in messages[-6:]
        ]

        return "Recent conversation summary: " + " | ".join(compact_lines)
