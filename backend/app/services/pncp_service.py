import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, date

from app.models.perfil import PerfilDeInteresse

PNCP_API_BASE_URL = "https://pncp.gov.br/api/consulta/v1"

async def _make_pncp_request(endpoint: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
    url = f"{PNCP_API_BASE_URL}/{endpoint}"
    all_results = []
    current_page = params.get("pagina", 1)

    async with httpx.AsyncClient(verify=False) as client:
        while True:
            params["pagina"] = current_page
            response = await client.get(url, params=params)
            response.raise_for_status() # Levanta exceção para erros HTTP
            data = response.json()
            
            if not data or not data.get("data"):
                break

            all_results.extend(data["data"])
            
            if data.get("totalPaginas", 0) > current_page:
                current_page += 1
            else:
                break
    return all_results

async def search_contratacoes_proposta(perfil: PerfilDeInteresse) -> List[Dict[str, Any]]:
    params = {
        "pagina": 1,
        "dataFinal": (datetime.now() + timedelta(days=30)).strftime("%Y%m%d"), # Busca por 30 dias a frente
    }

    if perfil.uf:
        params["uf"] = perfil.uf
    if perfil.municipio_ibge:
        params["codigoMunicipiolbge"] = perfil.municipioIbge
    if perfil.modalidade_contratacao:
        params["codigoModalidadeContratacao"] = perfil.modalidade_contratacao

    opportunities = await _make_pncp_request("contratacoes/proposta", params)

    # Filtragem local por palavras-chave e urgência
    filtered_opportunities = []
    for item in opportunities:
        if perfil.palavrasChave:
            objeto_compra = item.get("objetoContratacao", "").lower()
            if any(keyword.lower() in objeto_compra for keyword in perfil.palavrasChave):
                filtered_opportunities.append(item)
        else:
            filtered_opportunities.append(item)
    
    if perfil.prioridadeUrgencia == "urgente":
        today = datetime.now().date()
        filtered_opportunities = [ 
            op for op in filtered_opportunities 
            if "dataEncerramentoProposta" in op and 
            (datetime.strptime(op["dataEncerramentoProposta"], "%Y-%m-%dT%H:%M:%S").date() - today).days <= 3
        ]
    elif perfil.prioridadeUrgencia == "proximaSemana":
        today = datetime.now().date()
        filtered_opportunities = [ 
            op for op in filtered_opportunities 
            if "dataEncerramentoProposta" in op and 
            (datetime.strptime(op["dataEncerramentoProposta"], "%Y-%m-%dT%H:%M:%S").date() - today).days <= 7
        ]

    return filtered_opportunities

async def search_contratacoes_publicacao(
    data_inicial: date,
    data_final: date,
    codigo_modalidade_contratacao: Optional[int] = None,
    uf: Optional[str] = None,
    codigo_municipio_ibge: Optional[str] = None,
    cnpj: Optional[str] = None,
    codigo_unidade_administrativa: Optional[int] = None,
    id_usuario: Optional[int] = None,
) -> List[Dict[str, Any]]:
    params = {
        "dataInicial": data_inicial.strftime("%Y%m%d"),
        "dataFinal": data_final.strftime("%Y%m%d"),
        "pagina": 1,
    }
    if codigo_modalidade_contratacao:
        params["codigoModalidadeContratacao"] = codigo_modalidade_contratacao
    if uf:
        params["uf"] = uf
    if codigo_municipio_ibge:
        params["codigoMunicipiolbge"] = codigo_municipio_ibge
    if cnpj:
        params["cnpj"] = cnpj
    if codigo_unidade_administrativa:
        params["codigoUnidadeAdministrativa"] = codigo_unidade_administrativa
    if id_usuario:
        params["idUsuario"] = id_usuario
    
    return await _make_pncp_request("contratacoes/publicacao", params)

async def search_pca_usuario(
    ano_pca: int,
    id_usuario: int,
    codigo_classificacao_superior: Optional[int] = None,
) -> List[Dict[str, Any]]:
    params = {
        "anoPca": ano_pca,
        "idUsuario": id_usuario,
        "pagina": 1,
    }
    if codigo_classificacao_superior:
        params["codigoClassificacaoSuperior"] = codigo_classificacao_superior
    
    return await _make_pncp_request("pca/usuario", params)

async def search_atas(
    data_inicial: date,
    data_final: date,
) -> List[Dict[str, Any]]:
    params = {
        "dataInicial": data_inicial.strftime("%Y%m%d"),
        "dataFinal": data_final.strftime("%Y%m%d"),
        "pagina": 1,
    }
    return await _make_pncp_request("atas", params)

async def search_contratos(
    data_inicial: date,
    data_final: date,
) -> List[Dict[str, Any]]:
    params = {
        "dataInicial": data_inicial.strftime("%Y%m%d"),
        "dataFinal": data_final.strftime("%Y%m%d"),
        "pagina": 1,
    }
    return await _make_pncp_request("contratos", params)