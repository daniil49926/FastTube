import os
from typing import Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


class TestValidLoadVideo:
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

    def test_valid_load_video(
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
        media_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "media_for_test")
        response = client.post(
            url="/video/v1/video/",
            files={
                "file": (
                    "test_name.mp4",
                    open(f"{media_path}/ValidVideo.mp4", "rb"),
                    "video/mp4",
                )
            },
            data={"title": "test", "description": "test_description"},
            headers={
                "Authorization": f"{response.json()['token_type']} {response.json()['access_token']}",
                "Content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            },
        )
        assert response.status_code == 200
        assert response.json()["title"] == "test"
