# Tellux — Etat du projet au 1er juin 2026

**Auteur :** porteur du projet Tellux Corse.
**Objet :** photo nette de l'etat du projet a la date de publication, Phase 1 EM-mairie publique. Renvoie vers `ROADMAP.md`, `ARCHITECTURE.md` et `CHANGELOG.md` pour les details techniques par axe.
**Destination proposee :** racine du repo public `dellahstella/tellux`, fichier `ETAT_PROJET.md` (succede `docs/internal/ETAT_PROJET_2026-04-25.md` qui restait prive).

---

## 1. Synthese executive

Tellux est une plateforme cartographique consacree a la distribution territoriale des champs electromagnetiques en Corse, croisee avec les donnees geologiques, patrimoniales et environnementales de l'ile. Le projet est publie sous licence MIT, sans publicite ni revente de donnees.

Le perimetre **Phase 1** publie au 1er juin 2026 couvre :

- Une cartographie EM publique (`app.html`) integrant antennes ANFR, lignes electriques EDF SEI, modele geomagnetique IGRF-14, anomalies crustales EMAG2v3, classification radon ASNR.
- Des outils communaux (`mairies.html`) : fiche par commune, generateur de courriers institutionnels, checklist deploiement antenne, cadre legal, espace citoyen.
- Une documentation scientifique publique de reference (`cadre-scientifique.html`, `methode-et-limites.html`, `transparence.html`, `guide-utilisation.html`, `glossaire.html`).
- Un dataset structure de 30 mesures certifiees ANFR/EXEM redistribuees en JSON.

Des declinaisons thematiques ulterieures sont planifiees dans la `ROADMAP.md` mais ne font pas l'objet de cette photo Phase 1.

---

## 2. Etat technique de la production

### 2.1 Branches et deploiement

- **`main`** : etat de la prod a la date de publication. Sert `tellux.pages.dev`. Hebergement Cloudflare Pages, deploiement assets-only Worker (`wrangler.jsonc`).
- **`dev`** : etat de developpement courant, en avance d'une PR sur `main` au moment de la redaction.

Le cycle de versioning suit Semantic Versioning ; le detail des PRs mergees et des modifications est dans `CHANGELOG.md`.

### 2.2 Pages publiees

| Application | Fichier | Statut |
|---|---|---|
| Landing | `index.html` | En prod. Section Ressources : 4 documents publics + 1 dataset, footer 5 liens en 2 clusters (« Le projet » + « Legal & gouvernance »). |
| Cartographie EM | `app.html` | En prod. Compteur runtime antennes ANFR aligne sur la source ANFR CartoRadio. |
| Outils mairies | `mairies.html` | En prod. Fiche commune avec 4 blocs (antennes, etablissements sensibles, contexte geophysique, points atypiques). Generateur de courriers via pdfmake. |
| Demarche scientifique | `cadre-scientifique.html` | En prod. Document de reference complet, 10 sections + Annexe A. Section 9.2 alignee sur les chiffres ANFR canoniques. |
| Methode et limites | `methode-et-limites.html` | En prod. Posture epistemique, ce que Tellux mesure, vocabulaire impose, pieges rhetoriques ecartes. |
| Transparence | `transparence.html` | En prod. Sources institutionnelles, statuts epistemiques, zones gelees, cadres ethiques territoriaux, architecture/code/licences. |
| Guide d'utilisation | `guide-utilisation.html` | En prod. Comment lire chaque couche, unites, gradients, interpretation des indices. |
| Glossaire | `glossaire.html` | En prod. Lexique des termes physiques, metrologiques, epistemiques. |
| Mentions legales et confidentialite | `mentions-legales.html` | En prod. Section confidentialite integree (`#confidentialite`). |
| Retractations | `retractations.html` | En prod. Journal public des retraits, anonymisations et reformulations substantielles. |

`donnees-vie-privee.html` est court-circuitee par redirect 301 vers `mentions-legales.html#confidentialite`. `retractations.html` reste accessible directement.

### 2.3 Stack technique

HTML monolithique sans bundler ni framework cote client, mobilisant Leaflet, Turf.js, Papa Parse via CDN. Base de contributions citoyennes hebergee sur Supabase region `eu-west-1` (Irlande, Union europeenne) avec securite au niveau des lignes (Row Level Security). Polices Fraunces et IBM Plex Sans auto-hebergees sous Open Font License. Code source integral publie sur le depot public dellahstella/tellux sous licence MIT. Aucun traceur tiers, aucune publicite, aucune revente de donnees.

### 2.4 Couche ANFR — chiffres canoniques

Source : snapshot Supabase `antennas_corse` du 24 avril 2026. Cf. `docs/em-mairie/data-sources/antennes_corse_notes.md` et `cadre-scientifique.html` § 9.2.

- **3 000 antennes individuelles** geolocalisees (2G, 3G, 4G, 5G non millimetrique, tous operateurs).
- **2 986 antennes** dans les contours communaux IGN de **219 des 360 communes corses**.
- **14 antennes** sur sites littoraux ou portuaires hors contour strict (ilots Cerbicale, mole nord du port de Bastia), incluses dans le total par la declaration ANFR.
- **1 026 supports distincts** (groupage lat/lon/operateur).
- Densite moyenne de l'ordre de **0,12 support / km²**.
- **30 fiches de mesures certifiees ANFR/EXEM** (Corse 2024-2026), redistribuees en JSON structure et accessibles depuis la page d'accueil.

---

## 3. Couche scientifique / publication

