from  fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.user import UserCRUD
from db.session import get_session
from auth.tokens import decode_token


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
    user_crud: UserCRUD = Depends(UserCRUD),
):  
    try:
        token = request.cookies.get("access_token")
        payload = decode_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await user_crud.get_user_by_email(email, session)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user