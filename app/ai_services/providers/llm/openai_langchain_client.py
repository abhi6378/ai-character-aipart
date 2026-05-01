from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.ai_services.config.ai_settings import ai_settings
from app.ai_services.observability.langsmith import configure_langsmith
from app.ai_services.providers.llm.base_llm import LLMResult


class OpenAILangChainClient:
    """
    OpenAI LLM client using LangChain.

    Use this for real model calls.
    Tests should use MockLLMClient to avoid API calls.
    """

    def __init__(self, model_name: str | None = None) -> None:
        configure_langsmith()

        if not ai_settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing. Use MockLLMClient for local tests "
                "or set OPENAI_API_KEY in .env for real calls."
            )

        self._model_name = model_name or ai_settings.llm_model_name
        self._llm = ChatOpenAI(
            model=self._model_name,
            api_key=ai_settings.openai_api_key,
        )

    async def generate(
        self,
        *,
        system_prompt: str,
        user_message: str,
        metadata: dict | None = None,
    ) -> LLMResult:
        response = await self._llm.ainvoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message),
            ],
            config={
                "metadata": metadata or {},
                "tags": ["ai-character", "character-response"],
            },
        )

        usage = getattr(response, "usage_metadata", None) or {}

        return LLMResult(
            content=str(response.content),
            tokens_input=usage.get("input_tokens", 0),
            tokens_output=usage.get("output_tokens", 0),
            model_name=self._model_name,
        )
