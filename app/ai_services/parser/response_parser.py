from __future__ import annotations

import json
import re
from typing import Any

from app.ai_services.contracts import ParsedAssistantMessage
from app.ai_services.parser.action_parser import ActionParser
from app.ai_services.parser.emotion_extractor import EmotionExtractor
from app.ai_services.parser.fallback_handler import FallbackHandler


class ResponseParser:
    """
    Parses raw LLM output into a clean assistant message.

    Expected preferred format:
    {
        "display_text": "...",
        "action_text": "...",
        "emotion": "playful"
    }

    The parser also supports fallback handling for malformed output.
    """

    _JSON_FENCE_PATTERN = re.compile(
        r"```(?:json)?\s*(.*?)\s*```",
        re.DOTALL | re.IGNORECASE,
    )

    def __init__(
        self,
        emotion_extractor: EmotionExtractor | None = None,
        action_parser: ActionParser | None = None,
        fallback_handler: FallbackHandler | None = None,
    ) -> None:
        self._emotion_extractor = emotion_extractor or EmotionExtractor()
        self._action_parser = action_parser or ActionParser()
        self._fallback_handler = fallback_handler or FallbackHandler()

    def parse(self, raw_text: str | None) -> ParsedAssistantMessage:
        if not raw_text or not raw_text.strip():
            return self._fallback_handler.build_fallback(raw_text=raw_text)

        cleaned_raw = raw_text.strip()

        parsed_json = self._try_parse_json(cleaned_raw)
        if parsed_json is not None:
            return self._parse_json_payload(parsed_json, cleaned_raw)

        # Last-resort fallback: treat raw text as dialogue.
        emotion = self._emotion_extractor.extract(text=cleaned_raw)
        display_text = self._remove_leading_emotion_tag(cleaned_raw)
        display_text, action_text = self._action_parser.split_action_and_dialogue(
            display_text=display_text,
            action_text=None,
        )

        if not display_text:
            return self._fallback_handler.build_fallback(raw_text=raw_text)

        return ParsedAssistantMessage(
            display_text=display_text,
            action_text=action_text,
            emotion=emotion,
            raw_text=raw_text,
        )

    def _parse_json_payload(
        self,
        payload: dict[str, Any],
        raw_text: str,
    ) -> ParsedAssistantMessage:
        display_text = str(payload.get("display_text") or "").strip()
        action_text = payload.get("action_text")
        emotion = self._emotion_extractor.extract(
            emotion=str(payload.get("emotion") or ""),
            text=display_text,
        )

        if not display_text:
            return self._fallback_handler.build_fallback(raw_text=raw_text)

        display_text, action_text = self._action_parser.split_action_and_dialogue(
            display_text=display_text,
            action_text=str(action_text).strip() if action_text else None,
        )

        return ParsedAssistantMessage(
            display_text=display_text,
            action_text=action_text,
            emotion=emotion,
            raw_text=raw_text,
        )

    def _try_parse_json(self, text: str) -> dict[str, Any] | None:
        possible_json = self._extract_json_from_markdown_fence(text)

        try:
            parsed = json.loads(possible_json)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None

        return parsed

    def _extract_json_from_markdown_fence(self, text: str) -> str:
        match = self._JSON_FENCE_PATTERN.search(text)
        if match:
            return match.group(1).strip()

        return text

    def _remove_leading_emotion_tag(self, text: str) -> str:
        return re.sub(r"^\s*\[[a-zA-Z_ -]+\]\s*", "", text).strip()
