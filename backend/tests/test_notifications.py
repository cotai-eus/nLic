import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import UserCreate
from app.models.notification import Notification
from app.models.perfil import PerfilDeInteresse
import uuid

@pytest.fixture
async def authenticated_client_with_profile(client: AsyncClient, session_override: AsyncSession):
    # Register a user
    user_data = UserCreate(email="notif_user@example.com", password="notifpassword")
    await client.post("/auth/register", json=user_data.model_dump())

    # Login the user
    login_response = await client.post(
        "/auth/jwt/login",
        data={"username": "notif_user@example.com", "password": "notifpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}

    # Get current user to extract ID
    me_response = await client.get("/auth/me")
    user_id = me_response.json()["id"]

    # Create a profile for the user
    profile_data = {
        "nome_perfil": "Notif Test Profile",
        "palavras_chave": ["test", "notification"],
        "prioridade_urgencia": "qualquerPrazo"
    }
    profile_response = await client.post("/api/v1/perfis/", json=profile_data)
    profile_id = profile_response.json()["id"]

    return client, user_id, profile_id

@pytest.mark.asyncio
async def test_get_notifications(authenticated_client_with_profile: tuple[AsyncClient, str, str], db_session: AsyncSession):
    client, user_id, profile_id = authenticated_client_with_profile

    # Manually create a notification in the database
    new_notification = Notification(
        id=uuid.uuid4(),
        user_id=uuid.UUID(user_id),
        profile_id=uuid.UUID(profile_id),
        numero_controle_pncp="PNCP12345",
        tipo="email",
        status="sent",
        conteudo={"title": "Test Opportunity", "value": 1000}
    )
    db_session.add(new_notification)
    await db_session.commit()
    await db_session.refresh(new_notification)

    response = await client.get("/api/v1/notifications/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert any(n["numero_controle_pncp"] == "PNCP12345" for n in response.json())

@pytest.mark.asyncio
async def test_get_notification_by_id(authenticated_client_with_profile: tuple[AsyncClient, str, str], db_session: AsyncSession):
    client, user_id, profile_id = authenticated_client_with_profile

    # Manually create a notification in the database
    new_notification = Notification(
        id=uuid.uuid4(),
        user_id=uuid.UUID(user_id),
        profile_id=uuid.UUID(profile_id),
        numero_controle_pncp="PNCP67890",
        tipo="push",
        status="pending",
        conteudo={"title": "Another Opportunity", "value": 500}
    )
    db_session.add(new_notification)
    await db_session.commit()
    await db_session.refresh(new_notification)

    response = await client.get(f"/api/v1/notifications/{new_notification.id}")
    assert response.status_code == 200
    assert response.json()["numero_controle_pncp"] == "PNCP67890"
