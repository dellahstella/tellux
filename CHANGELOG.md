# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)
Versioning sémantique : [SemVer](https://semver.org/lang/fr/)

---

## [2.10.2] — 2026-05-01

### Added — Ancres `id="term-{slug}"` sur les 94 entrées de `glossaire.html` (PR à venir, sprint `feat/glossaire-ancres-liens`)

Sprint de polissage post-livraison du glossaire (sprints N + P + Q). Chaque entrée `<dt>` reçoit une ancre stable au format `id="term-{slug}"` permettant le partage de liens directs vers une entrée spécifique (par exemple `https://tellux.pages.dev/glossaire.html#term-igrf-international-geomagnetic-reference-field`).

**Convention de slug appliquée** : libellé en minuscules, accents retirés (NFKD), translittération `µ → u` / `² → 2` / `³ → 3`, caractères non-alphanumériques remplacés par `-`, pas de `-` consécutifs, préfixe `term-` systématique pour éviter collision avec les ancres alphabétiques `letter-X` existantes.

**Statistiques** : 94 ancres ajoutées, 0 collision détectée (94 slugs uniques sur 94 libellés).

### Changed — Renvois croisés `cf. X` du glossaire transformés en liens cliquables internes

73 occurrences `<em>cf. X</em>` (sur 74 au total, l'occurrence restante étant la méta-référence `<em>cf. terme</em>` dans l'introduction décrivant le format) transformées en `<a class="xref" href="#term-{slug}">cf. X</a>`. Les renvois pointent désormais vers l'entrée correspondante du glossaire.

**Mapping libellé → slug avec aliases** : 186 alias générés (94 libellés complets + sigles avant em-dash + parties après em-dash + unités entre parenthèses) pour résoudre les renvois courts (`cf. ANFR` → `term-anfr-agence-nationale-des-frequences`, `cf. nSv/h` → `term-nanosievert-par-heure-nsv-h`).

**Renvois orphelins** : 0. Tous les `cf. X` ont trouvé une entrée correspondante dans le glossaire.

### Changed — CSS `glossaire.html`

Trois règles CSS ajoutées sous la déclaration existante de `.xref` :

- `dl.glossary dd a.xref { border-bottom: none; }` — neutralise le soulignement par défaut des liens hérité du style global `<a>` de la page.
- `dl.glossary dd a.xref:hover { color: var(--tx-ardoise); border-bottom: 1px solid var(--tx-mica); }` — état hover discret cohérent avec la sobriété de la page.
- `dl.glossary dt[id] { scroll-margin-top: 80px; }` — décalage visuel lors d'un scroll vers une ancre, pour éviter que l'entrée cible soit collée au bord supérieur de la fenêtre.

### Validation

- ✅ 94 ancres `term-X` créées, 73 liens `<a class="xref">` générés, 0 lien cassé (vérifié par script Python).
- ✅ Aucune collision avec les ancres existantes `letter-X` (préfixe distinct).
- ✅ Aucune modification du contenu textuel des entrées (libellés, définitions, sources, exemples).
- ✅ Aucune modification de la structure générale de la page (header, sommaire, footer, sections).
- ✅ Aucune nouvelle entrée ajoutée ni supprimée.
- ✅ Palette DA v2 gelée respectée (variables existantes uniquement).

---

## [2.10.1] — 2026-05-01

### Changed — Cohérence transversale Glossaire : 4 pages éditoriales restantes (PR à venir, sprint `feat/glossaire-footers-suite`)

Sprint complémentaire au sprint P (`[2.10.0]`) qui avait traité les 5 pages éditoriales prioritaires. Ce sprint Q ferme la cohérence transversale en ajoutant le lien Glossaire sur les 4 pages restantes.

**Pages mises à jour** :

- **`cadre-scientifique.html`** : footer `page-footer` (l. 715) — Glossaire inséré entre Accueil et Mentions légales (Rétractations absente sur cette page).
- **`methode-et-limites.html`** : footer `page-footer` (l. 533) — même pattern.
- **`mairies.html`** : footer `mr-footer-links` (l. 663) — Glossaire inséré entre Cartographie EM et Mentions légales. Aucune modification des balises Open Graph ni des balises SEO posées au sprint L.
- **`app.html`** : nouveau lien `<a class="hdr-btn" href="/glossaire.html" target="_blank" rel="noopener">Glossaire</a>` ajouté dans le header `hdr-actions` (l. 1165) entre « Comprendre les termes » et « À propos ». Le bouton « Comprendre les termes » et la fonction `openGlossaryDrawer()` (drawer interne) sont **strictement préservés** : le nouveau lien pointe vers la page publique complète sans interférer avec le drawer existant.

**Page exclue** : `corpus.html` n'existe pas dans le repo public (retirée lors d'un sprint Phase D antérieur). Périmètre réduit de 5 à 4 fichiers.

**Cohérence transversale acquise** : le lien Glossaire est désormais présent dans les 9 pages éditoriales du repo public (5 sprint P + 4 sprint Q). Le 3ᵉ et dernier livrable Phase 1 ROADMAP « Glossaire technique intégré » est traité de bout en bout.

### Validation

- ✅ Aucune modification du contenu de `glossaire.html`.
- ✅ Aucune modification des balises SEO/Open Graph de `mairies.html` (sprint L préservé).
- ✅ Aucune modification des Sections 7-10 ni du sommaire de `cadre-scientifique.html` (sprint J préservé).
- ✅ Aucune modification des fonctions JavaScript de `app.html` (`openGlossaryDrawer()`, zones GELÉES).
- ✅ Aucune dépendance externe ajoutée.

---

## [2.10.0] — 2026-05-01

