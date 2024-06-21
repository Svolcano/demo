from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from settings import SQLALCHEMY_DATABASE_URL


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_maker = None
        self.session = None

    def init_db(self):
        # Database connection parameters...

        # Creating an asynchronous engine
        self.engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

        # Creating an asynchronous session class
        self.session_maker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False
        )
        self.session = async_scoped_session(self.session_maker, scopefunc=current_task)

    async def close(self):
        # Closing the database session...
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()


# Initialize the DatabaseSessionManager
sessionmanager = DatabaseSessionManager()
