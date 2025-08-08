from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Optional
from decouple import config


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=int(config("ACCESS_TOKEN_EXPIRE_MINUTES")))
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config("SECRET_KEY"), algorithm=config("ALGORITHM"))