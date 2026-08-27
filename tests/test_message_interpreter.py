from ai_core.intent import Intent
from ai_core.llm_errors import LLMProviderError
from ai_core.llm_output import LLMInterpretation
from ai_core.message_interpreter import interpret_user_message


class FakeLLMProvider:
    def interpret(self, message: str) -> LLMInterpretation:
        return LLMInterpretation(
            intent=Intent.BOOK,
            entities={
                "service_name": "Haircut",
                "customer_name": "Dana",
            },
        )


def test_interpret_user_message_uses_deterministic_logic_without_llm():
    intent, entities = interpret_user_message(
        "I want to book Haircut",
        service_names=("Haircut",),
    )

    assert intent is Intent.BOOK
    assert entities.service_name == "Haircut"


def test_interpret_user_message_uses_llm_provider_when_available():
    intent, entities = interpret_user_message(
        "Please arrange something for Dana",
        llm_provider=FakeLLMProvider(),
    )

    assert intent is Intent.BOOK
    assert entities.service_name == "Haircut"
    assert entities.customer_name == "Dana"


class FailingLLMProvider:
    def interpret(self, message: str) -> LLMInterpretation:
        raise LLMProviderError("LLM unavailable")


def test_interpret_user_message_falls_back_when_llm_fails():
    intent, entities = interpret_user_message(
        "I want to book Haircut",
        service_names=("Haircut",),
        llm_provider=FailingLLMProvider(),
    )

    assert intent is Intent.BOOK
    assert entities.service_name == "Haircut"
