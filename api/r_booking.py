from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.booking import BookingCRUD
from schemas.booking import BookingCreate, BookingPublic
from db.session import get_session
from db.models import Booking
# from auth.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=BookingCreate, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    booking_crud: BookingCRUD = Depends(BookingCRUD),
    session: AsyncSession = Depends(get_session)
):
    return await booking_crud.create_booking(booking_data, session)


@router.get("/", response_model=List[BookingPublic])
async def get_all_bookings(
    booking_crud: BookingCRUD = Depends(BookingCRUD),
    session: AsyncSession = Depends(get_session)
):
    return await booking_crud.get_objects(session, ["user", "barber", "service"])