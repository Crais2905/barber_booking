from pydantic import BaseModel, Field, EmailStr
# from typing import Optional



class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str 


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPublic(UserBase):
    id: int 
    is_barber: bool
    # barber: Optional[Barber]r