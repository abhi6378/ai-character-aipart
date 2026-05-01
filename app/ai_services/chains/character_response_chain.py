from __future__ import annotations

from app.ai_services.prompts import BuiltPrompt
from app.ai_services.providers.llm.base_llm import BaseLLMClient, LLMResult


class CharacterResponseChain:
    """
    Chain wrapper for generating a character response.

    In this project, LangChain usage stays inside provider/client layer.
    This class keeps the application flow clean and testable.
    """

    def __init__(self, llm_client: BaseLLMClient) -> None:
        self._llm_client = llm_client

    async def run(
        self,
        *,
        built_prompt: BuiltPrompt,
        metadata: dict | None = None,
    ) -> LLMResult:
        return await self._llm_client.generate(
            system_prompt=built_prompt.system_prompt,
            user_message=built_prompt.user_message,
            metadata={
                **built_prompt.metadata,
                **(metadata or {}),
            },
        )
