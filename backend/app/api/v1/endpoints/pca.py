from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from app.services.pncp_service import search_pca_usuario

router = APIRouter(
    prefix="/api/v1/pca",
    tags=["pca"]
)

@router.get("/usuario")
async def get_pca_usuario(
    ano_pca: int = Query(..., description="Ano do PCA"),
    id_usuario: int = Query(..., description="ID do usuário"),
    codigo_classificacao_superior: Optional[int] = Query(None, description="Código da classificação superior"),
    pagina: int = Query(1, ge=1, description="Número da página")
):
    result = await search_pca_usuario(
        ano_pca=ano_pca,
        id_usuario=id_usuario,
        codigo_classificacao_superior=codigo_classificacao_superior,
    )
    return result
