from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import date

from app.services.pncp_service import search_atas

router = APIRouter(
    prefix="/api/v1/atas",
    tags=["atas"]
)

@router.get("/")
async def get_atas(
    data_inicial: date = Query(..., description="Data inicial do período de vigência (YYYYMMDD)"),
    data_final: date = Query(..., description="Data final do período de vigência (YYYYMMDD)"),
    pagina: int = Query(1, ge=1, description="Número da página")
):
    result = await search_atas(
        data_inicial=data_inicial,
        data_final=data_final,
    )
    return result
