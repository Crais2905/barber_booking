from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.services import ServicesCRUD
from schemas.services import ServicesCreate, ServicesPublic
from db.session import get_session

router = APIRouter()


@router.post("/", response_model=ServicesPublic, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: ServicesCreate,
    service_crud: ServicesCRUD = Depends(ServicesCRUD),
    session: AsyncSession = Depends(get_session)
):
    return await service_crud.write_to_db(service_data, session)


@router.get("/", response_model=List[ServicesPublic], status_code=status.HTTP_200_OK)
async def get_services(
    service_crud: ServicesCRUD = Depends(ServicesCRUD),
    session: AsyncSession = Depends(get_session)
):
    return await service_crud.get_objects(session)


@router.get("/{service_id}/", response_model=ServicesPublic, status_code=status.HTTP_200_OK)
async def get_service(
    service_id: int, 
    service_crud: ServicesCRUD = Depends(ServicesCRUD),
    session: AsyncSession = Depends(get_session)
):
    return await service_crud.get_object_by_id(service_id, session)


@router.delete("/{service_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: int,
    service_crud: ServicesCRUD = Depends(ServicesCRUD),
    session: AsyncSession = Depends(get_session)
):
    return await service_crud.delete_object_by_id(service_id, session)
