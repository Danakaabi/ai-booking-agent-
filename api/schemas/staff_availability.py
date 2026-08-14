from datetime import time

from pydantic import BaseModel, model_validator

from api.schemas.availability import DayOfWeek


class StaffAvailability(BaseModel):
    staff_id: str
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    active: bool = True

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError(
                "end_time must be later than start_time"
            )

        return self