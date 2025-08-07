from pydantic import BaseModel, Field


class ServicesCreate(BaseModel):
    name: str = Field(max_length=128)
    description: str
    duration_minute: int
    price: int


class ServicesPublic(ServicesCreate):
    id: int