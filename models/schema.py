from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserScore(BaseModel):
    user_id: str
    score_modifier: Optional[float] = 0
    score: float


class TokenData(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginInfo(BaseModel):
    username: str
    password: str


class User(BaseModel):
    user_id: str
    role: str
    score: float
    last_login: datetime
    username: Optional[str]
