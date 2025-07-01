# API CN - Sistema de Contratações Públicas

[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)](https://docs.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.14-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)

Sistema completo para gerenciamento de contratações públicas com integração ao Portal Nacional de Contratações Públicas (PNCP).

## 🚀 Início Rápido

### Pré-requisitos

- Docker 24.0+ e Docker Compose V2
- Make (opcional, mas recomendado)
- Git

### Configuração Inicial

```bash
# Clone o repositório
git clone <repository-url>
cd apiCN

# Configure o ambiente
make setup

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Inicie o ambiente de desenvolvimento
make dev
```

### Acesso às Aplicações

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050
- **Adminer** (dev): http://localhost:8080

## 📁 Estrutura do Projeto

```
apiCN/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints da API
│   │   ├── core/           # Configurações
│   │   ├── db/             # Banco de dados
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── services/       # Lógica de negócio
│   │   └── main.py         # App principal
│   ├── tests/              # Testes
│   ├── Dockerfile          # Container backend
│   └── pyproject.toml      # Dependências Python
├── frontend/               # App React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Páginas
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # Serviços API
│   │   └── types/          # Tipos TypeScript
│   ├── Dockerfile          # Container frontend
│   └── package.json        # Dependências Node.js
├── config/                 # Configurações
│   ├── nginx/              # Config Nginx
│   ├── pgadmin/            # Config pgAdmin
│   └── redis.conf          # Config Redis
├── scripts/                # Scripts automação
├── e2e-tests/              # Testes E2E
├── performance-tests/      # Testes performance
├── docker-compose.yml      # Produção
├── docker-compose.dev.yml  # Desenvolvimento
├── docker-compose.test.yml # Testes
├── Makefile               # Comandos úteis
└── README.md              # Documentação
```

## 🛠️ Comandos Disponíveis

### Desenvolvimento

```bash
make dev           # Inicia ambiente de desenvolvimento
make stop          # Para todos os serviços
make restart       # Reinicia serviços
make logs          # Mostra logs de todos os serviços
make logs-backend  # Logs específicos do backend
make logs-frontend # Logs específicos do frontend
```

### Produção

```bash
make prod          # Inicia ambiente de produção
make build         # Builda todas as imagens
```

### Testes

```bash
make test          # Executa todos os testes
make test-backend  # Testes do backend apenas
make test-frontend # Testes do frontend apenas
make lint          # Executa linting
```

### Banco de Dados

```bash
make migrate       # Executa migrações
make migration MSG="descrição"  # Cria nova migração
make backup        # Backup do banco
make restore FILE=backup.sql.gz # Restaura backup
make seed          # Popula com dados exemplo
```

### Utilitários

```bash
make shell-backend # Acessa shell do backend
make shell-db      # Acessa shell do PostgreSQL
make health        # Verifica saúde dos serviços
make clean         # Remove containers e volumes
```

## 🧪 Testes

O projeto inclui uma suíte completa de testes:

### Backend
- **Testes Unitários**: Modelos, serviços, utilitários
- **Testes de Integração**: APIs, banco de dados
- **Cobertura**: Mínimo 80% de cobertura de código

### Frontend
- **Testes Unitários**: Componentes, hooks, utilitários
- **Testes de Integração**: Fluxos completos
- **Testes E2E**: Playwright para testes end-to-end

### Performance
- **Testes de Carga**: K6 para testes de performance
- **Monitoramento**: Métricas de resposta e throughput

### Segurança
- **OWASP ZAP**: Testes de segurança automatizados
- **Análise de Dependências**: Verificação de vulnerabilidades

### Executar Testes

```bash
# Todos os testes
./scripts/test.sh

# Testes específicos
make test-backend
make test-frontend

# Testes E2E
docker-compose -f docker-compose.test.yml run --rm e2e-test

# Testes de performance
docker-compose -f docker-compose.test.yml run --rm performance-test
```

## 🔒 Segurança

### Autenticação
- JWT tokens com refresh automático
- Senhas hasheadas com bcrypt
- Rate limiting configurável
- Sessões seguras

### Infraestrutura
- HTTPS obrigatório em produção
- Headers de segurança configurados
- Certificados SSL/TLS
- Isolamento de containers

### Banco de Dados
- Conexões criptografadas
- Pool de conexões otimizado
- Backup automático
- Isolamento por ambiente

## 📊 Monitoramento

### Logs
- Logs estruturados com Loguru
- Rotação automática de arquivos
- Níveis de log configuráveis
- Correlação de requisições

### Health Checks
- Verificação de saúde de todos os serviços
- Monitoramento de conectividade
- Alertas automáticos
- Métricas de performance

### Métricas
- Tempo de resposta da API
- Taxa de erro por endpoint
- Uso de recursos (CPU, memória)
- Conexões de banco de dados

## 🚀 Deploy

### Desenvolvimento
```bash
make dev
```

### Produção
```bash
# Configure variáveis de produção
cp .env.example .env.prod
# Edite .env.prod com configurações de produção

# Inicie produção
ENVIRONMENT=production make prod
```

### CI/CD
O projeto inclui configurações para:
- GitHub Actions
- GitLab CI
- Jenkins
- Docker Hub/Registry

## 🔧 Configuração

### Variáveis de Ambiente

Principais variáveis de configuração:

```env
# Banco de Dados
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
POSTGRES_DB=apicn_db
POSTGRES_USER=apicn_user
POSTGRES_PASSWORD=secure_password

# Segurança
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
BCRYPT_ROUNDS=12

# Redis
REDIS_URL=redis://:password@host:port/db

# PNCP
PNCP_API_URL=https://pncp.gov.br/api/consulta/v1
PNCP_API_KEY=your_api_key

# Frontend
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=API CN
```

### Customização

#### Backend
- **Modelos**: Adicione novos modelos em `backend/app/models/`
- **Endpoints**: Crie novos endpoints em `backend/app/api/v1/endpoints/`
- **Serviços**: Implemente lógica em `backend/app/services/`

#### Frontend
- **Componentes**: Adicione em `frontend/src/components/`
- **Páginas**: Crie em `frontend/src/pages/`
- **Hooks**: Desenvolva em `frontend/src/hooks/`

## 📝 Documentação Adicional

- [Guia de Desenvolvimento](docs/development.md)
- [Arquitetura do Sistema](docs/architecture.md)
- [Guia de Deployment](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Contribuição](docs/contributing.md)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentação**: [Wiki do Projeto](https://github.com/your-repo/wiki)
- **Slack**: #apicn-suporte

## 📈 Status do Projeto

- ✅ **Backend**: Completo e testado
- ✅ **Frontend**: Completo e testado
- ✅ **Docker**: Configuração completa
- ✅ **Testes**: Suíte completa implementada
- ✅ **CI/CD**: Pipeline configurado
- ✅ **Documentação**: Completa e atualizada
- ✅ **Segurança**: Implementada e auditada
- 🚀 **Produção**: Pronto para deploy
