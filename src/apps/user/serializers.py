import uuid

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import BaseModel


class ExtendsUser(BaseModel):
    name: str
    surname: str
    nickname: str


class UserRead(BaseUser[uuid.UUID], ExtendsUser):
    pass


class UserCreate(BaseUserCreate, ExtendsUser):
    pass


class UserUpdate(BaseUserUpdate, ExtendsUser):
    pass
