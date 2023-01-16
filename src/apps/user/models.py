from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, Integer, String

from core.db.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "User"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    surname: str = Column(String, nullable=False)
    nickname: str = Column(String, nullable=False, unique=True)
