from typing import List
from datetime import timedelta, datetime

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.booking import BookingCRUD
from api.services.barber import BarberCRUD
from api.services.services import ServicesCRUD
from schemas.booking import BookingCreate, BookingPublic
from db.session import get_session
from db.models import Booking, User
from utils.booking import check_barber_time, check_booking_intersection
from auth.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=BookingPublic, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    booking_crud: BookingCRUD = Depends(BookingCRUD),
    barber_crud: BarberCRUD = Depends(BarberCRUD),
    services_crud: ServicesCRUD = Depends(ServicesCRUD),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):  
    barber = await barber_crud.get_object_by_id(booking_data.barber_id, session)
    service = await services_crud.get_object_by_id(booking_data.service_id, session)

    if not barber or not service:
        raise HTTPException(status_code=400, detail="Barber or Service with given id does not exist")
    
    barber_bookings = await booking_crud.get_barber_bookings_by_date(barber.id, booking_data.date, session)
    booking_start = datetime.combine(datetime.today(), booking_data.time)
    booking_end = (booking_start + timedelta(minutes=service.duration_minute)).time()

    if not (
        check_barber_time(barber, booking_data.time, booking_end) 
        and check_booking_intersection(list(barber_bookings), booking_data.time, booking_end, service)
    ):
        raise HTTPException(status_code=400, detail="This time is already booked.")
    
    booking_data.user_id = current_user.id
    return await booking_crud.create_booking(booking_data, session)


@router.get("/", response_model=List[BookingPublic])
async def get_all_bookings(
    booking_crud: BookingCRUD = Depends(BookingCRUD),
    session: AsyncSession = Depends(get_session)
):
    return await booking_crud.get_objects(session, ["user", "barber", "service"])


@router.get("/{booking_id}/", response_model=BookingPublic, status_code=status.HTTP_200_OK)
async def get_booking(
    booking_id: int,
    booking_crud: BookingCRUD = Depends(BookingCRUD),
    session: AsyncSession = Depends(get_session)
):
    return await booking_crud.get_object_by_id(booking_id, session)


@router.delete("/{booking_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    booking_crud: BookingCRUD = Depends(BookingCRUD),
    session: AsyncSession = Depends(get_session)
):
    return await booking_crud.delete_object_by_id(booking_id, session)