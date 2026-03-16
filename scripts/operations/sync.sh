# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. Architectural Integrity: Implementation must adhere to the Master Software Architecture.
# 2. Synchronized Updates: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. No Ghost Edits: All significant modifications must be documented in the project's audit trail.

# 3. No Ghost Edits: All significant modifications must be documented in the project's audit trail.

#!/bin/bash
# FarmSense Auto-Sync Script
# Syncs changes between Antigravity IDE and Zo Computer

# Dynamically find the current script directory (works across environments)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

LOG_FILE="$DIR/sync.log"

echo "$(date): Auto-sync script started" >> "$LOG_FILE"

while true; do
  # 1. Check for internet connectivity via git (bypasses ICMP/ping blocks on restricted networks)
  if ! git ls-remote origin -h refs/heads/main > /dev/null 2>&1; then
    echo "$(date): No internet connection to repository, waiting..." >> "$LOG_FILE"
    sleep 60
    continue
  fi
  
  # 2. Commit any uncommitted local changes FIRST so they aren't lost or ignored
  if [ -n "$(git status --porcelain)" ]; then
    git add . > /dev/null 2>&1
    git commit -m "Auto-sync: Updates from edge/device" > /dev/null 2>&1
    echo "$(date): Committed local changes" >> "$LOG_FILE"
  fi
  
  # 3. Fetch remote changes
  git fetch origin > /dev/null 2>&1
  
  # 4. Compare local branch vs remote tracking branch
  LOCAL=$(git rev-parse HEAD 2>/dev/null)
  REMOTE=$(git rev-parse origin/main 2>/dev/null)
  
  if [ "$LOCAL" != "$REMOTE" ]; then
    echo "$(date): Divergence detected, syncing..." >> "$LOG_FILE"
    
    # Attempt to rebase our commits on top of incoming remote changes
    PULL_RESULT=$(git pull --rebase origin main 2>&1)
    
    if [ $? -eq 0 ]; then
      echo "$(date): Pull/Rebase successful" >> "$LOG_FILE"
      
      # Now check if we are ahead of remote, if so, push
      NEW_LOCAL=$(git rev-parse HEAD 2>/dev/null)
      if [ "$NEW_LOCAL" != "$REMOTE" ]; then
        if git push origin main > /dev/null 2>&1; then
          echo "$(date): Pushed local changes successfully" >> "$LOG_FILE"
        else
          echo "$(date): Push failed" >> "$LOG_FILE"
        fi
      fi
    else
      echo "$(date): Pull failed (conflict): $PULL_RESULT" >> "$LOG_FILE"
      # If a rebase conflict occurs, abort it to prevent leaving git in a broken state
      git rebase --abort > /dev/null 2>&1
    fi
  fi
  
  sleep 30
done