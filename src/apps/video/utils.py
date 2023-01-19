from pathlib import Path
from typing import IO, Generator
from builtins import object

import aiofiles
from fastapi import HTTPException, UploadFile
from sqlalchemy.future import select
from starlette.requests import Request

from apps.video.models import Video


async def write_video(file_name: str, file: UploadFile) -> None:
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)


def ranged(
    file: IO, start: int = 0, stop: int = None, chunk_size: int = 10000
) -> Generator[bytes, None, None]:
    spent = 0

    file.seek(start)
    while True:
        chunk_length = min(chunk_size, stop - start - spent) if stop else chunk_size
        if chunk_length <= 0:
            break
        data = file.read(chunk_length)
        if not data:
            break
        spent += chunk_length
        yield data

    if hasattr(file, "close"):
        file.close()


async def stream_video(
        request: Request,
        video_id: int,
        session: object
) -> tuple:
    async with session.begin():
        video_path = await session.execute(
            select(Video.file_path).where(Video.id == video_id)
        )
    video_path = video_path.scalars().one_or_none()
    if not video_path:
        raise HTTPException(status_code=404, detail="Video not found")

    video = Path(video_path).open("rb")
    video_size = Path(video_path).stat().st_size
    content_length = video_size
    status_code = 200
    headers = {}
    content_range = request.headers.get("range")

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split("=")[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + "-").split("-"))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(video_size - 1, int(range_end)) if range_end else video_size - 1
        content_length = (range_end - range_start) + 1
        video = ranged(video, start=range_start, stop=range_end + 1)
        status_code = 206
        headers["Content-Range"] = f"bytes {range_start}-{range_end}/{video_size}"

    return video, status_code, content_length, headers
