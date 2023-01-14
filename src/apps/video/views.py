import aiofiles
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.future import select

from apps.video.models import Video
from apps.video.serializers import VideoOut
from core.db import database
from core.db.exception_models import Message404
from core.settings import settings

v1 = APIRouter()


@v1.get("/video/{vid}", response_model=VideoOut, responses={404: {"model": Message404}})
async def get_video(vid: int) -> Video:
    async with database.session.begin():
        video = await database.session.execute(
            select(Video).where(Video.id == vid, Video.in_ban_list != 0)
        )
    video = video.scalars().one_or_none()
    return (
        video
        if video
        else JSONResponse(status_code=404, content={"message": "User not found"})
    )


@v1.post("/video/", response_model=VideoOut)
async def create_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
) -> Video:
    file_path = f"{settings.BASE_DIR}/media/{file.filename}"
    await write_video(file_path, file)
    new_v = Video(title=title, description=description, file_path=file_path, user_id=1)
    async with database.session.begin():
        database.session.add(new_v)
    return new_v


async def write_video(file_name: str, file: UploadFile) -> None:
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)
