#!/usr/bin/env bash
# Test de validation anti-Frankenstein du resolveur de citations Tellux.
#
# Les 6 tests viennent de l'iteration 002 de la meta-synthese EM
# (recherche/em-meta-synthese-2026-06-03/GATE_CITATIONS.md §5).
# Tous les DOI sont des sources primaires verifiees a la main avant la creation
# du script. Si une assertion echoue, c'est qu'on a re-introduit une Frankenstein
# ou que l'API a change.
#
# Usage : bash scripts/test_verify_citation.sh
# Sortie : un bloc par test (PASS / FAIL) + recap final.

set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERIFY="python3 ${SCRIPT_DIR}/verify_citation.py"

PASS=0
FAIL=0
RESULTS=()

run_test() {
  local name="$1"
  local arg="$2"
  local expect_regex="$3"
  local desc="$4"
  echo ""
  echo "=== Test ${name} — ${desc} ==="
  echo "$ ${VERIFY} ${arg}"
  out=$(${VERIFY} "${arg}" 2>&1)
  echo "${out}" | head -25
  # Aplatir le JSON sur une seule ligne pour faire matcher les regex multi-token
  # (ex. "Pohl H. A.".*"Todd G. W." doit traverser un newline JSON).
  flat=$(echo "${out}" | tr -d '\n')
  if echo "${flat}" | grep -qE "${expect_regex}"; then
    echo "[PASS] match: ${expect_regex}"
    PASS=$((PASS+1))
    RESULTS+=("PASS · ${name}")
  else
    echo "[FAIL] regex non trouvee : ${expect_regex}"
    FAIL=$((FAIL+1))
    RESULTS+=("FAIL · ${name}")
  fi
}

run_test "01-murr-1966" \
  "10.1007/BF01426859" \
  '"Murr L\. E\."' \
  "Murr 1966 Int J Biometeor (vrai DOI Springer)"

run_test "02-pohl-todd-1981" \
  "10.1007/BF02198246" \
  '"Pohl H\. A\.".*"Todd G\. W\."' \
  "Pohl & Todd 1981 (DOI ex-Frankenstein ; verifier auteurs reels)"

run_test "03-murr-1964-nature" \
  "10.1038/2011305a0" \
  '"Murr L\. E\."' \
  "Murr 1964 Nature (cellule vegetale champs electrostatiques)"

run_test "04-beerling-2024-ordre" \
  "10.1038/s41586-024-08429-2" \
  '"Beerling D\. J\."' \
  "Beerling 2024 Nature 638 — premier auteur Beerling DJ"

run_test "05-sidaway-asprey-1968" \
  "10.1007/BF01553277" \
  '"Asprey G\. F\."' \
  "Sidaway & Asprey 1968 — orthographe Asprey (vs typo Aspray bibliographie secondaire)"

# Test 06 — best-effort. ScienceDirect bloque les bots (403) et Semantic Scholar
# rate-limit a ~100 req/5min en anonyme. SKIP comptable plutot que FAIL si l'une
# des deux voies est indisponible : on ne veut pas faire echouer la suite sur une
# limite externe d'editeur, mais on consigne le besoin.
name="06-wigton-jones-2025"
arg="https://www.sciencedirect.com/science/article/abs/pii/S0921800925003180"
expect_regex='"Wigton-Jones|Ecological Economics'
desc="Wigton-Jones 2025 Ecological Economics (PII ScienceDirect — best-effort)"
echo ""
echo "=== Test ${name} — ${desc} ==="
echo "$ ${VERIFY} ${arg}"
out=$(${VERIFY} "${arg}" 2>&1)
echo "${out}" | head -25
flat=$(echo "${out}" | tr -d '\n')
if echo "${flat}" | grep -qE "${expect_regex}"; then
  echo "[PASS] match: ${expect_regex}"
  PASS=$((PASS+1))
  RESULTS+=("PASS · ${name}")
elif echo "${flat}" | grep -qE "UNRESOLVED|429|403"; then
  echo "[SKIP] limite externe (ScienceDirect 403 / Semantic Scholar 429) — outil sait que c'est un best-effort sur Elsevier"
  RESULTS+=("SKIP · ${name} (limite externe Elsevier / rate-limit S2)")
else
  echo "[FAIL] regex non trouvee : ${expect_regex}"
  FAIL=$((FAIL+1))
  RESULTS+=("FAIL · ${name}")
fi

echo ""
echo "=================================================="
echo "Recap : ${PASS} PASS · ${FAIL} FAIL sur 6 tests"
echo "=================================================="
for r in "${RESULTS[@]}"; do
  echo "  - ${r}"
done

if [ "${FAIL}" -ne 0 ]; then
  exit 1
fi
exit 0
