from app.ai_services.parser import ActionParser, EmotionExtractor, ResponseParser


def test_response_parser_parses_valid_json():
    parser = ResponseParser()

    raw = (
        '{"display_text": "Arre Mahendra, 5 din baad aaye ho.", '
        '"action_text": "Aisha smiles softly.", '
        '"emotion": "playful"}'
    )

    parsed = parser.parse(raw)

    assert parsed.display_text == "Arre Mahendra, 5 din baad aaye ho."
    assert parsed.action_text == "Aisha smiles softly."
    assert parsed.emotion == "playful"


def test_response_parser_handles_markdown_json_fence():
    parser = ResponseParser()

    raw = """```json
{"display_text": "Main yahin thi.", "action_text": null, "emotion": "caring"}
```"""

    parsed = parser.parse(raw)

    assert parsed.display_text == "Main yahin thi."
    assert parsed.action_text is None
    assert parsed.emotion == "caring"


def test_response_parser_falls_back_to_raw_text():
    parser = ResponseParser()

    raw = "[playful] Arre, tum finally aa gaye!"

    parsed = parser.parse(raw)

    assert parsed.display_text == "Arre, tum finally aa gaye!"
    assert parsed.emotion == "playful"


def test_response_parser_uses_fallback_for_empty_text():
    parser = ResponseParser()

    parsed = parser.parse("")

    assert parsed.display_text
    assert parsed.emotion == "neutral"


def test_response_parser_normalizes_invalid_emotion():
    parser = ResponseParser()

    raw = '{"display_text": "Hello!", "emotion": "super_magic"}'

    parsed = parser.parse(raw)

    assert parsed.emotion == "neutral"


def test_action_parser_extracts_star_action():
    parser = ActionParser()

    dialogue, action = parser.split_action_and_dialogue(
        display_text="*Aisha smiles softly.* Main yahin hoon."
    )

    assert action == "Aisha smiles softly."
    assert dialogue == "Main yahin hoon."


def test_emotion_extractor_reads_bracket_emotion():
    extractor = EmotionExtractor()

    emotion = extractor.extract(text="[romantic] Tum aa gaye?")

    assert emotion == "romantic"
