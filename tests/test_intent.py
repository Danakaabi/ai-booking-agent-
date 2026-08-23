from ai_core.intent import Intent


def test_intent_values_are_stable():
    assert Intent.BOOK.value == "book"
    assert Intent.RESCHEDULE.value == "reschedule"
    assert Intent.CANCEL.value == "cancel"
    assert Intent.CHECK_AVAILABILITY.value == "check_availability"
    assert Intent.GET_SERVICES.value == "get_services"
    assert Intent.GET_STAFF.value == "get_staff"
    assert Intent.UNKNOWN.value == "unknown"

from ai_core.intent_detector import detect_intent


def test_detect_intent_recognizes_english_booking():
    assert detect_intent("I want to book an appointment") == Intent.BOOK


def test_detect_intent_recognizes_arabic_booking():
    assert detect_intent("أبغى أحجز موعد") == Intent.BOOK


def test_detect_intent_recognizes_cancellation_case_insensitively():
    assert detect_intent("I want to CANCEL my appointment") == Intent.CANCEL


def test_detect_intent_recognizes_reschedule():
    assert detect_intent("I want to reschedule my appointment") == Intent.RESCHEDULE


def test_detect_intent_recognizes_availability():
    assert detect_intent("What slots are available?") == Intent.CHECK_AVAILABILITY


def test_detect_intent_recognizes_services():
    assert detect_intent("What services do you offer?") == Intent.GET_SERVICES


def test_detect_intent_recognizes_staff():
    assert detect_intent("Who are the staff?") == Intent.GET_STAFF


def test_detect_intent_returns_unknown_for_unrecognized_message():
    assert detect_intent("Hello there") == Intent.UNKNOWN


def test_detect_intent_returns_unknown_for_empty_message():
    assert detect_intent("   ") == Intent.UNKNOWN


def test_detect_intent_prioritizes_cancel_over_booking_word():
    assert detect_intent("I want to cancel my booking") == Intent.CANCEL
