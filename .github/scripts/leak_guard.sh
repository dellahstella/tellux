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
# Élargi le 2026-09-24 (brief FUITE_APERCUS_CLOUDFLARE, volet II) au code et à la configuration
# (.py .mjs .js .cjs .sql .sh .css .tsv .svg .geojson, fichiers « point » et fichiers sans extension) :
# deux fichiers .sql et .py nommaient le dépôt privé sans que le garde les lise, alors que tout
# fichier tracké est aussi SERVI sur le site (Cloudflare Pages publie la racine du dépôt).
# PROPRIÉTÉ, et non inventaire : hors répertoires exclus, toute extension tracée qui n'est ni texte
# (TEXT_EXTS/TEXT_NAMES) ni binaire déclaré (BINARY_EXTS, médias et polices seulement : un PDF ou un
# DOCX n'y figure PAS et force donc une décision) émet un finding CONFIG bloquant — une extension
# nouvelle force une décision au lieu de rester aveugle en silence. Témoins :
# .github/scripts/leak_guard_temoins.sh, exécuté par le workflow avant chaque scan (un fichier par
# extension couverte doit être détecté ; plancher : aucune extension texte ne peut en sortir en silence).
#
# LIMITES CONNUES (ce que le garde NE voit PAS) :
#   - Il ne lit que `git ls-files` : un fichier NON SUIVI n'est jamais scanné, même s'il est publié
#     ailleurs (déploiement fait depuis un disque local, artefact de CI, fichier généré puis déposé à
#     la main). Il n'accepte pas de fichier en argument, seulement une racine de dépôt git (un fichier
#     passé en argument ne rend que CONFIG scanner_interrompu). Pour relire un fichier non suivi — ex.
#     MANIFESTE_ETAT.md, que la procédure de clôture demande de faire relire « au scan anti-fuite » :
#     le copier dans un dépôt jetable (git init ; git add), y copier .github/scripts/leak_guard.sh, lancer
#     le garde sur ce dépôt. Hors CI, sans les secrets (LEAK_TERMS_REGEX, LEAK_CONFIDENTIAL_REGEX,
#     LEAK_CORPUS_REPO_REGEX), les classes raison_sociale, module_confidentiel et corpus_repo ne sont PAS
#     lues : chacune émet un CONFIG, et un résultat sans FUITE n'est pas un feu vert.
#   - Les répertoires exclus ci-dessous (docs/assets, docs/data, public/data, _data, tests/fixtures)
#     restent aveugles aux classes FUITE/PROSCRIT (seule PERSO lit public/data/*.json), et une extension
#     inconnue n'y émet aucun CONFIG.
#   - Ses propres fichiers (leak_guard.sh, son allowlist, sa dette, ses témoins, leak-guard.yml), ainsi
#     que package.json et node_modules, ne sont jamais scannés — mais ils sont servis. La table RULES
#     ci-dessous porte donc ses motifs en clair : n'y figure que ce qui peut être public. Un motif qui
#     serait lui-même une fuite va dans un secret (raison sociale, modules confidentiels, et depuis le
#     brief EXPOSITIONS_ET_GARDE du 2026-09-25 le nom du dépôt privé, que RULES publiait jusque-là).
#     Ce qui a été retiré de RULES reste lisible dans l'historique git : seul l'état courant est propre.
#   - Il ne voit que l'état COURANT : ni l'historique, ni les tags, ni les déploiements d'aperçu déjà
#     publiés (qui gardent l'arbre de leur commit, cf. inventaire privé du 2026-09-24).
#
# Dette connue : .github/scripts/leak_guard_dette.txt (« chemin<TAB>label<TAB>empreinte »). Une
# EXPOSITION RÉELLE déjà présente, en attente d'une décision (Cran C), y est inscrite avec
# l'empreinte de SA ligne : UNE occurrence de cette ligne ressort en classe DETTE (signalée, non
# bloquante) ; toute autre occurrence — ligne différente, copie identique, autre fichier — reste
# FUITE (bloquante) ; une entrée qui ne correspond plus à rien émet un CONFIG bloquant (dette
# corrigée → retirer l'entrée dans la même PR). Ce n'est PAS l'allowlist : l'allowlist tait un faux
# positif pour toujours, la dette nomme une fuite à corriger.
#
# Sortie (stdout) : une ligne par finding « FICHIER:LIGNE<TAB>CLASSE<TAB>LABEL ».
# NE RECOPIE JAMAIS la chaîne sensible détectée (seul l'emplacement + la classe).
#
# Motifs tenus en secret (secrets GitHub Actions, passés en variables d'environnement) : raison
# sociale (LEAK_TERMS_REGEX), modules confidentiels (LEAK_CONFIDENTIAL_REGEX), nom du dépôt privé
# (LEAK_CORPUS_REPO_REGEX). Secret absent ou vide → la classe n'est pas lue ET un CONFIG bloquant est
# émis, jamais un passage silencieux (cf. scan_secret plus bas).
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
  rm -f "${DETTE_VUES:-}" "${DETTE_NORM:-}" 2>/dev/null
  exit 0
}
trap finish EXIT
ROOT="${1:-.}"
cd "$ROOT" 2>/dev/null || exit 0
ALLOW=".github/scripts/leak_guard_allowlist.txt"
DETTE_FILE=".github/scripts/leak_guard_dette.txt"
DETTE_VUES="$(mktemp)"
DETTE_NORM="$(mktemp)"
# Labels dont la classe n'a pas été lue (secret absent, motif refusé, régex invalide) : leur dette
# ne peut pas être dite « périmée » — elle n'a pas été évaluée (cf. fin de script).
NON_EVALUES=" "
# Copie normalisée (sans CR ni commentaires) : une entrée saisie sous Windows doit correspondre.
if [ -f "$DETTE_FILE" ]; then
  tr -d '\r' < "$DETTE_FILE" | sed -e '1s/^\xEF\xBB\xBF//' -e 's/[[:space:]]*$//' \
    | grep -vE '^[[:space:]]*(#|$)' > "$DETTE_NORM"
  if ! command -v sha256sum >/dev/null 2>&1; then
    printf '%s\t%s\t%s\n' "(config)" "CONFIG" "sha256sum_absent_dette_non_evaluee"
  fi
