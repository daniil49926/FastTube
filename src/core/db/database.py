from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.settings import settings

DATABASE_URL = settings.PG_DSN

CONNECT_TRY = settings.MAX_ATTEMPTS_TO_CONN_TO_PG

engine = create_async_engine("postgresql+asyncpg://" + DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

session = async_session()
Base = declarative_base()


