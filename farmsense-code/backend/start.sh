#!/bin/bash
# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# WARNING: Production deployments MUST set these via environment variables
# DO NOT commit actual secrets to version control

cd /home/workspace/Bxthre3/projects/the-farmsense-project/farmsense-code/backend
source venv/bin/activate

export PORT=${PORT:-8000}
export JWT_SECRET=${JWT_SECRET:-"dev-jwt-secret-change-in-production"}
export SECRET_KEY=${SECRET_KEY:-"dev-secret-key-change-in-production-min-32-chars"}
export DATABASE_URL=${DATABASE_URL:-"postgresql://farmsense_user:farmsense_secure_2026@localhost:5432/farmsense_core"}
export TIMESCALE_URL=${TIMESCALE_URL:-"postgresql://farmsense_user:farmsense_secure_2026@localhost:5432/farmsense_timeseries"}
export MAP_DATABASE_URL=${MAP_DATABASE_URL:-"postgresql://farmsense_user:farmsense_secure_2026@localhost:5432/farmsense_core"}

# Validate required env vars in production
if [ "$NODE_ENV" = "production" ]; then
  if [ "$JWT_SECRET" = "dev-jwt-secret-change-in-production" ]; then
    echo "ERROR: JWT_SECRET must be set in production"
    exit 1
  fi
fi

uvicorn app.api.main:app --host 0.0.0.0 --port $PORT