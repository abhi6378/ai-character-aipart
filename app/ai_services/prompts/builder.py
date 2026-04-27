from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.ai_services.contracts import (
    CharacterContext,
    ContinuityContext,
    LanguageContext,
    MemoryContext,
    UserPersonaContext,
)
from app.ai_services.prompts.injectors import (
    CharacterInjector,
    ContinuityInjector,
    LanguageInjector,
    MemoryInjector,
    PersonaInjector,
)
from app.ai_services.prompts.loader import PromptLoader
from app.ai_services.prompts.registry import (
    DEFAULT_CHAT_PROMPT_VERSION,
    get_chat_prompt_path,
)


class BuiltPrompt(BaseModel):
    """Final prompt object produced by PromptBuilder."""

    prompt_version: str
    system_prompt: str
    user_message: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class PromptBuilder:
    """
    Builds prompts for the character chat flow.

    This class does not call the LLM.
    It only converts context into a clean prompt.
    """

    def __init__(
        self,
        loader: PromptLoader | None = None,
        character_injector: CharacterInjector | None = None,
        persona_injector: PersonaInjector | None = None,
        memory_injector: MemoryInjector | None = None,
        continuity_injector: ContinuityInjector | None = None,
        language_injector: LanguageInjector | None = None,
    ) -> None:
        self._loader = loader or PromptLoader()
        self._character_injector = character_injector or CharacterInjector()
        self._persona_injector = persona_injector or PersonaInjector()
        self._memory_injector = memory_injector or MemoryInjector()
        self._continuity_injector = continuity_injector or ContinuityInjector()
        self._language_injector = language_injector or LanguageInjector()

    def build_chat_prompt(
        self,
        *,
        character: CharacterContext,
        user_persona: UserPersonaContext,
        memory: MemoryContext,
        continuity: ContinuityContext,
        user_message: str,
        language: LanguageContext | None = None,
        prompt_version: str = DEFAULT_CHAT_PROMPT_VERSION,
    ) -> BuiltPrompt:
        template_path = get_chat_prompt_path(prompt_version)
        template = self._loader.load(template_path)

        system_prompt = template.format(
            character_section=self._character_injector.render(character),
            persona_section=self._persona_injector.render(user_persona),
            memory_section=self._memory_injector.render(memory),
            continuity_section=self._continuity_injector.render(continuity),
            language_section=self._language_injector.render(language),
        )

        return BuiltPrompt(
            prompt_version=prompt_version,
            system_prompt=system_prompt.strip(),
            user_message=user_message.strip(),
            metadata={
                "character_id": character.character_id,
                "character_version_id": character.character_version_id,
                "prompt_version": prompt_version,
                "memory_count": len(memory.selected_memories),
                "recent_message_count": len(memory.recent_messages),
                "language_mode": (
                    language.response_language
                    if language is not None
                    else continuity.language_mode
                ),
            },
        )
