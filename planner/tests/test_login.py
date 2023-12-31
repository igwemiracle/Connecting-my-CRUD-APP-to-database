import httpx
import pytest


@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "TestUsername",
        "password": "TestPassword"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    test_response = {
        "message": "User created successfully"
    }
    response = await default_client.post("user/signup",
                                        json = payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response

@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "TestUsername",
        "password": "TestPassword"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    # initiate the request and test the responses:
    response = await default_client.post("/user/signin", json=payload,headers=headers)
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"


