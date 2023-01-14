import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from core.db.database import Base


class Video(Base):
    __tablename__ = "Video"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(50), nullable=False)
    description: str = Column(String(500), nullable=False)
    file_path: str = Column(String(1000), nullable=False)
    create_at: datetime.datetime = Column(DateTime, default=datetime.datetime.now())
    user_id: int = Column(Integer, ForeignKey("User.id"))
    in_ban_list: int = Column(Integer, default=0)
