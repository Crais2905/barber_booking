from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserPublic, UserLogin
from auth.tokens import create_access_token
from api.services.user import UserCRUD
from db.session import get_session

router = APIRouter()


@router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
    user_crud: UserCRUD = Depends(UserCRUD),
):
    existing_user = await user_crud.get_user_by_email(user_data.email, session)

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    return await user_crud.write_to_db(user_data, session)


@router.post("/login/")
async def login(
    login_data: UserLogin,
    response: Response,
    user_crud: UserCRUD = Depends(UserCRUD),
    session: AsyncSession = Depends(get_session)
):
    user = await user_crud.get_user_by_email(login_data.email, session)

    if not user or not await user_crud.verify_password(password=login_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.email})
    response.set_cookie("access_token", access_token)

    return {
        "access_token": access_token
    }

