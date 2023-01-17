from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.future import select

from apps.user.models import User
from core.db import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

v1 = APIRouter()


@v1.get("/token")
async def read_token(_token: str = Depends(oauth2_scheme)):
    return {"token": _token}


@v1.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with database.session.begin():
        user = await database.session.execute(
            select(User).where(
                User.username == form_data.username and User.is_active == 1
            )
        )
    user = user.scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def fake_decode_token(token):
    return await get_user(token)


async def get_user(username: str):
    async with database.session.begin():
        user = await database.session.execute(
            select(User).where(User.username == username and User.is_active == 1)
        )
    user = user.scalars().one_or_none()
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password
