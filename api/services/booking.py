from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from sqlalchemy.orm import selectinload

from .connector import Connector
from db.models import Booking
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
    
    
    async def get_barber_bookings_by_date(
        self,
        barber_id: int,
        date: date,
        session: AsyncSession
    ):
        stmt = (select(self.model)
            .options(selectinload(Booking.service))
            .where(Booking.barber_id == barber_id)
            .where(Booking.date == date)
        )

        return await session.scalars(stmt)