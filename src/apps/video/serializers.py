import datetime

from pydantic import BaseModel


class BaseVideo(BaseModel):
    title: str
    description: str
    file_path: str
    user_id: int

    class Config:
        orm_mode = True


class VideoIn(BaseVideo):
    ...


class VideoOut(BaseVideo):
    id: int
    create_at: datetime.datetime
    in_ban_list: int
