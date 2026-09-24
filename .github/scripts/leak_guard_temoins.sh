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
for e in html md txt yml json py mjs js cjs sql sh css tsv svg; do
  case "$TEXT_EXTS" in *" $e "*) : ;; *) echo "ÉCHEC   plancher : .$e absent de TEXT_EXTS"; exit 1 ;; esac
done

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK" || exit 1
git init -q . && git config user.email temoins@exemple.invalid && git config user.name temoins \
  && git config core.autocrlf false
mkdir -p .github/scripts noms docs/data
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
printf 'ligne de dette %s\nautre ligne %s\n' "$DECLENCHEUR" "$DECLENCHEUR" > "temoin_dette.py"
H=$(printf '%s' "ligne de dette $DECLENCHEUR" | sha256sum | cut -c1-16)
printf 'temoin_dette.py\tforme_sarl\t%s\nfichier_disparu.py\tforme_sarl\t0000000000000000\n' "$H" \
  > .github/scripts/leak_guard_dette.txt
git add -A >/dev/null

env -u LEAK_TERMS_REGEX -u LEAK_CONFIDENTIAL_REGEX bash .github/scripts/leak_guard.sh . > sortie.txt 2>/dev/null

ECHECS=0
attendu() { # motif (ERE, ligne entière) description
  if grep -qE "^$1\$" sortie.txt; then echo "OK      $2"; else echo "ÉCHEC   $2 (attendu : $1)"; ECHECS=$((ECHECS+1)); fi
}
absent() { # motif description
  if grep -qE "$1" sortie.txt; then echo "ÉCHEC   $2 (présent : $1)"; ECHECS=$((ECHECS+1)); else echo "OK      $2"; fi
}
n=0
for ext in $TEXT_EXTS; do attendu "temoin\.$ext:1	FUITE	forme_sarl" "extension .$ext lue"; n=$((n+1)); done
for nom in $TEXT_NAMES; do attendu "noms/$nom:1	FUITE	forme_sarl" "fichier sans extension « $nom » lu"; n=$((n+1)); done
attendu "temoin_majuscules\.MD:1	FUITE	forme_sarl" "extension en majuscules lue"
absent "^temoin_binaire\." "binaire déclaré .$BIN1 non lu"
attendu "temoin_inconnu\.zzqx	CONFIG	extension_non_classee_zzqx" "extension inconnue → CONFIG bloquant"
attendu "SANS_EXTENSION_NON_DECLARE	CONFIG	extension_non_classee_sans_extension" "sans extension non déclaré → CONFIG bloquant"
absent "^docs/data/temoin_exclu" "répertoire exclu docs/data non lu (limite documentée)"
attendu "temoin_dette\.py:1	DETTE	forme_sarl" "ligne inscrite en dette → DETTE"
attendu "temoin_dette\.py:2	FUITE	forme_sarl" "autre ligne du même fichier → FUITE"
attendu "fichier_disparu\.py	CONFIG	dette_perimee_forme_sarl" "entrée de dette orpheline → CONFIG bloquant"
attendu "\(meta\)	META	sentinelle_fin_de_scan" "scan complet (sentinelle)"
absent "scanner_interrompu" "scan non interrompu"

echo "---"
echo "$n extensions ou noms déclarés texte testés ; écarts : $ECHECS"
[ "$ECHECS" -eq 0 ] || exit 1
exit 0
