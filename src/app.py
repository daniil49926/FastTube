import uvicorn

from core.application import get_app
from core.settings import settings

app = get_app()

if __name__ == "__main__":
    uvicorn.run(
        app="app:app", reload=settings.RELOAD, host=settings.HOST, port=settings.PORT
    )
