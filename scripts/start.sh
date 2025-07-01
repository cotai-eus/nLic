#!/bin/bash

# Ensure .env exists
if [ ! -f .env ]; then
  echo "Creating .env file from .env.example..."
  cp .env.example .env
fi

# Start Docker Compose services
echo "Starting Docker Compose services..."
docker-compose up -d --build

echo "nRadar services started. Access the API at http://localhost:8000/docs"
