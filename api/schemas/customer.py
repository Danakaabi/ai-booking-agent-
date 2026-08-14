from pydantic import BaseModel, Field


class Customer(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=8, max_length=20)
    active: bool = True