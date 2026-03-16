#!/bin/bash
cd /home/workspace/Bxthre3/the-farmsense-project/farmsense-code/backend
source venv/bin/activate
export PORT=${PORT:-8000}

# Security: Load secrets from environment variables only - never hardcode
# Required env vars: SECRET_KEY, DATABASE_URL, TIMESCALE_URL, MAP_DATABASE_URL
if [ -z "$SECRET_KEY" ]; then
    echo "ERROR: SECRET_KEY environment variable is required"
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL environment variable is required"
    exit 1
fi

export SECRET_KEY
export DATABASE_URL
export TIMESCALE_URL
export MAP_DATABASE_URL

uvicorn app.api.main:app --host 0.0.0.0 --port $PORT
