import pytest

from ai_core.intent import Intent
from ai_core.llm_interpreter import interpret_message
from ai_core.llm_output import LLMInterpretation


class FakeLLMProvider:
    def interpret(self, message: str) -> LLMInterpretation:
        return LLMInterpretation(
            intent=Intent.GET_SERVICES,
        )


def test_interpret_message_uses_provider() -> None:
    result = interpret_message(
        "What services do you offer?",
        provider=FakeLLMProvider(),
    )

    assert result.intent is Intent.GET_SERVICES


def test_interpret_message_rejects_blank_message() -> None:
    with pytest.raises(
        ValueError,
        match="message must be a non-empty string",
    ):
        interpret_message(
            "   ",
            provider=FakeLLMProvider(),
        )
