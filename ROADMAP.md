# Tellux — Feuille de route publique

**Dernière mise à jour :** 3 juillet 2026 — cycle RF : couche radiofréquence reconstruite sur ~3 000 antennes ANFR réelles (2G/3G/4G/5G) + faisceaux hertziens + radiodiffusion TDF, avec **calibration interne** sur les mesures certifiées ANFR/EXEM, présentée comme « estimation centrale d'ordre de grandeur du champ extérieur » (PR [#901](https://github.com/dellahstella/tellux/pull/901), [#898](https://github.com/dellahstella/tellux/pull/898)) ; heatmap composite séparée par grandeur homogène (magnétique nT / RF V/m, PR [#897](https://github.com/dellahstella/tellux/pull/897)) ; Section 9 RF de `cadre-scientifique.html` alignée sur cette calibration, directivité d'antenne écartée par décision documentée, libellé « calée sur » (PR [#909](https://github.com/dellahstella/tellux/pull/909), [#911](https://github.com/dellahstella/tellux/pull/911), [#913](https://github.com/dellahstella/tellux/pull/913)) ; restauration de l'accroche « Révéler l'invisible » sur la landing (PR [#908](https://github.com/dellahstella/tellux/pull/908)) ; liens morts corrigés et DOI pérennisés (PR [#899](https://github.com/dellahstella/tellux/pull/899), [#900](https://github.com/dellahstella/tellux/pull/900)). Précédente : 1ᵉʳ juin 2026 — cycle mai-juin : corrections géomagnétiques temps réel à trois niveaux (Dst si disponible, Kp NOAA SWPC pondéré, IGRF-14 statique de base) avec multi-observatoires INTERMAGNET (PR [#742](https://github.com/dellahstella/tellux/pull/742)-[#744](https://github.com/dellahstella/tellux/pull/744)) ; harmonisation des chiffres ANFR sur la landing, `cadre-scientifique.html` § 9.2 et `app.html` à partir du snapshot CartoRadio du 24 avril 2026 (3 000 antennes individuelles, 1 026 supports distincts, 219 des 360 communes corses, PR [#749](https://github.com/dellahstella/tellux/pull/749), PR [#758](https://github.com/dellahstella/tellux/pull/758)) ; refonte du footer en 5 liens / 2 clusters identique sur les 11 pages publiques et redirects 301 sur les pages légales fusionnées (PR [#751](https://github.com/dellahstella/tellux/pull/751)) ; correction du filtre côtier d'`app.html` qui plafonnait le compteur d'antennes affiché à 534 (filtre géométrique trop agressif remplacé par un filtre commune-based, compteur passe à ~3 000, PR [#756](https://github.com/dellahstella/tellux/pull/756)) ; harmonisation du logo et du footer d'`app.html` avec la landing (logo cliquable vers `/`, suppression du lien redondant `tellux.pages.dev`, PR [#760](https://github.com/dellahstella/tellux/pull/760)) ; retrait du compteur partiel « 219 communes » de la tuile stat de la landing (PR [#753](https://github.com/dellahstella/tellux/pull/753)). Précédente : 1ᵉʳ mai 2026 (nuit) — fermeture des 3 livrables Phase 1 « Livrables restants » : intégration Sections 7-10 méthodologiques sur `cadre-scientifique.html` (sprint J, PR [#295](https://github.com/dellahstella/tellux/pull/295)), UI avancée `app.html` (sélecteur de domaines + badges temps réel, sprint O, PR [#298](https://github.com/dellahstella/tellux/pull/298) + [#299](https://github.com/dellahstella/tellux/pull/299)), glossaire technique intégré (sprints P + Q, PR [#300](https://github.com/dellahstella/tellux/pull/300) + [#302](https://github.com/dellahstella/tellux/pull/302)). Optimisation SEO+performance sur `mairies.html` (sprint L, PR [#293](https://github.com/dellahstella/tellux/pull/293) + [#294](https://github.com/dellahstella/tellux/pull/294), gain Lighthouse Performance +24).

Document de référence publique présentant la trajectoire générale du projet Tellux. Les détails opérationnels, calendriers précis et éléments stratégiques restent en pilotage interne.

**Note de lecture.** Le terme « phase 1 » désigne dans ce document l'étape actuelle de développement de Tellux : la cartographie EM publique. Les modules d'extension envisagés au-delà ne sont pas détaillés publiquement à ce stade.

---

## 1. Périmètre actuel et trajectoire

Tellux est aujourd'hui structuré autour d'**une application principale publique** : la cartographie électromagnétique territoriale (`app.html`), accompagnée d'outils communaux (`mairies.html`) et d'une documentation publique en trois volets (démarche scientifique, méthode et limites, guide d'utilisation). Cette phase 1 est en cours de stabilisation.

Des modules d'extension thématiques pourront être envisagés sous condition de stabilisation préalable de la phase 1, sans calendrier public à ce stade.

---

## 2. Phase 1 — Cartographie EM (en cours, 2026)

### Cible

Publication d'une application de cartographie électromagnétique territoriale rigoureuse et sobre, couvrant quatre domaines physiques distincts :

- **Magnétique statique** (IGRF-14, anomalies crustales EMAG2v3, WMM 2025 cross-check)
- **Magnétique basse fréquence** (ELF 50 Hz, lignes HTA réelles, postes sources, éoliennes)
- **Radiofréquences** (antennes ANFR, émetteurs TDF de radiodiffusion)
- **Ionisant** (composante cosmique altitudinale, classification radon officielle)

### Livrables restants

Les trois livrables Phase 1 « Livrables restants » sont désormais tous traités :

- **Documentation méthodologique par domaine physique** — livré (sprint J, PR [#295](https://github.com/dellahstella/tellux/pull/295), Sections 7-10 sur `cadre-scientifique.html`, cf. `CHANGELOG.md` `[2.8.5]`).
- **Phase d'UI avancée (sélecteur de domaines, badges temps réel)** — livré (sprint O, PR [#298](https://github.com/dellahstella/tellux/pull/298) + [#299](https://github.com/dellahstella/tellux/pull/299), chips de filtre par domaine physique et badges temps réel sur `app.html`, cf. `CHANGELOG.md` `[2.9.0]`).
- **Glossaire technique intégré** — livré (sprints P + Q, PR [#300](https://github.com/dellahstella/tellux/pull/300) + [#302](https://github.com/dellahstella/tellux/pull/302), nouvelle page `glossaire.html` à la racine et lien Glossaire ajouté sur les 9 pages éditoriales, cf. `CHANGELOG.md` `[2.10.0]` + `[2.10.1]`).

La mise à jour de la landing vers une cohérence totale avec la phase 1 publique est livrée (audit Phase D, sprints D1, D2, D1bis, D1ter et retrait éditorial section SPDIAC, cf. `CHANGELOG.md` `[2.8.0]`).

### Avancées techniques majeures avril-juillet 2026

- **2026-04-21/22** : refonte du modèle Biot-Savart sur les lignes HTA réelles (8 386 polylines depuis l'open data EDF SEI), intégration des lignes BT, sommation vectorielle 2D, fermeture des dettes `ELF-CALIB-001` (PR #69), `WMM-CROSSCHECK-001` (PR #67), `BDFORET-V2-001` (partielle, PR #67), `ELF-VECTOR-001` et `BT-ELF-001` (PR #71). Nouvelle dette `BT-CALIBRATION-001` détectée à l'audit post-merge.
- **2026-04-23** : fermeture `INTL-CRUSTAL-001` (module de comparaison crustale mondiale en EM pur) et `CSS-HARMONISATION-001` (palette DA v2 sémantique).
- **2026-04-24** : Cowork Session B — clarification du modèle EMAG2v3 vs WDMAM (note de recherche `docs/EMAG2_WDMAM_NOTE_RECHERCHE.md`), production des géométries officielles radon par commune (253 polygones ASNR intégrés via PR #130), correction de 5 coordonnées GPS U/Th (PR #131). Cowork Session A — production de la version 1 publique de `mairies.html` (PRs #136 à #140), fermeture `SUPABASE-COMMUNE-FIELD-001` (PR #137) et `ANTENNES-REFRESH-001` (PR #138).
- **2026-04-25** : finalisation du document de spécification méthodologique (23 pages) destiné à une relecture critique externe par un physicien tiers. Document archivé hors du repo public.
- **2026-05-01** : audit Phase D livré sur le site public (sprints `audit-D1`, `audit-D2`, `audit-D1bis`, `audit-D1ter`, `retrait-section-spdiac`). Alignement de la terminologie ASNR sur 14 mentions d'actualité (`index.html`, `methode-et-limites.html`, `guide-utilisation.html`, `transparence.html`, `cadre-scientifique.html`, `app.html`), ajout d'une section « Cadres éthiques de référence » sur `transparence.html` (Charte data Corse + Guide IA Smart Isula), fixes structurants landing (compteur antennes, footer SIRET, libellé contact projet). Une section « Inscription territoriale » a été ajoutée puis retirée de la landing dans le même cycle, sur décision éditoriale. Détail dans `CHANGELOG.md` `[2.8.0]`. En parallèle, révisions documentaires internes appliquées hors repo public (bascule EUPL → MIT sur 17 occurrences, reformulation Supabase 2.3.7 autour de l'audit CLOUD Act).
- **2026-05-01 (soir)** : intégration des Sections 7-10 méthodologiques par domaine physique sur `cadre-scientifique.html` (sprint J, PR [#295](https://github.com/dellahstella/tellux/pull/295)). Quatre sections homogènes ajoutées entre la Section 6 et l'Annexe A (Magnétique statique, Magnétique basse fréquence ELF 50 Hz, Radiofréquences, Rayonnement ionisant), chacune en 7 sous-sections (définition, phénoménologie, sources, formules, incertitudes, dettes associées, ce que la modélisation permet/ne permet pas). Volume total ajouté : ≈ 3 820 mots de prose. Sommaire enrichi (passe de 7 à 11 entrées), liens cliquables inter-sections, retraits éditoriaux en Section 1 (cohérence doctrine éditoriale post-cycle audit Phase D). Détail dans `CHANGELOG.md` `[2.8.5]`. Livre le chantier ROADMAP « Documentation méthodologique par domaine physique ».
- **2026-05-01 (soir)** : optimisation SEO et performance de `mairies.html` (sprint L, PR [#293](https://github.com/dellahstella/tellux/pull/293) + [#294](https://github.com/dellahstella/tellux/pull/294)). Score Lighthouse Performance 57 → **81** (+24), LCP/FCP 6.1 s → 1.5 s, TTI 7.6 s → 2.2 s grâce au lazy load `pdfmake` (chargement différé au premier clic « Télécharger PDF »). Élision française appliquée sur le préfixe « Mairie de [NOM DE LA COMMUNE] » dans la génération PDF des courriers (Ajaccio → « Mairie d'Ajaccio », L'Île-Rousse → « Mairie de l'Île-Rousse »). Enrichissement Open Graph et Twitter Cards (9 meta tags ajoutées). Détail dans `CHANGELOG.md` `[2.8.4]`. Livre le chantier ROADMAP « Backlog SEO post-release `mairies.html` ». Quatre anomalies hors périmètre détectées par Lighthouse et formalisées en suivi interne (`ROBOTS-TXT-001`, `A11Y-CONTRAST-001`, `MAIRIES-CLS-TBT-001`, `MAIRIES-REDIRECTS-001`).
- **2026-05-01 (nuit)** : phase d'UI avancée sur `app.html` (sprint O, PR [#298](https://github.com/dellahstella/tellux/pull/298) + [#299](https://github.com/dellahstella/tellux/pull/299), commit prod `2e23a0b`). Sélecteur de domaines physiques (5 chips de filtre additifs en haut de la sidebar : Tous / Statique / ELF / RF / Ionisant) et 4 badges temps réel toujours visibles dans le panneau Conditions (Kp NOAA SWPC, Réseau RTE eco2mix, Live Supabase, Orage Blitzortung caché si pas d'activité). 18 boutons annotés `data-domains`. Synchronisation des badges via hook dans `updateCondSummaries()` (rythme 30 s déjà en place), pas de `setInterval` dédié. Aucune nouvelle variable CSS racine, palette DA v2 gelée respectée. Détail dans `CHANGELOG.md` `[2.9.0]`. Livre le chantier ROADMAP « Phase d'UI avancée ».
- **2026-05-01 (nuit)** : intégration du glossaire technique public (sprints P et Q, PR [#300](https://github.com/dellahstella/tellux/pull/300) + [#302](https://github.com/dellahstella/tellux/pull/302), commits prod `34aa961` et `fa2678a`). Nouvelle page publique `/glossaire.html` à la racine (~48 ko, 642 lignes, 94 entrées alphabétiques sur 21 lettres, fontes auto-hébergées Fraunces + IBM Plex Sans, aucune dépendance externe). Lien Glossaire ajouté dans les footers/headers des 9 pages éditoriales du repo public : 5 pages prioritaires sprint P (`index.html`, `transparence.html`, `retractations.html`, `mentions-legales.html`, `donnees-vie-privee.html`) et 4 pages restantes sprint Q (`cadre-scientifique.html`, `methode-et-limites.html`, `mairies.html`, `app.html` via nouveau lien `hdr-btn` `target="_blank"` sans toucher au drawer interne `openGlossaryDrawer()`). `corpus.html` confirmé absent du repo public, exclu du périmètre. Détail dans `CHANGELOG.md` `[2.10.0]` et `[2.10.1]`. Livre le chantier ROADMAP « Glossaire technique intégré ».
- **2026-05-25 / 2026-05-26** : corrections géomagnétiques temps réel sur `app.html` (sprint astro v1 + v2, PR [#742](https://github.com/dellahstella/tellux/pull/742)-[#744](https://github.com/dellahstella/tellux/pull/744)). Hiérarchie à trois niveaux pour la composante magnétique statique : indice Dst si disponible, sinon Kp NOAA SWPC pondéré, sinon IGRF-14 statique de base. Multi-observatoires INTERMAGNET intégrés au pipeline d'enrichissement. Section 5.3 « Corrections géomagnétiques temps réel » ajoutée sur `cadre-scientifique.html` pour documenter la chaîne complète.
- **2026-05-31** : harmonisation des chiffres ANFR sur les trois surfaces publiques (PR [#749](https://github.com/dellahstella/tellux/pull/749)). Source de vérité unique : extraction CartoRadio du 24 avril 2026 documentée dans `docs/em-mairie/data-sources/antennes_corse_notes.md` — **3 000 antennes individuelles**, **1 026 supports distincts** (groupage lat/lon/opérateur), **219 des 360 communes corses**. Tuile stat de la landing alignée (« 3 000 antennes / 1 026 supports »), légendes d'`app.html` mises à jour (974 → 1 026 supports), `cadre-scientifique.html` § 9.2 reformulé. Régression silencieuse historique tracée dans `CHANGELOG.md` (la landing était passée de « ~960 sites » à « 566 sites » sans entrée de suivi).
- **2026-06-01** : refonte du footer en 5 liens / 2 clusters identique sur les 11 pages publiques du repo (cluster « Le projet » : Application carte / Outils mairies / Ressources — cluster « Légal & gouvernance » : Mentions légales & confidentialité / Transparence) et pose des redirects 301 sur les pages légales fusionnées (PR [#751](https://github.com/dellahstella/tellux/pull/751)). `donnees-vie-privee.html` redirige désormais vers `mentions-legales.html#confidentialite` et `retractations.html` vers `transparence.html#retractations` ; les fichiers sources sont conservés pendant une période d'amortissement (suivi interne `LEGAL-PAGES-FUSION-CLEANUP-001`). Glossaire ajouté en 5ᵉ carte de la section `#ressources` de la landing. Retrait du compteur partiel « 219 communes » de la tuile stat antennes de la landing, ambigu sans contexte (PR [#753](https://github.com/dellahstella/tellux/pull/753)).
- **2026-06-01** : correction du compteur d'antennes ANFR d'`app.html`, plafonné à 534 en production alors que la base recense 3 000 antennes individuelles (PR [#756](https://github.com/dellahstella/tellux/pull/756)). Diagnostic chiffré : filtre côtier géométrique (12 clauses bbox) rejetait 180 antennes individuelles dont environ 166 onshore à tort. Remplacement par un filtre commune-based exploitant le champ `commune` déjà présent dans le SELECT Supabase (les antennes sans rattachement administratif à une commune corse sont considérées offshore). Découplage de deux compteurs : nombre d'antennes individuelles affiché à l'utilisateur (~3 000), nombre de positions distinctes pour les marqueurs Leaflet (~552, performance). Amendement éditorial de `cadre-scientifique.html` § 9.2 pour aligner sur le total 3 000 antennes individuelles (PR [#758](https://github.com/dellahstella/tellux/pull/758)) : décomposition entre 2 986 antennes dans les contours communaux IGN et 14 sur sites littoraux ou portuaires hors contour strict (îlots Cerbicale au sud-est de Porto-Vecchio, môle nord du port de Bastia), incluses dans le total par la déclaration ANFR.
- **2026-06-01** : harmonisation visuelle du logo et du footer d'`app.html` avec la landing (PR [#760](https://github.com/dellahstella/tellux/pull/760)). Logo cliquable retournant à l'accueil (`href="/"` au lieu de `#`), `aria-label` ajouté, hover aligné sur la landing (`opacity:0.85`). Footer aligné sur le motif 5 liens / 2 clusters, suppression du lien redondant `tellux.pages.dev` (déjà accessible depuis chaque page). Barre d'outils carto strictement inchangée.

- **2026-07-03** : publication de la page de **culture scientifique** `geomagnetisme.html` — globe géomagnétique historique interactif (−8000 → 2025), données réelles embarquées (reconstruction CALS10k.2 GFZ avant 1900, IGRF-14 de 1900 à 2025, fond terre/mer GLOBE NOAA/NGDC), page autonome testée contre un oracle scientifique (60 valeurs, budget d'erreur documenté), liée depuis la rangée Ressources de la landing (PR [#912](https://github.com/dellahstella/tellux/pull/912), retouches accessibilité PR [#916](https://github.com/dellahstella/tellux/pull/916)). **Livré** ; registre distinct de la couche EM d'`app.html` et du patrimoine, **hors chemin critique** de la Phase 1 — enrichissement de médiation scientifique sans dépendance ni impact sur les livrables cartographiques.
- **2026-06 / 2026-07** : stabilisation de la couche **radiofréquence**. Passage du proxy figé (20 antennes + fond départemental + facteur ×25) à une superposition des émetteurs réels — ~3 000 antennes ANFR (2G/3G/4G/5G) + faisceaux hertziens + radiodiffusion TDF, propagation Friis champ libre — recalée en interne sur les 30 mesures certifiées ANFR/EXEM extérieures, présentée comme « estimation centrale d'ordre de grandeur du champ extérieur » (PR [#901](https://github.com/dellahstella/tellux/pull/901), [#898](https://github.com/dellahstella/tellux/pull/898)). Heatmap composite séparée en deux couches à grandeur homogène — magnétique nT / RF V/m (PR [#897](https://github.com/dellahstella/tellux/pull/897)). Section 9 RF de `cadre-scientifique.html` mise en cohérence (source unifiée, calibration interne, dispersion ×/÷ 3,3 en validation croisée) ; la **modélisation de la directivité d'antenne a été prototypée puis écartée** (ne généralise pas à cette échelle : dépointage inobservable en open data, dégrade l'accord aux mesures), le modèle isotrope étant **maintenu par décision documentée** (PR [#909](https://github.com/dellahstella/tellux/pull/909), [#911](https://github.com/dellahstella/tellux/pull/911), [#913](https://github.com/dellahstella/tellux/pull/913)). En parallèle : restauration de l'accroche « Révéler l'invisible » sur la landing (PR [#908](https://github.com/dellahstella/tellux/pull/908)), pérennisation de citations/DOI et durcissement du scanner de liens (PR [#899](https://github.com/dellahstella/tellux/pull/899), [#900](https://github.com/dellahstella/tellux/pull/900), [#902](https://github.com/dellahstella/tellux/pull/902)).

### Chantiers techniques prioritaires en cours

- ~~**Audit `emag` vs `crustal` dans `app.html`** : confirmer que les couches ne pointent pas vers les mêmes tuiles (suivi interne `EMAG-CRUSTAL-AUDIT-001`).~~ **Clôturé** — `EMAG-CRUSTAL-AUDIT-001` a été fermé après audit (`emag` et `crustal` fonctionnellement distincts, pas de redondance).
- ~~**Pages publiques `/transparence` et `/retractations`** sur `tellux.pages.dev`~~ **Publiées et opérationnelles** — `/transparence.html` est en production et a été enrichie le 1ᵉʳ mai 2026 d'une section « Cadres éthiques de référence » (audit Phase D, PR [#276](https://github.com/dellahstella/tellux/pull/276)). `/retractations.html` est également publiée et accessible directement ; depuis le chantier footer/redirects du 1ᵉʳ juin 2026 (PR [#751](https://github.com/dellahstella/tellux/pull/751)), elle est aussi atteignable via l'ancre `#retractations` de `/transparence.html`.
- ~~**Backlog SEO post-release `mairies.html`** : ajustements `h1`, lazy load `pdfmake`, élision « Mairie d'Ajaccio », Twitter Cards, audit Lighthouse. Non urgent, à traiter après stabilisation v1.~~ **Livré 1ᵉʳ mai 2026 (sprint L, PR [#293](https://github.com/dellahstella/tellux/pull/293) + [#294](https://github.com/dellahstella/tellux/pull/294))**, gain Lighthouse Performance +24.

---

## 3. Modules d'extension envisagés

Tellux pourra être étendu, à mesure que les conditions de conduite scientifique rigoureuse sont réunies, par des modules thématiques complémentaires. Ces modules ne sont pas activés à ce jour et aucun calendrier public n'est annoncé : leur conduite suppose la stabilisation préalable de la phase 1.

### Agrégation DIM

Dépôt contributif des dossiers d'information aux maires (DIM) : les communes qui utilisent Tellux uploadent leurs DIM reçus des opérateurs. Tellux devient le premier agrégateur de DIM corses, complémentaire à CartoRadio. Documents légalement publics (obligation de mise à disposition, L.34-9-1 II D). Prérequis : espace upload authentifié mairies, stockage Supabase fichiers, interface de contribution et modération. Pipeline : courrier MAIRIE_05 → upload DIM → couche Tellux.

### Dépôt ouvert des résultats de mesurage radon communaux

Permettre à une commune commanditaire de déposer les résultats de ses mesurages réglementaires du radon dans les établissements recevant du public dont elle est propriétaire, agrégés ensuite par Tellux à l'échelle territoriale, en complément de la classification radon officielle déjà publiée sur `app.html` et `mairies.html`. Prérequis : espace de dépôt authentifié mairies, stockage des résultats, interface de contribution et modération. Chantier de plus grande ampleur, non engagé, à envisager après stabilisation de la phase 1.

---

## 4. Jalons

| Jalon | Livrable | Horizon |
|-------|----------|---------|
| 1 | Stabilisation architecturale (landing cohérente, périmètre phase 1 figé) | 2026 T2 |
| 2 | Première relecture méthodologique externe | 2026-2027 |
| 3 | Déblocage des constantes gelées post-relecture | 2026 T3 ou ultérieur |
| 4 | Publication phase 1 stabilisée + communication publique | 2026 T3 |

---

## 5. Principes de pilotage

### Discipline sur le périmètre

Chaque phase est strictement cadrée. Les modules suivants existent techniquement dans le dépôt public mais ne sont pas mis en avant dans la landing ni les dossiers de financement en cours.

### Humilité épistémique

- Refus de l'alarmisme et de la trivialisation
- Distinction systématique mécanisme / effet biologique / effet sanitaire / impact populationnel
- Documentation des tensions plutôt que résolution prématurée
- Trois formulations proscrites dans tout contenu Tellux : (1) « deux réalités différentes » (le champ EM est un seul champ physique), (2) « les mesures ne s'additionnent pas » (principe de superposition), (3) « naturel = bénin » (les perturbations géologiques ne sont pas intrinsèquement inoffensives)

### Transparence et ouverture

- Transparence sur financements, partenariats et conflits d'intérêts
- Préférence pour les financements publics
- Ouverture des données et du code selon les principes FAIR
- Pré-enregistrement des protocoles avant collecte de données

### Indépendance

Projet indépendant. Architecture modulaire permettant la montée en gamme progressive.

---

## 6. Chantiers différés — déclenchement relecture méthodologique externe

Les chantiers suivants sont suspendus en attente de la validation méthodologique externe sur les zones gelées du modèle de calcul.

### Chantier 1 — Enrichissement éditorial du Guide d'utilisation

- **Statut :** publié, enrichissement éditorial possible
- **Type :** document pédagogique grand public
- **Objet :** expliquer comment lire chaque couche de la carte Tellux, les unités, l'interprétation des gradients, ce qu'est (et n'est pas) l'indice composite.
- **Destinataire :** visiteurs non spécialistes du site
- **État actuel :** publié en `/guide-utilisation.html` et lié depuis la section `#ressources` de la landing. L'ambition initiale du chantier (interprétation des gradients, indice composite, ordres de grandeur) peut dépasser le contenu actuel ; une refonte éditoriale enrichie reste possible une fois la relecture méthodologique externe avancée.
- **Dépendance :** indépendant de toute conversion PDF (la documentation publique est servie en `.html`).

### Chantier 2 — Rédaction du document « Hygiène EM à domicile »

- **Statut :** à rédiger
- **Type :** document pratique grand public
- **Objet :** recommandations et repères concrets sur l'exposition électromagnétique domestique, fondés sur les références biomédicales retenues par Tellux
- **Destinataire :** public concerné par la réduction d'exposition EM
- **État actuel :** non commencé, aucune source rédactionnelle existante. Sera publié en `.html` dans le repo public, sur le modèle des autres documents publics du projet.

---

## 7. Chantiers différés — module mairies (`mairies.html`)

Les chantiers suivants concernent l'évolution de l'outillage communal. Ils sont tracés mais non engagés : chacun suppose un arbitrage éditorial préalable, sans calendrier public à ce stade.

### Chantier 3 — Restructuration de l'onglet courrier par public

- **Statut :** différé, non engagé
- **Type :** refonte structurelle de `mairies.html`
- **Objet :** réorganiser l'ensemble de l'onglet « Générer un courrier » par public destinataire (citoyen / mairie / entrepreneur) plutôt que par fonction, en généralisant à tout le module — y compris les courriers électromagnétiques — le regroupement par public déjà amorcé pour le seul domaine radon (PR [#959](https://github.com/dellahstella/tellux/pull/959)).
- **État actuel :** non engagé. Le domaine radon sert de première application concrète du principe, scopée volontairement pour ne pas re-toucher tout le module en une fois.
- **Dépendance :** arbitrage éditorial préalable sur la structure cible du module.

### Chantier 4 — Ligne de présentation explicite en tête du module

- **Statut :** différé, non engagé
- **Type :** ajustement éditorial de `mairies.html`
- **Objet :** ajouter en tête du module une ligne présentant explicitement sa fonction, en conservant l'ossature actuelle centrée sur la relation commune/mairie (pas de bascule vers un positionnement de coordination citoyenne grand public, écarté à ce stade pour des raisons de sobriété éditoriale de la phase 1).
- **État actuel :** non engagé.
- **Dépendance :** arbitrage éditorial préalable sur la formulation.

---

## 8. Limites techniques

Le suivi détaillé des limites techniques ouvertes et fermées est tenu en interne.

---

*Fin du document. Mises à jour à chaque jalon structurant.*
