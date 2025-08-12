from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from schemas.barber import BarberCreate, BarberPublic 
# from auth.dependencies import get_current_user
from api.services.barber import BarberCRUD
from db.session import get_session
from db.models import Barber, User

router = APIRouter()


@router.post("/", response_model=BarberPublic, status_code=status.HTTP_201_CREATED)
async def create_barber(
    barber_data: BarberCreate,
    barber_crud: BarberCRUD = Depends(BarberCRUD),
    session: AsyncSession = Depends(get_session)
):
    return await barber_crud.write_to_db(barber_data, session)


@router.get("/", response_model=List[BarberPublic], status_code=status.HTTP_200_OK)
async def get_barbers(
    barber_crud: BarberCRUD = Depends(BarberCRUD),
    session: AsyncSession = Depends(get_session),
):
    return await barber_crud.get_objects(session)


@router.get("/{barber_id}/", response_model=BarberPublic, status_code=status.HTTP_200_OK)
async def get_barber(
    barber_id: int, 
    barber_crud: BarberCRUD = Depends(BarberCRUD),
    session: AsyncSession = Depends(get_session),
):
    return await barber_crud.get_object_by_id(barber_id, session)


@router.delete("/{barber_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_barber(
    barber_id: int, 
    barber_crud: BarberCRUD = Depends(BarberCRUD),
    session: AsyncSession = Depends(get_session),
):
   return await barber_crud.delete_object_by_id(barber_id, session)