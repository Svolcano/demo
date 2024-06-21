from sqlalchemy import Column, DateTime, Float, String

from database.db_base import Base


class TUser(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    role = Column(String)
    score = Column(Float)
    last_login = Column(DateTime)
    username = Column(String, unique=True)
    password = Column(String)
