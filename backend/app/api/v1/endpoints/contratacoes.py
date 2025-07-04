from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import date

from app.services.pncp_service import search_contratacoes_proposta, search_contratacoes_publicacao
from app.models.perfil import PerfilDeInteresse # Assuming PerfilDeInteresse is needed for search_contratacoes_proposta

router = APIRouter(
    tags=["contratacoes"]
)

@router.get("/proposta")
async def get_contratacoes_proposta(
    data_final: date = Query(..., description="Data final do período de propostas (YYYYMMDD)"),
    codigo_modalidade_contratacao: Optional[int] = Query(None, description="Código da modalidade de contratação"),
    pagina: int = Query(1, ge=1, description="Número da página")
):
    # Create a dummy PerfilDeInteresse for now, as the service expects it
    # In a real scenario, this would come from user's profile or a more complex logic
    dummy_perfil = PerfilDeInteresse(
        nome_perfil="dummy",
        palavras_chave=[],
        prioridade_urgencia="qualquerPrazo",
        uf=None,
        municipio_ibge=None,
        modalidade_contratacao=codigo_modalidade_contratacao,
        notificacao_push=False,
        notificacao_email=False
    )

    # Chama o serviço passando os parâmetros relevantes
    result = await search_contratacoes_proposta(
        dummy_perfil
    )
    return result

@router.get("/publicacao")
async def get_contratacoes_publicacao(
    data_inicial: date = Query(..., description="Data inicial de publicação (YYYYMMDD)"),
    data_final: date = Query(..., description="Data final de publicação (YYYYMMDD)"),
    codigo_modalidade_contratacao: Optional[int] = Query(None, description="Código da modalidade de contratação"),
    uf: Optional[str] = Query(None, description="Unidade Federativa"),
    codigo_municipio_ibge: Optional[str] = Query(None, description="Código IBGE do município"),
    cnpj: Optional[str] = Query(None, description="CNPJ"),
    codigo_unidade_administrativa: Optional[int] = Query(None, description="Código da unidade administrativa"),
    id_usuario: Optional[int] = Query(None, description="ID do usuário"),
    pagina: int = Query(1, ge=1, description="Número da página")
):
    result = await search_contratacoes_publicacao(
        data_inicial=data_inicial,
        data_final=data_final,
        codigo_modalidade_contratacao=codigo_modalidade_contratacao,
        uf=uf,
        codigo_municipio_ibge=codigo_municipio_ibge,
        cnpj=cnpj,
        codigo_unidade_administrativa=codigo_unidade_administrativa,
        id_usuario=id_usuario
    )
    return result
