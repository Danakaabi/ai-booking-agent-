class LLMError(Exception):
    """Base exception for LLM integration failures."""


class LLMProviderError(LLMError):
    """Raised when the external LLM provider fails."""


class LLMOutputValidationError(LLMError):
    """Raised when the LLM returns invalid structured output."""
