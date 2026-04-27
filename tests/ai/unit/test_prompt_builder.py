from app.ai_services.contracts import LanguageContext
from app.ai_services.prompts import PromptBuilder
from tests.ai.fixtures.fake_character_data import FAKE_CHARACTER
from tests.ai.fixtures.fake_continuity_data import FAKE_CONTINUITY
from tests.ai.fixtures.fake_memory_data import FAKE_MEMORY_CONTEXT
from tests.ai.fixtures.fake_user_persona_data import FAKE_USER_PERSONA


def test_prompt_builder_includes_all_required_sections():
    builder = PromptBuilder()

    language = LanguageContext(
        detected_language="hinglish",
        response_language="hinglish",
        tts_preprocessing_required=True,
    )

    built_prompt = builder.build_chat_prompt(
        character=FAKE_CHARACTER,
        user_persona=FAKE_USER_PERSONA,
        memory=FAKE_MEMORY_CONTEXT,
        continuity=FAKE_CONTINUITY,
        language=language,
        user_message="Hey Aisha, main 5 din baad aaya hu.",
    )

    assert built_prompt.prompt_version == "chat_v1"
    assert "Character Context:" in built_prompt.system_prompt
    assert "Aisha" in built_prompt.system_prompt
    assert "Mahendra" in built_prompt.system_prompt
    assert "User prefers natural Hinglish conversation." in built_prompt.system_prompt
    assert "Last Context Summary" in built_prompt.system_prompt
    assert "Reply in natural Roman Hinglish" in built_prompt.system_prompt
    assert built_prompt.user_message == "Hey Aisha, main 5 din baad aaya hu."
    assert built_prompt.metadata["character_version_id"] == "char_ver_001"


def test_prompt_builder_without_language_context_uses_continuity_language():
    builder = PromptBuilder()

    built_prompt = builder.build_chat_prompt(
        character=FAKE_CHARACTER,
        user_persona=FAKE_USER_PERSONA,
        memory=FAKE_MEMORY_CONTEXT,
        continuity=FAKE_CONTINUITY,
        language=None,
        user_message="Hello",
    )

    assert "Detect the user's language naturally" in built_prompt.system_prompt
    assert built_prompt.metadata["language_mode"] == "hinglish"
