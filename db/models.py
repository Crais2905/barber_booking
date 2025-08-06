from typing import Optional
from datetime import datetime

from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Boolean, Text, DateTime, Date, Time


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[int] = mapped_column(Integer, nullable=False)
    is_barber: Mapped[bool] = mapped_column(Boolean)
    barber: Mapped[Optional['Barber']] = relationship("Barber", back_populates="user")


class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    duration_minute: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


class Barber(Base):
    __tablename__ = 'barber' 

    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    available_hours: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), unique=True)
    user: Mapped[User] = relationship(back_populates='barber')


class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    barber_id: Mapped[int] = mapped_column(Integer, ForeignKey('barber.id'))
    service_id: Mapped[int] = mapped_column(Integer, ForeignKey('service.id'))
    created_at: Mapped[datetime] =  mapped_column(DateTime, default=datetime.now)
    date: Mapped[datetime] = mapped_column(Date)
    time: Mapped[datetime] = mapped_column(Time)
