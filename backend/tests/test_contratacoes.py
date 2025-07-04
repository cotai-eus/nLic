import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_get_contratacoes_proposta(client: AsyncClient):
    response = await client.get("/api/v1/contratacoes/proposta")
    assert response.status_code == 422
