#!/bin/bash
# FarmSense Backend Startup Script
# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

cd /home/workspace/Bxthre3/projects/the-farmsense-project/farmsense-code/backend
source venv/bin/activate

export PORT=${PORT:-8000}

# Validate required env vars in production
if [ "$NODE_ENV" = "production" ]; then
  if [ -z "$JWT_SECRET" ]; then
    echo "ERROR: JWT_SECRET must be set in production"
    exit 1
  fi
  if [ -z "$SECRET_KEY" ]; then
    echo "ERROR: SECRET_KEY must be set in production"
    exit 1
  fi
fi

uvicorn app.api.main:app --host 0.0.0.0 --port $PORT
