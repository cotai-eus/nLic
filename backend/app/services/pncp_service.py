import httpx
from typing import List, Dict, Any
from datetime import datetime, timedelta

from app.models.perfil import PerfilDeInteresse

PNCP_API_BASE_URL = "https://pncp.gov.br/api/consulta/v1"

async def search_opportunities(perfil: PerfilDeInteresse) -> List[Dict[str, Any]]:
    url = f"{PNCP_API_BASE_URL}/contratacoes/proposta"
    params = {
        "pagina": 1,
        "dataFinal": (datetime.now() + timedelta(days=30)).strftime("%Y%m%d"), # Busca por 30 dias a frente
    }

    if perfil.uf:
        params["uf"] = perfil.uf
    if perfil.municipioIbge:
        params["codigoMunicipiolbge"] = perfil.municipioIbge
    if perfil.modalidadeContratacao:
        params["codigoModalidadeContratacao"] = perfil.modalidadeContratacao

    # TODO: Adicionar filtro por categoria quando a API do PNCP suportar ou mapear

    opportunities = []
    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(url, params=params, verify=False) # verify=False para ignorar SSL
            response.raise_for_status() # Levanta exceção para erros HTTP
            data = response.json()
            
            if not data or not data.get("data"): # Verifica se há dados
                break

            for item in data["data"]:
                # Filtragem local por palavras-chave
                if perfil.palavrasChave:
                    objeto_compra = item.get("objetoContratacao", "").lower()
                    if any(keyword.lower() in objeto_compra for keyword in perfil.palavrasChave):
                        opportunities.append(item)
                else:
                    opportunities.append(item)
            
            # Lógica de paginação
            if data.get("totalPaginas", 0) > params["pagina"]:
                params["pagina"] += 1
            else:
                break

    # Filtragem por prioridade de urgência
    if perfil.prioridadeUrgencia == "urgente":
        today = datetime.now().date()
        opportunities = [ 
            op for op in opportunities 
            if "dataEncerramentoProposta" in op and 
            (datetime.strptime(op["dataEncerramentoProposta"], "%Y-%m-%dT%H:%M:%S").date() - today).days <= 3
        ]
    elif perfil.prioridadeUrgencia == "proximaSemana":
        today = datetime.now().date()
        opportunities = [ 
            op for op in opportunities 
            if "dataEncerramentoProposta" in op and 
            (datetime.strptime(op["dataEncerramentoProposta"], "%Y-%m-%dT%H:%M:%S").date() - today).days <= 7
        ]

    return opportunities
