import pytest
from pydantic import ValidationError

from ai_core.intent import Intent
from ai_core.llm_output import LLMInterpretation


def test_llm_interpretation_accepts_supported_intent() -> None:
    result = LLMInterpretation(intent=Intent.BOOK)

    assert result.intent is Intent.BOOK
    assert result.entities.service_name is None
    assert result.entities.customer_name is None
    assert result.entities.customer_phone is None
    assert result.entities.booking_datetime is None
    assert result.entities.staff_name is None


def test_llm_interpretation_validates_entities() -> None:
    result = LLMInterpretation(
        intent=Intent.CHECK_AVAILABILITY,
        entities={
            "service_name": "Haircut",
            "staff_name": "Sara",
        },
    )

    assert result.intent is Intent.CHECK_AVAILABILITY
    assert result.entities.service_name == "Haircut"
    assert result.entities.staff_name == "Sara"


def test_llm_interpretation_rejects_unknown_intent_value() -> None:
    with pytest.raises(ValidationError):
        LLMInterpretation(intent="invented_action")
