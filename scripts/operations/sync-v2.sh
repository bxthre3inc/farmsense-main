#!/bin/bash
# Robust Git Sync v2 - Replaces broken sync.sh

REPO_DIR="/home/workspace/Bxthre3/projects/the-farmsense-project"
LOG_FILE="$REPO_DIR/sync-v2.log"
LOCK_FILE="/tmp/farmsense-sync.lock"
MAX_RETRIES=3
RETRY_DELAY=60

# Prevent concurrent runs
if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "$(date): Sync already running (PID $PID)" >> "$LOG_FILE"
        exit 0
    fi
fi
echo $$ > "$LOCK_FILE"

cd "$REPO_DIR" || exit 1

echo "$(date): Starting sync cycle" >> "$LOG_FILE"

# Check connectivity
if ! git ls-remote origin -h refs/heads/main > /dev/null 2>&1; then
    echo "$(date): No connectivity to origin" >> "$LOG_FILE"
    rm -f "$LOCK_FILE"
    exit 1
fi

# Stash any local changes (including untracked)
git stash push -u -m "Auto-stash before sync $(date)" > /dev/null 2>&1
STASH_CREATED=$?

# Fetch and check divergence
git fetch origin
divergence=$(git rev-list --left-right --count HEAD...origin/main 2>/dev/null | tr '\t' ' ')
behind=$(echo "$divergence" | awk '{print $2}')
ahead=$(echo "$divergence" | awk '{print $1}')

# If behind origin, fast-forward
git merge --ff-only origin/main 2>/dev/null
if [ $? -eq 0 ]; then
    echo "$(date): Fast-forwarded to origin/main" >> "$LOG_FILE"
else
    # Divergence requires merge
    echo "$(date): Divergence detected: $ahead ahead, $behind behind" >> "$LOG_FILE"
    
    # Try merge with auto-resolution favoring theirs for conflicts
    git merge origin/main -X theirs --no-edit > /tmp/merge-output.txt 2>&1
    if [ $? -eq 0 ]; then
        echo "$(date): Merge successful (favoring remote)" >> "$LOG_FILE"
    else
        # Hard conflict - log and alert
        echo "$(date): HARD CONFLICT - requires manual resolution" >> "$LOG_FILE"
        cat /tmp/merge-output.txt >> "$LOG_FILE"
        git merge --abort 2>/dev/null
        
        # Create INBOX alert for manual intervention
        echo "# HARD GIT CONFLICT - Manual Resolution Required
**Time:** $(date)
**Repo:** $REPO_DIR
**Issue:** Auto-merge failed, manual resolution required
**Action:** Run git status in repo directory and resolve conflicts
        " > "/home/workspace/Bxthre3/INBOX/GIT-CONFLICT-$(date +%Y%m%d-%H%M).md"
        
        rm -f "$LOCK_FILE"
        exit 1
    fi
fi

# Push any local commits that survived merge
if [ "$ahead" -gt 0 ]; then
    if git push origin main > /dev/null 2>&1; then
        echo "$(date): Pushed local commits" >> "$LOG_FILE"
    else
        echo "$(date): Push failed - may need manual check" >> "$LOG_FILE"
    fi
fi

# Restore stashed changes (they may conflict - if so, alert)
if [ $STASH_CREATED -eq 0 ]; then
    git stash pop > /tmp/stash-pop.txt 2>&1
    if [ $? -ne 0 ]; then
        echo "$(date): STASH CONFLICT - Stashed changes conflict with remote" >> "$LOG_FILE"
        cat /tmp/stash-pop.txt >> "$LOG_FILE"
        # Create alert
        echo "# STASH CONFLICT - Manual Review Required
**Time:** $(date)
**Issue:** Stashed local changes conflict with remote. Stash preserved.
**Action:** Review with git stash list and git stash show -p
        " > "/home/workspace/Bxthre3/INBOX/STASH-CONFLICT-$(date +%Y%m%d-%H%M).md"
    else
        echo "$(date): Restored stashed changes" >> "$LOG_FILE"
    fi
fi

echo "$(date): Sync cycle complete" >> "$LOG_FILE"
rm -f "$LOCK_FILE"
