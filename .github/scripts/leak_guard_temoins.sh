#!/usr/bin/env bash
# Témoins du garde-fou anti-fuite (R5) — 2026-09-24, brief FUITE_APERCUS_CLOUDFLARE, volet II.
#
# Un garde étendu mais inopérant serait pire qu'avant : ce script PROUVE, à chaque exécution du
# workflow, que chaque extension déclarée texte est réellement lue. Il construit un dépôt jetable
# (mktemp), y dépose un fichier témoin par extension de TEXT_EXTS et par nom de TEXT_NAMES — listes
# LUES dans leak_guard.sh, jamais recopiées ici, pour que témoins et garde ne puissent pas diverger —,
# y lance le garde et exige un finding FUITE/forme_sarl sur chacun.
# Il vérifie aussi les limites déclarées :
#   - extension en majuscules lue ;
#   - binaire déclaré NON lu ;
#   - extension inconnue et fichier sans extension non déclaré → CONFIG extension_non_classee ;
#   - répertoire exclu (docs/data) NON lu (aveugle documenté : un changement de périmètre se voit) ;
#   - dette : ligne inscrite → DETTE ; autre ligne du même fichier → FUITE ; entrée orpheline → CONFIG.
# Et les motifs tenus en secret (brief EXPOSITIONS_ET_GARDE, 2026-09-25), avec des valeurs FACTICES,
# jamais les vraies (le workflow ne passe aucun secret à ce step) :
#   - secret absent, vide ou blanc → CONFIG bloquant, pour chacun des trois ;
#   - secret présent → motif retrouvé, malgré la casse, les espaces, un CRLF et une ligne vide ;
#   - motif universel, régex invalide → CONFIG ; dette d'une classe non lue → « non évaluée », jamais
#     « périmée » ;
#   - canari du dépôt privé : motif présent dans l'historique du garde → rien ; absent → CONFIG ;
#     historique tronqué → CONFIG.
# Sortie : une ligne OK/ÉCHEC par témoin ; code retour 1 au premier écart (le job échoue).
set -uo pipefail

GUARD="$(cd "$(dirname "$0")" && pwd)/leak_guard.sh"
[ -f "$GUARD" ] || { echo "ÉCHEC : leak_guard.sh introuvable"; exit 1; }

lire_liste() { # nom de variable → contenu entre guillemets de sa ligne d'affectation dans le garde
  grep -E "^$1=\"" "$GUARD" | head -1 | sed -E "s/^$1=\"(.*)\"$/\1/"
}
TEXT_EXTS="$(lire_liste TEXT_EXTS)"
TEXT_NAMES="$(lire_liste TEXT_NAMES)"
BINARY_EXTS="$(lire_liste BINARY_EXTS)"
[ -n "${TEXT_EXTS// /}" ] && [ -n "${TEXT_NAMES// /}" ] && [ -n "${BINARY_EXTS// /}" ] || {
  echo "ÉCHEC : listes TEXT_EXTS / TEXT_NAMES / BINARY_EXTS illisibles dans le garde"; exit 1; }
# Plancher : les extensions ajoutées le 2026-09-24 ne peuvent pas quitter TEXT_EXTS en silence
# (les passer en BINARY_EXTS les rendrait aveugles sans qu'aucun autre contrôle ne bronche).
for e in html htm md markdown txt yml yaml json jsonc geojson py mjs js cjs sql sh css tsv svg gitignore gitattributes htmlhintrc assetsignore; do
  case "$TEXT_EXTS" in *" $e "*) : ;; *) echo "ÉCHEC   plancher : .$e absent de TEXT_EXTS"; exit 1 ;; esac
done

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK" || exit 1
git init -q . && git config user.email temoins@exemple.invalid && git config user.name temoins \
  && git config core.autocrlf false
mkdir -p .github/scripts noms docs/data
# Historique factice pour le canari : une version ANCIENNE du garde portait le motif du dépôt
# privé en clair (comme la vraie, jusqu'au 2026-09-24). Valeur factice, jamais la vraie.
MOTIF_DEPOT="zzqdepot-temoin"
printf '# version ancienne\nFUITE\tcorpus_repo\t%s\t-i\n' "$MOTIF_DEPOT" > .github/scripts/leak_guard.sh
git add .github/scripts/leak_guard.sh && git commit -q -m "version ancienne" || { echo "ÉCHEC : commit de l'historique factice"; exit 1; }
cp "$GUARD" .github/scripts/leak_guard.sh
: > .github/scripts/leak_guard_allowlist.txt
DECLENCHEUR="SARL"   # motif public du garde (classe FUITE, label forme_sarl)

