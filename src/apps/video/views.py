from uuid import uuid4
from builtins import object

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

# from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.future import select

from apps.auth.utils import get_current_active_user
from apps.user.models import User
from apps.video.models import Video
from apps.video.serializers import VideoOut
from apps.video.utils import write_video
from core.db.database import get_db
from core.db.exception_models import Message418  # , Message404
from core.settings import settings

v1 = APIRouter()


# @v1.get("/video/{vid}", response_model=VideoOut, responses={404: {"model": Message404}})
# async def get_video(vid: int) -> StreamingResponse | JSONResponse:
#     async with database.session.begin():
#         video_path = await database.session.execute(
#             select(Video.file_path).where(Video.id == vid, Video.in_ban_list == 0)
#         )
#     video_path = video_path.scalars().one_or_none()
#     if not video_path:
#         return JSONResponse(status_code=404, content={"message": "Video not found"})
#     video = await read_video(video_path)
#     return StreamingResponse(video, media_type="video/mp4")


@v1.post("/video/", response_model=VideoOut, responses={418: {"model": Message418}})
async def create_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    current_user: User = Depends(get_current_active_user),
    session: object = Depends(get_db)
) -> Video:
    async with session.begin():
        user_id = await session.execute(select(current_user.id))
    uid = user_id.scalars().first()
    file_path = (
        f"{settings.BASE_DIR}/media/{uid}_{uuid4()}.{file.filename.split('.')[-1]}"
    )

    if file.content_type == "video/mp4":
        await write_video(file_path, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")

    new_v = Video(
        title=title, description=description, file_path=file_path, user_id=uid
    )
    async with session.begin():
        session.add(new_v)
    return new_v
