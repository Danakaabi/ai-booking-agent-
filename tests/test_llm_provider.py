from ai_core.entities import ExtractedEntities
from ai_core.intent import Intent
from ai_core.llm_output import LLMInterpretation
from ai_core.llm_provider import LLMProvider


class FakeLLMProvider:
    def interpret(self, message: str) -> LLMInterpretation:
        return LLMInterpretation(
            intent=Intent.BOOK,
            entities=ExtractedEntities(
                service_name="Haircut",
                customer_name="Dana",
            ),
        )


def use_provider(
    provider: LLMProvider,
    message: str,
) -> LLMInterpretation:
    return provider.interpret(message)


def test_fake_provider_can_be_used_through_llm_provider_contract() -> None:
    provider = FakeLLMProvider()

    result = use_provider(
        provider,
        "I want to book a haircut",
    )

    assert result.intent is Intent.BOOK
    assert result.entities.service_name == "Haircut"
    assert result.entities.customer_name == "Dana"
