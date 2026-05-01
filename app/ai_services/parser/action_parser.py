from __future__ import annotations

import re


class ActionParser:
    """
    Extracts short action text from assistant output.

    Supported examples:
    - *Aisha smiles softly.* Main yahin hoon.
    - [Aisha smiles softly.] Main yahin hoon.
    """

    _STAR_ACTION_PATTERN = re.compile(r"^\s*\*(.*?)\*\s*", re.DOTALL)
    _BRACKET_ACTION_PATTERN = re.compile(r"^\s*\[(.*?)\]\s*", re.DOTALL)

    def split_action_and_dialogue(
        self,
        *,
        display_text: str,
        action_text: str | None = None,
    ) -> tuple[str, str | None]:
        cleaned_text = display_text.strip()

        if action_text:
            return cleaned_text, action_text.strip()

        star_match = self._STAR_ACTION_PATTERN.match(cleaned_text)
        if star_match:
            action = star_match.group(1).strip()
            dialogue = cleaned_text[star_match.end():].strip()
            return dialogue, action

        bracket_match = self._BRACKET_ACTION_PATTERN.match(cleaned_text)
        if bracket_match:
            possible_action = bracket_match.group(1).strip()

            # If bracket looks like emotion only, do not treat it as action.
            if len(possible_action.split()) > 1:
                dialogue = cleaned_text[bracket_match.end():].strip()
                return dialogue, possible_action

        return cleaned_text, None
