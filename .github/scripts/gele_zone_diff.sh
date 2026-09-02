#!/usr/bin/env bash
# GELE — détecteur de modification des zones gelées d'app.html, par EXTRACTION + COMPARAISON
# de contenu (brief O, 2026-09-02 : « la détection doit être par nature du changement, pas
# par grep nu »).
#
# Remplace le grep-sur-diff historique (leak-guard.yml, step « Diff zones gelées » avant ce
# commit) : celui-ci comptait toute ligne AJOUTÉE/RETIRÉE du diff contenant les MOTS
# "EXPERT_WEIGHTS_DEFAULT"/"EXPERT_BOUNDS_DEFAULT"/"EXPERT_EPISTEMIC_NOTE"/"calcGammaAmbient"/
# "NCRP" en sous-chaîne, n'importe où dans le fichier. Vérifié par grep direct (brief O, étape 1) :
# ces mots apparaissent aussi dans des DIZAINES de lignes de commentaires/références sans
# rapport, dispersées dans tout app.html (ex. lignes citant "NCRP-001 intact" en prose pour
# expliquer POURQUOI un autre calcul n'y touche pas). Un PR modifiant l'une de ces lignes de
# commentaire aurait déclenché un GELE bloquant sur du contenu qui n'a JAMAIS touché une valeur
# gelée — exactement le risque nommé par le brief : « un détecteur qui se déclenche sur toute
# mention d'une constante gelée bloquerait des PR légitimes et finirait désactivé ».
#
# Principe : pour chaque zone nommée, extraire son texte EXACT depuis BASE et HEAD (ancré par
# un motif stable — regex de déclaration, jamais un numéro de ligne codé en dur, qui dérive au
# fil des éditions ailleurs dans le fichier), puis comparer les deux extraits octet à octet.
# Une mention du nom hors de sa propre déclaration ne peut plus matcher — seule la VALEUR
# déclarée compte. Insensible à la dérive de ligne (les deux extractions sont refaites à
# chaque appel, sur le contenu réel de chaque révision).
#
# Périmètre actuel (5 zones — cf. CLAUDE.md local / registre ADR pour la doctrine complète) :
#   EXPERT_WEIGHTS_DEFAULT  (GELÉ-001a — verrou physicien tiers MAINTENU)
#   EXPERT_EPISTEMIC_NOTE   (GELÉ-001a — idem)
#   EXPERT_BOUNDS_DEFAULT   (GELÉ-001b — re-dérivable EN INTERNE sous conditions strictes depuis
#                            ADR-042/047, mais reste Cran C : aucune régression d'auto-merge,
#                            "recalage en zone gelée ≠ jamais mécanique" demeure — un finding ici
#                            n'est PAS une fausse alerte même si la valeur est légitimement
#                            re-dérivable, seul QUI peut l'approuver diffère de GELÉ-001a)
#   GAMMA_TERRESTRE_PAR_LITHOTYPE (NCRP-001 — bloc de données sous Cran C explicite, cf.
#                            commentaire app.html ~L7428 : « dégel d'une composante déjà
#                            publique sous double zone gelée... PR non auto-mergée »)
#   CONVERSION_NGY_TO_NSV   (NCRP-001 — coefficient de conversion nGy→nSv, fait partie de la
#                            formule au même titre que les coefficients Verdoya ; absent du
#                            périmètre grep-nu historique alors que c'est un vrai levier de la
#                            formule NCRP 94)
#
# GAP CONNU, SIGNALÉ (pas masqué, brief O étape 3) : ce périmètre ne couvre PAS le gating
# ACTIVE.foretdense / calcVegetationAttenuation() dans RF_field() — le contenu réel touché par
# la dette CLASSIFICATION-ZONE-GELEE-PR1068-001. Aucun symbole de cette dette ne figure dans le
# pattern grep-nu historique NI dans la liste ci-dessus : un détecteur par étendue de ligne bien
# conçu sur le périmètre ACTUEL ne rattrape PAS ce cas — c'est un gap de PÉRIMÈTRE (quels
# symboles comptent comme "zone gelée"), pas une imprécision technique de ce script. Étendre le
# périmètre est une décision de classification doctrine : proposée à Soleil (cf. rapport brief O),
# jamais auto-adoptée ici.
#
# Sortie (stdout) : une ligne par finding « FICHIER:LIGNE<TAB>GELE<TAB>label », même format que
# leak_guard.sh (le gate PR lit les deux fichiers de la même façon). Le "LIGNE" est toujours le
# littéral "diff" (comme l'implémentation précédente) : le diff exact n'est jamais recopié, par
# doctrine (ne jamais recopier une valeur potentiellement sensible/en cours d'arbitrage).
# Toujours exit 0 (détecteur, pas un gate — cf. leak-guard.yml pour le step qui bloque).
#
# Usage : gele_zone_diff.sh <base_sha> <head_sha> [fichier=app.html]

