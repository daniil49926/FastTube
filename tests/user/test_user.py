from fastapi.testclient import TestClient

from core.application import get_app

client = TestClient(get_app())


def test_healthchecker():
    response = client.get("/healthchecker/v1/test")
    assert response.status_code == 200
    assert response.json() == {"result": "OK"}
