# Use a imagem oficial do Python
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala o Poetry
RUN pip install poetry

# Copia os arquivos de dependências do Poetry para o WORKDIR
COPY backend/pyproject.toml ./pyproject.toml
COPY backend/poetry.lock ./poetry.lock

# Copia o arquivo .env para o WORKDIR
COPY .env ./

# Instala as dependências do projeto
RUN poetry config virtualenvs.create false && poetry install --only main --no-root --no-interaction --no-ansi

# Copia o código da aplicação para o WORKDIR
COPY backend/app ./app

# Expõe a porta que o FastAPI estará rodando
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
