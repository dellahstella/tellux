#!/bin/bash
# Script de fermeture session Cowork — à exécuter en FIN de chaque session
# Usage : bash scripts/cowork_end.sh

SENTINEL_PATH_FILE=".cowork_sentinel_path"

echo "=== COWORK SESSION END ==="

# Vérification sentinel
if [ ! -f "$SENTINEL_PATH_FILE" ]; then
  echo "⚠️  SENTINEL PATH ABSENT — cowork_start.sh n'a pas été exécuté ou sandbox a rotaté"
else
  SENTINEL_FILE=$(cat "$SENTINEL_PATH_FILE")
  if [ ! -f "$SENTINEL_FILE" ]; then
    echo "🔴 SENTINEL ABSENT DU DISQUE — RISQUE DE PERTE DE PRODUCTION"
    echo "   Fichier attendu : $SENTINEL_FILE"
    echo "   → Vérifier manuellement chaque fichier produit avant de fermer"
  else
    echo "✅ Sentinel OK : $(cat $SENTINEL_FILE)"
  fi
fi

echo ""
echo "=== FICHIERS MODIFIÉS (git) ==="
git status --short

echo ""
echo "=== FICHIERS RÉCENTS SUR DISQUE (30 dernières minutes) ==="
find . -newer .git/index -not -path "./.git/*" -not -path "./node_modules/*" \
  -type f | grep -v "__pycache__" | head -30

echo ""
echo "=== STASH EXISTANTS ==="
git stash list

echo ""
echo "=== ACTION REQUISE ==="
echo "Transmettre ce rapport à Claude chat pour décision commit/stash"
rm -f "$SENTINEL_PATH_FILE"
