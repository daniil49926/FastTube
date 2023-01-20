from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.application import get_app


@pytest.fixture
def app():
    yield get_app()


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, Any, None]:

    with TestClient(app) as client:
        yield client
