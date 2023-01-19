from builtins import object
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates

from apps.video.utils import stream_video
from core.db.database import get_db
from core.settings import settings

v1 = APIRouter()

templates_dir = settings.TEMPLATE_DIR
templates = Jinja2Templates(directory=templates_dir)


@v1.get("/{vid}", response_class=HTMLResponse)
async def player(request: Request, vid: int):
    return templates.TemplateResponse("player.html", {"request": request, "path": vid})


@v1.get("/get_video/{vid}")
async def get_video_for_player(request: Request, vid: int, session: object = Depends(get_db)) -> StreamingResponse:
    file, status_code, content_length, headers = await stream_video(request, vid, session)
    response = StreamingResponse(file, media_type="video/mp4", status_code=status_code)
    response.headers.update(
        {
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            **headers,
        }
    )
    return response
