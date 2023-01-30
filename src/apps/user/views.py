from builtins import object

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.future import select

from apps.auth.utils import get_current_active_user
from apps.user.models import User
from apps.user.serializers import UserIn, UserInDB, UserOut
from apps.user.utils import send_verify_on_email
from core.db.database import get_db
from core.db.exception_models import Message404
from core.redisdb.redisdb import get_redis_conn
from core.security.auth_security import get_password_hash

v1 = APIRouter()


@v1.get("/users/{uid}", response_model=UserOut, responses={404: {"model": Message404}})
async def get_user(uid: int, session=Depends(get_db)) -> User:
    async with session.begin():
        user = await session.execute(
            select(User).where(User.id == uid, User.is_active == 1)
        )
    user = user.scalars().one_or_none()
    return (
        user
        if user
        else JSONResponse(status_code=404, content={"message": "User not found"})
    )


@v1.post("/users", response_model=UserOut)
async def add_user(
    user: UserIn, background_task: BackgroundTasks, session: object = Depends(get_db)
) -> User:
    hash_pass = get_password_hash(user.password)
    new_user = UserInDB(
        name=user.name,
        surname=user.surname,
        username=user.username,
        gender=user.gender,
        email=user.email,
        hashed_password=hash_pass,
    )
    user = User(**new_user.dict())
    async with session.begin():
        session.add(user)
    background_task.add_task(
        send_verify_on_email, email=user.email, username=user.name, uid=user.id
    )
    return user


@v1.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@v1.get("/verify-email/{uid}/{link_body}")
async def confirm_email(uid: int, link_body: str, session: object = Depends(get_db)):
    redis_ = get_redis_conn()
    if not redis_:
        return JSONResponse(
            status_code=500, content={"message": "Server error plz try letter"}
        )
    op_rez = redis_.get(f"{uid}").decode("utf-8")
    if not op_rez:
        return JSONResponse(status_code=404, content={"message": "Unable to confirm"})
    if op_rez == link_body:
        async with session.begin():
            user = await session.execute(select(User).where(User.id == uid))
        user = user.scalars().one_or_none()
        user.is_active = 1
        await session.commit()
        return user
    return JSONResponse(status_code=403, content={"message": "Unable to confirm"})
