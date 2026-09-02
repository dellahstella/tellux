#!/usr/bin/env bash
# R5 — Garde-fou doctrine anti-fuite (scanner présence FUITE + PROSCRIT + PERSO).
#
# DÉTECTE et SIGNALE uniquement. N'écrit, ne corrige, ne supprime rien.
# TOUJOURS exit 0 (alert-only : ne casse jamais le build ; le workflow lit la sortie, pas le code retour).
# EXCEPTION PERSO (brief I, 2026-09-02, #903 : « alert-only non trié ne protège de rien ») : la
# classe PERSO (données personnelles — adresses, coordonnées de domicile) est BLOQUANTE au gate
# PR, comme FUITE/CONFIG déjà — le scanner reste toujours exit 0 (détecteur), c'est le step
# « Gate bloquant » du workflow qui lit sa sortie et bloque sur ces 3 classes précises.
# FAIL-LOUD (durci 2026-07-10, audit) : toute dégradation du scan lui-même (fichier sauté par le
# cap de taille, régex invalide, grep en échec, scan interrompu avant la fin, secret absent) émet
# un finding CONFIG — bloquant au gate PR. Un scan requis n'est jamais silencieusement partiel.
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
# Alert-only par CODE RETOUR (le workflow lit la sortie, pas le code) — mais plus jamais de
# faux pass sur crash (audit 2026-07-10) : si le script n'atteint pas sa dernière ligne
# (abort set -u, erreur interne), le trap émet un finding CONFIG (bloquant au gate PR,
# fail-closed) au lieu de laisser des findings partiels passer pour un scan complet.
SCAN_COMPLET=0
finish() {
  if [ "${SCAN_COMPLET:-0}" != "1" ]; then
    printf '%s\t%s\t%s\n' "(config)" "CONFIG" "scanner_interrompu_scan_partiel"
  fi
  # Sentinelle POSITIVE (revue évaluateur PR #947) : le gate PR EXIGE cette ligne META.
  # Sans elle (script qui ne se lance même pas — erreur de syntaxe → findings.txt vide mais
  # existant — ou tué avant son trap), le gate échoue. Fail-closed jusqu'au lancement.
  # Classe META = plomberie : exclue du compte de findings et de l'issue (filtre workflow).
  printf '%s\t%s\t%s\n' "(meta)" "META" "sentinelle_fin_de_scan"
  exit 0
}
trap finish EXIT
ROOT="${1:-.}"
cd "$ROOT" 2>/dev/null || exit 0
ALLOW=".github/scripts/leak_guard_allowlist.txt"

# Extensions texte scannées. Les binaires (webp/png/woff2/…) et le code (py/js/sql/…) sont exclus de
# facto (hors whitelist), ce qui réduit le risque de faux positifs et le bruit.
TEXT_EXTS=" html htm md markdown txt yml yaml json jsonc "
# 2 MiB : anti dump de données / binaire résiduel (faux positifs + perf). Relevé de 512 KiB le
# 2026-07-10 (audit) : app.html (~538 Ko, surface publique n°1) dépassait l'ancien cap depuis sa
# création et était SILENCIEUSEMENT exclu de tout le scan de présence. Tout skip-par-cap est
# désormais fail-loud (finding CONFIG, cf. plus bas) — ne jamais re-rendre ce skip silencieux.
SIZE_CAP=$((2 * 1024 * 1024))

# Construit la liste des fichiers à scanner depuis l'index git (tracké = clonable sur le public).
# Exclut : répertoires de données/binaires, fixtures, lockfiles/manifests npm, et les fichiers DU
# garde-fou lui-même (ils contiennent les termes-déclencheurs → auto-fuite garantie sinon).
# Émet des enregistrements typés : « F<TAB>chemin » (à scanner) ou « CAP<TAB>chemin<TAB>taille »
# (au-dessus du cap). Les fichiers sautés par le cap sont ENREGISTRÉS (fail-loud plus bas,
# finding CONFIG), jamais oubliés en silence.
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
    if [ "${sz:-0}" -gt "$SIZE_CAP" ]; then
      printf 'CAP\t%s\t%s\n' "$f" "$sz"
      continue
    fi
    printf 'F\t%s\n' "$f"
  done
}

RAW_LIST="$(list_files)"
FILES="$(printf '%s\n' "$RAW_LIST" | awk -F'\t' '$1=="F"{print $2}')"