fi

# Extensions texte scannées (élargies le 2026-09-24 au code et à la configuration, cf. en-tête).
# Comparaison en minuscules : un .MD ou un .Py n'échappe plus au scan.
TEXT_EXTS=" html htm md markdown txt yml yaml json jsonc geojson py mjs js cjs sql sh css tsv svg gitignore gitattributes htmlhintrc assetsignore "
# Fichiers sans extension lus comme du texte (nom exact du fichier, sans le chemin).
TEXT_NAMES=" LICENSE _headers _redirects pre-commit "
# Binaires déclarés : jamais scannés. Toute autre extension → CONFIG extension_non_classee (bloquant).
BINARY_EXTS=" webp png jpg jpeg gif ico bmp avif woff woff2 ttf otf eot mp3 mp4 webm "
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
      .github/scripts/leak_guard.sh|.github/scripts/leak_guard_allowlist.txt|.github/scripts/leak_guard_dette.txt|.github/scripts/leak_guard_temoins.sh|.github/workflows/leak-guard.yml) continue ;;
    esac
    local base="${f##*/}" ext
    if [ "${base#*.}" = "$base" ]; then
      # Aucun point dans le nom : fichier sans extension, lu seulement s'il est déclaré texte.
      case "$TEXT_NAMES" in *" $base "*) : ;; *) printf 'UNK\t%s\t%s\n' "$f" "sans_extension"; continue ;; esac
    else
      ext="${base##*.}"; ext="${ext,,}"
      case "$TEXT_EXTS" in
        *" $ext "*) : ;;
        *) case "$BINARY_EXTS" in *" $ext "*) continue ;; *) printf 'UNK\t%s\t%s\n' "$f" "$ext"; continue ;; esac ;;
      esac
    fi
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
  local cls="$1" label="$2" rx="$3" flags="$4" filelist="${5:-$FILES}" f m n line out rc h
  # Fail-loud régex (audit 2026-07-10) : une ERE invalide faisait échouer grep en silence
  # (2>/dev/null, code retour perdu) → classe entière non scannée SANS signal. Pré-validation
  # sur /dev/null : 1 = régex valide sans match, ≥ 2 = régex invalide → finding CONFIG
  # (bloquant au gate PR). Le contenu de la régex n'est JAMAIS recopié (label seulement).
  grep -qE $flags -- "$rx" /dev/null 2>/dev/null
  if [ $? -ge 2 ]; then
    printf '%s\t%s\t%s\n' "(config)" "CONFIG" "regex_invalide_${label}"
    NON_EVALUES="$NON_EVALUES$label "
    return 0
  fi
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    [ -f "$f" ] || continue
    is_allowed "$f" "$label" && continue
    # -a : lire comme du texte même avec un octet NUL ou non UTF-8 ; sans lui, GNU grep ≥ 3.5
    # retire en silence les lignes d'un fichier jugé binaire (message sur stderr, rc=0).
    out=$(grep -anE $flags -- "$rx" "$f" 2>/dev/null); rc=$?
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
      # Dette connue : même fichier, même label, même ligne (empreinte) → DETTE, non bloquante.
      if [ -s "$DETTE_NORM" ]; then
        h=$(printf '%s' "${line%$'\r'}" | sha256sum 2>/dev/null | cut -c1-16)
        # Une entrée ne couvre qu'UNE occurrence : une copie identique de la ligne reste FUITE.
        if [ -n "$h" ] && grep -qxF "$f"$'\t'"$label"$'\t'"$h" "$DETTE_NORM" \
           && ! grep -qxF "$f"$'\t'"$label"$'\t'"$h" "$DETTE_VUES"; then
          printf '%s\t%s\t%s\n' "$f" "$label" "$h" >> "$DETTE_VUES"
          printf '%s:%s\t%s\t%s\n' "$f" "$n" "DETTE" "$label"
          continue
        fi
      fi
      printf '%s:%s\t%s\t%s\n' "$f" "$n" "$cls" "$label"
    done <<< "$out"
  done <<< "$filelist"   # une ligne par chemin : un nom avec espace n'est plus découpé
}

