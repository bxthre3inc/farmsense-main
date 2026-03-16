#!/bin/bash
cd "$(dirname "$0")"
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm ci
fi
PORT=${PORT:-5173}
echo "Starting FarmSense Portal on port $PORT..."
npm run dev -- --host --port "$PORT"
