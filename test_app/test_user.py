import json
from urllib import response

from fastapi.testclient import TestClient
from main import app
from schemas.user import UserCreate

client = TestClient(app)


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_user():
    payload = {
        'username': 'maximus',
        'email': 'optimusrobot@goodness.com',
        'password': 'saymyname',
        'full_name': 'Optimus Robot'
    }
    response = client.post("/users", json=payload)
    add_user_data = response.json()
    assert add_user_data["message"] == "User added successfully"
    assert add_user_data["data"]["username"] == "maximus"
