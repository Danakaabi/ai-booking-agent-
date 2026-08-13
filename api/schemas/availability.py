from datetime import time
from enum import Enum

from pydantic import BaseModel, model_validator


class DayOfWeek(str, Enum):
    sunday = "sunday"
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"


class Availability(BaseModel):
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