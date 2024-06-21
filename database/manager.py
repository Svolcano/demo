import asyncio
import logging
import sys
from typing import AsyncIterator, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.append("/Users/scw/Documents/wp/python_exercise/mianshi/")
from database.db_base import Base, sessionmanager
from database.tables import TUser
from models import schema

logger = logging.getLogger(__name__)


class Repo:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def fake_get_user(self, user_id: str) -> Optional[schema.User]:
        if user_id == "1":
            return schema.User(
                user_id="1", role="staff", score=0, last_login="2024-06-19 11:41:28"
            )
        elif user_id == "0":
            return schema.User(
                user_id="0", role="admin", score=100, last_login="2024-06-19 11:41:28"
            )
        return None

    async def get_user(self, user_id) -> Optional[TUser]:
        logger.info("get_user")
        result = await self.session.execute(
            select(TUser).where(TUser.user_id == user_id)
        )
        row = result.scalar()
        if row:
            return row
        else:
            return None

    async def update_user(self, user: TUser) -> None:
        logger.info("update_user")
        u = await self.session.execute(
            select(TUser).where(TUser.user_id == user.user_id)
        )
        u.socre = user.score
        u.last_login = user.last_login
        await self.session.commit()


async def get_user_by_name(db: AsyncSession, username: str) -> Optional[TUser]:
    logger.info("get_user")
    result = await db.execute(select(TUser).where(TUser.username == username))
    one = result.scalar()
    if one:
        return one
    else:
        return None


async def get_db() -> AsyncIterator[AsyncSession]:
    session = sessionmanager.session()
    logger.info("******* db connection open ....")
    if session is None:
        raise Exception("DatabaseSessionManager is not initialized")
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        # Closing the session after use...
        logger.info("******* db connection will close....")
        await session.close()


def get_repo(db_session: AsyncSession) -> AsyncIterator[Repo]:
    return Repo(db_session)


if __name__ == "__main__":
    from datetime import datetime

    from tools.token_utils import get_password_hash

    async def async_main() -> None:
        sessionmanager.init_db()
        engine = sessionmanager.engine
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async for db_session in get_db():
            async with db_session.begin():
                db_session.add_all(
                    [
                        TUser(
                            user_id="1",
                            username="staff001",
                            role="staff",
                            score=0,
                            last_login=datetime.now(),
                            password=get_password_hash("123456"),
                        ),
                        TUser(
                            user_id="0",
                            username="boss",
                            role="admin",
                            score=100,
                            last_login=datetime.now(),
                            password=get_password_hash("123456"),
                        ),
                    ]
                )

    asyncio.run(async_main())
