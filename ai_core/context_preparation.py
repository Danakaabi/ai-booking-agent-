from ai_core.entities import ExtractedEntities
from ai_core.resolved_entities import ResolvedEntities
from api.schemas.conversation import BookingContext


def prepare_booking_context(
    entities: ExtractedEntities,
    resolved: ResolvedEntities,
) -> BookingContext:
    """Prepare AI-derived data for the existing conversation booking context."""

    return BookingContext(
        service_id=resolved.service_id,
        customer_name=entities.customer_name,
        customer_phone=entities.customer_phone,
        booking_datetime=entities.booking_datetime,
        staff_id=resolved.staff_id,
    )
