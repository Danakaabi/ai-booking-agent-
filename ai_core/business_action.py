from enum import Enum


class BusinessAction(str, Enum):
    """Business operations that the AI core may request."""

    CREATE_BOOKING = "create_booking"
