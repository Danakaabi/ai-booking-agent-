from datetime import datetime

from pydantic import BaseModel, Field


class ExtractedEntities(BaseModel):
    """Structured information extracted from a user message."""

    service_name: str | None = Field(default=None, min_length=1)
    customer_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    customer_phone: str | None = Field(
        default=None,
        min_length=8,
        max_length=20,
    )
    booking_datetime: datetime | None = None
    staff_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
