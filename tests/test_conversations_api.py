from bson import ObjectId
from fastapi.testclient import TestClient

from api.main import app
from database.repositories.conversations import conversations_collection


client = TestClient(app)


def test_create_conversation_endpoint():
    response = client.post("/conversations")

    assert response.status_code == 200

    data = response.json()

    try:
        assert "id" in data
        assert data["state"] == "active"
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