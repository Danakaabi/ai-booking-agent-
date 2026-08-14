from fastapi import APIRouter, HTTPException

from api.schemas.customer import Customer
from database.repositories.customers import (
    create_customer,
    get_all_customers,
    get_customer_by_id,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post("")
def create_customer_route(customer: Customer) -> dict:
    return create_customer(customer)

@router.get("")
def get_customers_route() -> list[dict]:
    return get_all_customers()



@router.get("/{customer_id}")
def get_customer_route(customer_id: str) -> dict:
    customer = get_customer_by_id(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer