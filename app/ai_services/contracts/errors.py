class AIServiceError(Exception):
    """Base exception for AI service errors."""


class AIContractError(AIServiceError):
    """Raised when AI request/response contract is invalid."""


class AIProviderError(AIServiceError):
    """Raised when LLM or TTS provider fails."""


class AIParsingError(AIServiceError):
    """Raised when model response cannot be parsed safely."""
