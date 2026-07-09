#!/usr/bin/env bash
# R5 — Garde-fou doctrine anti-fuite (scanner présence FUITE + PROSCRIT).
#
# DÉTECTE et SIGNALE uniquement. N'écrit, ne corrige, ne supprime rien.
# TOUJOURS exit 0 (alert-only : ne casse jamais le build ; le workflow lit la sortie, pas le code retour).
#
# Périmètre (élargi 2026-06-29, ADR-019) : tous les fichiers TEXTE TRACKÉS sur le repo public
# (= clonables), pas seulement les .html déployés. Surface dérivée de `git ls-files` (les fichiers
# gitignored sont exclus de facto : _drafts/, recherche/, _corpus/, .claude/…), filtrée par extension
# texte + garde-fous (répertoires de données/binaires exclus, cap taille, auto-exclusion des fichiers
# DU garde-fou lui-même). Motivation : le 2026-06-29 un .md tracké (docs/i18n/NOTE_METHODE_CO.md) a
# porté une mention de financement conditionnel et a échappé au scan limité aux .html (fix manuel #893).
#
# Sortie (stdout) : une ligne par finding « FICHIER:LIGNE<TAB>CLASSE<TAB>LABEL ».
# NE RECOPIE JAMAIS la chaîne sensible détectée (seul l'emplacement + la classe).
#
# Le terme confidentiel (raison sociale) vient du secret GH Actions LEAK_TERMS_REGEX
# (variable d'environnement). Absent → la classe raison_sociale est sautée proprement (pas d'échec).
#
# Allowlist : .github/scripts/leak_guard_allowlist.txt (format « chemin<TAB>label »).
# Le « chemin » est relatif à la racine du repo (ex. docs/i18n/NOTE_METHODE_CO.md), ce qui permet
# une allowlist PAR CHEMIN (ex. mentions-legales.html allowliste raison_sociale/siret_spaced pour LCEN).
# Exception PROSCRIT « cité/réfuté » : un passage proscrit entre guillemets ou accompagné
# d'un marqueur de réfutation sur la même ligne n'est pas signalé (pédagogie, ex. methode-et-limites §3.2).
#
# NB zones gelées (GELÉ-001 / NCRP-001) : traitées par DIFF dans le workflow, pas par ce scanner de présence.

set -uo pipefail
trap 'exit 0' EXIT   # alert-only ABSOLU : quoi qu'il arrive (même abort set -u / erreur interne), on sort 0
ROOT="${1:-.}"
cd "$ROOT" 2>/dev/null || exit 0
ALLOW=".github/scripts/leak_guard_allowlist.txt"

# Extensions texte scannées. Les binaires (webp/png/woff2/…) et le code (py/js/sql/…) sont exclus de
# facto (hors whitelist), ce qui réduit le risque de faux positifs et le bruit.
TEXT_EXTS=" html htm md markdown txt yml yaml json jsonc "
SIZE_CAP=$((512 * 1024))   # 512 KiB : anti dump de données / binaire résiduel (faux positifs + perf).

# Construit la liste des fichiers à scanner depuis l'index git (tracké = clonable sur le public).
# Exclut : répertoires de données/binaires, fixtures, lockfiles/manifests npm, et les fichiers DU
# garde-fou lui-même (ils contiennent les termes-déclencheurs → auto-fuite garantie sinon).
list_files() {
  git ls-files -z 2>/dev/null | while IFS= read -r -d '' f; do
    case "$f" in
      docs/assets/*|docs/data/*|public/data/*|_data/*|tests/fixtures/*) continue ;;
      */node_modules/*|*/package-lock.json|*package.json)              continue ;;
      .github/scripts/leak_guard*|.github/workflows/leak-guard.yml)    continue ;;
    esac
    local ext="${f##*.}"
    case "$TEXT_EXTS" in *" $ext "*) : ;; *) continue ;; esac
    local sz
    sz=$(wc -c < "$f" 2>/dev/null || echo 0)
    [ "${sz:-0}" -gt "$SIZE_CAP" ] && continue
    printf '%s\n' "$f"
  done
}

FILES="$(list_files)"

