from os import environ
import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'health' : 'works'}

def test_auth_error():
    responce = client.post("/token",
        data={'username': '', 'password': ''}
    )
    access_token = responce.json().get("access_token")
    assert access_token == None
    message = responce.json().get("detail")[0].get("msg") 
    assert message == "field required"

def test_auth_success():
    responce = client.post("/token",
        data={'username': 'test1', 'password': '1234'}
    )
    access_token = responce.json().get("access_token")
    assert access_token

def test_create_account():
    responce = client.post("/token",
        data={'username': 'test1', 'password': '1234'}
    )
    access_token = responce.json().get("access_token")
    responce = client.post('/account/',
        json={
            "balance": 1000
        },
        headers={
        "Authorization": "bearer " + access_token
        }
    )
    assert responce.status_code == 200
    assert responce.json().get("balance") == 1000
