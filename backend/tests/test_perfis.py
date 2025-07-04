import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.perfil import Perfil


@pytest.mark.asyncio
async def test_create_perfil(client: AsyncClient, db: AsyncSession):
    response = await client.post(
        "/api/v1/perfis/",
        json={
            "nomePerfil": "Test Profile",
            "palavrasChave": ["test", "pytest"],
            "uf": "SP",
            "municipioIbge": "3550308",
            "modalidadeContratacao": 1,
            "categoria": "Produto",
            "prioridadeUrgencia": "urgente",
            "notificacaoPush": True,
            "notificacaoEmail": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nomePerfil"] == "Test Profile"
    assert "id" in data

@pytest.mark.asyncio
async def test_read_perfil(client: AsyncClient, db: AsyncSession):
    perfil = Perfil(
        nomePerfil="Test Profile",
        palavrasChave=["test", "pytest"],
        uf="SP",
        municipioIbge="3550308",
        modalidadeContratacao=1,
        categoria="Produto",
        prioridadeUrgencia="urgente",
        notificacaoPush=True,
        notificacaoEmail=False,
    )
    db.add(perfil)
    await db.commit()
    await db.refresh(perfil)

    response = await client.get(f"/api/v1/perfis/{perfil.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nomePerfil"] == "Test Profile"
    assert data["id"] == perfil.id
