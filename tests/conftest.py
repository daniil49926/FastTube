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


@pytest.fixture()
def user_fixt():
    return {
        "name": "Ketrin",
        "surname": "Belloboss",
        "username": "belloboss99",
        "gender": 2,
        "email": "bellobosss99@example.com",
        "password": "SamiySecretniyParol_$123",
    }
