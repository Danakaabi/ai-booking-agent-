import pytest
from pydantic import ValidationError

from api.schemas.conversation import BookingContext, MessageCreate, MessageRole


def test_message_create_accepts_valid_user_message():
    message = MessageCreate(
        role=MessageRole.USER,
        content="I want to book a haircut",
    )

    assert message.role == MessageRole.USER
    assert message.content == "I want to book a haircut"


def test_message_create_rejects_empty_content():
    with pytest.raises(ValidationError):
        MessageCreate(
            role=MessageRole.USER,
            content="",
        )


def test_message_create_rejects_invalid_role():
    with pytest.raises(ValidationError):
        MessageCreate(
            role="invalid-role",
            content="Hello",
        )


def test_booking_context_can_be_empty():
    context = BookingContext()

    assert context.service_id is None
    assert context.customer_name is None
    assert context.customer_phone is None
    assert context.booking_datetime is None
    assert context.staff_id is None


def test_booking_context_accepts_partial_booking_data():
    context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
    )

    assert context.service_id == "service-123"
    assert context.customer_name == "Dana"
    assert context.customer_phone is None
    assert context.booking_datetime is None
    assert context.staff_id is None

def test_booking_context_rejects_invalid_partial_data():
    with pytest.raises(ValidationError):
        BookingContext(
            customer_name="D",
        )