# Surface dédiée à la classe PERSO (brief I, 2026-09-02) : scripts/*.json et public/data/*.json.
# public/data/* est exclu de $FILES ci-dessus (list_files()) pour les classes FUITE/PROSCRIT —
# volumes de données, pas de la prose, jamais scannés pour ces motifs-là. La classe PERSO a besoin
# d'y regarder précisément : c'est là qu'a été trouvée (2026-09-02) l'adresse d'une mesure
# résidentielle (public/data/cartoradio_certified_corse.json), servie telle quelle par le site —
# un fichier de données PEUT porter une fuite qu'une prose ne porterait jamais, et inversement.
# scripts/*.json n'a besoin d'aucun ajout : jamais exclu de $FILES, déjà couvert.
list_perso_files() {
  git ls-files -z -- 'scripts/*.json' 'public/data/*.json' 2>/dev/null | while IFS= read -r -d '' f; do
    case "$f" in
      .github/scripts/leak_guard*) continue ;;
    esac
    local sz
    sz=$(wc -c < "$f" 2>/dev/null || echo 0)
    if [ "${sz:-0}" -gt "$SIZE_CAP" ]; then
      printf 'CAP\t%s\t%s\n' "$f" "$sz"
      continue
    fi
    printf 'F\t%s\n' "$f"
  done
}
RAW_PERSO_LIST="$(list_perso_files)"
PERSO_FILES="$(printf '%s\n' "$RAW_PERSO_LIST" | awk -F'\t' '$1=="F"{print $2}')"

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

scan_rule() { # class label regex flags [filelist=$FILES]
  local cls="$1" label="$2" rx="$3" flags="$4" filelist="${5:-$FILES}" f m n line out rc
  # Fail-loud régex (audit 2026-07-10) : une ERE invalide faisait échouer grep en silence
  # (2>/dev/null, code retour perdu) → classe entière non scannée SANS signal. Pré-validation
  # sur /dev/null : 1 = régex valide sans match, ≥ 2 = régex invalide → finding CONFIG
  # (bloquant au gate PR). Le contenu de la régex n'est JAMAIS recopié (label seulement).
  grep -qE $flags -- "$rx" /dev/null 2>/dev/null
  if [ $? -ge 2 ]; then
    printf '%s\t%s\t%s\n' "(config)" "CONFIG" "regex_invalide_${label}"
    return 0
  fi
  for f in $filelist; do
    [ -f "$f" ] || continue
    is_allowed "$f" "$label" && continue
    out=$(grep -nE $flags -- "$rx" "$f" 2>/dev/null); rc=$?
    if [ "$rc" -ge 2 ]; then
      # grep a planté sur CE fichier (illisible, etc.) : fichier non scanné pour cette classe
      # → fail-loud, pas de trou silencieux.
      printf '%s\t%s\t%s\n' "$f" "CONFIG" "grep_echec_${label}"
      continue
    fi
    [ "$rc" -ne 0 ] && continue
    while IFS= read -r m; do
      [ -z "$m" ] && continue
      n="${m%%:*}"; line="${m#*:}"
      if [ "$cls" = "PROSCRIT" ] && is_cited_refuted "$line"; then continue; fi
      printf '%s:%s\t%s\t%s\n' "$f" "$n" "$cls" "$label"
    done <<< "$out"
  done
}

# Anti-endormissement : si aucune surface n'a été énumérée (git absent / index vide), émettre un
# finding VISIBLE pour qu'une issue s'ouvre — évite un faux « 0 finding / run vert » trompeur.
if [ -z "${FILES//[[:space:]]/}" ]; then
  printf '%s\t%s\t%s\n' "(config)" "CONFIG" "aucune_surface_enumeree_git_ls-files_vide"
fi

# Fail-loud skip-par-cap (audit 2026-07-10) : tout fichier texte tracké au-dessus du cap émet
# un finding CONFIG (bloquant au gate PR) — un skip DÉLIBÉRÉ se déclare dans l'allowlist
# (« chemin<TAB>cap_taille »), jamais en silence. Précédent : app.html sauté depuis avril 2026.
printf '%s\n' "$RAW_LIST" | awk -F'\t' '$1=="CAP"{print $2 "\t" $3}' | while IFS=$'\t' read -r f sz; do
  [ -z "$f" ] && continue
  is_allowed "$f" "cap_taille" && continue
  printf '%s\t%s\t%s\n' "$f" "CONFIG" "saute_cap_taille_${sz}o_NON_SCANNE"
