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

    BASE_DIR: str = _BASE_DIR
    TEMPLATE_DIR: str = _BASE_DIR + "/templates"
    MAX_ATTEMPTS_TO_CONN_TO_PG: int = 5

    CRYPTO_KEY: bytes = os.environ.get("CRYPTO_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720

    MAIL_USER: str = os.environ.get("MAIL_USER")
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASS")

    REDIS_HOST: str = os.environ.get("REDIS_HOST")
    REDIS_LOGIN: str = os.environ.get("REDIS_LOGIN")
    REDIS_PWD: str = os.environ.get("REDIS_PWD")
    REDIS_PORT: int = os.environ.get("REDIS_PORT")

    TESTING: bool = os.environ.get("TESTING")


settings = __Settings()
