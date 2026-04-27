from app.ai_services.contracts import (
    ChatMessageContext,
    MemoryContext,
    MemoryItemContext,
)


FAKE_MEMORY_CONTEXT = MemoryContext(
    recent_messages=[
        ChatMessageContext(
            role="user",
            content="Aaj kaafi work tha, isliye late aaya.",
            created_at="2026-04-20T10:00:00",
        ),
        ChatMessageContext(
            role="assistant",
            content="Koi baat nahi, main wait kar rahi thi.",
            created_at="2026-04-20T10:00:10",
        ),
    ],
    selected_memories=[
        MemoryItemContext(
            memory_id="mem_001",
            memory_type="preference",
            content="User prefers natural Hinglish conversation.",
            salience_score=0.9,
            is_pinned=True,
        ),
        MemoryItemContext(
            memory_id="mem_002",
            memory_type="fact",
            content="User is working on an AI character app.",
            salience_score=0.7,
            is_pinned=False,
        ),
    ],
    summary="User was busy with work last time and returned after some gap.",
)