done

while IFS=$'\t' read -r cls label rx flags; do
  [ -z "${cls:-}" ] && continue
  scan_rule "$cls" "$label" "$rx" "${flags:-}"
done <<< "$RULES"

# Fail-loud skip-par-cap pour la surface PERSO (même discipline que $FILES plus haut) : un
# scripts/*.json ou public/data/*.json au-dessus du cap de taille n'est jamais sauté en silence.
printf '%s\n' "$RAW_PERSO_LIST" | awk -F'\t' '$1=="CAP"{print $2 "\t" $3}' | while IFS=$'\t' read -r f sz; do
  [ -z "$f" ] && continue
  is_allowed "$f" "cap_taille" && continue
  printf '%s\t%s\t%s\n' "$f" "CONFIG" "saute_cap_taille_${sz}o_NON_SCANNE_perso"
done

# Classe PERSO (brief I, 2026-09-02) — BLOQUANTE au gate PR (cf. en-tête).
#
# PAS un grep ligne à ligne, DÉLIBÉRÉMENT : un motif nu sur "adresse_complete"/"voie"/
# "code_postal" matche AUSSI les fiches extérieur public de public/data/cartoradio_certified_corse.json
# (151/236, adresse de mesure sur la voie publique — légitime, pas une fuite) — testé, constaté
# en écrivant cette règle : un grep nu aurait bloqué CE FICHIER PRODUCTION en permanence, sur du
# contenu attendu. Détection par CO-OCCURRENCE dans le même enregistrement plutôt : « champ
# d'adresse » + « marqueur résidentiel », l'un sans l'autre n'est pas une fuite. Chaque
# enregistrement JSON est délimité par sa clé d'identifiant ("id":/"numero":, les deux schémas
# rencontrés le 2026-09-02) — pas un vrai parseur JSON, une segmentation par ligne-marqueur
# suffisante pour ce format (un enregistrement par bloc, jamais imbriqué).
# Coordonnées GPS (« >3 décimales hors couche de référence ») délibérément absentes : testé
# mentalement contre les couches géo légitimes du repo (antennes ANFR, radon, patrimoine — toutes
# précises par nature), écarté comme trop bruyant pour rester exploitable. Non implémentée plutôt
# que livrée peu fiable — cf. dette CARTORADIO-INGESTION-PERSO-CONVENTION-001 (registre privé).
# Vérifié avant merge (pas supposé) sur les deux fichiers réels de l'incident (copies hors dépôt) :
# 8/8 puis 77/77 détectés sur les versions AVANT correctif ; 0/0 sur la version corrigée.
scan_perso_coocurrence() { # label field_regex context_regex filelist
  local label="$1" field_rx="$2" ctx_rx="$3" filelist="$4" f
  for f in $filelist; do
    [ -f "$f" ] || continue
    is_allowed "$f" "$label" && continue
    awk -v FRX="$field_rx" -v CRX="$ctx_rx" -v FIL="$f" -v LBL="$label" '
      function flush() {
        if (buf != "" && buf ~ CRX && buf ~ FRX) {
          print FIL ":" startline "\tPERSO\t" LBL
        }
      }
      /"(id|numero)"[ \t]*:/ { flush(); buf=""; startline=NR }
      { buf = buf "\n" $0 }
      END { flush() }
    ' "$f"
  done
}
scan_perso_coocurrence "adresse_voie_residentiel" \
  '"(adresse_complete|voie)"[ \t]*:[ \t]*"[^"]' \
  '"type_environnement"[ \t]*:[ \t]*"residentiel"|"environnement"[ \t]*:[ \t]*"Lieu d.habitation"' \
  "$PERSO_FILES"
scan_perso_coocurrence "code_postal_residentiel" \
  '"code_postal"[ \t]*:[ \t]*"[0-9]{5}"' \
  '"type_environnement"[ \t]*:[ \t]*"residentiel"|"environnement"[ \t]*:[ \t]*"Lieu d.habitation"' \
  "$PERSO_FILES"

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

SCAN_COMPLET=1
exit 0
