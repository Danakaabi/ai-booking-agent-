import pytest

from ai_core.decision import AIDecision, NextAction
from ai_core.intent import Intent
from ai_core.missing_fields import MissingField
from ai_core.response_generator import generate_response


def test_generate_response_asks_for_service():
    decision = AIDecision(
        intent=Intent.BOOK,
        missing_fields=(MissingField.SERVICE_ID,),
        next_action=NextAction.ASK_USER,
    )

    response = generate_response(decision)

    assert response == "Which service would you like to book?"


def test_generate_response_asks_for_customer_phone():
    decision = AIDecision(
        intent=Intent.BOOK,
        missing_fields=(MissingField.CUSTOMER_PHONE,),
        next_action=NextAction.ASK_USER,
    )

    response = generate_response(decision)

    assert response == "What phone number should I use for the booking?"


def test_generate_response_uses_first_missing_field():
    decision = AIDecision(
        intent=Intent.BOOK,
        missing_fields=(
            MissingField.CUSTOMER_NAME,
            MissingField.CUSTOMER_PHONE,
        ),
        next_action=NextAction.ASK_USER,
    )

    response = generate_response(decision)

    assert response == "What name should I use for the booking?"


def test_generate_response_rejects_ask_user_without_missing_fields():
    decision = AIDecision(
        intent=Intent.BOOK,
        next_action=NextAction.ASK_USER,
    )

    with pytest.raises(
        ValueError,
        match="ASK_USER decision requires at least one missing field",
    ):
        generate_response(decision)


def test_generate_response_handles_unknown_decision():
    decision = AIDecision(
        intent=Intent.UNKNOWN,
        next_action=NextAction.UNKNOWN,
    )

    response = generate_response(decision)

    assert response == "I could not understand your request. Please try again."
