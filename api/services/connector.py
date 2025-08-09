from fastapi import Depends
from decouple import config
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, delete
from sqlalchemy.orm import selectinload

from db.session import get_session

class Connector:
    def __init__(self, model):
        self.model = model


    async def write_to_db(self, data, session: AsyncSession):
        stmt = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await session.execute(stmt)
        await session.commit()

        return result.scalar()

    
    async def get_object_by_id(
        self, obj_id: int,
        session: AsyncSession,
        selectinload_field: Any = None,
    ):
        stmt = select(self.model).where(self.model.id == obj_id)

        if selectinload_field is not None:
            stmt = stmt.options(selectinload(getattr(self.model, selectinload_field)))

        return await session.scalar(stmt)
    

    async def get_objects(self, session, selectinload_field: Any = None,):
        stmt = select(self.model)

        if selectinload_field is not None:
            stmt = stmt.options(selectinload(getattr(self.model, selectinload_field)))
            
        return await session.scalars(stmt)
    

    async def delete_object_by_id(self, obj_id: int, session: AsyncSession):
        stmt = delete(self.model).where(self.model.id == obj_id).returning(self.model)
        stmt_result = await session.execute(stmt)
        await session.commit()

        return stmt_result.scalar()