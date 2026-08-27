from ai_core.llm_output import LLMInterpretation
from ai_core.llm_provider import LLMProvider


def interpret_message(
    message: str,
    *,
    provider: LLMProvider,
) -> LLMInterpretation:
    """Interpret a user message through the configured LLM provider."""

    if not isinstance(message, str) or not message.strip():
        raise ValueError("message must be a non-empty string")

    return provider.interpret(message.strip())
