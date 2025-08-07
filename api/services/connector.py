from fastapi import Depends
from contextlib import asynccontextmanager
from decouple import config

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import insert, delete

from db.session import get_session

class Connector:
    def __init__(self, model):
        self.model = model


    async def write_to_db(self, data, session: AsyncSession):
        stmt = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await session.execute(stmt)
        await session.commit()

        return result.scalar()

    
    async def get_object_by_id(self, obj_id: int, session: AsyncSession):
        stmt = select(self.model).where(self.model.id == obj_id)
        return await session.scalar(stmt)
    

    async def get_objects(self, session):
        stmt = select(self.model)
        return await session.scalars(stmt)
    

    async def delete_object_by_id(self, obj_id: int, session: AsyncSession):
        stmt = delete(self.model).where(self.model.id == obj_id).returning(self.model)
        stmt_result = await session.execute(stmt)
        await session.commit()

        return stmt_result.scalar()