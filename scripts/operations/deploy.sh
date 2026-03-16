# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. Architectural Integrity: Implementation must adhere to the Master Software Architecture.
# 2. Synchronized Updates: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. No Ghost Edits: All significant modifications must be documented in the project's audit trail.

# 3. No Ghost Edits: All significant modifications must be documented in the project's audit trail.

#!/bin/bash
# FarmSense Deployment Script
# Pulls latest changes from GitHub and restarts services if needed

set -e

echo "🚀 Deploying FarmSense..."

# Pull latest changes
echo "📥 Pulling latest from origin/main..."
git fetch origin
git pull origin main

# Check if backend changed
if git diff --name-only HEAD@{1} HEAD | grep -q "farmsense-code/backend"; then
    echo "📦 Backend changes detected, restarting services..."
    # Add your service restart commands here
    # Example: systemctl restart farmsense-backend (or your service manager)
fi

# Check if frontend changed
if git diff --name-only HEAD@{1} HEAD | grep -q "farmsense-code/frontend"; then
    echo "🎨 Frontend changes detected, you may need to rebuild..."
    # Add your frontend build commands here
fi

echo "✅ Deployment complete!"
echo "Run 'git log --oneline -5' to see recent changes"