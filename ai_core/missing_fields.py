from enum import Enum


class MissingField(str, Enum):
    """Booking-context fields that may be required by an AI workflow."""

    SERVICE_ID = "service_id"
    CUSTOMER_NAME = "customer_name"
    CUSTOMER_PHONE = "customer_phone"
    BOOKING_DATETIME = "booking_datetime"
    STAFF_ID = "staff_id"
