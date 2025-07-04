---
applyTo: '**'
---
# Plano Técnico de Implementação - nRadar

## Visão Geral

O **nRadar** é um sistema automatizado de monitoramento de oportunidades no PNCP, com foco em personalização via *Perfis de Interesse*. Ele realiza chamadas à API pública do PNCP, filtra os resultados localmente e envia notificações para os usuários com base em suas preferências.

---

## 🔍 Exemplos de Requisições (cURL) Utilizadas pelo App

**Consultar Contratações com Período de Propostas em Aberto**
```bash
curl -k -X 'GET' \
"https://pncp.gov.br/api/consulta/v1/contratacoes/proposta?dataFinal=20230831&codigoModalidadeContratacao=8&pagina=1" \
-H "accept: */*"
```

**Consultar Contratações por Data de Publicação**
```bash
curl -X 'GET' \
'https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao?dataInicial=20230801&dataFinal=20230802&codigoModalidadeContratacao=8&uf=DF&codigoMunicipiolbge=5300108&cnpj=00059311000126&codigoUnidadeAdministrativa=194035&idUsuario=3&pagina=1' \
-H 'accept: */*'
```

**Consultar Itens de PCA por Ano, idUsuario e Classificação Superior**
```bash
curl -X 'GET' \
'https://pncp.gov.br/api/consulta/v1/pca/usuario?anoPca=2023&idUsuario=3&codigoClassificacaoSuperior=979&pagina=1' \
-H 'accept: */*'
```

**Consultar Atas de Registro de Preço por Período de Vigência**
```bash
curl -X 'GET' \
'https://pncp.gov.br/api/consulta/v1/atas?dataInicial=20230701&dataFinal=20230831&pagina=1' \
-H 'accept: */*'
```

**Consultar Contratos por Data de Publicação**
```bash
curl -k -X GET "https://pncp.gov.br/api/consulta/v1/contratos?dataInicial=20230801&dataFinal=20230831&pagina=1" \
-H "accept: */*"
```

---

## 🎯 Funcionalidade Central: Criação e Gerenciamento de Perfis de Interesse

### Campos por Perfil

| Campo                        | Descrição                                                                 |
|-----------------------------|---------------------------------------------------------------------------|
| `nomePerfil`                | Nome identificador do perfil (ex: "Equipamentos de TI - Sul")             |
| `palavrasChave`             | Lista de termos para busca textual no campo `objetoCompra`                |
| `uf`                        | Unidade Federativa para filtro geográfico                                 |
| `municipioIbge`             | Código do IBGE para o município                                           |
| `modalidadeContratacao`     | Código da modalidade (opcional)                                           |
| `categoria`                 | Produto, Serviço, Obras, Informática (baseado na seção 5.11 do PNCP)      |
| `prioridadeUrgencia`        | Filtro por prazo de encerramento da proposta                              |
| `notificacaoPush`           | Booleano: Habilita ou não notificações push                               |
| `notificacaoEmail`          | Booleano: Habilita ou não notificações por e-mail                         |

### Valores para `prioridadeUrgencia`:

| Opção             | Regra                                                                 |
|------------------|-----------------------------------------------------------------------|
| `urgente`         | `dataEncerramentoProposta - hoje <= 3 dias`                          |
| `proximaSemana`   | `dataEncerramentoProposta - hoje <= 7 dias`                          |
| `qualquerPrazo`   | Sem filtro adicional por urgência                                    |

---

## 🧱 Stack Tecnológica

