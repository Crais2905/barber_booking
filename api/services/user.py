from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from api.services.connector import Connector
from db.models import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCRUD(Connector):
    def __init__(self):
        super().__init__(User)


    async def write_to_db(self, data, session):
        hashed_password = password_context.hash(data.password)
        db_user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            hashed_password=hashed_password
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user
        

    async def get_user_by_email(
        self,
        email: str, 
        session: AsyncSession,            
    ):
        stmt = select(self.model).where(User.email == email)
        return await session.scalar(stmt)
    

    async def verify_password(self, password: str, hashed_password: str):
        return password_context.verify(password, hashed_password)