#!/bin/bash
# Script de démarrage session Cowork — à exécuter en DÉBUT de chaque session
# Usage : bash scripts/cowork_start.sh "Description courte de la session"

SESSION_DESC="${1:-session-sans-description}"
SENTINEL_FILE="/tmp/tellux_sentinel_$(date +%s).txt"
SENTINEL_PATH_FILE=".cowork_sentinel_path"

echo "$SENTINEL_FILE" > "$SENTINEL_PATH_FILE"
echo "TELLUX_COWORK_SENTINEL|$(date -Iseconds)|$SESSION_DESC" > "$SENTINEL_FILE"

echo "=== COWORK SESSION START ==="
echo "Sentinel : $SENTINEL_FILE"
echo "Session  : $SESSION_DESC"
echo "Date     : $(date)"
echo ""
echo "=== GIT STATUS ==="
git status --short | head -30
echo ""
echo "=== BRANCHE ACTIVE ==="
git branch --show-current || echo "HEAD DETACHÉ"
echo ""
echo "=== DERNIERS COMMITS ==="
git log --oneline -5
