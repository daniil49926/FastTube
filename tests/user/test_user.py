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

    def test_valid_create_user(
        self,
        app: FastAPI,
        client: TestClient,
        user_fixt: Dict[str, str],
    ):
        response = client.post(url="/user/v1/users", json=user_fixt)
        assert response.status_code == 200

    def test_valid_get_user(
        self,
        app: FastAPI,
        client: TestClient,
        user_fixt: Dict[str, str],
    ):
        response = client.post(url="/user/v1/users", json=user_fixt)
        response = client.get(url=f"user/v1/users/{response.json()['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == user_fixt.get("name")

    def test_valid_get_me(
        self,
        app: FastAPI,
        client: TestClient,
        user_fixt: Dict[str, str],
    ):
        _ = client.post(url="/user/v1/users", json=user_fixt)
        response = client.post(
            url="/token",
            data={
                "grant_type": "",
                "username": user_fixt.get("username"),
                "password": user_fixt.get("password"),
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )
        response = client.get(
            url="/user/v1/me",
            headers={
                "Authorization": f"{response.json()['token_type']} {response.json()['access_token']}"
            },
        )
        assert response.status_code == 200
        assert response.json()["name"] == user_fixt.get("name")
        assert response.json()["username"] == user_fixt.get("username")
