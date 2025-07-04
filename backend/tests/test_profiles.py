import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import UserCreate

@pytest.fixture
async def authenticated_client(client: AsyncClient, session_override: AsyncSession):
    # Register a user
    user_data = UserCreate(email="profile_user@example.com", password="profilepassword")
    await client.post("/auth/register", json=user_data.model_dump())

    # Login the user
    login_response = await client.post(
        "/auth/jwt/login",
        data={"username": "profile_user@example.com", "password": "profilepassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]

    client.headers = {"Authorization": f"Bearer {token}"}
    return client

@pytest.mark.asyncio
async def test_create_profile(authenticated_client: AsyncClient):
    profile_data = {
        "nome_perfil": "Teste Profile",
        "palavras_chave": ["licitacao", "software"],
        "prioridade_urgencia": "qualquerPrazo"
    }
    response = await authenticated_client.post("/api/v1/perfis/", json=profile_data)
    assert response.status_code == 201
    assert response.json()["nome_perfil"] == "Teste Profile"
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_profiles(authenticated_client: AsyncClient):
    # Create a profile first
    profile_data = {
        "nome_perfil": "Another Profile",
        "palavras_chave": ["hardware"],
        "prioridade_urgencia": "qualquerPrazo"
    }
    await authenticated_client.post("/api/v1/perfis/", json=profile_data)

    response = await authenticated_client.get("/api/v1/perfis/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert any(p["nome_perfil"] == "Another Profile" for p in response.json())

@pytest.mark.asyncio
async def test_update_profile(authenticated_client: AsyncClient):
    # Create a profile
    profile_data = {
        "nome_perfil": "Profile to Update",
        "palavras_chave": ["old"],
        "prioridade_urgencia": "qualquerPrazo"
    }
    create_response = await authenticated_client.post("/api/v1/perfis/", json=profile_data)
    profile_id = create_response.json()["id"]

    updated_data = {
        "nome_perfil": "Updated Profile",
        "palavras_chave": ["new", "updated"],
        "prioridade_urgencia": "urgente"
    }
    response = await authenticated_client.put(f"/api/v1/perfis/{profile_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["nome_perfil"] == "Updated Profile"
    assert "new" in response.json()["palavras_chave"]

@pytest.mark.asyncio
async def test_delete_profile(authenticated_client: AsyncClient):
    # Create a profile
    profile_data = {
        "nome_perfil": "Profile to Delete",
        "palavras_chave": ["delete"],
        "prioridade_urgencia": "qualquerPrazo"
    }
    create_response = await authenticated_client.post("/api/v1/perfis/", json=profile_data)
    profile_id = create_response.json()["id"]

    response = await authenticated_client.delete(f"/api/v1/perfis/{profile_id}")
    assert response.status_code == 204

    # Verify it's deleted
    get_response = await authenticated_client.get(f"/api/v1/perfis/{profile_id}")
    assert get_response.status_code == 404
