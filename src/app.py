import uvicorn
from core.db import database

from core.settings import settings
from core.application import get_app


app = get_app()


@app.on_event("startup")
async def shutdown():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await database.session.close()
    await database.engine.dispose()

if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        reload=settings.RELOAD,
        host=settings.HOST,
        port=settings.PORT
    )
