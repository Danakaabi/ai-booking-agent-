from pydantic import BaseModel


class Service(BaseModel):
    name: str
    duration_minutes: int
    price: float
    active: bool