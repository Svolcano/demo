import logging
import time
from logging.handlers import RotatingFileHandler
from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from database.manager import get_db, get_user_by_name, sessionmanager
from models.schema import TokenData

logger = logging.getLogger(__name__)


def init_logger() -> None:
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d]-%(funcName)s- %(levelname)s: %(message)s"
    )
    log_file_handler = RotatingFileHandler(
        filename="logs/api_log.log", maxBytes=10485760, backupCount=2, encoding="utf8"
    )
    log_file_handler.setFormatter(formatter)
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log.addHandler(log_file_handler)


def init() -> None:
    init_logger()
    sessionmanager.init_db()


def to_dict(obj: Any) -> Dict:
    d = {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
    if "password" in d:
        del d["password"]
    return d


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> dict:
    logger.info("")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        logger.info("payload: %s", payload)
        exp: str = payload.get("exp")
        if exp:
            if exp < int(time.time()):
                raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_name(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return to_dict(user)
