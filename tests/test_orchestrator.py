from datetime import datetime

from ai_core.business_action import BusinessAction
from ai_core.decision import NextAction
from ai_core.intent import Intent
from ai_core.orchestrator import process_message
from api.schemas.conversation import BookingContext
from ai_core.missing_fields import MissingField

def test_process_message_combines_new_entities_with_existing_context():
    current_context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
        booking_datetime=datetime(2026, 8, 24, 17, 0),
    )

    decision, context_update = process_message(
        "I want to book, my phone is 0501234567",
        current_context=current_context,
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[],
    )

    assert decision.intent == Intent.BOOK
    assert decision.entities.customer_phone == "0501234567"
    assert decision.missing_fields == ()
    assert decision.next_action == NextAction.CALL_TOOL


def test_process_message_asks_user_when_context_is_still_incomplete():
    current_context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
    )

    decision, context_update = process_message(
        "I want to book, my phone is 0501234567",
        current_context=current_context,
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[],
    )

    assert decision.intent == Intent.BOOK
    assert decision.entities.customer_phone == "0501234567"
    assert decision.missing_fields == (
        MissingField.BOOKING_DATETIME,
    )
    assert decision.next_action == NextAction.ASK_USER


def test_process_message_resolves_service_name_during_full_flow():
    current_context = BookingContext(
        customer_name="Dana",
        customer_phone="0501234567",
        booking_datetime=datetime(2026, 8, 24, 17, 0),
    )

    decision, context_update = process_message(
        "I want to book Haircut",
        current_context=current_context,
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[],
    )

    assert decision.intent == Intent.BOOK
    assert decision.entities.service_name == "Haircut"
    assert decision.missing_fields == ()
    assert decision.next_action == NextAction.CALL_TOOL
    assert decision.business_action == BusinessAction.CREATE_BOOKING

    assert context_update.service_id == "service-123"
    assert context_update.customer_name is None
    assert context_update.customer_phone is None
    assert context_update.booking_datetime is None
    assert context_update.staff_id is None


def test_process_message_returns_unknown_decision_for_unknown_intent():
    decision, context_update = process_message(
        "Hello there",
        current_context=BookingContext(),
        services_by_id={},
        staff_members=[],
    )

    assert decision.intent == Intent.UNKNOWN
    assert decision.missing_fields == ()
    assert decision.next_action == NextAction.UNKNOWN


def test_process_message_continues_active_booking_intent():
    current_context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
    )

    decision, context_update = process_message(
        "0501234567",
        current_context=current_context,
        services_by_id={},
        staff_members=[],
        active_intent=Intent.BOOK,
    )

    assert decision.intent == Intent.BOOK
    assert decision.next_action == NextAction.ASK_USER
    assert context_update.customer_phone == "0501234567"


def test_process_message_preserves_deterministic_behavior_without_llm():
    decision, context_update = process_message(
        "I want to book Haircut",
        current_context=BookingContext(
            customer_name="Dana",
            customer_phone="0501234567",
            booking_datetime=datetime(2026, 8, 24, 17, 0),
        ),
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[],
    )

    assert decision.intent == Intent.BOOK
    assert decision.entities.service_name == "Haircut"
    assert decision.business_action == BusinessAction.CREATE_BOOKING
    assert decision.next_action == NextAction.CALL_TOOL
    assert context_update.service_id == "service-123"


from ai_core.llm_output import LLMInterpretation


class FakeOrchestratorLLMProvider:
    def interpret(self, message: str) -> LLMInterpretation:
        return LLMInterpretation(
            intent=Intent.BOOK,
            entities={
                "service_name": "Haircut",
                "customer_name": "Dana",
                "customer_phone": "0501234567",
                "booking_datetime": datetime(2026, 8, 24, 17, 0),
            },
        )


def test_process_message_can_use_llm_interpretation():
    decision, context_update = process_message(
        "Arrange my appointment please",
        current_context=BookingContext(),
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[],
        llm_provider=FakeOrchestratorLLMProvider(),
    )

    assert decision.intent == Intent.BOOK
    assert decision.entities.customer_name == "Dana"
    assert decision.entities.customer_phone == "0501234567"
    assert decision.entities.service_name == "Haircut"
    assert context_update.service_id == "service-123"
    assert decision.next_action == NextAction.CALL_TOOL


from ai_core.llm_errors import LLMProviderError


class FailingOrchestratorLLMProvider:
    def interpret(self, message: str) -> LLMInterpretation:
        raise LLMProviderError("LLM unavailable")


def test_process_message_falls_back_when_llm_provider_fails():
    decision, context_update = process_message(
        "I want to book Haircut",
        current_context=BookingContext(
            customer_name="Dana",
            customer_phone="0501234567",
            booking_datetime=datetime(2026, 8, 24, 17, 0),
        ),
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[],
        llm_provider=FailingOrchestratorLLMProvider(),
    )

    assert decision.intent == Intent.BOOK
    assert decision.entities.service_name == "Haircut"
    assert decision.business_action == BusinessAction.CREATE_BOOKING
    assert decision.next_action == NextAction.CALL_TOOL
    assert context_update.service_id == "service-123"
