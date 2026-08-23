import pytest
from pydantic import ValidationError

from ai_core.decision import AIDecision, NextAction
from ai_core.entities import ExtractedEntities
from ai_core.intent import Intent
from ai_core.missing_fields import MissingField


def test_ai_decision_accepts_structured_result():
    entities = ExtractedEntities(
        service_name="Haircut",
        customer_phone="0501234567",
    )

    decision = AIDecision(
        intent=Intent.BOOK,
        entities=entities,
        missing_fields=(MissingField.BOOKING_DATETIME,),
        next_action=NextAction.ASK_USER,
    )

    assert decision.intent == Intent.BOOK
    assert decision.entities.service_name == "Haircut"
    assert decision.entities.customer_phone == "0501234567"
    assert decision.missing_fields == (MissingField.BOOKING_DATETIME,)
    assert decision.next_action == NextAction.ASK_USER


def test_ai_decision_uses_empty_entities_by_default():
    decision = AIDecision(
        intent=Intent.UNKNOWN,
        next_action=NextAction.UNKNOWN,
    )

    assert decision.entities == ExtractedEntities()
    assert decision.missing_fields == ()


def test_ai_decision_rejects_invalid_intent():
    with pytest.raises(ValidationError):
        AIDecision(
            intent="not_a_real_intent",
            next_action=NextAction.UNKNOWN,
        )


def test_ai_decision_rejects_invalid_next_action():
    with pytest.raises(ValidationError):
        AIDecision(
            intent=Intent.BOOK,
            next_action="not_a_real_action",
        )



def test_ai_decision_rejects_invalid_missing_field():
    with pytest.raises(ValidationError):
        AIDecision(
            intent=Intent.BOOK,
            missing_fields=("not_a_real_field",),
            next_action=NextAction.ASK_USER,
        )