# Anti-endormissement : si aucune surface n'a été énumérée (git absent / index vide), émettre un
# finding VISIBLE pour qu'une issue s'ouvre — évite un faux « 0 finding / run vert » trompeur.
if [ -z "${FILES//[[:space:]]/}" ]; then
  printf '%s\t%s\t%s\n' "(config)" "CONFIG" "aucune_surface_enumeree_git_ls-files_vide"
fi

# Extension non classée (2026-09-24) : ni texte ni binaire déclaré → CONFIG bloquant. Décider
# explicitement (TEXT_EXTS, TEXT_NAMES ou BINARY_EXTS) plutôt que laisser un fichier servi hors scan.
printf '%s\n' "$RAW_LIST" | awk -F'\t' '$1=="UNK"{print $2 "\t" $3}' | while IFS=$'\t' read -r f ext; do
  [ -z "$f" ] && continue
  printf '%s\t%s\t%s\n' "$f" "CONFIG" "extension_non_classee_${ext}"
done

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
# Coordonnées GPS (« >3 décimales hors couche de référence ») : hors de cette classe, et la raison
# est MESURÉE, et non estimée, depuis le 2026-09-12.
# Règle candidate '"(lat|lon|latitude|longitude)"[ \t]*:[ \t]*-?[0-9]+\.[0-9]{4,}' passée sur la
# surface PERSO (14 fichiers suivis) : 2 455 lignes signalées, dans 6 fichiers, TOUS des couches géo
# légitimes — antennes ANFR, mesures certifiées, éoliennes, postes sources, sites, émetteurs TDF.
# Sur un gate bloquant, c'est le dépôt gelé : le motif d'écartement tient.
# Ce que la mesure CORRIGE dans la raison d'origine : le bruit n'est pas diffus, il est concentré
# sur 6 fichiers — is_allowed + leak_guard_allowlist.txt le tairaient sans peine. Mais la règle
# n'émettrait alors plus rien aujourd'hui (0 finding hors de ces 6) : tout son signal porterait sur
# des fichiers NON listés, donc à venir, au prix d'une liste à tenir — et une liste périmée ne se
# signale pas. Elle reste donc dehors pour ce coût-là, pas pour du bruit.
# Arbitrage ouvert (règle + allowlist, ou exclusion par propriété déclarée plutôt que par liste) :
# cf. dette CARTORADIO-INGESTION-PERSO-CONVENTION-001 (registre privé).
# Vérifié avant merge (pas supposé) sur les deux fichiers réels de l'incident (copies hors dépôt) :
# 8/8 puis 77/77 détectés sur les versions AVANT correctif ; 0/0 sur la version corrigée.
scan_perso_coocurrence() { # label field_regex context_regex filelist
  local label="$1" field_rx="$2" ctx_rx="$3" filelist="$4" f
  while IFS= read -r f; do
    [ -n "$f" ] || continue
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
  done <<< "$filelist"
}
scan_perso_coocurrence "adresse_voie_residentiel" \
  '"(adresse_complete|voie)"[ \t]*:[ \t]*"[^"]' \
  '"type_environnement"[ \t]*:[ \t]*"residentiel"|"environnement"[ \t]*:[ \t]*"Lieu d.habitation"' \
  "$PERSO_FILES"
