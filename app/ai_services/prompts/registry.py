from __future__ import annotations

from pathlib import Path


DEFAULT_CHAT_PROMPT_VERSION = "chat_v1"
DEFAULT_SUMMARY_PROMPT_VERSION = "summary_v1"
DEFAULT_FACT_EXTRACTION_PROMPT_VERSION = "fact_extract_v1"

PROMPT_TEMPLATE_ROOT = Path(__file__).parent / "templates"


CHAT_PROMPT_TEMPLATES = {
    "chat_v1": PROMPT_TEMPLATE_ROOT / "system" / "chat_v1.md",
}

SUMMARY_PROMPT_TEMPLATES = {
    "summary_v1": PROMPT_TEMPLATE_ROOT / "summary" / "summary_v1.md",
}

FACT_EXTRACTION_PROMPT_TEMPLATES = {
    "fact_extract_v1": PROMPT_TEMPLATE_ROOT / "extraction" / "fact_extract_v1.md",
}


def get_chat_prompt_path(version: str = DEFAULT_CHAT_PROMPT_VERSION) -> Path:
    try:
        return CHAT_PROMPT_TEMPLATES[version]
    except KeyError as exc:
        raise ValueError(f"Unknown chat prompt version: {version}") from exc


def get_summary_prompt_path(version: str = DEFAULT_SUMMARY_PROMPT_VERSION) -> Path:
    try:
        return SUMMARY_PROMPT_TEMPLATES[version]
    except KeyError as exc:
        raise ValueError(f"Unknown summary prompt version: {version}") from exc


def get_fact_extraction_prompt_path(
    version: str = DEFAULT_FACT_EXTRACTION_PROMPT_VERSION,
) -> Path:
    try:
        return FACT_EXTRACTION_PROMPT_TEMPLATES[version]
    except KeyError as exc:
        raise ValueError(f"Unknown fact extraction prompt version: {version}") from exc
