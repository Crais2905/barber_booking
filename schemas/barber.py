from pydantic import BaseModel
from schemas.user import UserPublic


class BarberCreate(BaseModel):
    bio: str
    available_hours: int
    user_id: int

class BarberCreatePublic(BarberCreate):
    id: int

class BarberPublic(BaseModel):
    bio: str
    available_hours: int
    id: int
    user: UserPublic