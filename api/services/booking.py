from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, delete

from .connector import Connector
from db.models import Service, User, Barber, Booking
from schemas.booking import BookingCreate

class BookingCRUD(Connector):
    def __init__(self):
        super().__init__(Booking)


    async def create_booking(
        self, 
        booking_data: BookingCreate,
        session: AsyncSession
    ):
        stmt = insert(self.model).values(booking_data.model_dump()).returning(self.model)
        result = await session.execute(stmt)
        await session.commit()

        return result.scalar()
    
    # async def get_all_bookings(
    #     self, 
    #     session: AsyncSession,
    #     offset: int = 0,
    #     limit: int = 10,
    # ):
    #     booking = 