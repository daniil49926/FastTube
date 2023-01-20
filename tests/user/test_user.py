from typing import Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


class TestUsers:
    @pytest.fixture
    def user_fixt(self) -> Dict[str, str]:
        return {
            "name": "Oussama",
            "surname": "Benladen",
            "username": "Shached338",
            "gender": 1,
            "email": "shached338@example.com",
            "password": "S@udiArabiaB_hhh338",
        }

    def test_valid_user(
        self,
        app: FastAPI,
        client: TestClient,
        user_fixt: Dict[str, str],
    ):
        response = client.post(url="/user/v1/users", json=user_fixt)
        assert response.status_code == 200
