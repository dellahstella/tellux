#!/usr/bin/env bash
# R5 — Garde-fou doctrine anti-fuite (scanner présence FUITE + PROSCRIT).
#
# DÉTECTE et SIGNALE uniquement. N'écrit, ne corrige, ne supprime rien.
# TOUJOURS exit 0 (alert-only : ne casse jamais le build ; le workflow lit la sortie, pas le code retour).
#
# Scanne UNIQUEMENT les surfaces .html publiques servies à la racine.
# Sortie (stdout) : une ligne par finding « FICHIER:LIGNE<TAB>CLASSE<TAB>LABEL ».
# NE RECOPIE JAMAIS la chaîne sensible détectée (seul l'emplacement + la classe).
#
# Le terme confidentiel (raison sociale) vient du secret GH Actions LEAK_TERMS_REGEX
# (variable d'environnement). Absent → la classe raison_sociale est sautée proprement (pas d'échec).
#
# Allowlist : .github/scripts/leak_guard_allowlist.txt (format « fichier<TAB>label »).
# Exception PROSCRIT « cité/réfuté » : un passage proscrit entre guillemets ou accompagné
# d'un marqueur de réfutation sur la même ligne n'est pas signalé (pédagogie, ex. methode-et-limites §3.2).
#
# NB zones gelées (GELÉ-001 / NCRP-001) : traitées par DIFF dans le workflow, pas par ce scanner de présence.

set -uo pipefail
ROOT="${1:-.}"
cd "$ROOT" 2>/dev/null || exit 0
ALLOW=".github/scripts/leak_guard_allowlist.txt"

FILES="index.html app.html patrimoine.html cadre-scientifique.html mairies.html guide-et-glossaire.html methode-et-limites.html transparence.html mentions-legales.html"

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

while IFS=$'\t' read -r cls label rx flags; do
  [ -z "${cls:-}" ] && continue
  scan_rule "$cls" "$label" "$rx" "${flags:-}"
done <<< "$RULES"

if [ -n "${LEAK_TERMS_REGEX:-}" ]; then
  scan_rule "FUITE" "raison_sociale" "$LEAK_TERMS_REGEX" "-i"
else
  echo "WARN: LEAK_TERMS_REGEX absent — classe raison_sociale non scannée (dégradation propre)." >&2
fi

exit 0
