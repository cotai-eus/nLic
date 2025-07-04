import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.perfil import PerfilDeInteresse as Perfil
import uuid


@pytest.mark.anyio
async def test_create_perfil(client: AsyncClient, db: AsyncSession):
    response = await client.post(
        "/api/v1/perfis/",
        json={
            "nome_perfil": "Test Profile",
            "palavras_chave": ["test", "pytest"],
            "uf": "SP",
            "municipio_ibge": "3550308",
            "modalidade_contratacao": "1",
            "categoria": "Produto",
            "prioridade_urgencia": "urgente",
            "notificacao_push": True,
            "notificacao_email": False,
        },
    )
    assert response.status_code == 401

@pytest.mark.anyio
async def test_read_perfil(client: AsyncClient, db: AsyncSession):
    perfil = Perfil(
        id=uuid.uuid4(),
        nome_perfil="Test Profile",
        palavras_chave=["test", "pytest"],
        uf="SP",
        municipio_ibge="3550308",
        modalidade_contratacao="1",
        categoria="Produto",
        prioridade_urgencia="urgente",
        notificacao_push=True,
        notificacao_email=False,
    )
    db.add(perfil)
    await db.commit()
    await db.refresh(perfil)

    response = await client.get(f"/api/v1/perfis/{perfil.id}")
    assert response.status_code == 401
