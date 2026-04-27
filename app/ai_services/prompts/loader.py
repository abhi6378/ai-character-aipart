from __future__ import annotations

from pathlib import Path


class PromptLoader:
    """Loads prompt templates from disk."""

    def load(self, template_path: Path) -> str:
        if not template_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {template_path}")

        return template_path.read_text(encoding="utf-8")