for ext in $TEXT_EXTS; do printf 'temoin %s %s\n' "$ext" "$DECLENCHEUR" > "temoin.$ext"; done
for nom in $TEXT_NAMES; do printf 'temoin %s %s\n' "$nom" "$DECLENCHEUR" > "noms/$nom"; done
printf 'temoin %s\n' "$DECLENCHEUR" > "temoin_majuscules.MD"
set -- $BINARY_EXTS; BIN1="$1"
printf 'temoin %s\n' "$DECLENCHEUR" > "temoin_binaire.$BIN1"
printf 'temoin %s\n' "$DECLENCHEUR" > "temoin_inconnu.zzqx"
printf 'temoin %s\n' "$DECLENCHEUR" > "SANS_EXTENSION_NON_DECLARE"
printf 'temoin %s\n' "$DECLENCHEUR" > "docs/data/temoin_exclu.json"
printf 'a\0b\ntemoin %s\n' "$DECLENCHEUR" > "temoin_nul.md"                 # octet NUL avant le déclencheur
printf 'caf\xe9 temoin %s\n' "$DECLENCHEUR" > "temoin_latin1.md"            # octet non UTF-8 sur la ligne
printf 'temoin %s\n' "$DECLENCHEUR" > "temoin espace.md"                     # espace dans le nom
printf 'ligne de dette %s\nautre ligne %s\nligne de dette %s\n' "$DECLENCHEUR" "$DECLENCHEUR" "$DECLENCHEUR" \
  > "temoin_dette.py"                                                        # ligne 3 = copie de la 1
H=$(printf '%s' "ligne de dette $DECLENCHEUR" | sha256sum | cut -c1-16)
# Motifs tenus en secret : un témoin par classe, en MAJUSCULES (le motif est lu sans égard à la casse).
printf 'voir %s ici\ndette %s connue\nraison ZZQRAISON\nmodule ZZQMODULE\n' "${MOTIF_DEPOT^^}" "${MOTIF_DEPOT^^}" \
  > "temoin_secret.md"
HS=$(printf '%s' "dette ${MOTIF_DEPOT^^} connue" | sha256sum | cut -c1-16)
# Registre de dette saisi « à la Windows » : BOM en tête, CRLF, espace final sur l'entrée.
printf '\xEF\xBB\xBF# commentaire\r\ntemoin_dette.py\tforme_sarl\t%s \r\nfichier_disparu.py\tforme_sarl\t0000000000000000\r\ntemoin_secret.md\tcorpus_repo\t%s\r\n' "$H" "$HS" \
  > .github/scripts/leak_guard_dette.txt
git add -A >/dev/null

sans_secrets() { env -u LEAK_TERMS_REGEX -u LEAK_CONFIDENTIAL_REGEX -u LEAK_CORPUS_REPO_REGEX "$@"; }
sans_secrets bash .github/scripts/leak_guard.sh . > sortie.txt 2>/dev/null

ECHECS=0
SORTIE=sortie.txt   # sortie du passage en cours
attendu() { # motif (ERE, ligne entière) description
  if grep -qE "^$1\$" "$SORTIE"; then echo "OK      $2"; else echo "ÉCHEC   $2 (attendu : $1)"; ECHECS=$((ECHECS+1)); fi
}
absent() { # motif description
  if grep -qE "$1" "$SORTIE"; then echo "ÉCHEC   $2 (présent : $1)"; ECHECS=$((ECHECS+1)); else echo "OK      $2"; fi
}
n=0
for ext in $TEXT_EXTS; do attendu "temoin\.$ext:1	FUITE	forme_sarl" "extension .$ext lue"; n=$((n+1)); done
for nom in $TEXT_NAMES; do attendu "noms/$nom:1	FUITE	forme_sarl" "fichier sans extension « $nom » lu"; n=$((n+1)); done
attendu "temoin_majuscules\.MD:1	FUITE	forme_sarl" "extension en majuscules lue"
absent "^temoin_binaire\." "binaire déclaré .$BIN1 non lu"
attendu "temoin_inconnu\.zzqx	CONFIG	extension_non_classee_zzqx" "extension inconnue → CONFIG bloquant"
attendu "SANS_EXTENSION_NON_DECLARE	CONFIG	extension_non_classee_sans_extension" "sans extension non déclaré → CONFIG bloquant"
absent "^docs/data/temoin_exclu" "répertoire exclu docs/data non lu (limite documentée)"
attendu "temoin_nul\.md:2	FUITE	forme_sarl" "octet NUL dans le fichier : ligne lue"
attendu "temoin_latin1\.md:1	FUITE	forme_sarl" "octet non UTF-8 sur la ligne : ligne lue"
attendu "temoin espace\.md:1	FUITE	forme_sarl" "nom de fichier avec espace lu"
attendu "temoin_dette\.py:1	DETTE	forme_sarl" "ligne inscrite en dette → DETTE (registre avec BOM, CRLF, espace final)"
attendu "temoin_dette\.py:2	FUITE	forme_sarl" "autre ligne du même fichier → FUITE"
attendu "temoin_dette\.py:3	FUITE	forme_sarl" "copie identique de la ligne en dette → FUITE"
attendu "fichier_disparu\.py	CONFIG	dette_perimee_forme_sarl" "entrée de dette orpheline → CONFIG bloquant"
absent "dette_perimee_$" "commentaire du registre (après BOM) non pris pour une entrée"
attendu "\(meta\)	META	sentinelle_fin_de_scan" "scan complet (sentinelle)"
absent "scanner_interrompu" "scan non interrompu"

