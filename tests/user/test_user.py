from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app import app
from core.db.database import get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    yield db


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_healthchecker():
    response = client.get("/healthchecker/v1/test")
    assert response.status_code == 200
    assert response.json() == {"result": "OK"}
