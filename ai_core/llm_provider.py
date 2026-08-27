from typing import Protocol

from ai_core.llm_output import LLMInterpretation


class LLMProvider(Protocol):
    """Contract implemented by LLM providers."""

    def interpret(self, message: str) -> LLMInterpretation:
        """Interpret a user message into validated structured output."""
        ...
