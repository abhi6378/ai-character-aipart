import asyncio

from app.ai_services.chains import CharacterResponseChain
from app.ai_services.contracts import LanguageContext
from app.ai_services.prompts import PromptBuilder
from app.ai_services.providers.llm import MockLLMClient
from tests.ai.fixtures.fake_character_data import FAKE_CHARACTER
from tests.ai.fixtures.fake_continuity_data import FAKE_CONTINUITY
from tests.ai.fixtures.fake_memory_data import FAKE_MEMORY_CONTEXT
from tests.ai.fixtures.fake_user_persona_data import FAKE_USER_PERSONA


def test_character_response_chain_with_mock_llm():
    async def run():
        prompt_builder = PromptBuilder()
        llm = MockLLMClient()
        chain = CharacterResponseChain(llm_client=llm)

        language = LanguageContext(
            detected_language="hinglish",
            response_language="hinglish",
            tts_preprocessing_required=True,
        )

        built_prompt = prompt_builder.build_chat_prompt(
            character=FAKE_CHARACTER,
            user_persona=FAKE_USER_PERSONA,
            memory=FAKE_MEMORY_CONTEXT,
            continuity=FAKE_CONTINUITY,
            language=language,
            user_message="Hey Aisha, main 5 din baad aaya hu.",
        )

        result = await chain.run(
            built_prompt=built_prompt,
            metadata={"test_name": "character_response_chain_mock"},
        )

        assert result.content
        assert "Mahendra" in result.content
        assert result.model_name == "mock-llm"

    asyncio.run(run())
