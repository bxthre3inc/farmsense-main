#!/bin/bash
# FarmSense API Start Script with Environment Variables
# This script exports variables explicitly for supervisord compatibility

cd /home/workspace/Bxthre3/the-farmsense-project/farmsense-code/backend

# Export required environment variables
export PORT="${PORT:-8001}"
export SECRET_KEY="${SECRET_KEY:-}"
export JWT_SECRET="${JWT_SECRET:-}"
export DATABASE_URL="${DATABASE_URL:-}"
export TIMESCALE_URL="${TIMESCALE_URL:-}"
export MAP_DATABASE_URL="${MAP_DATABASE_URL:-}"

# Validate required variables
if [ -z "$SECRET_KEY" ]; then
    echo "ERROR: SECRET_KEY environment variable is required"
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL environment variable is required"
    exit 1
fi

echo "Starting FarmSense API with Supabase connection..."
echo "PORT: $PORT"
echo "DATABASE_URL is set: [yes]"

source venv/bin/activate
uvicorn app.api.main:app --host 0.0.0.0 --port $PORT
