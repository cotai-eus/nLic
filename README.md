# nRadar - Sistema de Monitoramento de Licitações

O nRadar é um sistema automatizado de monitoramento de oportunidades no Portal Nacional de Contratações Públicas (PNCP), com foco em personalização via Perfis de Interesse. Ele realiza chamadas à API pública do PNCP, filtra os resultados localmente e envia notificações para os usuários com base em suas preferências.

## Visão Geral

Este repositório contém o backend completo do nRadar, construído com FastAPI, PostgreSQL, Celery e Redis. Ele é projetado para ser robusto, escalável e fácil de implantar usando Docker.

## Funcionalidades

- **Autenticação de Usuários:** Cadastro, login (JWT), recuperação e verificação de senha.
- **Perfis de Interesse:** Criação, leitura, atualização e exclusão de perfis personalizados para monitoramento de licitações.
- **Monitoramento de Oportunidades:** Robô Celery que busca periodicamente novas oportunidades no PNCP com base nos perfis de interesse.
- **Notificações:** Envio de notificações por e-mail (com placeholders para push).

## Stack Tecnológica

- **Backend:** Python 3.12+ (FastAPI)
- **Banco de Dados:** PostgreSQL
- **Agendamento:** Celery + Redis
- **Autenticação:** FastAPI Users (JWT, bcrypt)
- **Requisições HTTP:** httpx
- **Containerização:** Docker + Docker Compose
- **Gerenciamento de Dependências:** Poetry

## Estrutura de Diretórios

```
nRadar/
├── .github/                  # Workflows de CI/CD
├── backend/                  # Código-fonte do backend (FastAPI)
│   ├── app/
│   │   ├── main.py            # Ponto de entrada da aplicação FastAPI
│   │   ├── models/              # Modelos de dados (SQLAlchemy e Pydantic)
│   │   ├── auth/                # Módulo de autenticação
│   │   ├── services/           # Lógica de negócios e integração com PNCP
│   │   ├── workers/           # Workers Celery
│   │   ├── utils/               # Utilitários e helpers
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/ # Endpoints REST
│   │   └── celery_app.py      # Configuração do Celery
│   ├── tests/                 # Testes unitários e de integração
│   ├── pyproject.toml
│   ├── poetry.lock
│   └── Dockerfile
├── db/                       # Migrações, seeds e scripts de banco de dados
│   ├── migrations/
│   ├── seeds/
│   └── init.sql               # Script de inicialização do DB
├── scripts/                  # Scripts utilitários
│   └── setup_env.sh           # Script para configurar o ambiente
├── docker-compose.yml
├── .env.example              # Exemplo de variáveis de ambiente
├── .gitignore
├── README.md
```

## Setup do Ambiente de Desenvolvimento

1.  **Pré-requisitos:**
    - Docker e Docker Compose instalados.
    - Git instalado.

2.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/nRadar.git
    cd nRadar
    ```

3.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto, copiando o `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Edite o arquivo `.env` e preencha a `SECRET_KEY` com uma string aleatória e segura. As outras variáveis já vêm com valores padrão para desenvolvimento.

4.  **Inicie os serviços com Docker Compose:**
    ```bash
    docker-compose up -d --build
    ```
    Este comando irá:
    - Construir as imagens Docker para o backend, Celery Worker e Celery Beat.
    - Iniciar os contêineres do PostgreSQL, Redis, Backend, Celery Worker e Celery Beat.
    - Executar o `db/init.sql` para criar as tabelas iniciais no banco de dados.

5.  **Verifique o status dos serviços:**
    ```bash
    docker-compose ps
    ```
    Todos os serviços devem estar `Up`.

6.  **Acesse a API:**
    A API do FastAPI estará disponível em `http://localhost:8000`.
    A documentação interativa (Swagger UI) estará em `http://localhost:8000/docs`.

## Uso da API

Consulte a documentação interativa em `http://localhost:8000/docs` para detalhes sobre os endpoints de autenticação e gerenciamento de perfis.

### Exemplo de Fluxo de Autenticação e Criação de Perfil

1.  **Registrar um novo usuário:**
    `POST /auth/register`
    ```json
    {
        "email": "test@example.com",
        "password": "your_secure_password"
    }
    ```

2.  **Fazer login para obter um token JWT:**
    `POST /auth/jwt/login`
    ```json
    {
        "username": "test@example.com",
        "password": "your_secure_password"
    }
    ```
    Copie o `access_token` da resposta.

3.  **Criar um perfil de interesse:**
    `POST /api/v1/perfis`
    Adicione o `Bearer Token` (o `access_token` obtido no login) no cabeçalho `Authorization`.
    ```json
    {
        "nomePerfil": "Equipamentos de TI - SP",
        "palavrasChave": ["computador", "servidor", "notebook"],
        "uf": "SP",
        "notificacaoEmail": true
    }
    ```

## Testes

Para executar os testes (ainda em desenvolvimento):

1.  **Acesse o contêiner do backend:**
    ```bash
    docker-compose exec backend bash
    ```

2.  **Execute os testes com Poetry:**
    ```bash
    poetry run pytest
    ```

## CI/CD (GitHub Actions)

O projeto inclui workflows de GitHub Actions em `.github/workflows/` para:

- **Testes e Lint:** Executar testes e verificações de lint a cada push ou Pull Request.
- **Build e Push de Imagens Docker:** Construir e enviar imagens Docker para um registry (configuração futura).

## Contribuição

1.  Faça um fork do repositório.
2.  Crie uma nova branch para sua feature (`git checkout -b feature/minha-nova-feature`).
3.  Implemente suas mudanças e escreva testes.
4.  Certifique-se de que todos os testes passem e o lint esteja limpo.
5.  Crie um Pull Request para a branch `main`.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