### Added — Page publique `glossaire.html` (PR à venir, sprint `feat/glossaire-page-integration`)

Nouvelle page publique `/glossaire.html` (~48 KB, 642 lignes) : glossaire technique de 94 entrées couvrant le vocabulaire scientifique, technique et méthodologique de Tellux. Draft produit par Cowork session 1ᵉʳ mai 2026 dans `Tellux/_drafts/glossaire/` (untracked, hors repo public), intégré tel quel à la racine du repo.

**Couverture alphabétique** : 21 lettres présentes (A à Z hors J, O, Q, X, Y — laissées absentes, pas d'entrées pertinentes pour Phase 1). Entrées triées alphabétiquement, avec ancres `#entry-XXX` pour cross-référencement futur.

**Style aligné DA v2** : palette gelée (Ardoise, Pierre, Mica, Brume, Maquis, Ocre, Porphyre, Tyrrhénien) appliquée via les variables CSS racines existantes. Fontes auto-hébergées Fraunces (titres) + IBM Plex Sans (texte courant) chargées depuis `assets/fonts/`. Aucune nouvelle dépendance externe.

### Changed — 5 footers mis à jour avec lien Glossaire

Insertion d'un lien `<a href="/glossaire.html">Glossaire</a>` dans la liste de navigation pied de page de 5 pages publiques :

- **`index.html`** : 2 emplacements modifiés. Bloc `lp-contact-mentions` (entre Rétractations et Mentions légales) et bloc `lp-footer-right` (entre Rétractations et Ressources).
- **`transparence.html`** : footer `page-footer` (entre Rétractations et Mentions légales).
- **`retractations.html`** : footer `page-footer` (entre Transparence et Mentions légales).
- **`mentions-legales.html`** : footer `page-footer` (entre Rétractations et Données & vie privée).
- **`donnees-vie-privee.html`** : footer `page-footer` (entre Rétractations et Mentions légales).

**Note de sprint Q-bis prévu** : 5 pages publiques restantes (`cadre-scientifique.html`, `methode-et-limites.html`, `mairies.html`, `corpus.html`, `app.html`) ont un footer hétérogène ou structuré différemment. Mise à jour groupée prévue dans un sprint Q-bis dédié pour préserver l'homogénéité visuelle.

### Validation

- ✅ Page `glossaire.html` : 642 lignes, ~48 KB, fontes auto-hébergées présentes (`assets/fonts/fraunces/` + `assets/fonts/ibm-plex-sans/`).
- ✅ Logo SVG vérifié : `assets/logo/tellux_logo.svg` présent.
- ✅ Aucune modification des fonctions JavaScript des 5 pages modifiées (footers uniquement).
- ✅ Aucune dépendance externe ajoutée.
- ✅ Aucune nouvelle variable CSS racine introduite.

Livre le chantier ROADMAP « Glossaire technique public » identifié dans le brief Cowork.

---

## [2.9.0] — 2026-05-01

### Added — UI avancée `app.html` : sélecteur de domaines + badges temps réel (PR à venir, sprint `feat/ui-avancee-domaines-badges`)

Sprint UI avancée listé dans la ROADMAP section 2 « Phase 1 — Livrables restants » : « Phase d'UI avancée (sélecteur de domaines, badges temps réel) ». Désormais traité.

**Sélecteur de domaines physiques** (chips de filtre, Option A1) :

- 5 chips ajoutés en haut de la sidebar `layers-accordion`, juste après le bouton `sidebar-toggle` : **Tous** (état initial actif), **Statique**, **ELF**, **RF**, **Ionisant**.
- Cliquer sur un chip filtre les toggles de couches selon leur domaine physique. Mapping : 18 boutons `<button class="lbtn" id="b-X">` annotés d'un attribut `data-domains` (valeurs parmi `statique`, `elf`, `rf`, `ionisant`, `tous`, `visuel` — séparées par espace pour les multi-domaines comme `b-cav` = ionisant + statique).
- Toggles « Tous » (Champ composite, Mesures EM, Sites géophysiques remarquables) et « Visuel » (Hydrographie, Forêts publiques) restent toujours visibles quel que soit le filtre.
- Un groupe d'accordion qui ne contient plus aucun toggle visible est masqué automatiquement (transition propre en cas de filtre exclusif).
- Aucun toggle masqué par filtre ne perd son état actif/inactif : retour à « Tous » restaure l'état tel quel.
- Fonction `filterByDomain(domain)` ajoutée dans le bloc `<script>` principal, en cohérence avec le style des fonctions existantes.

**Badges temps réel** (panneau Conditions toujours visible, Option B1) :

- 4 badges ajoutés en tête du panneau `cond-panel`, au-dessus des 4 sous-sections existantes (qui restent en accordion replié par défaut, comportement préservé) :
  - **Kp** (indice d'activité géomagnétique, NOAA SWPC)
  - **Réseau** (charge réseau Corse condensée en multiplicateur ×N, RTE eco2mix)
  - **Live** (statut Supabase, indicateur dot pending/ok/error synchronisé sur `sb-status-dot`)
  - **Orage** (caché par défaut, affiché uniquement si activité orageuse détectée par Blitzortung)
- Fonction `syncBadges()` ajoutée pour synchroniser les valeurs depuis les éléments sources (`kp-v`, `res-charge`, `sb-status-dot`, `lightning-v`) vers les badges. Hookée dans `updateCondSummaries()` (rythme 30 s déjà en place) et dans le `setTimeout` initial de 2 s — pas de `setInterval` dédié, intégration propre dans le tick existant.

### Changed — Variables CSS racines `app.html` non modifiées

Les chips et badges utilisent uniquement les variables CSS existantes (`--bg`, `--bg3`, `--pierre-ombre`, `--maquis`, `--maquis-clair`, `--mica`, `--ardoise-clair`, `--tx`, `--tx3`, `--border`, `--mono`). Aucune nouvelle variable racine introduite, palette DA v2 gelée respectée.

### Validation

- ✅ `node --check` OK sur les 2 blocs `<script>` inline d'`app.html` (~301 KB de JS après strip des commentaires HTML)
- ✅ Aucune modification des fonctions `tog()`, `toggleAccordion()`, `toggleCondSection()`, `togFailles`, `togPostesSources`, `togPointsChauds`, `togSitesRemarquables`
- ✅ Aucune modification des 4 sous-sections existantes du panneau Conditions (`cond-sec-solaire`, `cond-sec-atmo`, `cond-sec-reseau`, `cond-sec-contribs`)
- ✅ Aucune modification des zones GELÉES (`EXPERT_WEIGHTS_DEFAULT`, `EXPERT_BOUNDS_DEFAULT`, `EXPERT_EPISTEMIC_NOTE`, `calcGammaAmbient` formule NCRP 94)
- ✅ Aucune dépendance externe ajoutée

Livre le chantier ROADMAP « Phase d'UI avancée (sélecteur de domaines, badges temps réel) » de la section 2 Phase 1.

---

## [2.8.5] — 2026-05-01

### Added — Documentation méthodologique par domaine physique sur `cadre-scientifique.html` (PR à venir, sprint `chore/methodo-sections-7-10-cadre-scientifique`)

Intégration de 4 nouvelles sections homogènes dans `cadre-scientifique.html`, une par domaine physique du modèle Tellux. Drafts produits par Cowork session 1ᵉʳ mai 2026 dans `Tellux/_drafts/methodo/` (untracked, hors repo public). Livre le chantier ROADMAP « Documentation méthodologique par domaine physique » de la section 2 « Phase 1 ».

**Nouvelles sections** (insérées entre Section 6 et Annexe A) :

- **Section 7 — Magnétique statique** (#section-7-magnetique-statique) : ~870 mots, 7 sous-sections homogènes (définition physique, phénoménologie Corse, sources, formules `calcMagneticStatic`, incertitudes, dettes associées, ce que la modélisation permet et ne permet pas).
- **Section 8 — Magnétique basse fréquence ELF 50 Hz** (#section-8-elf) : ~950 mots, mêmes 7 sous-sections, autour de `calcMagneticELF_v2` et du réseau EDF SEI.
- **Section 9 — Radiofréquences** (#section-9-rf) : ~970 mots, autour de `calcRF` et de la base CartoRadio ANFR.
- **Section 10 — Rayonnement ionisant** (#section-10-ionisant) : ~1 030 mots, autour de `calcGammaAmbient` et `calcRadonPotential`, classification ASNR décret 2018-434.

Volume total prose ajouté : ≈ 3 820 mots.

### Changed — Sommaire et navigation `cadre-scientifique.html`

- Sommaire enrichi de 4 entrées (Sections 7 à 10) entre Section 6 et Annexe A.
- Liens cliquables inter-sections ajoutés dans la prose des 4 nouvelles sections (Section 7 ↔ 8, Section 8 ↔ 6/7, Section 9 ↔ 8/10, Section 10 ↔ 7/8/9, Section 7 ↔ Annexe A) — recommandation Cowork retenue pour faciliter la navigation.
- Section 1 reformulée pour retirer la mention publique d'une candidature FEDER/ANR/Collectivité de Corse (cohérence avec la doctrine éditoriale post-cycle audit Phase D : pas de mention publique d'attribution conditionnelle). Avant : « Le projet vise une mise à disposition publique via tellux.pages.dev, ainsi qu'une valorisation dans des dossiers de financement auprès de la Collectivité de Corse, de l'Agence nationale de la recherche, et des dispositifs FEDER. » Après : « Le projet est mis à disposition publique via tellux.pages.dev. »
- Footer : « Dernière mise à jour : avril 2026 » → « mai 2026 » (cohérent avec la modification substantielle de la page).

### Anomalies hors périmètre signalées par Cowork

- **Recouvrement éditorial Sections 4-5 actuelles vs nouvelles Sections 8-10** : la Section 4 (« Composante gamma terrestre ») et la Section 5 (« Superposition magnétique ») couvrent partiellement le même terrain que les Sections 10 et 7-8 nouvelles. Refactorisation transversale possible (fusion dans la nouvelle structure par domaine), à arbitrer dans un sprint Cowork ultérieur.
- **Mention valeurs Téléray dans `app.html`** (commentaire de `calcGammaAmbient` : « 80–120 nSv/h ») cohérente avec la fourchette plus large 75–150 nSv/h citée en Section 10.2 — pas de correction requise mais point de vigilance.

---

## [2.8.4] — 2026-05-01

### Changed — Backlog SEO et performance `mairies.html` (PR à venir, sprint `chore/seo-mairies-backlog`)

Sprint d'amélioration SEO et performance de l'application communale, listé depuis avril 2026 dans la ROADMAP section 2 « Chantiers techniques en cours ». Audit Lighthouse réalisé avant et après pour mesurer l'effet.

**Scores Lighthouse :**

| Catégorie | Avant | Après | Δ |
|---|---|---|---|
| Performance | 57 | **81** | **+24** |
| Accessibility | 96 | 96 | = |
| Best Practices | 100 | 100 | = |
| SEO (preview) | 92 | 61 | -31 (faux négatif preview, voir notes) |

Web vitals (avant → après) : LCP 6.1 s → 1.5 s, FCP 6.1 s → 1.5 s, Speed Index 6.1 s → 1.8 s, TTI 7.6 s → 2.2 s.

**Modifications appliquées :**

- **Lazy load `pdfmake`** : retrait des deux balises `<script src="...pdfmake...">` du `<head>` (chargement synchrone au boot, ~600 ko + ~200 ko de fonts). Nouvelle fonction `loadPdfMake()` qui injecte dynamiquement les deux scripts CDN au premier clic sur « Télécharger PDF », avec indication visuelle « Préparation du PDF… » sur le bouton et retry au prochain clic en cas d'échec réseau. Integrity hashes conservés.
- **Élision française** sur le préfixe `Mairie de [NOM DE LA COMMUNE]` dans la génération PDF des courriers : nouvelle fonction `applyMairieElision()` appliquée comme pré-traitement dans `substitute()` et `substituteHtml()` avant la substitution générique. Voyelle ou voyelle accentuée → « Mairie d'Ajaccio », « Mairie d'Évisa ». Article L' déjà inclus dans le nom officiel (« L'Île-Rousse ») → « Mairie de l'Île-Rousse » (article minusculé). Apostrophe typographique cohérente avec les templates existants.
- **Open Graph et Twitter Cards** : enrichissement des meta tags dans le `<head>`. Ajout `og:type`, `og:locale` (`fr_FR`), `og:site_name`, `og:image`, `og:image:alt` et les 4 balises `twitter:card`/`title`/`description`/`image`. Image temporaire : `assets/logo/favicon_512.png` (512×512, ratio 1:1) avec `twitter:card` en `summary` (cohérent avec ratio carré). Asset Open Graph dédié 1200×630 (1.91:1) à produire en session Soleil dédiée — non créé d'autorité dans ce sprint.
- **Hiérarchie h1** : audit confirme un seul `<h1>` (l.436 « Outils administratifs · Communes corses »), hiérarchie h1 → h2 → h3 propre. Aucune modification requise.

**Notes** :

- La régression SEO apparente sur preview Cloudflare (92 → 61) est un faux positif : les URL preview portent un `X-Robots-Tag: noindex` automatique pour éviter l'indexation des URLs temporaires (audit Lighthouse signale `is-crawlable: Page is blocked from indexing`). À reconfirmer sur prod après merge.
- Anomalies hors périmètre détectées et signalées (non corrigées) : `robots-txt` invalide (présent avant et après), `color-contrast` insuffisant (présent avant et après), CLS et TBT en légère régression à surveiller.

---

## [2.8.3] — 2026-05-01

### Changed — Audit cohérence `DETTES_TECHNIQUES.md` post-cycle audit Phase D (PR à venir, sprint `chore/audit-dettes-coherence-post-phase-d`)

Audit documentaire des dettes techniques pour fermer l'anomalie 4 hors périmètre signalée par la PR [#283](https://github.com/dellahstella/tellux/pull/283) (sprint hygiène repo) et l'anomalie hors périmètre signalée par la PR [#289](https://github.com/dellahstella/tellux/pull/289) (sprint audit EMAG-CRUSTAL).

Modifications cosmétiques appliquées :

- **Fix wording `WDMAM-NAMING-001`** (note de fermeture, section « Dettes fermées récemment ») : la note décrivait un pattern « bbox-dynamique reconstruit à chaque activation » qui ne correspondait plus à l'état actuel du code après le rollback de la PR #190. La note précise désormais le rollback vers la bbox fixe `[[41.3, 8.5], [43.1, 9.65]]` et la raison du rollback (URL dynamique manquant le `renderingRule EMAG2_Color_Scale` rendant l'image transparente), avec renvoi vers le commentaire `app.html:2092-2097`.
- **Actualisation terminologique IRSN → ASNR** sur 2 occurrences de la dette `RADON-DATASET-COVERAGE-001` (description et condition de déblocage), formulation `ASNR (anciennement IRSN)` selon la doctrine appliquée par les sprints `audit-D1`, `audit-D1bis`, `audit-D1ter`. Préserve la traçabilité historique vers les fiches data.gouv.fr publiées sous le slug IRSN tout en utilisant le nom d'autorité actuel.

Pas de fermeture, recadrage ou ouverture de dette dans ce sprint. Les arbitrages non triviaux sont remontés dans la description de la PR pour décision Soleil.

---

## [2.8.2] — 2026-05-01

### Changed — Fermeture de la dette `EMAG-CRUSTAL-AUDIT-001` après audit (PR à venir, sprint `chore/audit-emag-crustal-fermeture`)

Investigation conduite sur `app.html` pour confirmer ou infirmer la duplication potentielle entre les couches `emag` et `crustal`. Verdict : couches fonctionnellement distinctes, pas de redondance. Aucune modification de code applicatif requise. La dette est déplacée en section « Dettes fermées récemment » de [`DETTES_TECHNIQUES.md`](DETTES_TECHNIQUES.md) avec note d'audit détaillée.

- `emag` (l.2098 d'`app.html`) : `L.imageOverlay` raster régional Corse, endpoint NOAA NCEI EMAG2v3 ImageServer, bbox fixe `[[41.3, 8.5], [43.1, 9.65]]`.
- `crustal` (l.2657-2700+ d'`app.html`) : `L.layerGroup` vectoriel construit à partir du tableau `CRUSTAL_REFS` (5 entrées hardcodées Bangui, Kursk, Vredefort, Ries, Chicxulub) avec cercles + markers + panneau comparatif `_crustalGauge` qui *utilise* EMAG2v3 (complémentarité, pas redondance).

La portion « wdmam » de la dette avait été implicitement résolue par la fermeture de `WDMAM-NAMING-001` le 27 avril 2026.

---

## [2.8.1] — 2026-05-01

### Added — Page publique `retractations.html` (PR à venir, sprint `feat/retractations-page-integration`)

Nouvelle page publique de journal des rétractations, retraits et reformulations substantielles du projet, à la racine du repo. La page documente publiquement les évolutions éditoriales antérieures (retraits de pages, reformulations, anonymisations) à destination des institutions, scientifiques, journalistes et évaluateurs de dossiers. Six entrées factuelles à la livraison, présentées par ordre antichronologique : retrait section « Inscription territoriale » landing avant publication, retrait modules patrimoine et agronomie du dépôt public, reformulation accroche grand public en cadrage de dialogue institutionnel, retrait du compteur « 130+ études peer-reviewed » de la landing, reformulation de la cible candidature financement dans les contextes publics, anonymisation d'une mention nominative dans la documentation interne tracée. Style aligné DA v2 (Fraunces + IBM Plex Sans), structure cohérente avec `transparence.html` et `mentions-legales.html`. Draft source produit en session Cowork conservé dans `_drafts/retractations/` (untracked).

### Changed — Cohérence transversale des footers (4 fichiers)

- `index.html` : ajout de la ligne « Transparence · Rétractations · Mentions légales » dans le bloc `lp-contact-mentions`, et ajout du lien `Rétractations` dans le footer principal `lp-footer-right` à la suite des liens existants.
- `transparence.html` : ajout du lien `Rétractations` dans le footer après `Accueil`. Date de mise à jour avril 2026 → mai 2026.
- `mentions-legales.html` : ajout du lien `Rétractations` dans le footer après `Accueil`. Date de mise à jour avril 2026 → mai 2026.
- `donnees-vie-privee.html` : ajout du lien `Rétractations` dans le footer après `Accueil`. Date de mise à jour avril 2026 → mai 2026.

Hors périmètre validé Soleil : footers de `mairies.html`, `cadre-scientifique.html`, `methode-et-limites.html`, `guide-utilisation.html` non modifiés dans ce sprint, à arbitrer ultérieurement si besoin.

---

## [2.8.0] — 2026-05-01

### Changed — Terminologie ASNR sur les mentions d'actualité (PR [#274](https://github.com/dellahstella/tellux/pull/274), [#278](https://github.com/dellahstella/tellux/pull/278), [#280](https://github.com/dellahstella/tellux/pull/280))

Alignement de la terminologie « ASNR » (active depuis le 1ᵉʳ janvier 2025, suite à la fusion ASN+IRSN) sur l'ensemble des mentions IRSN d'actualité non millésimées du site public et du code applicatif. Les ~16 occurrences IRSN restantes sont toutes des références à des datasets explicitement millésimés 2018 (cartographie radon, décret 2018-434, NCRP 94, noms de colonne CSV `radon_class_IRSN`) et sont conservées en l'état.

- Sprint audit-D1 (PR [#274](https://github.com/dellahstella/tellux/pull/274)) : 7 occurrences contemporaines remplacées dans `index.html` (×5), `methode-et-limites.html` (×2), `guide-utilisation.html` (×2), `transparence.html` (×1).
- Sprint audit-D1bis (PR [#278](https://github.com/dellahstella/tellux/pull/278)) : 5 mentions d'actualité corrigées dans `cadre-scientifique.html` (×3 : sections 1, 4.1, 6.3) et `app.html` (×2 : footer fonctionnel L.1184 et `epistemic_note` de `calcGammaAmbient` L.4274).
- Sprint audit-D1ter (PR [#280](https://github.com/dellahstella/tellux/pull/280)) : 2 résiduels dans `app.html` (commentaire L.3992 « BRGM + ASNR + IGN BD TOPO » ; href L.1184 `https://teleray.irsn.fr` → `https://teleray.asnr.fr`, vivacité 200 OK confirmée par curl).

### Changed — Audit Phase D, fixes structurants landing (PR [#274](https://github.com/dellahstella/tellux/pull/274))

- Compteur antennes du bloc statistiques hero d'`index.html` aligné sur le chiffre exact daté `~960 sites ANFR` (avril 2026), avec mention en infobulle `title=` « plus de 3000 antennes individuelles ».
- Footer d'`index.html` enrichi avec le statut juridique : `Stella Canis Majoris · micro-entreprise SIRET 993 881 481 00010 · 20200 Bastia · 2026`.
- Ancre `#contact` d'`index.html` enrichie d'un libellé explicite : `Contact projet — Lucas Iannaccone Frasseto, porteur du projet Tellux Corse`.

### Added — Section « Cadres éthiques de référence » sur la page Transparence (PR [#276](https://github.com/dellahstella/tellux/pull/276))

Nouvelle section 4 dans `transparence.html` détaillant l'adhésion envisagée à la Charte de la donnée et de l'IA Corse (21 principes en 9 titres) et au Guide de bonne pratique IA Smart Isula (12 bonnes pratiques), conditionnelle à l'obtention d'un financement FEDER. Articulation préfigurée par les pratiques actuelles déjà visibles sur le site (MIT, RLS, polices auto-hébergées, pas de tracker). Renumérotation des sections actuelles 4 et 5 en 5 et 6.

### Added then Removed — Section « Inscription territoriale » sur la landing (PR [#276](https://github.com/dellahstella/tellux/pull/276) puis [#281](https://github.com/dellahstella/tellux/pull/281))

Cas particulier signalé pour clarté du lecteur : une section `#inscription-territoriale` a été ajoutée à `index.html` par la PR [#276](https://github.com/dellahstella/tellux/pull/276) (entre `#projet` et `#ressources`, 3 cartes empilées détaillant l'articulation au PO FEDER-FSE+ Corse 2021-2027, au SDTAN Smart Isula et au SPDIAC), puis retirée par la PR [#281](https://github.com/dellahstella/tellux/pull/281) sur décision éditoriale (sobriété de la landing publique, la cohérence narrative institutionnelle est portée par le dossier FEDER lui-même). Bilan net pour la version `[2.8.0]` : section absente du site public. Le draft markdown source (`_drafts/audit-D1/section_spdiac_landing.md`, untracked) est conservé localement pour usage potentiel ultérieur (par exemple page À propos dédiée).

---

## [2.7.0] — 2026-04-27

### Removed — Retrait des modules patrimoine et agronomie du dépôt public (PR `refactor/audit-transparence-corpus-public`)

- Suppression de `patrimoine.html` et `agronomie.html`. Les deux fichiers existaient dans le dépôt public sans être liés depuis la landing ; ils sont retirés à l'occasion de l'audit de transparence du 27 avril 2026 pour aligner le périmètre public sur la phase 1 effectivement publiée (cartographie EM, outils communaux, corpus). Contenus conservés en interne pour réactivation éventuelle dans une phase ultérieure financée.
- Mise à jour en cascade : `index.html` (bloc état d'avancement, références bibliographiques, sources territoire), `README.md`, `ROADMAP.md` (section périmètre, sections Phase 2/3/4 consolidées en une note neutre, renumérotation), `ARCHITECTURE.md`, `app.html` (lien biblio redirigé vers `corpus.html`).
- Anonymisation de la mention nominative du destinataire de la première sollicitation méthodologique externe dans `ROADMAP.md` (section 7) et `docs/auto-affinage-conception-v1.md`.
- Reformulation de la cible candidature financement (FEDER en priorité) dans les contextes publics.
- Reformulation de l'accroche grand public (`index.html`, `mairies.html`) en cadrage dialogue institutionnel non anxiogène.
- Retrait du chiffre « 130+ études peer-reviewed » du bloc numbers de la landing — non auditable publiquement.
- Documents de session internes-style (`AUDIT_SECTION_7_CORPUS.md`, `DATASETS_PATCH_COWORK_FIX.md`, `PILIERS_AB_RECOS_COWORK.md`) déplacés vers `docs/internal/` (gitignored).

Voir l'entrée correspondante dans `retractations.html` pour le détail des motifs.

---

## [2.6.1] — 2026-04-22

### Fixed — HOTFIX BT-CALIBRATION-001 (PR `hotfix/disable-bt-segments-calibration`)

- **Désactivation temporaire du calcul BT segments** dans `calcMagneticELF_v2` via flag `USE_BT_SEGMENTS = false`
- Bug de calibration identifié lors de la validation PR #71 : le modèle Biot-Savart + correction triphasée `k=0.5` est calibré sur géométrie pylône HTA (phases espacées 1–3 m) et inadapté au câble BT torsadé (phases espacées ~1 cm). Surestimation catastrophique en zone urbaine dense : ratios v2.5 → v2.6 atteignant ×210 (Bastia 33 592 nT au lieu de ~160 nT attendus)
- `BT_ZONES` proxy legacy v2.5 reprennent le relais automatiquement quand `USE_BT_SEGMENTS = false`
- Chargement asynchrone `bt_lines`, grille `BT_SEGMENT_GRID` et fonctions BT conservés pour réactivation future après recalibrage
- Correction du bug `_btLinesCalcLoading` non remis à `false` après succès (pattern `finally`)
- Warning console unique au premier calcul : traçabilité de la désactivation

### Validation runELFRegressionTest v2.6.1

Ratios urbains reviennent à des valeurs physiquement réalistes :
- Ajaccio centre : 14 253 → 205 nT
- Bastia centre : 33 592 → 117 nT
- Porto-Vecchio : 21 047 → 134 nT
- Calvi : 26 654 → 79 nT
- Corte : 7 737 → 433 nT
- Palaggiu : 1 164 → 1 521 nT (HTA vectoriel seul, proximité ligne réelle)
- Points éloignés : inchangés (offshore 11 nT, sommets 20–50 nT)

### Dette ouverte

- **BT-CALIBRATION-001** — recalibrage du modèle BT pour produire des ordres de grandeur physiquement réalistes. 3 leviers envisagés : recalibrage paramétrique (k, cap, dist min), modèle statistique densité BT par tuile, ou modèle Biot-Savart adapté câbles torsadés. Traitement en session dédiée avec validation physique préalable.

### Préservé depuis PR #71

- Sommation vectorielle HTA (gain scientifique conservé)
- Chargement asynchrone BT (infrastructure prête pour réactivation)
- Réintégration `POSTES_SOURCES` + `EOLIENNES_DATA` dans v2
- Zone GELE-001 intacte

---

## [2.6.0] — 2026-04-21

### Fermeture dettes ELF-VECTOR-001 + BT-ELF-001 (PR `feat/elf-bt-vectoriel`)

#### Chantier 1 — Sommation vectorielle (ELF-VECTOR-001)

- Nouvelle fonction `calcBiotSavartSegmentVec` : retourne `{bx, by}` en nT, direction perpendiculaire au segment (règle de la main droite)
- `calcMagneticELF_v2` migré vers sommation vectorielle 2D : `B_lines = sqrt(Bx² + By²)` avant ajout contributions ponctuelles
- Réintégration `POSTES_SOURCES` et `EOLIENNES_DATA` dans v2 (absents depuis PR #66 — regression corrigée)
- `calcBiotSavartSegment` scalaire conservée pour rétro-compatibilité et rollback
- Constante `BT_BASE_CURRENT_A = 60 A` ajoutée
- `runELFRegressionTest` mis à jour : colonne `v2.6_nT` + indicateur `bt_loaded`

#### Chantier 2 — Intégration BT réel (BT-ELF-001)

- Chargement asynchrone `loadBTLinesAsync` : bbox Corse complète (41.3–43.1°N / 8.5–9.7°E), pagination 1000/page, non bloquant
- Grille spatiale `BT_SEGMENT_GRID` / `BT_SEGMENTS_DATA` (structure identique à grille HTA)
- `getBTSegmentsNear` / `buildBTSegmentGrid` au même endroit que leurs homologues HTA
- `BT_ZONES` proxy conservées en fallback tant que `BT_SEGMENT_GRID` est null
- Déclenchement 200 ms après `buildSegmentGrid(all)` dans `loadReseau`

### Dettes fermées

- **ELF-VECTOR-001** ✓ — sommation vectorielle 2D
- **BT-ELF-001** ✓ — segments BT réels dans le calcul ELF

---

## [2.5.1] — 2026-04-21

### Vérification calibration ELF post-Biot-Savart v2 (chore `verif-elf-calib-post-merge`)

- **ELF-CALIB-001** — Audit des seuils visuels `scoreColor()` après migration Biot-Savart v2 (PR #65)
- Distribution v2 sur 20 points témoins : 40% Faible (<150 nT) · 15% Modéré (150–300 nT) · 15% Élevé (300–500 nT) · 30% Très élevé (>500 nT)
- **Scénario A retenu — aucun changement aux seuils 150 / 300 / 500 nT** : ancrage IARC 2B à 300 nT conservé, distribution cohérente avec la géographie HTA réelle de la Corse
- Correction cosmétique : légende `elf_domain` mise à jour ("Biot-Savart réel" + confiance ●●●) — entrée non active dans l'interface

---

## [2.5.0] — 2026-04-21

### Ajouts — Enrichissement datasets publics (PR `feat/enrichissement-datasets-publics`)

- Dataset `public/data/postes_sources_corse.json` — 21 postes HTB/HTA via OpenStreetMap (fallback EDF SEI indisponible)
- Dataset `public/data/eoliennes_corse.json` — 3 parcs éoliens Corse (Ersa, Lumio, Rogliano) via RTE ODRE 2022
- Dataset `public/data/points_chauds_radio_corse.json` — 5 sites U/Th documentaires (Argentella, Saleccia, Manso, Cap Corse, Murato)
- Loaders idempotents : `loadPostesSources`, `loadEoliennes`, `loadPointsChaudsRadio`
- Couches visuelles Leaflet + boutons menu : `b-postes`, `b-eoliennes` (Groupe 2), `b-points-chauds` (Groupe 3)
- Notes méthodologiques : `docs/data-sources/postes_sources_corse_notes.md`, `eoliennes_corse_notes.md`, `points_chauds_radio_corse_notes.md`

### Modifié — Calculs physiques

- `calcMagneticELF` : ajout contributions `poste_source` (modèle ponctuel 50 µT à 10 m, 1/d³, plafond 500 nT, pruning 1 km) et `eolienne` (2 µT à 10 m pour 2 MW, 1/d², plafond 300 nT, pruning 500 m)
- `calcGammaAmbient` : ajout `components.boost_ponctuel_nSv_h` + `boost_sources[]`. Décroissance linéaire depuis centre point chaud jusqu'au rayon d'influence, baseline 80 nSv/h soustraite. Les composantes terrestre NCRP 94 et API Téléray ASNR restent en attente.
- GELE-001 (pondérations `w_M = 0.40, w_RF = 0.40, w_I = 0.20`) **inchangé**

### Hors scope / dettes reportées

- **Chantier 4 BRGM radiométrie aérienne** : reportée, dette `BRGM-RADIO-001` (aucun flux WMS/WFS/download public identifié lors de l'audit)
- **Chantier 5 WMM 2025 cross-check** : reportée, dette `WMM-CROSSCHECK-001` (implémentation harmonique sphérique hors scope session)
- **Chantier 6 IGN BD Forêt V2** : reportée, dette `BDFORET-V2-001` (couche absente du WMS Géoplateforme raster, shapefile trop lourd pour app web)
### Modifié — Biot-Savart réel sur réseau HTA (PR `feat/biot-savart-reel-hta`)

- `calcMagneticELF` migré vers `calcMagneticELF_v2` : formule segment fini + correction triphasée sur 11 735 segments réels (expansion des 8386 polylines `hta_lines` Supabase) au lieu de 8 axes hardcodés
- Courant unique 225 A × `chargeFacteur` (Option B, dataset sans champ voltage — dette migration SQL)
- Champ RMS explicite (facteur 1/√2)
- Grille spatiale précalculée 1 km × 1.35 km au chargement `loadReseau` (10 704 tuiles)
- Calcul par clic : < 2 ms en moyenne (cible 50 ms largement battue)

### Ajouts

- Fonction `calcBiotSavartSegment()` — calcul unitaire par segment avec correction triphasée k=0.5 au-delà de 20 m
- Fonction `buildSegmentGrid()` + `getSegmentsNear()` — pré-indexation spatiale
- Fonction `runELFRegressionTest()` — validation sur 20 points témoins (5 urbains, 5 ruraux, 5 éloignés, 5 mégalithiques)
- Flag `USE_ELF_V2 = true` — bascule v1/v2 pour rollback d'urgence sans redéploiement

### Déprécié

- `calcMagneticELF_v1` conservée pour référence et rollback, sera supprimée en v3 après validation tiers
- 8 axes `HTA_SEGS` hardcodés : uniquement utilisés par v1, sortiront avec v1

### Documentation

- `docs/notes-tri/AUDIT_TELLUX_NIVEAU2_NOTE_EVOLUTION_BIOTSAVART_v1.md` — note scientifique complète avec tableau comparatif 20 points

---

## [2.4.0] — 2026-04-20

### Ajouts — Précision modèle (PR `feat/precision-radon-mnt-tdf`)

- Reverse geocoding commune via `api-adresse.data.gouv.fr` (`reverseGeocodeCommune`, cache `COMMUNE_CACHE`)
- Altimétrie réelle via IGN RGE Alti (`fetchAltitudeIGN`, cache `ALTITUDE_CACHE`)
- Correction rayonnement cosmique dans `calcGammaAmbient` : composante altitude ×4–5 selon z réel (vs 0 m fixe)
- Intégration 10 émetteurs TDF/radiodiffusion corse dans `calcRF` (modèle isotrope S = PAR/4πd², plafond 50 000 µW/m²)
- Jeu de données `public/data/radon_communes_level3_corse.json` — 28 communes niveau 3 décret 2018-434 (IRSN)
- Jeu de données `public/data/tdf_emitters_corse.json` — 10 émetteurs avec PAR estimées (ANFR/CSA)
- Notes méthodologie sources : `docs/data-sources/radon_communes_level3_corse_notes.md`, `docs/data-sources/tdf_emitters_corse_notes.md`
- Détection radon triple : règle département 2A entier + INSEE explicite + nom de commune normalisé
- Handler click carte rendu asynchrone avec `Promise.all([reverseGeocodeCommune, fetchAltitudeIGN])`

### Modifié — Précision modèle

- `calcGammaAmbient(lat, lon, altitude_m)` : accepte altitude réelle en 3ème paramètre
- `calcRadonPotential(lat, lon, options)` : accepte `commune_info`, retourne `class_source` et `official_classification`
- `calcAll_v2(lat, lon, options)` : passe `commune_info` et `altitude_m` aux fonctions calc sous-jacentes
- `calcRF` : blocs contributions structurés avec `source_type: 'broadcast_TDF'`
- `.gitignore` : `DATA/` → `/DATA/` (ancrage racine, corrige conflit Windows case-insensitive)
- Fond de carte : fond unique IGN Plan V2, suppression du switcher de fond, `maxZoom` 20 (`maxNativeZoom` 19)

### Ajouts — Interface (PR `feat/ui-menu-reorg`)

- 3 groupes accordéons thématiques dans la sidebar : « Modèle EM », « Sources anthropiques », « Contexte naturel »
- Panneau « Conditions actuelles » unifié : 3 sections repliables (géomagnétique, réseau électrique, météo/autre)
- Sparkline inline SVG (180×40 px) de la charge réseau Corse heure par heure (`PROFIL_HORAIRE_CORSE`)
- Marqueur rouge sur l'heure courante dans la sparkline
- Modal contribution restructuré en 3 onglets : Observation, Mesure terrain, Capteurs appareil (placeholder)

### Modifié — Interface

- Terminologie : « prédiction » → « champ composite estimé » dans toute l'interface (libellés, popups, titres)

---

## [2.3.0] — 2026-04-19

### Ajouts — Mode Expertise (PR `feat/v2-phase3-expertise`)

- Mode Expertise avec `EXPERT_WEIGHTS_DEFAULT` et `EXPERT_BOUNDS_DEFAULT` (GELÉS — GELÉ-001)
- Fonction `computeExpertComposite(lat, lon, weights)`
- Modal avertissement épistémique à l'activation du mode Expert
- Bandeau permanent rouge « MODE EXPERT ACTIF »
- Curseurs pondérations `w_M`, `w_RF`, `w_I` avec throttle 300 ms
- Export CSV enrichi UTF-8 BOM (`exportExpertCSV`)
- Partage URL hash `#/z=Z&c=LAT,LNG&m=DOM[&e=1]` (`shareURL`, `applyHashToMap`)
- Tests non-régression phase 3 (`tests/non-regression-v2-phase3.js`, catégories H–O, 7 invariants)

### Modifié

- Migration `calcPiezoScore` complète : retourne `susceptibility_nT`, plus d'appelant actif legacy

---

## [2.2.0] — 2026-04-19

### Ajouts — Modèle composite v2 phases 1 et 2

- `calcMagneticELF(lat, lon)` — champ basse fréquence (lignes HT, transformateurs)
- `calcRF(lat, lon)` — RF antennes ANFR
- `calcHeritageDensity(lat, lon)` — densité patrimoine (mégalithes + églises romanes)
- `calcAll_v2(lat, lon, options)` — orchestrateur multi-domaines
- Légende couleur Ocre (#C28533) / Porphyre (#8E2F1F) pour couches EM
- Popup v2 restructurée avec sections par domaine
- Section « À propos » réécrite (humilité épistémique, 3 formulations interdites)

### Corrigé

- Suppression de 10 occurrences « piézo » résiduelles (calcul et libellés)

---

## [2.1.0] — 2026-04-18

### Ajouts — Architecture en suite + mode Expertise phase 1–2

- DA v2 palette gelée : Ardoise, Pierre, Maquis, Ocre, Porphyre, Tyrrhénien
- Typographie Fraunces (titres) + IBM Plex Sans (corps)
- Sidebar desktop élargie à 420 px
- Aliasing typo corrigé (guillemets courbes → droits)

---

## [2.0.0] — 2026-04-14

### Architecture

- Pivot vers architecture en suite d'applications (`app.html`, `patrimoine.html`, `agronomie.html`)
- Suppression des fichiers historiques (`tellux_CORRECT.html`, `tellux_v6_design.html`, `TELLUX_LOGO_V7.html`)
- Remote GitLab désactivé, GitHub `dellahstella/tellux` devient remote unique
- Déploiement Cloudflare Workers via `wrangler.jsonc`