Les choix methodologiques sont publies dans `cadre-scientifique.html` (specification du modele : 4 domaines physiques, position epistemique, mode Expertise, ordres de grandeur par domaine, annexe traitement EMAG2v3). La posture epistemique (refus symetrique de l'alarmisme et de la trivialisation, position « C documentee » UNSCEAR 2012, distinction systematique des niveaux d'inference) est exposee dans `methode-et-limites.html`. La transparence operationnelle (sources, statuts epistemiques mesure/calcule/hypothese, zones gelees) est dans `transparence.html`. Une refonte de l'architecture documentaire est preparee en interne ; son objet est de fournir une porte d'entree synthetique pour les mairies, associations et journalistes en complement du document dense actuel.

Aucun systeme d'apprentissage statistique a risque interdit n'est deploye au sens du Reglement IA UE 2024 (pas de notation sociale, pas d'identification biometrique, pas de police predictive, pas de ciblage emotionnel).

---

## 4. Sessions menees recemment (cycle mai - 1er juin 2026)

Le detail PR par PR est dans `CHANGELOG.md`. Le cycle mai-juin a porte sur :

- L'harmonisation des chiffres ANFR entre landing, doc scientifique et compteur runtime de l'application (PR #749 + PR #756 + PR #758).
- La fusion des pages legales avec mise en place de redirects 301 pour preserver les liens existants (PR #751).
- La refonte du footer en 5 liens organises en 2 clusters (PR #751).
- Le retrait du sous-chiffre « 219 communes » de la tuile statistique antennes en landing (PR #753, arbitrage editorial).
- L'harmonisation du logo et du footer dans `app.html` (PR #760).
- L'actualisation de la `ROADMAP.md` pour le cycle (PR #762).

Une PR de **nettoyage des fichiers internes de travail** (`chore/untrack-internal-files-align-gitignore-2026-06-01`, PR #764) a desuive des dossiers de travail editoriaux et de coordination, alignant la liste des fichiers publies sur la regle de gitignore correspondante. Cette PR a ete mergee dans la branche de developpement, sa promotion vers la branche principale fait partie du cycle de releases courant.

---

## 5. Dettes ouvertes

Les limites techniques connues au 1er juin sont les suivantes :

- Les ponderations et bornes du mode Expertise sont gelees, en attente de validation methodologique externe.
- La composante terrestre du fond gamma (formule NCRP 94) est laissee en placeholder, dans l'attente de la meme validation methodologique externe.
- L'integration temps reel de l'API Teleray ASNR pour le debit de dose gamma ambiant reste a mettre en place.
- Le voltage par segment des lignes HTA / HTB est absent du dataset public ; un courant uniforme de repli est utilise.
- Le modele Biot-Savart applique aux lignes basse tension torsadees presente une calibration insuffisante ; le calcul segmente basse tension est desactive dans le moteur en attendant une recalibration physique dediee.
- L'integration plus complete des donnees de charge nationale RTE eco2mix est envisagee a un stade ulterieur.
- La radiometrie aerienne BRGM n'est pas integree a date.

Aucune de ces limites ne bloque la publication de la Phase 1.

---

## 6. Sources mobilisees et cadres de reference

Les sources mobilisees sont publiques et institutionnelles (ANFR, ASNR, BRGM, IGRF-14, EMAG2v3 NOAA, NOAA Space Weather Prediction Center, EDF SEI, IGN, INPN). Les pratiques actuelles (licence MIT, hebergement europeen, absence de tracker, polices auto-hebergees, code ouvert) prefigurent une articulation possible avec la Charte de la donnee et de l'IA de la Corse (21 principes en 9 titres) et le Guide de bonne pratique IA Smart Isula (12 bonnes pratiques).

---

## 7. Horizon et prochains jalons (Phase 1)

**Court terme.**

- Refonte de l'architecture documentaire : creation d'une page « Demarche scientifique - synthese » accessible non specialiste, condensation de la section position epistemique du document dense, fusion editoriale de la page Transparence dans la page Methode et limites. Preparation Cowork terminee, integration Code en attente.
- Promotion `dev -> main` des modifications du cycle 1er juin.
- Suppression effective des fichiers sources des pages legales fusionnees (`donnees-vie-privee.html`, `retractations.html`), au sens d'une PR `chore` dediee apres verification qu'aucun lien externe ne les cible directement.
- Actualisation de `CHANGELOG.md` pour consolider le cycle 1er juin en une entree groupee.

**Moyen terme.**

- Acces API Teleray ASNR, permettant l'integration temps reel du debit de dose gamma ambiant a la cartographie.
- Cadrage tension HTA par segment, permettant un modele Biot-Savart plus precis.
- Recalibration physique du modele basse tension torsadee.
- Densification de la couverture in situ par mesures certifiees, au-dela des 30 fiches ANFR/EXEM integrees.
- Eventuelle activation des declinaisons thematiques mentionnees dans la `ROADMAP.md`, selon la trajectoire de developpement.

**Reperes calendaires.**

- Le moteur de calcul est en phase de validation methodologique, pas de demonstration. Aucune limite connue ne bloque la publication Phase 1.
- Le cycle de releases reste mensuel a bimensuel selon l'activite.

---

## 8. Pour aller plus loin

- `ROADMAP.md` — feuille de route detaillee.
- `ARCHITECTURE.md` — architecture technique du moteur de calcul et des donnees.
- `CHANGELOG.md` — historique des changements.
- `cadre-scientifique.html` — specification methodologique complete (10 sections + annexe).
- `methode-et-limites.html` — posture epistemique et vocabulaire.
- `transparence.html` — sources institutionnelles, statuts epistemiques, zones gelees.

Pour toute question ou signalement d'erreur : `stelladluca@proton.me` ou issue publique sur `github.com/dellahstella/tellux/issues`. Les corrections substantielles apportees suite a un signalement sont tracees dans l'historique du depot.

---

**Fin de l'ETAT_PROJET public au 1er juin 2026.**
