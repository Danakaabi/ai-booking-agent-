from datetime import datetime

from ai_core.context_preparation import prepare_booking_context
from ai_core.entities import ExtractedEntities
from ai_core.resolved_entities import ResolvedEntities


def test_prepare_booking_context_combines_ai_data():
    booking_datetime = datetime(2026, 8, 24, 17, 0)

    entities = ExtractedEntities(
        service_name="Haircut",
        customer_name="Dana",
        customer_phone="0501234567",
        booking_datetime=booking_datetime,
        staff_name="Sara",
    )

    resolved = ResolvedEntities(
        service_id="service-123",
        staff_id="staff-123",
    )

    context = prepare_booking_context(
        entities,
        resolved,
    )

    assert context.service_id == "service-123"
    assert context.customer_name == "Dana"
    assert context.customer_phone == "0501234567"
    assert context.booking_datetime == booking_datetime
    assert context.staff_id == "staff-123"


def test_prepare_booking_context_preserves_partial_data():
    entities = ExtractedEntities(
        customer_phone="0501234567",
    )

    resolved = ResolvedEntities()

    context = prepare_booking_context(
        entities,
        resolved,
    )

    assert context.service_id is None
    assert context.customer_name is None
    assert context.customer_phone == "0501234567"
    assert context.booking_datetime is None
    assert context.staff_id is None