- **Backend**: Python 3.12+ (FastAPI)  
  [Python Docs](https://docs.python.org/3/) | [FastAPI Docs](https://fastapi.tiangolo.com/)
- **Gerenciador de dependências Python**: Poetry  
  [Poetry Docs](https://python-poetry.org/docs/)
- **Agendador**: Celery + Redis (ou alternativa com APScheduler para simplicidade)  
  [Celery Docs](https://docs.celeryq.dev/en/stable/) | [Redis Docs](https://redis.io/docs/) | [APScheduler Docs](https://apscheduler.readthedocs.io/en/latest/)
- **Banco de Dados**: PostgreSQL (com suporte a JSONB para palavras-chave e logs)  
  [PostgreSQL Docs](https://www.postgresql.org/docs/)
  - **Driver**: psycopg 3  
    [psycopg 3 Docs](https://www.psycopg.org/psycopg3/docs/)
- **Notificações**:
  - **E-mail**: SMTP + Mailgun/SendGrid  
    [SMTP RFC](https://datatracker.ietf.org/doc/html/rfc5321) | [Mailgun Docs](https://documentation.mailgun.com/en/latest/) | [SendGrid Docs](https://docs.sendgrid.com/)
  - **Push**: Firebase Cloud Messaging (FCM)  
    [FCM Docs](https://firebase.google.com/docs/cloud-messaging)
- **Infraestrutura**: Docker + Docker Compose + GitHub Actions  
  [Docker Docs](https://docs.docker.com/) | [Docker Compose Docs](https://docs.docker.com/compose/) | [GitHub Actions Docs](https://docs.github.com/en/actions)
- **Frontend (futuro)**: React + TailwindCSS (ou Next.js)  
  [React Docs](https://react.dev/) | [TailwindCSS Docs](https://tailwindcss.com/docs) | [Next.js Docs](https://nextjs.org/docs)
- **Gerenciador de dependências JS**: Yarn  
  [Yarn Docs](https://yarnpkg.com/getting-started)

---

## 📂 Estrutura de Diretórios

```bash
nRadar/
├── .github/
│   └── workflows/
│   └── instructions/
├── backend/                  # Código-fonte do backend (FastAPI)
│   ├── app/
│   │   ├── main.py            # Ponto de entrada da aplicação FastAPI
│   │   ├── models/              # Modelos de dados e Pydantic
│   │   ├── auth/                # Módulo de autenticação e cadastro de usuários
│   │   ├── services/           # Lógica de negócios e integração com PNCP
│   │   ├── workers/           # Worker para agendamento de tarefas
│   │   ├── utils/               # Filtros, utilitários e helpers
│   │   └── api/
│   │       └── v1/
│   │           └── endpoints/ # Endpoints REST organizados
│   ├── tests/                 # Testes unitários e de integração
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/                 # Código-fonte do frontend (React/Next.js)
│   ├── src/
│   ├── public/
│   ├── package.json         # Gerenciador de dependências JS
│   ├── yarn.lock
│   └── Dockerfile
├── db/                       # Migrações, seeds e scripts de banco de dados
│   ├── migrations/
│   ├── seeds/
│   └── init.sql
├── scripts/                  # Scripts utilitários e de automação
│   ├── start.sh
│   ├── setup_env.sh
│   └── backup_db.sh
├── docker-compose.yml
├── README.md
```

**Boas práticas aplicadas:**
- Inclusão do diretório `api/v1/endpoints` para organização dos endpoints REST.
- Uso de Poetry para dependências Python e Yarn para frontend.
- Inclusão explícita do driver psycopg 3 para PostgreSQL.
- Filtros e utilitários centralizados em `utils/`.
- Estrutura pronta para testes, CI/CD e escalabilidade.
- Inclusão do diretório `auth/` para autenticação e cadastro seguro de usuários.

---

## 🔁 Fluxo de Dados: Monitoramento de Oportunidades

```mermaid
graph TD
    A[Start: Robô Agendado] --> B{Buscar Perfis de Usuário no DB};
    B --> C{Loop por cada Perfil};
    C --> D[Montar Parâmetros para API PNCP];
    D --> E[Chamar GET /v1/contratacoes/proposta];
    E --> F{Resultados Recebidos?};
    F -- Sim --> G{Loop nos Resultados};
    F -- Não --> C;

    G --> H{Contém Palavra-Chave?};
    H -- Sim --> I{Já Notificado?};
    H -- Não --> G;

    I -- Não --> J[Enviar Notificação (Push/Email)];
    J --> K[Registrar Notificação no DB];
    K --> G;
    I -- Sim --> G;

    G -- Fim do Loop de Resultados --> C;
    C -- Fim do Loop de Perfis --> L[End];
```

---

## 🔐 Autenticação e Cadastro de Usuários

O nRadar deve implementar autenticação e cadastro de usuários de forma segura, seguindo as melhores práticas:

- **Cadastro de Usuário:** Endpoint para criação de conta, validação de e-mail e senha forte.
- **Login:** Endpoint seguro com autenticação baseada em JWT (JSON Web Token).
- **Hash de Senha:** Armazenamento seguro usando algoritmos como bcrypt/argon2.
- **Recuperação de Senha:** Fluxo de reset seguro via e-mail.
- **Proteção de Endpoints:** Perfis de interesse e notificações só acessíveis a usuários autenticados.
- **Validação e Rate Limit:** Proteção contra brute-force e validação de entrada.

**Sugestão de stack para autenticação:**
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/latest/) (ou implementação própria)
- [Passlib](https://passlib.readthedocs.io/en/stable/) para hash de senha
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/) para geração e validação de tokens

---

## 🧠 Regras de Negócio

* **Filtragem por Palavra-Chave**: Local, feito no campo `objetoCompra` (case-insensitive).  
  **Função:**  
  ```python
  def filtrar_por_palavra_chave(objeto_compra: str, palavras_chave: list[str]) -> bool:
      objeto = objeto_compra.lower()
      return any(palavra.lower() in objeto for palavra in palavras_chave)
  ```
* **Filtro de Urgência**: Calculado com `dataEncerramentoProposta - hoje`
* **Verificação de Duplicidade**: Baseada em `numeroControlePNCP` e ID do usuário
* **Limite de Notificações**: 1 notificação por oportunidade por perfil

---

## ✅ Boas Práticas

* Modularização clara por camadas (Model, Service, Worker)
* Uso de `.env` para variáveis sensíveis (email, notificações, etc)
* Testes unitários e mocks para chamadas à API externa
* Validação de dados com Pydantic
* Logs estruturados (JSON) para observabilidade
* Tolerância a falhas na API externa com `retry/backoff`
* Yarn para gerenciar dependências JS no frontend sempre usar comandos 'yarn install' e 'yarn add' para adicionar pacotes.

---

## 🚫 Restrições Conhecidas

* nRadar não possui:

  * npm, pip, sqlite
  * 
  * Webhooks para mudanças em tempo real

---

## 🧭 Futuras Extensões

* Integração com plano anual (`/v1/pca/usuario`)
* Alertas de renovação de contrato (`/v1/contratos`)
* Relatórios PDF automáticos
* Dashboard analítico com filtros por categoria/UF

---

## 📅 Agendamento de Execução

Exemplo com `Celery + Redis`:

```python
from celery import Celery

app = Celery('radar', broker='redis://localhost:6379/0')

@app.task
def executar_radar():
    from app.services.radar_bot import run
    run()

# schedule.py
from celery.schedules import crontab
app.conf.beat_schedule = {
    'executar-radar-cada-30-min': {
        'task': 'executar_radar',
        'schedule': crontab(minute='*/30')
    }
}
```

---

## 📘 Conclusão

O nRadar é um projeto robusto e extensível, com arquitetura escalável, integração com fonte governamental confiável, e foco em personalização de alertas. O plano acima cobre desde os perfis de interesse até o agendamento e tratamento de exceções.

---

## 💻 Configuração de GitHub para Commits

Para realizar commits com seu usuário do GitHub, configure seu nome e e-mail globalmente:
https://github.com/cotai-eus/nLic.git
```bash
git config --global user.name "cotai-eus"
git config --global user.email "eus.cotai@gmail.com"
```

Se quiser configurar apenas para este repositório, remova a flag `--global` e execute dentro da pasta do projeto:

```bash
git config user.name "SeuNomeNoGitHub"
git config user.email "seuemail@exemplo.com"
```

Para autenticação via HTTPS, utilize um [Personal Access Token (PAT)](https://github.com/settings/tokens) ao invés de senha ao fazer push/pull:

```bash
git push https://<token>@github.com/usuario/repositorio.git
```

Mais detalhes: [GitHub Docs - Configurar Git](https://docs.github.com/pt/get-started/getting-started-with-git)

---

```

Se quiser, posso gerar os arquivos Python correspondentes (`models`, `services`, etc.) com base nesse plano. Deseja isso?