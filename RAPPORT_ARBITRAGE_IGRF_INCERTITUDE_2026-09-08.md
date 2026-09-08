# Dossier d'arbitrage — incertitude affichée du champ statique géomagnétique (IGRF-14)

**Statut : dossier, pas un patch.** Aucune modification de la valeur affichée. Le choix du remède
et la valeur numérique sont un arbitrage Soleil (étiquetage scientifique). Généré en lecture seule
depuis `Tellux-fresh-2026-09-08/`, rev `main` au moment du push, contenu vérifié contre le code —
pas contre l'énoncé du brief qui a demandé ce dossier.

## 1. Ce qui est confirmé (code lu, cité)

**L'appel réseau est bien retiré, le modèle précalculé est source unique.**

- `fetchIGRF(lat,lon)` (app.html:6408-6411) : « Pas d'appel réseau → réponse immédiate au clic et
  au survol » — retourne `igrfFallback(...) + calcLCS1(...) + calcSq(...) + calcExternalCorr()`.
- `igrfFallback()` (app.html:6040) interpole `IGRF14_GRID`, une grille **précalculée** (app.html:5475
  et suivantes), commentée « Source : coefficients IGRF-14 (Alken et al. 2021), évalués
  analytiquement » et « IMPORTANT : les vraies valeurs Corse 2025 sont 46 150–47 200 nT » — la
  grille est ancrée à l'année 2025.
- `fetchIGRF_precise()` (variante réseau, BGS geomag web service) a été **retirée le 2026-09-04**
  (brief AG) — « zéro appelant dans tout le dépôt, confirmé par grep exhaustif » (app.html:6412-6414).

Aucune divergence avec la prémisse du brief sur ce point : confirmé.

## 2. L'incertitude réellement affichée, et sa composition déclarée dans le code

Le popup carte affiche, au clic, un badge de confiance dont l'infobulle dit (app.html:9245, avant
toute correction) :

> « Confiance : moyen — IGRF-14 + LCS1/EMAG2v3, ±100 nT »

Cette valeur « ±100 nT » vient du commentaire de la grille elle-même (app.html:5472) : « Précision :
±100 nT (interpolation grille 0,25°) ». Le code porte cependant une décomposition plus fine, non
affichée dans le badge, dans `epistemic_note` (app.html:6460) :

> « Incertitude : IGRF-14 interpolé sur grille 0,25° (±50–100 nT) + anomalie crustale LCS1 sur
> grille ~0,3° lat × 0,5° lon, 24 points (±20 nT). »

Donc : le badge affiche un seul chiffre rond (±100 nT) qui correspond à la borne haute de
l'**interpolation spatiale seule** ; il n'inclut pas explicitement les ±20 nT de l'anomalie
crustale LCS1 (bien que 100+20=120, proche de 100 arrondi — la marge est faible).

## 3. Ce qui N'A PAS pu être vérifié — signalé, pas forcé

**La dérive « 103–127 nT » citée dans le brief n'a été retrouvée nulle part** dans le code, les
commentaires, `ARCHITECTURE.md`, `CHANGELOG.md`, `ROADMAP.md`, ni dans la mémoire de session
accessible ici (recherche : `103.{0,10}127`, `dérive.*IGRF`, `secular`, `epoch`, `drift`, sur
l'ensemble du dépôt — aucune occurrence). Le brief lui-même prévient : « Ce brief est lui-même une
source de seconde main et peut être périmé. » Je le prends au mot : **ce chiffre est signalé comme
non retrouvé, pas confirmé, pas infirmé, pas réécrit par moi.** Si Soleil l'a en main par un autre
canal (mesure directe, calcul fait ailleurs), il complète ce dossier — il n'est pas reconstitué ici
par supposition.

**Ce que je peux dire, à titre de contexte, sans en faire un chiffre de dossier** : le code documente
une dérive de la **déclinaison** magnétique (~0,1°/an, app.html:6444-6446, contrôle décennal
2,28°→3,47° entre 2016 et 2026), ce qui est un axe différent de l'intensité totale F que couvre le
« ±100 nT » du badge. Un budget de dérive temporelle de F depuis l'ancrage 2025 de la grille n'est
tenu nulle part dans le code que j'ai lu.

## 4. Deux remèdes, exclusifs — coût et formulation, pas de choix

### (i) Élargir l'incertitude affichée

**Coût** : nul en développement — un changement de chaîne (`v2_conf_statique` / le texte du badge
app.html:9245 et 3422). Aucun risque de régression de calcul.
**Limite** : ne corrige rien à la précision réelle du modèle — rend seulement l'affichage honnête
sur ce qu'il ne sait pas.
**Formulation proposée (à valider ou amender)** : remplacer « ±100 nT » par une fourchette qui
inclut explicitement le terme crustal déjà documenté dans `epistemic_note`, par exemple
« ±100–120 nT » — ou, si Soleil confirme un chiffre de dérive temporelle distinct, l'incertitude
combinée correspondante.

### (ii) Réactualiser le modèle / rétablir l'appel réseau

**Coût** : ré-implémentation d'un appel réseau (BGS geomag web service ou équivalent), avec gestion
d'échec/fallback — précisément ce qui a été retiré le 2026-09-04 pour « zéro appelant ». Réintroduit
une dépendance externe et une latence potentielle sur le clic carte (le commentaire actuel valorise
explicitement l'absence d'appel réseau : « réponse immédiate au clic et au survol »).
**Alternative interne** : régénérer la grille précalculée à une époque plus récente que 2025 sans
rétablir d'appel réseau — coût de calcul offline, pas de dépendance runtime, mais ne règle que la
dérive due à l'ancienneté de la grille, pas l'interpolation elle-même.
**Formulation proposée (à valider ou amender)** : si la grille est régénérée, mettre à jour à la
fois la valeur et sa date d'ancrage dans le commentaire (actuellement « les vraies valeurs Corse
2025 sont... », app.html:5474) et, si pertinent, dans le badge affiché.

## 5. Ce qui reste hors de ce dossier

- Le choix entre (i) et (ii), et la valeur numérique retenue : arbitrage Soleil.
- La dette adjacente « grain d'étiquetage » (badge générique incapable de nommer une limite connue
  précise) : signalée par le brief comme hors scope, non traitée ici.
- Aucune ligne de `app.html` n'a été modifiée par ce dossier.
