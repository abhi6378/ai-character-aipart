from __future__ import annotations

from app.ai_services.contracts import ContinuityContext


class ContinuityInjector:
    """Renders user-character continuity state into a prompt section."""

    def render(self, continuity: ContinuityContext) -> str:
        parts = [
            f"Current Tone State: {continuity.tone_state or 'unknown'}",
            f"Relationship Label: {continuity.relationship_label or 'new'}",
            f"Relationship Score: {continuity.relationship_score}",
            f"Language Mode: {continuity.language_mode}",
        ]

        if continuity.last_interaction_at:
            parts.append(f"Last Interaction At: {continuity.last_interaction_at}")

        if continuity.last_context_summary:
            parts.append(
                f"Last Context Summary: {continuity.last_context_summary}"
            )

        return "\n".join(parts)
