from bson import ObjectId
from fastapi.testclient import TestClient
from datetime import datetime
from database.repositories.bookings import bookings_collection
from api.main import app
from database.repositories.conversations import conversations_collection
from database.repositories.messages import messages_collection

client = TestClient(app)


def test_create_conversation_endpoint():
    response = client.post("/conversations")

    assert response.status_code == 200

    data = response.json()

    try:
        assert "id" in data
        assert data["state"] == "active"
        assert data["active_intent"] is None
        assert "booking_context" in data
        assert data["booking_context"] == {
            "service_id": None,
            "customer_name": None,
            "customer_phone": None,
            "booking_datetime": None,
            "staff_id": None,
        }

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(data["id"])}
        )


def test_get_existing_conversation_endpoint():
    create_response = client.post("/conversations")
    created = create_response.json()

    try:
        response = client.get(
            f"/conversations/{created['id']}"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == created["id"]
        assert data["state"] == "active"
        assert "booking_context" in data

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(created["id"])}
        )


def test_get_missing_conversation_endpoint():
    response = client.get(
        "/conversations/000000000000000000000000"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"


def test_add_message_to_existing_conversation_endpoint():
    create_response = client.post("/conversations")
    conversation = create_response.json()

    try:
        response = client.post(
            f"/conversations/{conversation['id']}/messages",
            json={
                "role": "user",
                "content": "I want to book a haircut",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["conversation_id"] == conversation["id"]
        assert data["role"] == "user"
        assert data["content"] == "I want to book a haircut"
        assert "id" in data
        assert "created_at" in data

    finally:
        messages_collection.delete_many(
            {"conversation_id": conversation["id"]}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )

def test_add_message_to_missing_conversation_endpoint():
    response = client.post(
        "/conversations/000000000000000000000000/messages",
        json={
            "role": "user",
            "content": "Hello",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"


def test_get_conversation_history_endpoint():
    create_response = client.post("/conversations")
    conversation = create_response.json()

    try:
        client.post(
            f"/conversations/{conversation['id']}/messages",
            json={
                "role": "user",
                "content": "Hello",
            },
        )

        client.post(
            f"/conversations/{conversation['id']}/messages",
            json={
                "role": "assistant",
                "content": "Hi, how can I help?",
            },
        )

        response = client.get(
            f"/conversations/{conversation['id']}/messages"
        )

        assert response.status_code == 200

        history = response.json()

        assert len(history) == 3

        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Hello"

        assert history[1]["role"] == "assistant"
        assert (
            history[1]["content"]
            == "I could not understand your request. Please try again."
        )

        assert history[2]["role"] == "assistant"
        assert history[2]["content"] == "Hi, how can I help?"

    finally:
        messages_collection.delete_many(
            {"conversation_id": conversation["id"]}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )



def test_get_missing_conversation_history_endpoint():
    response = client.get(
        "/conversations/000000000000000000000000/messages"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"



def test_update_booking_context_endpoint():
    create_response = client.post("/conversations")
    conversation = create_response.json()

    try:
        response = client.patch(
            f"/conversations/{conversation['id']}/booking-context",
            json={
                "service_id": "service-123",
                "customer_name": "Dana",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["booking_context"]["service_id"] == "service-123"
        assert data["booking_context"]["customer_name"] == "Dana"
        assert data["booking_context"]["customer_phone"] is None

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_update_booking_context_for_missing_conversation_endpoint():
    response = client.patch(
        "/conversations/000000000000000000000000/booking-context",
        json={
            "customer_name": "Dana",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"


def test_create_booking_from_missing_conversation_endpoint():
    response = client.post(
        "/conversations/000000000000000000000000/bookings"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"

def test_create_booking_from_incomplete_context_endpoint():
    create_response = client.post("/conversations")
    conversation = create_response.json()

    try:
        response = client.post(
            f"/conversations/{conversation['id']}/bookings"
        )

        assert response.status_code == 422
        assert (
            response.json()["detail"]
            == "Booking context is incomplete"
        )

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )



def test_create_booking_from_complete_context_endpoint():
    create_response = client.post("/conversations")
    conversation = create_response.json()
    customer_name = "Conversation API Booking Test"

    bookings_collection.delete_many(
        {"customer_name": customer_name}
    )

    try:
        context_response = client.patch(
            f"/conversations/{conversation['id']}/booking-context",
            json={
                "service_id": "6a779ed59b6b145fcfe108ab",
                "customer_name": customer_name,
                "customer_phone": "0500000400",
                "booking_datetime": "2026-08-20T10:00:00",
            },
        )

        assert context_response.status_code == 200

        response = client.post(
            f"/conversations/{conversation['id']}/bookings"
        )

        assert response.status_code == 200

        booking = response.json()

        assert booking["customer_name"] == customer_name
        assert booking["service_id"] == "6a779ed59b6b145fcfe108ab"
        assert "id" in booking

    finally:
        bookings_collection.delete_many(
            {"customer_name": customer_name}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_create_booking_from_conversation_returns_service_not_found():
    create_response = client.post("/conversations")
    conversation = create_response.json()

    try:
        context_response = client.patch(
            f"/conversations/{conversation['id']}/booking-context",
            json={
                "service_id": "000000000000000000000000",
                "customer_name": "Conversation Missing Service API Test",
                "customer_phone": "0500000500",
                "booking_datetime": "2026-08-20T10:00:00",
            },
        )

        assert context_response.status_code == 200

        response = client.post(
            f"/conversations/{conversation['id']}/bookings"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Service not found"

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )

def test_user_message_updates_conversation_context_through_ai():
    create_response = client.post("/conversations")
    conversation = create_response.json()

    try:
        response = client.post(
            f"/conversations/{conversation['id']}/messages",
            json={
                "role": "user",
                "content": "I want to book Haircut",
            },
        )

        assert response.status_code == 200

        conversation_response = client.get(
            f"/conversations/{conversation['id']}"
        )

        assert conversation_response.status_code == 200

        updated_conversation = conversation_response.json()

        assert (
            updated_conversation["booking_context"]["service_id"]
            is not None
        )

    finally:
        messages_collection.delete_many(
            {"conversation_id": conversation["id"]}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_assistant_message_does_not_trigger_ai_context_update():
    create_response = client.post("/conversations")
    conversation = create_response.json()

    try:
        response = client.post(
            f"/conversations/{conversation['id']}/messages",
            json={
                "role": "assistant",
                "content": "I want to book Haircut",
            },
        )

        assert response.status_code == 200

        conversation_response = client.get(
            f"/conversations/{conversation['id']}"
        )

        assert conversation_response.status_code == 200

        updated_conversation = conversation_response.json()

        assert (
            updated_conversation["booking_context"]["service_id"]
            is None
        )

    finally:
        messages_collection.delete_many(
            {"conversation_id": conversation["id"]}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )
