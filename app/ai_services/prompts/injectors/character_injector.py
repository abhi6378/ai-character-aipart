from __future__ import annotations

from app.ai_services.contracts import CharacterContext


class CharacterInjector:
    """Renders character details into a prompt section."""

    def render(self, character: CharacterContext) -> str:
        parts = [
            f"Character Name: {character.name}",
            f"Character Description: {character.description}",
            f"Personality: {character.personality}",
        ]

        if character.speaking_style:
            parts.append(f"Speaking Style: {character.speaking_style}")

        if character.greeting_message:
            parts.append(f"Greeting Style Reference: {character.greeting_message}")

        if character.system_prompt:
            parts.append(f"Character System Notes: {character.system_prompt}")

        return "\n".join(parts)
