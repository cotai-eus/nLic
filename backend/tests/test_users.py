import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import UserCreate

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, session_override: AsyncSession):
    user_data = UserCreate(email="test@example.com", password="testpassword")
    response = await client.post("/auth/register", json=user_data.model_dump())
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, session_override: AsyncSession):
    # First, register a user
    user_data = UserCreate(email="login@example.com", password="loginpassword")
    await client.post("/auth/register", json=user_data.model_dump())

    # Then, try to login
    response = await client.post(
        "/auth/jwt/login",
        data={"username": "login@example.com", "password": "loginpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, session_override: AsyncSession):
    # Register and login a user
    user_data = UserCreate(email="current@example.com", password="currentpassword")
    await client.post("/auth/register", json=user_data.model_dump())
    login_response = await client.post(
        "/auth/jwt/login",
        data={"username": "current@example.com", "password": "currentpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]

    # Get current user with token
    response = await client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "current@example.com"
    assert "id" in response.json()
