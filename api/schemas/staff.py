from pydantic import BaseModel, Field


class Staff(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=8, max_length=20)
    service_ids: list[str] = Field(default_factory=list)
    active: bool = True