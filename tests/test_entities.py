from datetime import datetime

import pytest
from pydantic import ValidationError

from ai_core.entities import ExtractedEntities


def test_extracted_entities_can_be_partial():
    entities = ExtractedEntities(
        service_name="Haircut",
    )

    assert entities.service_name == "Haircut"
    assert entities.customer_name is None
    assert entities.customer_phone is None
    assert entities.booking_datetime is None
    assert entities.staff_name is None


def test_extracted_entities_accept_complete_data():
    booking_datetime = datetime(2026, 8, 24, 17, 0)

    entities = ExtractedEntities(
        service_name="Haircut",
        customer_name="Dana",
        customer_phone="0500000000",
        booking_datetime=booking_datetime,
        staff_name="Sara",
    )

    assert entities.service_name == "Haircut"
    assert entities.customer_name == "Dana"
    assert entities.customer_phone == "0500000000"
    assert entities.booking_datetime == booking_datetime
    assert entities.staff_name == "Sara"


def test_extracted_entities_reject_invalid_customer_name():
    with pytest.raises(ValidationError):
        ExtractedEntities(
            customer_name="D",
        )

from ai_core.entity_extractor import extract_entities


def test_extract_entities_recognizes_known_service():
    entities = extract_entities(
        "I want to book a Haircut",
        service_names=("Haircut", "Hair Coloring"),
    )

    assert entities.service_name == "Haircut"


def test_extract_entities_recognizes_known_staff():
    entities = extract_entities(
        "I want an appointment with Sara",
        staff_names=("Sara", "Nora"),
    )

    assert entities.staff_name == "Sara"


def test_extract_entities_recognizes_service_case_insensitively():
    entities = extract_entities(
        "I want a haircut",
        service_names=("Haircut",),
    )

    assert entities.service_name == "Haircut"


def test_extract_entities_extracts_and_normalizes_phone():
    entities = extract_entities(
        "My phone number is 050 123 4567"
    )

    assert entities.customer_phone == "0501234567"


def test_extract_entities_can_extract_multiple_entities():
    entities = extract_entities(
        "Book Haircut with Sara. My phone is 050-123-4567",
        service_names=("Haircut",),
        staff_names=("Sara",),
    )

    assert entities.service_name == "Haircut"
    assert entities.staff_name == "Sara"
    assert entities.customer_phone == "0501234567"


def test_extract_entities_returns_empty_entities_for_unknown_message():
    entities = extract_entities(
        "Hello, how are you?",
        service_names=("Haircut",),
        staff_names=("Sara",),
    )

    assert entities.service_name is None
    assert entities.customer_name is None
    assert entities.customer_phone is None
    assert entities.booking_datetime is None
    assert entities.staff_name is None


def test_extract_entities_does_not_match_known_name_inside_larger_word():
    entities = extract_entities(
        "I need a chair",
        service_names=("Hair",),
    )

    assert entities.service_name is None


def test_extract_entities_prefers_longest_known_name():
    entities = extract_entities(
        "I want Hair Coloring",
        service_names=("Hair", "Hair Coloring"),
    )

    assert entities.service_name == "Hair Coloring"
