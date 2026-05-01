import asyncio

from app.ai_services.providers.llm import MockLLMClient


def test_mock_llm_generate_returns_content():
    async def run():
        llm = MockLLMClient()

        result = await llm.generate(
            system_prompt="You are Aisha.",
            user_message="Hey",
            metadata={"test": True},
        )

        assert result.content
        assert result.model_name == "mock-llm"
        assert result.tokens_input > 0
        assert result.tokens_output > 0

    asyncio.run(run())
