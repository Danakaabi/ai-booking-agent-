import pytest
from pydantic import ValidationError
from database.repositories.customers import (
    create_customer,
    get_customer_by_id,
    get_all_customers,
)
from api.schemas.customer import Customer
from fastapi.testclient import TestClient

from api.main import app

client =TestClient(app)
def test_create_customer_api():
    response = client.post(
        "/customers",
        json={
            "name": "API Customer",
            "phone": "0500000010",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "API Customer"
    assert data["phone"] == "0500000010"
    assert data["active"] is True
    assert "id" in data



def test_customer_schema_accepts_valid_data():
    customer = Customer(
        name="Dana",
        phone="00000098",
    )

    assert customer.name == "Dana"
    assert customer.phone == "00000098"
    assert customer.active is True



def test_customer_schema_rejects_short_name():
    with pytest.raises(ValidationError):
        Customer(
            name="D",
            phone="0500000000",
        )


def test_create_customer_repository():
    customer = Customer(
        name="Dana",
        phone="0500000000",
    )

    created_customer = create_customer(customer)

    assert created_customer["name"] == "Dana"
    assert created_customer["phone"] == "0500000000"
    assert created_customer["active"] is True
    assert "id" in created_customer

###########################
########################3


def test_get_customer_by_id_repository():
    customer = Customer(
        name="Dana",
        phone="0500000000",
    )

    created_customer = create_customer(customer)

    customer_id = created_customer["id"]

    stored_customer = get_customer_by_id(customer_id)

    assert stored_customer is not None
    assert stored_customer["id"] == customer_id
    assert stored_customer["name"] == "Dana"
    assert stored_customer["phone"] == "0500000000"
    assert stored_customer["active"] is True



def test_get_customer_by_id_repository_not_found():
    customer = get_customer_by_id(
        "000000000000000000000000"
    )

    assert customer is None


##############
def test_get_all_customers_repository_returns_list():
    customer = Customer(
        name="Dana",
        phone="0500000000",
    )

    create_customer(customer)

    customers = get_all_customers()

    assert isinstance(customers, list)
    assert len(customers) > 0
    assert all("id" in customer for customer in customers)


def test_get_all_customers_excludes_inactive_customers():
    inactive_customer = Customer(
        name="Inactive Customer",
        phone="0500000001",
        active=False,
    )

    created_customer = create_customer(inactive_customer)

    customers = get_all_customers()

    customer_ids = [
        customer["id"]
        for customer in customers
    ]

    assert created_customer["id"] not in customer_ids
    assert all(
        customer["active"] is True
        for customer in customers
    )



def test_get_customers_api_returns_active_customers():
    active_customer = Customer(
        name="Active API Customer",
        phone="0500000011",
        active=True,
    )

    inactive_customer = Customer(
        name="Inactive API Customer",
        phone="0500000012",
        active=False,
    )

    create_customer(active_customer)
    create_customer(inactive_customer)

    response = client.get("/customers")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert all(customer["active"] is True for customer in data)

    names = [customer["name"] for customer in data]

    assert "Active API Customer" in names
    assert "Inactive API Customer" not in names




def test_get_customer_by_id_api():
    customer = Customer(
        name="Customer By ID",
        phone="0500000013",
    )

    created_customer = create_customer(customer)
    customer_id = created_customer["id"]

    response = client.get(f"/customers/{customer_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == customer_id
    assert data["name"] == "Customer By ID"
    assert data["phone"] == "0500000013"
    assert data["active"] is True


def test_get_customer_by_id_api_not_found():
    response = client.get(
        "/customers/000000000000000000000000"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"