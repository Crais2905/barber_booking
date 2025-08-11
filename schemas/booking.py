from pydantic import BaseModel, field_validator
from datetime import datetime, time, date

from schemas.barber import BarberPublic
from schemas.user import UserBase
from schemas.services import ServicesPublic


class BookingCreate(BaseModel):
    user_id: int
    barber_id: int
    service_id: int
    date: str
    time: str


    @field_validator("date")
    def date_validator(cls, value):
        try:
            return datetime.strptime(str(value), f"%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Дата повинна бути у форматі DD-MM-YYYY")
        
    
    @field_validator("time")
    def time_validator(cls, value):
        try:
            return datetime.strptime(str(value), "%H:%M").time()
        except ValueError:
            raise ValueError("Час повинен бути у форматі HH:MM")
        

class BookingPublic(BaseModel):
    id: int
    user: UserBase
    barber: BarberPublic
    service: ServicesPublic
    date: date
    time: time