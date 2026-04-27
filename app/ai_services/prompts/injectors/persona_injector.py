from __future__ import annotations

from app.ai_services.contracts import UserPersonaContext


class PersonaInjector:
    """Renders user persona details into a prompt section."""

    def render(self, persona: UserPersonaContext) -> str:
        display_name = persona.preferred_name or persona.display_name or "the user"

        parts = [
            f"User Display Name: {display_name}",
            f"Preferred Language: {persona.preferred_language}",
        ]

        if persona.persona_summary:
            parts.append(f"User Persona Summary: {persona.persona_summary}")

        return "\n".join(parts)
