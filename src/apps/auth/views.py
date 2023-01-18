import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select

from apps.auth.utils import get_oauth2_scheme
from apps.user.models import User
from core.db import database
from core.security.auth_security import create_access_token, verify_password
from core.settings import settings

v1 = APIRouter()

oauth2_scheme = get_oauth2_scheme()


@v1.get("/token")
async def read_token(_token: str = Depends(oauth2_scheme)):
    return {"token": _token}


@v1.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    async with database.session.begin():
        user = await database.session.execute(
            select(User).where(
                User.username == form_data.username and User.is_active == 1
            )
        )
    user = user.scalars().one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}