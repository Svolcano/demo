import logging
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from database.manager import get_db, get_repo
from models.schema import LoginInfo, Token, UserScore
from tools.token_utils import authenticate_user, create_access_token
from tools.utils import get_current_user, init, to_dict

logger = logging.getLogger()


init()


app = FastAPI()

logger.info("start ...")


@app.get("/ping")
async def ping(request: Request):
    logger.info("")
    return "pong"


@app.post("/user/score", dependencies=[Depends(get_current_user)])
async def add_score_endpoint(
    score: UserScore, db: AsyncSession = Depends(get_db)
) -> dict:
    logger.info("update user score.")
    score_data = score.model_dump()
    logger.info("data get {}".format(score_data))
    repo = get_repo(db)
    user_id = score_data["user_id"]
    user = await repo.get_user(user_id)
    if not user:
        logger.error("user with id %s not exists", user_id)
        raise HTTPException(status_code=400, detail="Bad Request")
    logger.info("Get user {}".format(user))
    if "score" in score_data:
        if user.role == "staff":
            user.score += score_data["score"]
            user.last_login = datetime.now()
            await repo.update_user(user)
            return to_dict(user)
        elif user.role == "admin":
            if "score_modifier" in score_data:
                user.score += score_data["score"] * score_data["score_modifier"]
                user.last_login = datetime.now()
                await repo.update_user(user)
                return to_dict(user)
    user.last_login = datetime.now()
    await repo.update_user(user)
    return to_dict(user)


@app.post("/token")
async def login_for_access_token(
    login_data: LoginInfo, db: AsyncSession = Depends(get_db)
) -> Token:
    logger.info(login_data.model_dump())
    user = await authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    logger.info("user is : %s", user.username)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
