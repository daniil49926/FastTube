import os

from pydantic import BaseSettings

from core.utils.load_env import load_environ

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_environ(_BASE_DIR)


class __Settings(BaseSettings):
    HOST: str = os.environ.get("APPLICATION_HOST")
    PORT: int = os.environ.get("APPLICATION_PORT")

    RELOAD: bool = True
    PG_DSN: str = os.environ.get("PG_DSN")

    BASE_DIR = _BASE_DIR
    MAX_ATTEMPTS_TO_CONN_TO_PG: int = 5


settings = __Settings()
