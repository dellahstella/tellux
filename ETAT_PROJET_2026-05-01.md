# Tellux — État du projet au 1er mai 2026

**Auteur :** session web Claude Opus 4.7, consolidation post-session 30 avril → 1er mai 2026 (15 PR mergées sur la session intensive du 1ᵉʳ mai 2026, dont la fermeture des 3 livrables Phase 1 « Livrables restants »)
**Objet :** photo nette de l'état du projet à cet instant. Remplace l'ensemble des recaps de sessions antérieurs.
**Usage :** à coller en début de toute future session pour récupérer le fil sans reconstitution.

---

## 1. Synthèse exécutive

Tellux est dans un état stable et productif. La couche scientifique consolidée a franchi une étape majeure le 30 avril avec la fusion intégrale du corpus en `TELLUX_CANON_INTEGRE.md` (1944 lignes, livrée en PR #6 puis enrichie). Les applications publiques `app.html` et `mairies.html` sont en production sur `tellux.pages.dev`. La couche publication externe est en cours de finalisation : il reste la note de synthèse institutionnelle universelle (étape I.2) avant clôture de cette couche.

Le projet entre dans une nouvelle phase où la priorité bascule : moins de production de nouveaux actifs, davantage de **sécurisation des actifs créés** et de **diversification des sources de financement**. Le pivot FEDER OS1.2 « Data & IA au service de l'intérêt général » est ouvert avec un verdict d'éligibilité confirmé sous condition de montage public-privé (consortium avec chef de file public obligatoire).

L'horizon opérationnel est désormais l'été 2026 : finalisation couche publication, consolidation actifs, montage consortium FEDER, première prestation privée éventuelle. L'ambition reste modulaire et progressive, sans engagement financier lourd avant sécurisation des premiers revenus.

---

## 2. État technique de la production

### 2.1 Branches et déploiement

`main` au 1ᵉʳ mai 2026 (nuit) est sur le commit `fa2678a` (sprint Q mergé, PR [#303](https://github.com/dellahstella/tellux/pull/303)). `dev` est aligné sur main.

Cycles livrés dans la session du 1ᵉʳ mai 2026 :

- **Cycle audit Phase D** (matin/après-midi) : `audit-D1` (PR [#274](https://github.com/dellahstella/tellux/pull/274) + [#275](https://github.com/dellahstella/tellux/pull/275)), `audit-D2` (PR [#276](https://github.com/dellahstella/tellux/pull/276) + [#277](https://github.com/dellahstella/tellux/pull/277)), `audit-D1bis` (PR [#278](https://github.com/dellahstella/tellux/pull/278) + [#279](https://github.com/dellahstella/tellux/pull/279)), `audit-D1ter` + `retrait-section-spdiac` regroupés (PR [#280](https://github.com/dellahstella/tellux/pull/280), [#281](https://github.com/dellahstella/tellux/pull/281), [#282](https://github.com/dellahstella/tellux/pull/282)).
- **Sprints documentaires et hygiène** : hygiène repo (PR [#283](https://github.com/dellahstella/tellux/pull/283) + [#284](https://github.com/dellahstella/tellux/pull/284)), retractations (PR [#285](https://github.com/dellahstella/tellux/pull/285) + [#286](https://github.com/dellahstella/tellux/pull/286)), README update (PR [#287](https://github.com/dellahstella/tellux/pull/287) + [#288](https://github.com/dellahstella/tellux/pull/288)), audit EMAG-CRUSTAL (PR [#289](https://github.com/dellahstella/tellux/pull/289) + [#290](https://github.com/dellahstella/tellux/pull/290)), audit cohérence DETTES (PR [#291](https://github.com/dellahstella/tellux/pull/291) + [#292](https://github.com/dellahstella/tellux/pull/292)).
- **Sprint L — SEO + performance `mairies.html`** (soir) : PR [#293](https://github.com/dellahstella/tellux/pull/293) + [#294](https://github.com/dellahstella/tellux/pull/294), commit prod `17e8eab`.
- **Sprint J — Sections 7-10 méthodologiques sur `cadre-scientifique.html`** (soir) : PR [#295](https://github.com/dellahstella/tellux/pull/295) + [#297](https://github.com/dellahstella/tellux/pull/297), commit prod `8bc60f9`.
- **Sprint M — hygiène repo post-J-L** (soir) : PR [#296](https://github.com/dellahstella/tellux/pull/296), commit `b549d82` puis promotion main `8bc60f9`.
- **Sprint N — Cowork glossaire** (soir) : drafts livrés dans `_drafts/glossaire/` (untracked, hors repo public), 94 entrées alphabétiques sur 21 lettres, intégrés ensuite par sprint P.
- **Sprint O — UI avancée `app.html`** (nuit) : PR [#298](https://github.com/dellahstella/tellux/pull/298) + [#299](https://github.com/dellahstella/tellux/pull/299), commit prod `2e23a0b`. Sélecteur de domaines physiques (chips) + badges temps réel dans le panneau Conditions.
- **Sprint P — intégration `glossaire.html` + 5 footers prioritaires** (nuit) : PR [#300](https://github.com/dellahstella/tellux/pull/300) + [#301](https://github.com/dellahstella/tellux/pull/301), commit prod `34aa961`.
- **Sprint Q — 4 footers restants** (nuit) : PR [#302](https://github.com/dellahstella/tellux/pull/302) + [#303](https://github.com/dellahstella/tellux/pull/303), commit prod `fa2678a`. `corpus.html` confirmé absent du repo public, exclu du périmètre.

Cloudflare Pages déploie automatiquement sur `tellux.pages.dev` à chaque push sur `main`.

### 2.2 Architecture en suite

| Application | Fichier | Statut |
|---|---|---|
| Landing | `index.html` | En prod, présentation Phase 1, footer enrichi lien Glossaire (sprint P) |
| Cartographie EM | `app.html` | En prod, Phase 1 stabilisée, ~460 Ko, **UI avancée livrée** (sprint O : chips de filtre par domaine physique + badges temps réel), nouveau lien Glossaire dans le header (sprint Q) |
| Outils mairies | `mairies.html` | En prod, v1 complète, 130 Ko, **SEO+perf optimisée** (sprint L, Lighthouse Performance 81), footer enrichi lien Glossaire (sprint Q) |
| Cadre scientifique | `cadre-scientifique.html` | En prod, ~80 Ko, sommaire à 11 entrées (sprint J : Sections 7-10 méthodologiques par domaine), footer enrichi lien Glossaire (sprint Q) |
| Glossaire technique | `glossaire.html` | **En prod** (sprint P), nouvelle page publique à la racine, ~48 Ko, 642 lignes, 94 entrées alphabétiques sur 21 lettres (A à Z hors J/O/Q/X/Y), palette DA v2 gelée, fontes auto-hébergées Fraunces + IBM Plex Sans, aucune dépendance externe |
| Patrimoine | `patrimoine.html` | Retiré du repo public, conservé localement |
| Agronomie | `agronomie.html` | Retiré du repo public, conservé localement |

Les pages publiques de support (transparence, mentions légales, méthode et limites, données vie privée, guide utilisation, retractations) sont en production. Le lien Glossaire est désormais présent dans les footers/headers des **9 pages éditoriales** du repo public (5 sprint P + 4 sprint Q ; `corpus.html` confirmé absent du repo, exclu du périmètre Q).

### 2.3 Stack technique

Cloudflare Pages sert la production. Cloudflare Workers via `wrangler.jsonc`. Backend Supabase (PostgreSQL + RLS), migrations 001-008 appliquées. GitHub `dellahstella/tellux` (public) pour le code applicatif, `dellahstella/tellux-corpus-internal` (privé) pour le corpus scientifique. N8N pour l'automatisation (workflow refresh antennes mensuel actif).

### 2.4 État de l'app.html

L'application Phase 1 a été nettoyée des résidus patrimoine (panneau géométrie mégalithique, biblio Thom/Leplat/Hoskin) au cours du cycle 4. Le périmètre est désormais aligné sur le positionnement déclaré : 4 domaines EM, couches contexte sobres, mode Expertise cadré, contributions utilisateur, export CSV, partage URL hash.

Le 1ᵉʳ mai 2026, quatre lignes ont été toilettées pour aligner la terminologie ASNR sur les mentions d'actualité (sprints `audit-D1bis` PR [#278](https://github.com/dellahstella/tellux/pull/278) et `audit-D1ter` PR [#280](https://github.com/dellahstella/tellux/pull/280)) : footer fonctionnel L.1184 (texte affiché « Téléray ASNR ↗ » et href `https://teleray.asnr.fr`), `epistemic_note` de `calcGammaAmbient` L.4274 (« Téléray ASNR »), et commentaire L.3992 d'agrégation des sources substrat (« BRGM + ASNR + IGN BD TOPO »). Les ~16 occurrences IRSN restantes dans le fichier sont toutes des références à des datasets explicitement millésimés 2018 (cartographie radon, décret 2018-434, NCRP 94, nom de colonne CSV `radon_class_IRSN`) et conservées intentionnellement.

**Sprint O (1ᵉʳ mai 2026, nuit, PR [#298](https://github.com/dellahstella/tellux/pull/298) + [#299](https://github.com/dellahstella/tellux/pull/299), commit prod `2e23a0b`) — UI avancée livrée :**

- **Sélecteur de domaines physiques** : 5 chips de filtre additifs ajoutés en haut de la sidebar `layers-accordion` (Tous / Statique / ELF / RF / Ionisant). 18 boutons `<button class="lbtn" id="b-X">` annotés d'un attribut `data-domains`. Toggles « tous » et « visuel » toujours visibles. Aucun toggle masqué par filtre ne perd son état actif/inactif. Fonction `filterByDomain(domain)` ajoutée dans le bloc `<script>` principal.
- **Badges temps réel dans le panneau Conditions** (4 badges en tête, sous-sections accordion préservées) : Kp (NOAA SWPC), Réseau (RTE eco2mix, multiplicateur condensé `×N.NN`), Live (statut Supabase, dot pending/ok/error synchronisé sur `sb-status-dot`), Orage (Blitzortung, caché si pas d'activité). Fonction `syncBadges()` hookée dans `updateCondSummaries()` (rythme 30 s déjà en place) et dans le `setTimeout` initial de 2 s — pas de `setInterval` dédié, intégration propre dans le tick existant.
- **Aucune nouvelle variable CSS racine introduite**, palette DA v2 gelée respectée. Aucune modification des fonctions `tog()`, `toggleAccordion()`, `toggleCondSection()`, ni des zones GELÉES (`EXPERT_WEIGHTS_DEFAULT`, `EXPERT_BOUNDS_DEFAULT`, `calcGammaAmbient` formule NCRP 94).

**Sprint Q (1ᵉʳ mai 2026, nuit, PR [#302](https://github.com/dellahstella/tellux/pull/302) + [#303](https://github.com/dellahstella/tellux/pull/303), commit prod `fa2678a`) — lien Glossaire dans le header :**

Nouveau lien `<a class="hdr-btn" href="/glossaire.html" target="_blank" rel="noopener">Glossaire</a>` ajouté dans `hdr-actions` (l. 1165) entre « Comprendre les termes » et « À propos ». Le bouton « Comprendre les termes » et la fonction `openGlossaryDrawer()` (drawer interne) restent strictement préservés : le nouveau lien pointe vers la page publique complète, complémentaire mais distincte du drawer.

### 2.5 Audit Phase D livré le 1ᵉʳ mai 2026

L'audit Phase D du site public et du dossier de pré-candidature FEDER a été produit en session web Claude le 1ᵉʳ mai 2026. Il a donné lieu à cinq sprints successifs livrés le même jour :

- **`audit-D1`** (PR [#274](https://github.com/dellahstella/tellux/pull/274) + [#275](https://github.com/dellahstella/tellux/pull/275)) — quatre fixes structurants sur la landing : alignement initial IRSN → ASNR (7 occurrences sur 4 fichiers), harmonisation du compteur antennes hero sur `~960 sites ANFR`, enrichissement du footer avec le statut juridique (`Stella Canis Majoris · micro-entreprise SIRET 993 881 481 00010 · 20200 Bastia · 2026`), libellé contact projet explicite (`Contact projet — Lucas Iannaccone Frasseto, porteur du projet Tellux Corse`).
- **`audit-D2`** (PR [#276](https://github.com/dellahstella/tellux/pull/276) + [#277](https://github.com/dellahstella/tellux/pull/277)) — ajout d'une section « Cadres éthiques de référence » sur `transparence.html` (Charte data Corse 21 principes en 9 titres, Guide IA Smart Isula 12 bonnes pratiques, articulation préfigurée par les pratiques actuelles, conditionnelle au financement FEDER) et d'une section « Inscription territoriale » sur `index.html` (PO FEDER-FSE+ Corse 2021-2027 RSO1.2 Ligne 2, SDTAN Smart Isula 22/074 AC, SPDIAC 2026E1009).
- **`audit-D3`** (hors repo public) — révisions du dossier de pré-candidature FEDER appliquées sur `Tellux/DOSSIER_PRECANDIDATURE_FINAL.md` (gitignored à la racine) et synchronisées dans le repo privé `tellux-corpus-internal/docs/` (commit `93612c5`). Bascule EUPL → MIT sur 17 occurrences (motif : licence permissive plus largement adoptée, compatibilité AAP, argument essaimage), reformulation intégrale de la sous-section 2.3.7 (Souveraineté) en quatre paragraphes structurés autour d'un audit juridique de conformité au CLOUD Act, alignement de la nuance Supabase Inc. (entité juridique américaine) vs instance technique `eu-west-1` Dublin Irlande sur les sous-sections 2.3.6, 2.3.3, 2.3.11.
- **`audit-D1bis`** (PR [#278](https://github.com/dellahstella/tellux/pull/278) + [#279](https://github.com/dellahstella/tellux/pull/279)) — toilettage complémentaire IRSN → ASNR sur 5 mentions d'actualité non millésimées résiduelles : `cadre-scientifique.html` sections 1, 4.1, 6.3 et `app.html` footer + `epistemic_note`.
- **`audit-D1ter`** + **`retrait-section-spdiac`** (PR [#280](https://github.com/dellahstella/tellux/pull/280), [#281](https://github.com/dellahstella/tellux/pull/281), [#282](https://github.com/dellahstella/tellux/pull/282)) — deux derniers résiduels IRSN dans `app.html` (commentaire L.3992 et href L.1184 vers `teleray.asnr.fr`, vivacité 200 OK confirmée par curl), et retrait éditorial de la section « Inscription territoriale » de la landing introduite quelques heures plus tôt par le sprint `audit-D2`. Décision Soleil : sobriété de la landing publique, la cohérence narrative institutionnelle est portée par le dossier FEDER lui-même. Section symétrique « Cadres éthiques de référence » sur `transparence.html` conservée intentionnellement.

État final post-cycle : plus aucune mention IRSN d'actualité (non millésimée) sur le site public ni dans le code applicatif. Le draft markdown source de la section SPDIAC (`_drafts/audit-D1/section_spdiac_landing.md`, untracked) est conservé localement pour réutilisation potentielle ultérieure (par exemple page À propos dédiée).

### 2.6 Sprint J — Documentation méthodologique par domaine physique (soir 1ᵉʳ mai 2026)

PR [#295](https://github.com/dellahstella/tellux/pull/295) (commit `9757021` sur dev, promotion main en attente). Drafts source produits par Cowork dans `Tellux/_drafts/methodo/` (untracked, hors repo public).

Quatre sections homogènes intégrées dans `cadre-scientifique.html` entre la Section 6 et l'Annexe A :

- **Section 7 — Magnétique statique** (`#section-7-magnetique-statique`, ≈ 870 mots) : autour de `calcMagneticStatic`, IGRF-14, EMAG2v3, AQU INTERMAGNET, Kp, Sq.
- **Section 8 — Magnétique basse fréquence ELF 50 Hz** (`#section-8-elf`, ≈ 950 mots) : autour de `calcMagneticELF_v2`, EDF SEI, Biot-Savart, dettes BT-CALIBRATION-001, HTA-TENSION-001, ELF-TRIPH-001, RTE-OPENDATA-001.
- **Section 9 — Radiofréquences** (`#section-9-rf`, ≈ 970 mots) : autour de `calcRF`, CartoRadio ANFR, ICNIRP 2020, modèle isotrope avec décroissance 1/d², 30 fiches certifiées EXEM intégrées.
- **Section 10 — Rayonnement ionisant** (`#section-10-ionisant`, ≈ 1 030 mots) : autour de `calcGammaAmbient` et `calcRadonPotential`, classification ASNR décret 2018-434, NCRP 94 (gelé `NCRP-001`), Téléray AJA + BAP.

Volume total ajouté : ≈ 3 820 mots de prose. Sommaire enrichi (passe de 7 à 11 entrées). Liens cliquables inter-sections ajoutés (recommandation Cowork retenue). Section 1 reformulée pour retrait mention publique candidature FEDER/ANR/Collectivité de Corse (cohérence doctrine éditoriale post-cycle audit Phase D). Footer date avril → mai 2026.

Livre le chantier ROADMAP « Documentation méthodologique par domaine physique » de la section 2 Phase 1.

### 2.7 Sprint L — SEO + performance `mairies.html` (soir 1ᵉʳ mai 2026)

PR [#293](https://github.com/dellahstella/tellux/pull/293) + [#294](https://github.com/dellahstella/tellux/pull/294) mergées sur main (commit prod `17e8eab`).

Score Lighthouse Performance **57 → 81** (+24). Web vitals : LCP/FCP 6.1 s → 1.5 s, TTI 7.6 s → 2.2 s, Speed Index 6.1 s → 1.8 s.

Modifications :

- **Lazy load `pdfmake`** : retrait du chargement synchrone au boot (~600 ko + 200 ko fonts) ; injection dynamique au premier clic « Télécharger PDF » via `loadPdfMake()` avec retry au prochain clic en cas d'échec réseau et indication visuelle « Préparation du PDF… ».
- **Élision française** : nouvelle fonction `applyMairieElision()` appliquée dans `substitute()` et `substituteHtml()` avant la substitution des `[VARIABLES]`. Voyelle ou voyelle accentuée → « Mairie d'Ajaccio » / « Mairie d'Évisa » ; article L' (L'Île-Rousse) → « Mairie de l'Île-Rousse » ; consonne → « Mairie de Bastia ».
- **Open Graph + Twitter Cards** : 9 meta tags ajoutées (`og:type`, `og:locale`, `og:site_name`, `og:image`, `og:image:alt` + 4 `twitter:*`). Image temporaire `assets/logo/favicon_512.png` (512×512, ratio 1:1) ; **asset Open Graph dédié 1200×630 (1.91:1) à produire en session Soleil dédiée DA / Cowork** — non créé d'autorité.
- **Audit `h1`** : un seul `<h1>` confirmé l.436, hiérarchie OK, pas de modification requise.

Livre le chantier ROADMAP « Backlog SEO post-release `mairies.html` » de la section 2 Phase 1.

Quatre anomalies hors périmètre détectées par Lighthouse et formalisées en dettes techniques (cf. `DETTES_TECHNIQUES.md`) : `ROBOTS-TXT-001`, `A11Y-CONTRAST-001`, `MAIRIES-CLS-TBT-001`, `MAIRIES-REDIRECTS-001`.

### 2.8 Sprint O — UI avancée `app.html` (nuit 1ᵉʳ mai 2026)

PR [#298](https://github.com/dellahstella/tellux/pull/298) + [#299](https://github.com/dellahstella/tellux/pull/299) mergées sur main (commit prod `2e23a0b`). Décisions Soleil retenues : Option A1 (chips de filtre additifs en haut de la sidebar, ne casse pas l'existant) et Option B1 (panneau Conditions toujours visible avec badges, sections accordion détaillées préservées).

Détails techniques consignés en section 2.4 ci-dessus (chips de filtre, badges temps réel, hook `syncBadges()` dans `updateCondSummaries()`).

Livre le chantier ROADMAP « Phase d'UI avancée (sélecteur de domaines, badges temps réel) » de la section 2 Phase 1.

### 2.9 Sprints P + Q — Glossaire technique intégré (nuit 1ᵉʳ mai 2026)

**Sprint P (PR [#300](https://github.com/dellahstella/tellux/pull/300) + [#301](https://github.com/dellahstella/tellux/pull/301), commit prod `34aa961`)** : intégration de la page `glossaire.html` à la racine du repo (draft Cowork sprint N). 642 lignes, ~48 ko, 94 entrées alphabétiques sur 21 lettres (A à Z hors J/O/Q/X/Y — pas d'entrées pertinentes Phase 1). Style aligné DA v2, fontes auto-hébergées Fraunces (titres) + IBM Plex Sans (texte courant) chargées depuis `assets/fonts/`. Aucune dépendance externe. Lien Glossaire ajouté dans les footers de 5 pages éditoriales prioritaires : `index.html` (2 emplacements : `lp-contact-mentions` + `lp-footer-right`), `transparence.html`, `retractations.html`, `mentions-legales.html`, `donnees-vie-privee.html`.

**Sprint Q (PR [#302](https://github.com/dellahstella/tellux/pull/302) + [#303](https://github.com/dellahstella/tellux/pull/303), commit prod `fa2678a`)** : lien Glossaire ajouté dans les 4 pages éditoriales restantes : `cadre-scientifique.html` (footer `page-footer`), `methode-et-limites.html` (footer `page-footer`), `mairies.html` (footer `mr-footer-links`), `app.html` (header `hdr-actions` via nouveau `<a class="hdr-btn">` `target="_blank"`, drawer interne `openGlossaryDrawer()` strictement préservé). `corpus.html` confirmé absent du repo public, exclu du périmètre.

Cohérence transversale acquise sur les **9 pages éditoriales** du repo public.

Livre le chantier ROADMAP « Glossaire technique intégré » de la section 2 Phase 1.

---

## 3. État de la couche publication externe

La couche publication est en finalisation à la suite de la session 30 avril → 1er mai 2026.

### 3.1 Étapes livrées

- **Étape D** : 22 amendements canon + 5 notes v2.2
- **Étape G** : note 10 produite (élément G1 absorbé dans cadre-scientifique.html Section 5.2 cible)
- **Étape H** : 12 amendements canon, note 10 absorbée
- **Fix** : Hermans, Maffei, tensions 12→13
- **Hygiène** : .gitattributes + correction SARL → micro-entreprise dans les documents projet
- **Étape I.1** : fusion intégrale `TELLUX_CANON_INTEGRE.md` (1944 lignes)
- **Étape I.3** : résumé exécutif (en finalisation)

### 3.2 Étapes restantes

- **Étape I.2** : note de synthèse institutionnelle universelle (priorité A, ~4-5h en Cowork)
- **Régénération `TELLUX_CANON_INTEGRE.md`** post-PR #6 : ~1h Code, contient encore les anciennes versions Hermans/Maffei/tensions (priorité B)
- **Mise à jour landing repo public** avec les 3 dérivés I.1+I.2+I.3 et apports note 10 G1 dans `cadre-scientifique.html` Section 5.2 (priorité C)

### 3.3 Étape J ouverte

Extraction roadmap après I.2 (lien avec auto-affinage et engine-extraction-plan).

---

## 4. État du backend Supabase

Migrations 001 à 008 appliquées. La migration 008 a été appliquée le 27 avril 2026 dans le cadre du cycle 4 (contribution metadata + IGRF). La migration 007 (`residuals` table) reste dormante, prévue pour l'étape P1 du roadmap auto-affinage.

Workflow GitHub Actions de refresh antennes ANFR mensuel actif. Pas de backup automatisé de la base à ce jour — dette à traiter (voir section 7).

---

## 5. Outreach institutionnel

### 5.1 Lettres envoyées le 27 avril 2026

Envoi groupé du dimanche pour arrivée en haut de la pile lundi matin :
- Santoni / UMR SPE Corte (PDF dossier scientifique v1.4)
- ASNR (Téléray + radon)
- EDF SEI
- BRGM

### 5.2 Statut au 1er mai 2026

Pas de réponse formelle reçue à ce jour. Le délai institutionnel normal (2-3 semaines silence puis follow-up court) est en cours. Pas de relance Santoni avant l'expiration de ce délai.

### 5.3 Ne pas relancer Santoni dans l'immédiat

La fenêtre Santoni est en pause. D'autres autorités compétentes peuvent être engagées en parallèle sans interférer (voir dossier FEDER consolidé, section consortium).

### 5.4 Différé

RTE différé post-financement. Profils B (Cagliari/Sassari Sardaigne) et C (ANSES/SCHEER UE) en Phase 2.

---

## 6. Dettes techniques actives

Tracées dans `DETTES_TECHNIQUES.md`, état au 1er mai 2026 :

- `CONTRIB-SCHEMA-001` : inconsistance stockage flux A/B contributions, moins critique depuis verrouillage flux B
- `RADON-CLASS-DUPLICATE` : duplication mapping radon, à traiter en Phase 0 extraction
- `HELPERS-INLINE-CONSTS` : constantes inline à hisser, Phase 0
- `RADON-DATASET-COVERAGE-001` : couverture partielle 2B vs décret 2018-434, à compléter

---

## 7. Risques actifs et chantiers de sécurisation

Cette section consigne les risques de perte ou dégradation des actifs Tellux. Le plan de sécurisation détaillé est dans le document `FEDER_OS1_2_DOSSIER_CONSOLIDE_2026-05-01.md` section diversification.

### 7.1 Hébergement

Cloudflare Pages et Supabase sont des entités américaines, soumises au CLOUD Act. Pour FEDER OS1.2 (souveraineté UE exigée), une migration ou un montage en consortium qui externalise la conformité hébergement vers le chef de file public est nécessaire. Risque latent indépendant de FEDER : exposition géopolitique non immédiate mais réelle.

### 7.2 Backup base Supabase

Pas de backup automatisé. Migrations versionnées dans `_migrations/` mais les contributions terrain sont irremplaçables si la base est perdue. Chantier prioritaire : script de backup quotidien.

### 7.3 Repo GitHub

Compte personnel Soleil. Pas de mirror externe vers une plateforme européenne (Codeberg, Forgejo, ou GitLab souverain). Mirror automatique recommandé pour anticiper la conformité UE et la résilience.

### 7.4 Domaine

`tellux.pages.dev` est un sous-domaine Cloudflare. Pas de domaine propre acquis. Acquisition d'un domaine `.corsica` est cohérente avec FEDER (engagement listé dans le cahier des charges) et représente une assise propre pour le projet.

### 7.5 Identité visuelle

Logo v14 (avril 2026) en local. Sources Figma à archiver. Pas de protection INPI à ce jour.

### 7.6 Dépendance Soleil

Toute la connaissance opérationnelle est concentrée sur Soleil. Documentation onboarding tiers à produire pour rendre le projet transmissible en cas d'imprévu.

---

## 8. Règles multi-agents en vigueur

Établies suite aux dérives constatées en session du 1er mai 2026.

- Pas de session Cowork et Claude Code en parallèle. Une seule session active à la fois.
- `git fetch` et `git status` systématiques en début de chaque session.
- Tâches inférieures à 4h : Claude Code seul.
- Tâches supérieures à 4h : Cowork seul, Code en pré et post-session.
- Cowork est en mode dégradé FUSE permanent : pas d'opérations git d'écriture autorisées.
- Code voit la vérité working tree, pas Cowork (qui voit des artefacts FUSE).
- Pré-cadrage avec Soleil obligatoire avant session multi-agent.
- Vérification factuelle obligatoire avant publication externe.

---

## 9. File d'attente actionnable

### 9.0 Phase 1 ROADMAP — livrables restants

Les **3 livrables Phase 1 « Livrables restants »** sont tous traités au 1ᵉʳ mai 2026 nuit :

- ✅ Documentation méthodologique par domaine physique (sprint J)
- ✅ Phase d'UI avancée — sélecteur de domaines + badges temps réel (sprint O)
- ✅ Glossaire technique intégré (sprints N + P + Q)

### 9.1 Priorité A — Boucler la couche publication

Vérifier le statut du merge PR #6. Lancer l'étape I.2 (note de synthèse institutionnelle universelle, ~4-5h en Cowork). Conditions : session dédiée Cowork, pré-cadrage avec Soleil sur le périmètre exact de la note (cible institutionnelle générique vs déclinaison spécifique).

### 9.2 Priorité B — Régénération `TELLUX_CANON_INTEGRE.md` post-PR #6

~1h en Code. Le fichier contient encore les anciennes versions Hermans, Maffei et tensions 12. À régénérer pour cohérence finale.

### 9.3 Priorité C — Mise à jour landing repo public

Intégration des 3 dérivés I.1, I.2, I.3 dans le repo public. Apports note 10 G1 dans `cadre-scientifique.html` Section 5.2.

### 9.4 Chantiers différés / parqués (post-livrables Phase 1)

- **Polissage glossaire** (différé, décision Soleil) : ajout d'ancres `id` par terme dans `glossaire.html` + transformation des `<span class="xref">` en liens cliquables. Sprint dédié à programmer.
- **Refactorisation transversale Sections 4/5 → 7-10 dans `cadre-scientifique.html`** (parqué, Cowork dédié) : éviter les doublons entre les sections agrégées 4/5 et les nouvelles sections détaillées 7-10 livrées au sprint J.
- **Asset Open Graph 1200×630 dédié pour `mairies.html`** (parqué, Cowork DA) : signalé au sprint L. Image temporaire actuelle `assets/logo/favicon_512.png` (512×512) à remplacer par un asset 1.91:1 dédié.
- **4 dettes Lighthouse à arbitrer** (déjà tracées dans `DETTES_TECHNIQUES.md` par sprint M) : `ROBOTS-TXT-001`, `A11Y-CONTRAST-001`, `MAIRIES-CLS-TBT-001`, `MAIRIES-REDIRECTS-001`.

### 9.5 Suivants

Étape J : extraction roadmap après I.2. Lien avec `auto-affinage-conception-v1.md` et `tellux-engine-extraction-plan.md`.

---

## 10. Position épistémique et garde-fous

Inchangés depuis `PROJECT_INSTRUCTIONS_v3.md`. Les trois formulations proscrites restent proscrites. Monte d'Oro reste le centre géométrique des mégalithes. Les zones gelées GELÉ-001 (`EXPERT_WEIGHTS_DEFAULT`, `EXPERT_BOUNDS_DEFAULT`, `EXPERT_EPISTEMIC_NOTE`) restent gelées sans validation post-relecture physicien tiers. La formule NCRP 94 terrestre gamma reste un placeholder.

---

## 11. Notes pour la prochaine session

1. Lire ce fichier en entier
2. Lire `PROJECT_INSTRUCTIONS_v3.md` (règles communes + spécifiques par environnement)
3. Lire `FEDER_OS1_2_DOSSIER_CONSOLIDE_2026-05-01.md` si la session porte sur le financement
4. Si session technique : lire aussi `DETTES_TECHNIQUES.md` et `auto-affinage-conception-v1.md`
5. Si session corpus : lire `TELLUX_HYPOTHESES_PROTOCOLES.md` et `TELLUX_MODELE_CALCUL.md`
6. Vérifier la dernière commit sur `dev` et `main` avant toute action

---

*Fin de l'état projet. À actualiser après chaque session significative ou tous les 7 jours.*
