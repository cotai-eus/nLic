# Stage 1: Builder
FROM python:3.13-slim as builder

# Instalar Poetry
RUN pip install poetry

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de dependências
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true

# Instalar dependências do projeto
# --no-root: não instala o pacote do projeto em si
# --no-dev: não instala as dependências de desenvolvimento
RUN poetry install --no-root

# Stage 2: Final Image
FROM python:3.13-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o ambiente virtual do builder
COPY --from=builder /app/.venv /app/.venv

# Ativar o ambiente virtual
ENV PATH="/app/.venv/bin:$PATH"

# Copiar o código da aplicação
COPY ./app /app/app

# Expor a porta que o FastAPI vai usar
EXPOSE 8000