from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import date

from app.services.pncp_service import search_contratos

router = APIRouter(
    prefix="/api/v1/contratos",
    tags=["contratos"]
)

@router.get("/")
async def get_contratos(
    data_inicial: date = Query(..., description="Data inicial de publicação (YYYYMMDD)"),
    data_final: date = Query(..., description="Data final de publicação (YYYYMMDD)"),
    pagina: int = Query(1, ge=1, description="Número da página")
):
    result = await search_contratos(
        data_inicial=data_inicial,
        data_final=data_final,
    )
    return result
