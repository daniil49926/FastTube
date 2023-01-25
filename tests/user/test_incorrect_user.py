from typing import Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


class TestIncorrectUser:
    @pytest.fixture()
    def user_fixt(self):
        return {
            "name": "Ketrin",
            "surname": "Belloboss",
            "username": "belloboss99",
            "gender": 2,
            "email": "bellobosss99@example.com",
            "password": "SamiySecretniyParol_$123",
        }

    @pytest.mark.parametrize(
        "user",
        [
            {
                "name": "Oussama",
                "surname": "Benladen",
                "gender": 1,
                "email": "shached338@example.com",
                "password": "S@udiArabiaB_hhh338",
            },
            {
                "name": "Oussama",
                "surname": "Benladen",
                "username": "username",
                "gender": 1,
                "email": "gdddg",
                "password": "S@udiArabiaB_hhh338",
            },
            {
                "name": "Oussama",
                "surname": "Benladen",
                "username": "username",
                "gender": 999,
                "email": "gdddg",
                "password": "S@udiArabiaB_hhh338",
            },
            {
                "name": "Test name",
                "surname": "Testsurname",
                "username": "super_user3023",
                "gender": 0,
                "email": "supermario@example.com",
                "password": "Prosto_p*ssw0rd",
            },
            {
                "name": "Testname",
                "surname": "Test surname",
                "username": "super_user3023",
                "gender": 0,
                "email": "supermario@example.com",
                "password": "Prosto_p*ssw0rd",
            },
        ],
    )
    def test_incorrect_create_user(
        self,
        app: FastAPI,
        client: TestClient,
        user: Dict[str, str],
    ):
        response = client.post(url="/user/v1/users", json=user)
        assert response.status_code == 422

    def test_incorrect_get_user(
        self,
        app: FastAPI,
        client: TestClient,
        user_fixt: Dict[str, str],
    ):
        response = client.post(url="/user/v1/users", json=user_fixt)
        response = client.get(url=f"user/v1/users/{response.json()['id'] + 1}")
        assert response.status_code == 404

    def test_incorrect_get_me(
        self,
        app: FastAPI,
        client: TestClient,
        user_fixt: Dict[str, str],
    ):
        _ = client.post(url="/user/v1/users", json=user_fixt)
        _ = client.post(
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
        response = client.get(url="/user/v1/me")
        assert response.status_code == 401
