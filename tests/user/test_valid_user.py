from typing import Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "user",
    [
        {
            "name": "Oussama",
            "surname": "Benladen",
            "username": "Shached338",
            "gender": 1,
            "email": "shached338@example.com",
            "password": "S@udiArabiaB_hhh338",
        },
        {
            "name": "Testname",
            "surname": "Testsurname",
            "username": "super_user3023",
            "gender": 0,
            "email": "supermario@example.com",
            "password": "Prosto_p*ssw0rd",
        },
        {
            "name": "Ketrin",
            "surname": "Belloboss",
            "username": "belloboss99",
            "gender": 2,
            "email": "bellobosss99@example.com",
            "password": "SamiySecretniyParol_$123",
        },
    ],
)
class TestValidUsers:
    def test_valid_create_user(
        self,
        app: FastAPI,
        client: TestClient,
        user: Dict[str, str],
    ):
        response = client.post(url="/user/v1/users", json=user)
        assert response.status_code == 200

    def test_valid_get_user(
        self,
        app: FastAPI,
        client: TestClient,
        user: Dict[str, str],
    ):
        response = client.post(url="/user/v1/users", json=user)
        response = client.get(url=f"user/v1/users/{response.json()['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == user.get("name")

    def test_valid_get_me(
        self,
        app: FastAPI,
        client: TestClient,
        user: Dict[str, str],
    ):
        _ = client.post(url="/user/v1/users", json=user)
        response = client.post(
            url="/token",
            data={
                "grant_type": "",
                "username": user.get("username"),
                "password": user.get("password"),
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
        assert response.json()["name"] == user.get("name")
        assert response.json()["username"] == user.get("username")

    def test_get_user_by_uid(
        self,
        app: FastAPI,
        client: TestClient,
        user: Dict[str, str],
    ):
        response = client.post(url="/user/v1/users", json=user)
        response = client.get(url=f"/user/v1/users/{response.json()['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == user.get("name")
