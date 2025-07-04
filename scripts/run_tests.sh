#!/bin/bash

# Exit on error
set -e

# Clean up old volumes
docker compose -f /home/user/dev/nLic/docker-compose.test.yml down -v

# Build and run the test containers
docker compose -f /home/user/dev/nLic/docker-compose.test.yml up --build --abort-on-container-exit

# Clean up the test containers
docker compose -f /home/user/dev/nLic/docker-compose.test.yml down