set -uo pipefail
BASE="${1:?usage: gele_zone_diff.sh <base_sha> <head_sha> [file]}"
HEAD="${2:?usage: gele_zone_diff.sh <base_sha> <head_sha> [file]}"
FILE="${3:-app.html}"

# ZONEID<TAB>LABEL<TAB>ANCHOR_REGEX(ERE)<TAB>MODE(single|block)
# Ancre = motif de la ligne de DÉCLARATION uniquement (pas une mention/usage ailleurs).
ZONES=$(cat <<'ZONESEOF'
GELE-001a	expert_weights_default	^const EXPERT_WEIGHTS_DEFAULT	single
GELE-001b	expert_bounds_default	^const EXPERT_BOUNDS_DEFAULT	single
GELE-001a	expert_epistemic_note	^const EXPERT_EPISTEMIC_NOTE	single
NCRP-001	gamma_terrestre_par_lithotype	^const GAMMA_TERRESTRE_PAR_LITHOTYPE	block
NCRP-001	conversion_ngy_to_nsv	const CONVERSION_NGY_TO_NSV	single
ZONESEOF
)

# extract_zone sha anchor mode — imprime le texte de la zone sur stdout, code retour 0 si
# trouvée, 1 si absente de cette révision (fichier absent, ou ancre introuvable).
extract_zone() {
  local sha="$1" anchor="$2" mode="$3" content start end
  content=$(git show "${sha}:${FILE}" 2>/dev/null) || return 1
  [ -z "$content" ] && return 1
  start=$(printf '%s\n' "$content" | grep -nE -- "$anchor" | head -1 | cut -d: -f1)
  [ -z "${start:-}" ] && return 1
  if [ "$mode" = "single" ]; then
    printf '%s\n' "$content" | sed -n "${start}p"
  else
    # bloc : de la ligne d'ancrage jusqu'à la première ligne EXACTEMENT "};" qui suit.
    end=$(printf '%s\n' "$content" | tail -n "+${start}" | grep -nE '^\};[[:space:]]*$' | head -1 | cut -d: -f1)
    [ -z "${end:-}" ] && return 1
    end=$((start + end - 1))
    printf '%s\n' "$content" | sed -n "${start},${end}p"
  fi
}

while IFS=$'\t' read -r zoneid label anchor mode; do
  [ -z "${zoneid:-}" ] && continue
  BASE_TXT=$(extract_zone "$BASE" "$anchor" "$mode"); BASE_RC=$?
  HEAD_TXT=$(extract_zone "$HEAD" "$anchor" "$mode"); HEAD_RC=$?

  if [ "$BASE_RC" -ne 0 ] && [ "$HEAD_RC" -ne 0 ]; then
    continue  # zone absente des deux révisions (base antérieure à son introduction) — rien à comparer.
  fi
  if [ "$BASE_RC" -eq 0 ] && [ "$HEAD_RC" -ne 0 ]; then
    # Présente en BASE, disparue en HEAD : renommage/restructuration de la déclaration elle-même.
    # Traité comme un finding GELE (au moins aussi significatif qu'un changement de valeur —
    # un ancrage qui disparaît fait perdre la couverture de CE détecteur pour tous les PR suivants).
    printf '%s:diff\tGELE\t%s(%s_declaration_disparue)\n' "$FILE" "$zoneid" "$label"
    continue
  fi
  if [ "$BASE_RC" -ne 0 ] && [ "$HEAD_RC" -eq 0 ]; then
    continue  # absente de BASE, présente en HEAD : première introduction, pas une modification.
  fi
  if [ "$BASE_TXT" != "$HEAD_TXT" ]; then
    printf '%s:diff\tGELE\t%s(%s_modifiee)\n' "$FILE" "$zoneid" "$label"
  fi
done <<< "$ZONES"
