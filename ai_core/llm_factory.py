from ai_core.llm_config import load_llm_config
from ai_core.llm_provider import LLMProvider
from ai_core.openai_provider import OpenAILLMProvider


def create_llm_provider() -> LLMProvider | None:
    """Create the configured LLM provider when LLM is enabled."""

    config = load_llm_config()

    if not config.enabled:
        return None

    return OpenAILLMProvider(
        api_key=config.api_key,
        model=config.model,
        timeout_seconds=config.timeout_seconds,
    )
