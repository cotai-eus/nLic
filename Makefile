.PHONY: build up down logs shell db-shell clean

# Carrega variáveis do arquivo .env
-include .env

# Comandos Docker
DOCKER_COMPOSE = docker compose

# Cores
GREEN=\033[0;32m
NC=\033[0m # No Color

## ---------------------------------------
## Gestão da Stack Docker
## ---------------------------------------

build:
	@echo "${GREEN}Building Docker images...${NC}"
	@$(DOCKER_COMPOSE) build

up:
	@echo "${GREEN}Starting Docker stack...${NC}"
	@$(DOCKER_COMPOSE) up -d

down:
	@echo "${GREEN}Stopping Docker stack...${NC}"
	@$(DOCKER_COMPOSE) down

logs:
	@echo "${GREEN}Showing logs...${NC}"
	@$(DOCKER_COMPOSE) logs -f

## ---------------------------------------
## Acesso aos Containers
## ---------------------------------------

shell:
	@echo "${GREEN}Accessing backend container shell...${NC}"
	@$(DOCKER_COMPOSE) exec backend /bin/bash

db-shell:
	@echo "${GREEN}Listing PostgreSQL functions...${NC}"
	@$(DOCKER_COMPOSE) exec postgres psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "\df"

## ---------------------------------------
## Manutenção
## ---------------------------------------

test:
	@echo "${GREEN}Running tests...${NC}"
	@$(DOCKER_COMPOSE) run --rm backend pytest /app/tests

clean:
	@echo "${GREEN}Cleaning up Docker containers, volumes, and networks...${NC}"
	@$(DOCKER_COMPOSE) down -v --remove-orphans

# Exemplo de comando para inicializar o banco (se necessário)
# Este comando depende do init.sql já ser executado pelo entrypoint do postgres
db-init:
	@echo "${GREEN}Database is auto-initialized by Postgres entrypoint. Forcing re-initialization...${NC}"
	@$(DOCKER_COMPOSE) down -v
	@$(DOCKER_COMPOSE) up -d postgres
	@echo "${GREEN}Waiting for DB to be ready...${NC}"
	@sleep 10
	@echo "${GREEN}DB re-initialized.${NC}"


.DEFAULT_GOAL := help

help:
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  build      Build the Docker images for the project."
	@echo "  up         Start the Docker containers in detached mode."
	@echo "  down       Stop and remove the Docker containers."
	@echo "  logs       Follow the logs of all running containers."
	@echo "  shell      Access the shell of the backend container."
	@echo "  db-shell   Access the PostgreSQL shell."
	@echo "  clean      Stop containers and remove all associated volumes and networks."
	@echo "  db-init    (Re)initializes the database by resetting the postgres volume."
