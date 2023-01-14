import datetime

from sqlalchemy import Column, String, Integer, DateTime
from core.db.database import Base


class User(Base):
    __tablename__ = 'User'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    surname: str = Column(String, nullable=False)
    gender: int = Column(Integer, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    created_at: datetime.datetime = Column(DateTime, default=datetime.datetime.now())
    is_active: int = Column(Integer, nullable=False, default=1)
