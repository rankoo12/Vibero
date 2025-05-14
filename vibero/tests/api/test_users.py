pytest_plugins = ["pytest_asyncio"]
import httpx
import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_user(async_client: httpx.AsyncClient):
    response = await async_client.post(
        "/users", json={"username": "test_user", "email": "test@example.com"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "test_user"
    assert data["email"] == "test@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_users(async_client: httpx.AsyncClient):
    response = await async_client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert isinstance(users, list)


@pytest.mark.asyncio
async def test_delete_user(async_client: httpx.AsyncClient):
    # First create a user
    response = await async_client.post(
        "/users", json={"username": "delete_me", "email": "delete@example.com"}
    )
    user_id = response.json()["id"]

    # Then delete
    delete_response = await async_client.delete(f"/users/{user_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
