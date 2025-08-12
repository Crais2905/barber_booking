from pydantic import BaseModel, field_validator
from datetime import time, datetime

from schemas.user import UserPublic


class BarberCreate(BaseModel):
    bio: str
    work_end_time: str 
    user_id: int

    @field_validator("work_end_time")
    def time_validator(cls, value):
        try:
            return datetime.strptime(str(value), "%H:%M").time()
        except ValueError:
            raise ValueError("Час повинен бути у форматі HH:MM")


class BarberPublic(BaseModel):
    bio: str
    work_end_time: time
    id: int
    user: UserPublic