scan_perso_coocurrence "code_postal_residentiel" \
  '"code_postal"[ \t]*:[ \t]*"[0-9]{5}"' \
  '"type_environnement"[ \t]*:[ \t]*"residentiel"|"environnement"[ \t]*:[ \t]*"Lieu d.habitation"' \
  "$PERSO_FILES"

# ─── Motifs tenus en secret ──────────────────────────────────────────────────────────────────
# Ce fichier est servi : un motif qui serait lui-même une fuite ne peut pas y figurer. Il vient d'un
# secret GitHub Actions, que le workflow passe en variable d'environnement :
#   LEAK_TERMS_REGEX        → raison_sociale       (raison sociale)
#   LEAK_CONFIDENTIAL_REGEX → module_confidentiel  (modules confidentiels, portée pré-compétitive)
#   LEAK_CORPUS_REPO_REGEX  → corpus_repo          (nom du dépôt privé ; en clair dans RULES jusqu'au
#                                                   2026-09-24, cf. canari ci-dessous)
# Format commun : expression régulière étendue (grep -E), lue sans égard à la casse.
# Normalisation, qui ne peut qu'ÉLARGIR ce que le motif détecte : retrait des CR (un « \r » final,
# saisie Windows, ferait correspondre le motif à RIEN, en silence), des espaces en tête et en fin
# de ligne et des lignes vides. Plusieurs lignes restent permises (grep -E les lit en alternatives).
# Refus BLOQUANTS (CONFIG), jamais de dégradation silencieuse :
#   - secret absent, ou vide après normalisation → <label>_NON_SCANNEE_secret_absent ;
#   - motif qui correspond à la ligne vide (il signalerait tout le dépôt) → <label>_motif_universel ;
#   - régex invalide → regex_invalide_<label> (dans scan_rule).
# Le contenu d'un secret n'est jamais imprimé (label seulement).
MOTIF_NORMALISE=""
scan_secret() { # label nom_du_secret valeur — renvoie 1 si la classe n'a pas été lue
  local label="$1" nom="$2" rx
  rx="$(printf '%s' "$3" | tr -d '\r' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' | grep -v '^$')"
  MOTIF_NORMALISE="$rx"
  if [ -z "$rx" ]; then
    echo "WARN: $nom absent ou vide — classe $label non scannée." >&2
    printf '%s\t%s\t%s\n' "(config)" "CONFIG" "${label}_NON_SCANNEE_secret_absent"
    NON_EVALUES="$NON_EVALUES$label "
    return 1
  fi
  if printf '\n' | grep -qiE -- "$rx" 2>/dev/null; then
    printf '%s\t%s\t%s\n' "(config)" "CONFIG" "${label}_motif_universel"
    NON_EVALUES="$NON_EVALUES$label "
    return 1
  fi
  scan_rule "FUITE" "$label" "$rx" "-i"
  case "$NON_EVALUES" in *" $label "*) return 1 ;; esac
  return 0
}

