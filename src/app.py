import uvicorn

from fastapi import Depends

from builtins import object
from core.application import get_app
from core.db import database
from core.db.database import get_db
from core.settings import settings

app = get_app()


@app.on_event("startup")
async def shutdown():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown(session: object = Depends(get_db)):
    await session.close()
    await database.engine.dispose()


if __name__ == "__main__":
    uvicorn.run(
        app="app:app", reload=settings.RELOAD, host=settings.HOST, port=settings.PORT
    )
