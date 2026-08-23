from enum import Enum


class Intent(str, Enum):
    """Supported user intents understood by the AI core."""

    BOOK = "book"
    RESCHEDULE = "reschedule"
    CANCEL = "cancel"
    CHECK_AVAILABILITY = "check_availability"
    GET_SERVICES = "get_services"
    GET_STAFF = "get_staff"
    UNKNOWN = "unknown"