# Canari du nom du dépôt privé. Un motif valide mais FAUX (faute de frappe à la création du
# secret) ne correspondrait à rien, et le garde passerait en silence. Or ce nom a figuré en clair
# dans CE fichier (table RULES) jusqu'au 2026-09-24 : l'historique git du fichier le contient, et
# le contiendra tant qu'il n'est pas réécrit. Le motif doit donc y correspondre, sinon CONFIG
# bloquant. Historique absent ou tronqué (clone superficiel) → CONFIG aussi : canari non évalué.
# Ce que le canari ne prouve pas : que le motif est assez ÉTROIT (un motif trop large se voit
# autrement, par des FUITE en nombre). Si ce fichier est renommé ou son historique réécrit, le
# canari échouera : c'est voulu, la décision redevient humaine.
# grep sans -q : avec pipefail, une sortie anticipée de grep tuerait git log (SIGPIPE) et ferait
# échouer le canari à tort.
canari_historique() { # label regex
  if [ "$(git rev-parse --is-shallow-repository 2>/dev/null)" != "false" ]; then
    printf '%s\t%s\t%s\n' "(config)" "CONFIG" "${1}_canari_non_evaluable_historique_absent"
  elif ! git log -p --format= -- .github/scripts/leak_guard.sh 2>/dev/null | grep -aiE -- "$2" >/dev/null; then
    printf '%s\t%s\t%s\n' "(config)" "CONFIG" "${1}_canari_absent_de_l_historique"
  fi
}

scan_secret "raison_sociale" "LEAK_TERMS_REGEX" "${LEAK_TERMS_REGEX:-}"
scan_secret "module_confidentiel" "LEAK_CONFIDENTIAL_REGEX" "${LEAK_CONFIDENTIAL_REGEX:-}"
if scan_secret "corpus_repo" "LEAK_CORPUS_REPO_REGEX" "${LEAK_CORPUS_REPO_REGEX:-}"; then
  canari_historique "corpus_repo" "$MOTIF_NORMALISE"
fi

# Dette périmée : une entrée qui n'a correspondu à aucune ligne (fuite corrigée, ligne modifiée ou
# fichier retiré) → CONFIG bloquant, pour que l'entrée soit retirée dans la PR qui corrige.
# Sauf si sa classe n'a pas été lue (secret absent, motif refusé) : la dette n'a alors pas été
# évaluée, et la dire « périmée » pousserait à retirer l'entrée d'une fuite toujours présente.
if [ -s "$DETTE_NORM" ]; then
  while IFS=$'\t' read -r df dl dh; do
    [ -z "${df:-}" ] && continue
    grep -qxF "$df"$'\t'"$dl"$'\t'"$dh" "$DETTE_VUES" 2>/dev/null && continue
    case "$NON_EVALUES" in
      *" $dl "*) printf '%s\t%s\t%s\n' "$df" "CONFIG" "dette_non_evaluee_${dl}" ;;
      *)         printf '%s\t%s\t%s\n' "$df" "CONFIG" "dette_perimee_${dl}" ;;
    esac
  done < "$DETTE_NORM"
fi

SCAN_COMPLET=1
exit 0