# --- Motifs tenus en secret : absents (passage ci-dessus, sans aucun secret) ---
for c in raison_sociale module_confidentiel corpus_repo; do
  attendu "\(config\)	CONFIG	${c}_NON_SCANNEE_secret_absent" "secret de $c absent → CONFIG bloquant"
done
attendu "temoin_secret\.md	CONFIG	dette_non_evaluee_corpus_repo" "dette d'une classe non lue → « non évaluée »"
absent "dette_perimee_corpus_repo" "dette d'une classe non lue jamais dite « périmée »"
absent "^temoin_secret\.md:" "classes secrètes non lues sans secret (aucun finding de contenu)"

# --- Motifs tenus en secret : présents (valeurs factices, saisie « à la Windows ») ---
SORTIE=sortie_secrets.txt
sans_secrets env LEAK_CORPUS_REPO_REGEX="  $MOTIF_DEPOT "$'\r\n\r\n' LEAK_TERMS_REGEX=$'zzqraison\r\n' \
  LEAK_CONFIDENTIAL_REGEX=' zzqmodule' bash .github/scripts/leak_guard.sh . > "$SORTIE" 2>/dev/null
attendu "temoin_secret\.md:1	FUITE	corpus_repo" "secret du dépôt privé présent → motif retrouvé (casse, espaces, CRLF, ligne vide)"
attendu "temoin_secret\.md:2	DETTE	corpus_repo" "ligne du dépôt privé inscrite en dette → DETTE"
attendu "temoin_secret\.md:3	FUITE	raison_sociale" "secret raison sociale présent → motif retrouvé"
attendu "temoin_secret\.md:4	FUITE	module_confidentiel" "secret modules confidentiels présent → motif retrouvé"
absent "NON_SCANNEE|motif_universel|canari|regex_invalide|dette_non_evaluee" "aucun CONFIG de secret quand les trois sont valides"
attendu "\(meta\)	META	sentinelle_fin_de_scan" "scan complet avec secrets (sentinelle)"

# --- Refus : chaque cas doit bloquer (CONFIG), jamais passer en silence ---
passe_depot() { # valeur du secret du dépôt privé → sortie dans $SORTIE
  sans_secrets env LEAK_CORPUS_REPO_REGEX="$1" bash .github/scripts/leak_guard.sh . > "$SORTIE" 2>/dev/null
}
SORTIE=sortie_canari.txt; passe_depot "zzqabsent-historique"
attendu "\(config\)	CONFIG	corpus_repo_canari_absent_de_l_historique" "motif valide absent de l'historique du garde (faute de frappe) → CONFIG"
SORTIE=sortie_universel.txt; passe_depot "zzq|"
attendu "\(config\)	CONFIG	corpus_repo_motif_universel" "motif qui correspond à tout → CONFIG"
attendu "temoin_secret\.md	CONFIG	dette_non_evaluee_corpus_repo" "motif refusé : dette « non évaluée »"
SORTIE=sortie_invalide.txt; passe_depot "zzq("
attendu "\(config\)	CONFIG	regex_invalide_corpus_repo" "régex invalide → CONFIG"
SORTIE=sortie_blanc.txt; passe_depot $' \r\n\t'
attendu "\(config\)	CONFIG	corpus_repo_NON_SCANNEE_secret_absent" "secret blanc (espaces, CRLF, tabulation) → CONFIG"
# Historique tronqué (clone superficiel) : le canari ne peut pas être évalué.
git rev-parse HEAD > .git/shallow
SORTIE=sortie_superficiel.txt; passe_depot "$MOTIF_DEPOT"
attendu "\(config\)	CONFIG	corpus_repo_canari_non_evaluable_historique_absent" "historique tronqué → canari non évalué → CONFIG"
rm -f .git/shallow

echo "---"
echo "$n extensions ou noms déclarés texte testés ; écarts : $ECHECS"
[ "$ECHECS" -eq 0 ] || exit 1
exit 0
