#!/bin/bash
if [ ! -f .env ]; then
  echo "Creating .env file..."
  cp .env.example .env
fi
