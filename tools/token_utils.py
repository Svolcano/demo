from datetime import datetime, timedelta
from typing import Optional, Union

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from database.manager import get_user_by_name
from database.tables import TUser


def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> Optional[TUser]:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = await get_user_by_name(db, username)
    if not pwd_context.verify(password, user.password):
        return None
    return user


def create_access_token(
    data: dict,
    expires_delta: Union[timedelta, None] = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
