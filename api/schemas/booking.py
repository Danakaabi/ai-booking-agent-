from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    service_id: str = Field(..., min_length=1)
    customer_name: str = Field(..., min_length=2, max_length=100)
    customer_phone: str = Field(..., min_length=8, max_length=20)
    booking_datetime: datetime
    status: Literal["confirmed", "cancelled"] = "confirmed"


class BookingUpdate(BaseModel):
    service_id: str | None = Field(default=None, min_length=1)
    customer_name: str | None = Field(default=None, min_length=2, max_length=100)
    customer_phone: str | None = Field(default=None, min_length=8, max_length=20)
    booking_datetime: datetime | None = None
    