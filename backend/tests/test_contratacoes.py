import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_contratacoes_proposta(client: AsyncClient):
    response = await client.get("/api/v1/contratacoes/proposta?dataFinal=20250831&codigoModalidadeContratacao=8&pagina=1")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
