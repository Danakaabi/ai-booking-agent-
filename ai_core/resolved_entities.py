from pydantic import BaseModel, Field


class ResolvedEntities(BaseModel):
    """Internal entity identifiers resolved from extracted names."""

    service_id: str | None = Field(default=None, min_length=1)
    staff_id: str | None = Field(default=None, min_length=1)
