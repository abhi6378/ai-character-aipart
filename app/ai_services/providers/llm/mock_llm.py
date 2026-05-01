from __future__ import annotations

from app.ai_services.providers.llm.base_llm import LLMResult


class MockLLMClient:
    """
    Local test LLM.

    Does not call OpenAI.
    Does not require API key.
    Used in unit/integration tests.
    """

    async def generate(
        self,
        *,
        system_prompt: str,
        user_message: str,
        metadata: dict | None = None,
    ) -> LLMResult:
        return LLMResult(
            content=(
                '{"display_text": "Arre Mahendra, 5 din baad aaye ho. '
                'Main soch rahi thi tum busy ho gaye.", '
                '"action_text": "Aisha smiles softly.", '
                '"emotion": "playful"}'
            ),
            tokens_input=100,
            tokens_output=35,
            model_name="mock-llm",
        )
