from builtins import object
from uuid import uuid4

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.future import select

from apps.auth.utils import get_current_active_user
from apps.user.models import User
from apps.video.models import Video
from apps.video.serializers import VideoOut
from apps.video.utils import write_video
from core.db.database import get_db
from core.db.exception_models import Message418
from core.settings import settings

v1 = APIRouter()


@v1.post("/video/", response_model=VideoOut, responses={418: {"model": Message418}})
async def create_video(
    background_task: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    current_user: User = Depends(get_current_active_user),
    session: object = Depends(get_db),
) -> Video:
    async with session.begin():
        user_id = await session.execute(select(current_user.id))
    uid = user_id.scalars().first()
    file_path = (
        f"{settings.BASE_DIR}/media/{uid}_{uuid4()}.{file.filename.split('.')[-1]}"
    )

    if file.content_type == "video/mp4":
        background_task.add_task(write_video, file_name=file_path, file=file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")

    new_v = Video(
        title=title, description=description, file_path=file_path, user_id=uid
    )
    async with session.begin():
        session.add(new_v)
    return new_v


@v1.get("/video/list-video/", response_model=list[VideoOut])
async def list_of_videos(session: object = Depends(get_db)) -> list[Video]:
    async with session.begin():
        videos = await session.execute(select(Video))
    videos = videos.scalars().all()
    return videos
