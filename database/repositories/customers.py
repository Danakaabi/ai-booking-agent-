from api.schemas.customer import  Customer
from database.connection import database
from bson import ObjectId

customers_collection = database["customers"]


def create_customer(customer: Customer) -> dict:
    customer_data = customer.model_dump()

    result = customers_collection.insert_one(customer_data)

    customer_data.pop("_id", None)
    customer_data["id"] = str(result.inserted_id)

    return customer_data


def get_customer_by_id(customer_id: str) -> dict | None:
    if not ObjectId.is_valid(customer_id):
        return None

    customer = customers_collection.find_one(
        {"_id": ObjectId(customer_id)}
    )

    if customer is None:
        return None

    customer["id"] = str(customer.pop("_id"))

    return customer


#########
def get_all_customers() -> list[dict]:
    customers = list(
        customers_collection.find(
            {"active": True}
        )
    )

    for customer in customers:
        customer["id"] = str(customer.pop("_id"))

    return customers