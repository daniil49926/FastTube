from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.future import select

from core.db import database
from core.db.exception_models import Message404
from apps.user.serializers import UserIn, UserOut
from apps.user.models import User


v1 = APIRouter()


@v1.get("/users/{uid}", response_model=UserOut, responses={404: {"model": Message404}})
async def get_user(uid: int) -> User:
    async with database.session.begin():
        user = await database.session.execute(
            select(User).where(User.id == uid, User.is_active == 1)
        )
    user = user.scalars().one_or_none()
    return user if user else JSONResponse(status_code=404, content={"message": "User not found"})


@v1.post("/users", response_model=UserOut)
async def add_user(user: UserIn) -> User:
    user = User(**user.dict())
    async with database.session.begin():
        database.session.add(user)
    return user
