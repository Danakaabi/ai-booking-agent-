from enum import Enum


class BusinessAction(str, Enum):
    """Business operations that the AI core may request."""

    CREATE_BOOKING = "create_booking"
    GET_SERVICES = "get_services"
    GET_STAFF = "get_staff"
