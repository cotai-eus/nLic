# Stage 1: Build - Instala dependências
FROM python:3.13-slim as builder

WORKDIR /app

# Copia os arquivos de dependência
COPY pyproject.toml poetry.lock ./ 



# Instala o Poetry
RUN pip install --no-cache-dir poetry

# Instala as dependências do projeto
RUN poetry config virtualenvs.create false &&     poetry install --no-interaction --no-ansi --no-root &&     poetry add anyio --extras asyncio --group dev
    
# Copia o código da aplicação
COPY . .

# Cria usuário não-root e define permissões
RUN useradd -m app && chown -R app:app /app
USER app


# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Instala curl para o healthcheck
USER root
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
USER app

# Healthcheck para verificar se a aplicação está rodando
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1