# CLASSE <TAB> LABEL <TAB> REGEX (ERE) <TAB> FLAGS (-i ou vide)
RULES=$(cat <<'RULESEOF'
FUITE	forme_sarl	\bSARL\b
FUITE	forme_sasu	\bSASU\b
FUITE	financement_feder	\bFEDER\b	-i
FUITE	financement_anr	\bANR\b
FUITE	financement_os12	OS ?1[.\-]?2	-i
FUITE	financement_candidature	candidature	-i
FUITE	corpus_repo	tellux-corpus-internal	-i
FUITE	corpus_axes	AXE_[A-R]\b
FUITE	siret_spaced	[0-9]{3}[ .][0-9]{3}[ .][0-9]{3}([ .][0-9]{5})?
FUITE	module_agronomie	agronomie	-i
FUITE	module_batiment	bâtiment	-i
PROSCRIT	deux_realites	deux réalités différentes	-i
PROSCRIT	additionnent_pas	ne s.{0,3}additionnent pas	-i
PROSCRIT	naturel_benin	naturel[^.]{0,12}bénin	-i
RULESEOF
)

is_allowed() { # file label
  [ -f "$ALLOW" ] || return 1
  grep -qE "^[[:space:]]*$1[[:space:]]+$2([[:space:]]|\$)" "$ALLOW"
}

is_cited_refuted() { # line — vrai si le passage est cité (guillemets) ou explicitement réfuté
  printf '%s' "$1" | grep -qE '«|»|inexacte|vectoriel|contenai|formulation'
}

scan_rule() { # class label regex flags
  local cls="$1" label="$2" rx="$3" flags="$4" f m n line
  for f in $FILES; do
    [ -f "$f" ] || continue
    is_allowed "$f" "$label" && continue
    while IFS= read -r m; do
      [ -z "$m" ] && continue
      n="${m%%:*}"; line="${m#*:}"
      if [ "$cls" = "PROSCRIT" ] && is_cited_refuted "$line"; then continue; fi
      printf '%s:%s\t%s\t%s\n' "$f" "$n" "$cls" "$label"
    done < <(grep -nE $flags -- "$rx" "$f" 2>/dev/null)
  done
}

# Anti-endormissement : si aucune surface n'a été énumérée (git absent / index vide), émettre un
# finding VISIBLE pour qu'une issue s'ouvre — évite un faux « 0 finding / run vert » trompeur.
if [ -z "${FILES//[[:space:]]/}" ]; then
  printf '%s\t%s\t%s\n' "(config)" "CONFIG" "aucune_surface_enumeree_git_ls-files_vide"
fi

while IFS=$'\t' read -r cls label rx flags; do
  [ -z "${cls:-}" ] && continue
  scan_rule "$cls" "$label" "$rx" "${flags:-}"
done <<< "$RULES"

if [ -n "${LEAK_TERMS_REGEX:-}" ]; then
  scan_rule "FUITE" "raison_sociale" "$LEAK_TERMS_REGEX" "-i"
else
  echo "WARN: LEAK_TERMS_REGEX absent — classe raison_sociale non scannée (dégradation propre)." >&2
  # Anti-endormissement : émet un finding VISIBLE (stdout) pour qu'une issue s'ouvre.
  # Évite un faux « 0 finding / run vert » alors que la classe la plus sensible n'est pas couverte.
  printf '%s\t%s\t%s\n' "(config)" "CONFIG" "raison_sociale_NON_SCANNEE_secret_absent"
fi

# Marqueurs de MODULES CONFIDENTIELS (portée pré-compétitive) : définis UNIQUEMENT dans le
# secret GH Actions LEAK_CONFIDENTIAL_REGEX (mécanisme non exposant) — volontairement NON
# énumérés ici, ce fichier étant public. Comme la raison sociale (LEAK_TERMS_REGEX), aucun
# terme sensible n'y apparaît en clair. Absent → classe sautée + finding CONFIG (anti-endormissement).
if [ -n "${LEAK_CONFIDENTIAL_REGEX:-}" ]; then
  scan_rule "FUITE" "module_confidentiel" "$LEAK_CONFIDENTIAL_REGEX" "-i"
else
  echo "WARN: LEAK_CONFIDENTIAL_REGEX absent — classe module_confidentiel non scannée (dégradation propre)." >&2
  printf '%s\t%s\t%s\n' "(config)" "CONFIG" "module_confidentiel_NON_SCANNEE_secret_absent"
fi

exit 0
