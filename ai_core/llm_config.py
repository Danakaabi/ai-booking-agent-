import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    """Runtime configuration for the OpenAI LLM provider."""

    enabled: bool
    api_key: str = ""
    model: str = ""
    timeout_seconds: float = 10.0


def load_llm_config() -> LLMConfig:
    """Load and validate LLM configuration from environment variables."""

    enabled_raw = os.getenv("LLM_ENABLED", "false").strip().lower()

    if enabled_raw not in {"true", "false"}:
        raise ValueError("LLM_ENABLED must be true or false")

    enabled = enabled_raw == "true"

    if not enabled:
        return LLMConfig(enabled=False)

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()
    timeout_raw = os.getenv("OPENAI_TIMEOUT_SECONDS", "10").strip()

    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    if not model:
        raise ValueError("OPENAI_MODEL is required")

    try:
        timeout_seconds = float(timeout_raw)
    except ValueError as exc:
        raise ValueError(
            "OPENAI_TIMEOUT_SECONDS must be a valid number"
        ) from exc

    if timeout_seconds <= 0:
        raise ValueError(
            "OPENAI_TIMEOUT_SECONDS must be greater than zero"
        )

    return LLMConfig(
        enabled=True,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
    )
