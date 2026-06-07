# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)
Versioning sémantique : [SemVer](https://semver.org/lang/fr/)

---

## [Harmonisation chiffres ANFR landing + doc scientifique + app — 2026-05-31]

### Fixed
- **`index.html`** (stat hero `.lp-map-stats`) : « 566 sites documentés / sites ANFR (mai 2026) » → « 3 000 antennes / 1 026 supports - 219 communes / Source ANFR CartoRadio - extraction avril 2026 ». Aligne le chiffre visible de la landing sur le snapshot Supabase `antennas_corse` du 24 avril 2026.
- **`cadre-scientifique.html`** (§ 9.2 Phénoménologie en Corse) : phrase « densité de l'ordre de 0,11 site/km² … 449 sites Corse-du-Sud + 511 sites Haute-Corse, soit environ 960 sites cumulés » remplacée par la formulation source ANFR validée en interne : « 2 986 antennes individuelles géolocalisées (2G/3G/4G/5G), 1 026 supports distincts, 219 des 360 communes corses, 14 antennes offshore Cerbicale/môle de Bastia ». Ajout d'une phrase de densité dérivée : « environ 8 700 km², densité moyenne de l'ordre de 0,12 support/km² » — restaure l'antécédent de la phrase suivante « Cette densité reste inférieure à celle des grandes agglomérations métropolitaines » (arbitrage interne : ajouter densité sourcée par support plutôt que supprimer la comparaison).
- **`app.html`** (2 occurrences L1451 légende couche, L1468 panneau sources) : « 974 supports » → « 1 026 supports ». Le compteur runtime du header (`nOnshore + ' antennes'`, calculé live sur le fetch Supabase) n'est pas touché — il était déjà correct.

### Notes
- Source de vérité unique : snapshot Supabase `antennas_corse` 2026-04-24 (`docs/em-mairie/data-sources/antennes_corse_notes.md`) — 3 000 antennes, 2 986 géolocalisées, 14 offshore, 1 026 supports (groupage lat/lon/opérateur), 219 communes.
- Régression silencieuse historique : la landing était passée de « ~960 sites » (PR #274) à « 566 sites » sans entrée CHANGELOG — cette entrée trace aussi cette dérive a posteriori (cf. AUDIT_SITE_PHASE_D « Écart 3.4 »).
- Hors scope (intacts) : compteur runtime header `app.html`, 30 fiches mesures ANFR/EXEM, fichiers `_archive/*`.

---

## [Acte source de vérité patrimoine + nettoyage branche morte — 2026-05-21]

### Changed
- **`ARCHITECTURE.md`** : section data architecture (§ 1 arborescence + § 3.bis) corrigée pour refléter l'architecture réelle post-Brief 33 split. `sites_patrimoine.json` est la **source de vérité runtime** de `patrimoine.html` ; `sites_corse.json` est DEPRECATED, sans consommateur runtime. Documentation du mécanisme `gps_locked` (~80 verrous éditoriaux, Brief 38) et de la doctrine d'édition (briefs ciblés + `scripts/brief_pipeline.py`, pas de pipeline de génération).

### Removed
- Branche distante `data/pip-corrections-vague-2` (commit unique `81d04c2`) supprimée — elle éditait `sites_corse.json` (fichier déprécié), sans effet runtime.

### Notes
- Acte formel : `docs/data/sites_patrimoine.json` est la source de vérité runtime du patrimoine (architecture en place depuis le **Brief 33 split**, 2026-05-06 — cf. audit `_drafts/AUDIT_COHERENCE_SOURCES_PATRIMOINE.md`).
- `sites_corse.json` **n'a pas été archivé** cette session : 2 scripts de maintenance le référencent encore (`scripts/brief_pipeline.py`, `scripts/corpus_health_check.py`). Archivage reporté à un chantier dédié incluant la mise à jour de ces scripts.
- Aucun changement runtime — mise en cohérence documentation ↔ réalité du repo.

---

## [D3 rebuild voie-a + D4 containment renforcé — 2026-05-21] (Étape 5 PR C)

### Changed (docs/data/pieves_polygons.json — dérivé prod régénéré)
- **Rebuild voie-a** : `docs/data/pieves_polygons.json` régénéré par `build_pieves_polygons.py`
  depuis le mapping v4 (cleanup D1) — fin de la « voie-b » (patches directs du dérivé).
- `version` → `v7-cleanup-mapping-amont-rebuild-2026-05-18`.
- 50 pieves. `stats.pieves_count` 51 → **50**, `stats.total_communes` 347 → **360** (auto-corrigés).
- Surface 8703.3 km² (écart <0,01 % vs prod). Sortie minifiée.
- **11 pieves changent de composition** vs l'ancienne prod (carte v4 cohérente ;
  l'ancienne prod était incohérente post-voie-b) — refonte assumée, arbitrage interne.
- 3 polygones auparavant invalides (`fiumorbo`, `gulfo_d_aiacciu`, `vallerustie`)
  régénérés valides. Override `pieve_bozio` préservé.

### Added / Changed (build_pieves_polygons.py)
- Câblage du mapping v4 (`pieves_added` + `transferts` + `renames`).
- Containment check renforcé **mapping ↔ dérivé** (`--strict-mapping`, mode warn
  par défaut) — guard anti-régression voie-b. Rebuild actuel : 0 écart.
- Sortie minifiée (cohérent prod + limite Cloudflare).

### Dettes
- **Clôturées** : `PIEVE-MAPPING-AMONT-DESYNCHRO-001` (HAUTE), `POLYGONE-INVALID-SELF-INTERSECTING-001`,
  `COMMUNES-COUNT-OBSOLETE-POST-VOIE-B-001`, `MAPPING-PRE-STRATD-AD-HOC-TRANSFERS-UNDOCUMENTED-001`.
- **Ouverte** : `MAPPING-PREQW-ORIGIN-UNKNOWN-001` (origine patrimonio/zicavo non investiguée).

### Chantier Étape 5 — terminé
D1 (mapping v4) + D2 (archivage scripts) + D3 (rebuild voie-a) + D4 (containment renforcé).
La voie-a est redevenue viable : mapping amont ↔ dérivé prod alignés.

---

## [D2 archivage scripts ad hoc — 2026-05-20] (Étape 5 PR B)

### Changed (scripts)
- 5 scripts one-shot historiques archivés vers `scripts/archive/phase_oneshots/` :
  `phase_d3_pieves.py`, `phase_qw_pieves.py`, `phase_r3_rename_ajaccio.py`,
  `phase_strat_d_patch_derive.py`, `phase_strat_d_phase2_splits.py` — `git mv`
  (historique préservé) + en-tête d'archivage. Aucun n'était référencé par la CI.
- `build_pieves_polygons.py` : intégration des métadonnées de l'ex-`phase_qw_pieves.py` —
  `QW_DIOCESES_FALLBACK` (diocese_medieval de secours) + strip générique du préfixe
  « Pieve di / d' », appliqués post-construction, pré-validation containment.

### Added
- `scripts/archive/phase_oneshots/README.md` (statut des scripts archivés).
- `scripts/archive/phase_oneshots/phase_strat_d_etape3_fusion_lota.py` — script
  rétroactif idempotent documentant la fusion `pieve_bastia` + `pieve_brando` →
  `pieve_lota` (exécutée par PR #648, jamais scriptée à l'époque).

### Unchanged (volontairement, scope strict)
- `docs/data/` (dérivé prod, mapping v4) — rebuild voie-a réservé à PR C.
- `phase_strat_d_retag_sites.py` et `phase_strat_d_phase2_retag_sites.py` conservés.

### Reference
- Brief Code D2 : Étape 5 PR B.
- Dette parent : `PIEVE-MAPPING-AMONT-DESYNCHRO-001` (HAUTE) — reste ouverte.

---

## [D1 cleanup mapping amont — 2026-05-20] (Étape 5 PR A)

### Method (brief REV2)
- Source de vérité : scripts ad hoc `phase_strat_d_*.py` (listes explicites) + mappings v1/v2/v3.
- PIP polygones prod = best-effort pour les communes sans source traçable (arbitrage interne 2026-05-20).
- `communes_count` prod considéré obsolète pour 16/50 pieves (dette PR C).

### Added
- `_drafts/pieves_communes_mapping_v4_cleanup_2026-05-18.json` — v4 incrémental (modèle v2/v3).
  - 8 `pieves_added` : piana, sagone, aregno, calenzana, ostriconi, castagniccia, lota, zicavo.
  - 29 `transferts` : 26 réaffectations zombies (PIP best-effort) + 3 rétro-doc Phase 2 (sorroinsu→vico).
  - 7 zombies retirés : ampugnani, caccia, campoloro, giovellina, balagne, bastia, brando.
- `scripts/validate_mapping.py` REV2 — cohérence interne mapping (0 zombie, 0 manquante, 360 communes).

### Removed
- Référence zombie `pieve_caccia` dans `_drafts/PIEVE_DOYENNES_OVERRIDES.json` (9 → 8 entrées).

### Fixed (mapping amont aligné)
- 7 zombies (slugs mapping → absent prod) → 0.
- 8 pieves manquantes (slugs prod → absent mapping) → 0.
- Total communes mappées : 360 (cohérent).

### Documented as debt (hors scope D1, fix PR C)
- `POLYGONE-INVALID-SELF-INTERSECTING-001` (3 polygones prod invalides).
- `COMMUNES-COUNT-OBSOLETE-POST-VOIE-B-001` (16/50 communes_count obsolètes).
- `MAPPING-PRE-STRATD-AD-HOC-TRANSFERS-UNDOCUMENTED-001` (26 communes PIP best-effort).
- `MAPPING-PREQW-ORIGIN-UNKNOWN-001` (origine zicavo/patrimonio).

### Unchanged (volontairement, scope strict)
- `docs/data/pieves_polygons.json` (rebuild en PR C).
- `docs/data/sites_patrimoine.json`, `docs/data/pieve_aliases.json`.
- Scripts `scripts/phase_*.py` (archivage en PR B).

### Reference
- Audit : `docs/em-mairie/operations/PIEVE_MAPPING_AMONT_AUDIT_2026-05-18.md`
- Brief Code REV2 : `docs/em-mairie/operations/PIEVE_MAPPING_AMONT_D1_BRIEF_CODE_2026-05-18_REV2.md`
- Dette parent : `PIEVE-MAPPING-AMONT-DESYNCHRO-001` (HAUTE) — reste ouverte, clôture PR C.

---

## [B-ZONES Tier 2 — 2026-05-20] (Étape 4 sprint)

### Added (sites_patrimoine.json)
- Champs `is_zone`, `zone_geometry` (GeoJSON `[lon, lat]`), `zone_source`, `zone_simplification_pts` sur 8 sites Tier 2 favorables.
- Polygones B-ZONES Tier 2 :
  - 5 monts (octogones manuels rayon ~2-3 km autour du sommet) : Monte Cinto, San Petrone, Stello, d'Oro, Renoso.
  - 2 sites OSM : Capu Rossu (relation 9376817, `natural=cape`), Lac de Nino (way 28890021 + buffer ~600 m pour englober les pozzines).
  - 1 pointe manuelle : Capu Bianchi / extrême nord Cap Corse.

### Compteurs
- Sites `is_zone: true` : 15 → **23**.
- Smoke test PIP Corse : **23/23 verts**.

### Reference
- Prérequis : PR A B-ZONES Tier 1 mergée et validée prod.
- Brief Code : `docs/em-mairie/operations/B_ZONES_BRIEF_CODE_2026-05-18.md`

---

## [B-ZONES Tier 1 — 2026-05-20] (Étape 4 sprint)

### Added (sites_patrimoine.json)
- Champs `is_zone`, `zone_geometry` (GeoJSON `[lon, lat]`), `zone_source`, `zone_simplification_pts` sur 15 sites naturels Tier 1.
- Polygones B-ZONES Tier 1 :
  - 3 réserves / aires protégées : Réserve de Scandola (OSM RNN), RBI du Tavignano (OSM), Forêt de Bonifatu / Cirque de Bonifato (OSM).
  - 3 forêts domaniales : Vizzavona, Tartagine, Valdu Niellu (OSM).
  - 4 gorges / défilés : Spelunca, Tavignano, Inzecca, Lancône (OSM RBI + tracés manuels).
  - 1 massif de pics : Aiguilles de Bavella (manuel).
  - 2 massifs : Haut-Asco (manuel restreint à la haute vallée), Ospedale (manuel).
  - 1 plateau : Coscione (manuel).
  - 1 désert + 1 calanche : Agriates, Calanche de Piana (manuel).

### Added (patrimoine.html)
- Renderer Leaflet polygones zones au hover (desktop, fade in/out 200 ms) + tap 1500 ms (mobile).
- CSS `.tlx-zone-hover` (ocre `#C28533`, fillOpacity 0.3, stroke opacity 0.8).
- `adaptSiteSchema` étendu : passthrough `is_zone` / `zone_geometry`.

### Added (scripts)
- `scripts/b_zones_smoke_test.py` — smoke test PIP bbox Corse + containment doyenné (15/15 verts).

### Compteurs
- Sites `is_zone: true` : 0 → **15**.
- Polygones zones rendus (au hover) : 0 → **15**.

### Reference
- Audit : `docs/em-mairie/operations/B_ZONES_AUDIT_2026-05-18.md`
- Brief Code : `docs/em-mairie/operations/B_ZONES_BRIEF_CODE_2026-05-18.md`
- Doctrine : ADR-001 (navigation pédagogique), `BP-FIX-RATTACHEMENT-COMPLET-001`

---

## [Étape 3 sprint — pieve_lota + labels diocese] — 2026-05-18

### Added
- **`pieve_lota`** (7 communes, 16 sites, diocese_medieval Mariana, doyenne_du_cap) — fusion Cap Corse sud côte est, regroupant l'ancienne pieve_bastia + pieve_brando + intégration historique Pieve di Lota / Pieve di Sisco. Polygon = UNION shapely 7 communes (~124 km² simplify 0.0005). Hameaux préservés dans `note_rattachement` : Toga/Lupino/Cardo (Bastia), Miomo (Santa-Maria-di-Lota), Erbalunga (Brando). Option A audit Cowork 2026-05-18 validée en interne.
- **2 nouveaux aliases v4** : `pieve_bastia → pieve_lota`, `pieve_brando → pieve_lota`. Total aliases : 3 → 5.
- **Suffixe `(médiéval)`** au label diocese affiché en popup pieve legacy (sujets 1+2) pour clarifier ambiguïté slug ↔ diocese.

### Removed
- `pieve_bastia` (1 commune Bastia, fusionnée dans pieve_lota)
- `pieve_brando` (6 communes, fusionnée dans pieve_lota)

### Changed
- 16 sites retag vers `pieve_lota` : 6 sites pieve_bastia + 8 sites pieve_brando + 2 anomalies double-retag (`oratoire_santa_croce_bastia_haute_bastia_citadelle` ex-pieve_nebbiu/doy_golo, `san_giovanni_bastia_terra_vecchia` ex-pieve_biguglia/doy_golo). Doctrine `BP-FIX-RATTACHEMENT-COMPLET-001` stricte.
- `pieve_patrimonio` : `diocese_medieval "?" → "Nebbiu"` (Patrimonio historiquement diocèse Nebbiu/Cap), `name "pieve_patrimonio" → "Patrimonio"` (cosmétique).

### Compteurs
- Pieves : 51 → **50** (-2 supprimées + 1 créée)
- Aliases : 3 → **5** (+2)
- Sites retag : **16** (14 simple + 2 anomalies)
- Anti-ghost validation : 0 site résiduel pieve_bastia / 0 site résiduel pieve_brando
- pieve_lota total sites : **16** (attendu)

### Reference
- Doctrine voie-b patch direct du dérivé (cohérence Phase 1+2)
- Hash legacy `#du_cap/bastia` + `#du_cap/brando` préservés via aliases v4

---

## [Sprint hygiène, Étape 1] — 2026-05-18

### Fixed (3 corrections data sites)
- `casteddu_bastelica` (option a interne) : `commune_insee 2A031 (Bastelica) → 2B012 (Altiani)`, `commune_nom Bastelica → Altiani`, `pieve_rogna → pieve_altiani`. Coord verrouillé inchangé (42.217/9.255). Nom site conservé (toponymie homonyme à clarifier en phase ultérieure).
- `tour_d_isolella_sette_navi` : `commune_insee 2A258 (Renno faux) → 2A228 (Pietrosella officiel)`. Pieve/doyenne déjà cohérents.
- `pont_genois_de_piedipartino` : `commune_insee 2B231 (Pigna faux) → 2B221 (Piedipartino officiel)`, `pieve_aregno → pieve_orezza`, `doyenne_balagne → doyenne_du_golo` (BP-FIX-RATTACHEMENT-COMPLET-001).

### Closed (7 dettes traitées)
- 3 résolues par correction data : `CASTEDDU-BASTELICA-COORD-DOUTE-001`, `TOUR-ISOLELLA-INSEE-DISCORDANCE-001`, `PIEVE-PIEDIPARTINO-INSEE-DISCORDANCE-001`
- 3 fermées par invalidation/cosmétique : `FARINOLE-COORD-DOUTE-001` (faux positif, coord cohérent), `PIEVE-VENACO-OVERFLOW-VISUEL-GEOMETRIQUE-001` (cosmétique acceptable Phase 1 beta), `PIEVE-SORROINSU-CINARCA-POST-MIGRATION-PHASE2-001` (équilibre 4+9 communes OK)
- Sticker Balagne : documenté non-bug (image fonctionnelle, contraste cosmétique à améliorer en pass design en phase préliminaire, hors-scope hygiène)

### Audit
- Mismatches visuel↔data résiduels : **1 → 0** (audit MCP 2026-05-18)
- Aucune nouvelle dette ouverte

### Reference
- INSEE officiels croisés via `scripts/.cache/communes-{2A,2B}.geojson`
- Doctrine `BP-FIX-RATTACHEMENT-COMPLET-001` strictement appliquée pour piedipartino
- Préserve doctrine `gps_locked=true` (coord casteddu_bastelica inchangée, seules metadata corrigées)

---

## [§8 Mécanisme doyenne_contemporain_override + bozio] — 2026-05-18

### Added
- **Mécanisme générique `doyenne_contemporain_override`** dans `pieves_polygons.json` : champ optionnel string (slug doyenné valide) qui prime sur `doyenne_contemporain_majoritaire` dans toutes les lectures `patrimoine.html` (drill-down N2→N3, `pieveDoyenneBySlugV2`, `pievesByDoyenneLayer`).
- **`override_rationale`** : champ texte optionnel pour traçabilité doctrinale.
- **Préservation override sur rebuild** dans `scripts/build_pieves_polygons.py` (même pattern que `note_rattachement`, doctrine voie-b patch direct dérivé).

### Changed
- `pieve_bozio.doyenne_contemporain_override = "doyenne_cortenais"` (rationale : identité doctrinale Cortenais, paghjella, malgré ratio géo PO 53/47 post-ingestion alesani Phase 1).

### Resolved
- **9 mismatches visuel↔data → 1** (audit MCP 2026-05-18) :
  - 8 sites `pieve_bozio` désormais visibles en N2 Cortenais (résolu par override)
  - 1 résiduel : `casteddu_bastelica` (dette pré-existante `CASTEDDU-BASTELICA-COORD-DOUTE-001`, hors-scope §8)

### Notes
- `pieve_rogna` : doy_maj = PO conservé (ratio 88% PO, 4/5 sites cohérents). Pas d'override nécessaire.
- `pieve_sartene` (28/28 Extrême-Sud) et `pieve_gulfo_d_aiacciu` (11/11 Ajaccio) cohérents, pas d'override.
- `doyenne_contemporain_majoritaire` préservé pour traçabilité du calcul géo brut.

### Compteurs (51 pieves total)
- `doyenne_cortenais` : 8 → **9** (bozio rejoint)
- `doyenne_plaine_orientale` : 7 → **6** (bozio quitte)

### Reference
- Doctrine `BP-FIX-RATTACHEMENT-COMPLET-001` préservée (pas de retag sites, ils sont déjà cortenais déclarés)
- Audit MCP prod 2026-05-18 : 541 sites, 97% cohérents

---

## [Cleanup fiches pieves — 2026-05-18]

### Removed (public repo)
- 68 fiches markdown `fiches_patrimoine/pieves/*.md` (34 pieves × v2 + v3)
- `fiches_patrimoine/RAPPORT_SESSION_PIEVES_V3.md`

### Added (corpus privé)
- `_corpus/fiches_pieves/` (66 fiches actives + 1 rapport vague 3)
- `_corpus/fiches_pieves/_archive_matiere_premiere/` (2 fiches cap_corse + 1 README)

### Notes
- `_redirects` Cloudflare non ajouté (curl §3.2 non lancé, SPA fallback acceptable)
- U1 Phase 1 toujours actif : `patrimoine.html` skip `fetchFiche` pour `ficheType === 'pieves'` (lignes 2396, 2414, 2444)

### Reference
- Doctrine : ADR-001 + U1 Phase 1 (Stratégie D)
- Commit privé : `909d525` (corpus privé tellux)
- Ouvre suivi interne sur la vague 4 des fiches pieves (19 pieves prod sans fiche)

### Volume
- Public retiré : ~607 KB

---

## [§6 Nav N2→N2 directe] — 18 mai 2026

### Added
- **Pattern 4 (clic direct polygone doyenné voisin)** : en N2, les polygones des doyennés voisins deviennent cliquables (`pointer-events:auto`), avec curseur pointer, transition d'opacité au hover et stroke ocre épaissi. Clic → switch direct vers le doyenné cible (réutilise `enterNiveau2View` : cleanup pièves+dim+sticker actuel, attach nouveau, `flyToBounds` ~1s).
- **Pattern 2 (breadcrumb dropdown)** : en N2 actif, le segment doyenné du breadcrumb devient un trigger (`bc-doy-trigger`) avec chevron `▾`. Clic / Enter / Space ouvre un dropdown listant les 9 autres doyennés avec leur vignette (`bc-doy-mini-img`) ou fallback initiale (`bc-doy-mini-fallback`). Sélection → switch vers la cible. Fermeture sur clic extérieur, Escape, ou seconde activation du trigger.
- **Pré-fetch sticker au hover** : `mouseover` sur polygone doyenné voisin en N2 déclenche un préchargement `new Image()` du thumb correspondant (via `DOYENNE_ILLUSTRATIONS` + `_illustrationUrl(raw, 'thumb')`). Échec silencieux (no-op).
- **Fade swap sticker** : transition `opacity .25s ease` sur `#doyenne-mini-sticker`. À l'arrivée d'un nouveau sticker, l'ancien perd son `id` (libère l'anti-doublon), reçoit `.swapping` (opacity → 0), puis est retiré du DOM 250 ms plus tard.

### Changed
- `enterNiveau2View` réutilisable en mode A→B (déjà idempotent : cleanup avant attach).
- `flyToBounds` ajusté à `duration: 1.0, easeLinearity: 0.5` pour la transition fluide entre doyennés voisins.
- `updateBreadcrumb` produit deux variantes du segment doyenné selon `niveau-2 && !niveau-3` actif.

### Guards
- `onDoyenneClick` retourne immédiatement si `slug === currentDoyenneSlug` en N2 (clic sur le doyenné actuel = no-op, évite reset inutile).

### Reference
- Brief §6 Nav N2→N2 directe (Pattern 4 + Pattern 2 + flyTo 1s + préchargement + fade swap), validé en interne 2026-05-18.
- Pas de dette préexistante (`PATRIMOINE-NAV-N2-N2-DIRECTE-001` n'existait pas dans le suivi interne).

---

## [Stratégie D Phase 2 — Splits vico/balagne] — 18 mai 2026

### Added
- **4 nouvelles pieves** :
  - `pieve_piana` (7 communes : Osani, Partinello, Serriera, Ota, Piana, Évisa, Cristinacce) — doyenne_piana_vico_sari. Multipolygon Scandola UNESCO préservé. Note pédagogique golfe de Porto.
  - `pieve_sagone` (2 communes : Cargèse + Coggia migré cinarca) — doyenne_piana_vico_sari. Note pédagogique diocèse médiéval + Cargèse paese grec.
  - `pieve_ostriconi` (14 communes : Palasca, Belgodère, Urtaca, Novella, Pietralba, Lama, Occhiatana, Costa, Ville-di-Paraso, Speloncato, Olmi-Cappella, Vallica, Pioggiola, Mausoléo) — doyenne_balagne. Note pédagogique bassin versant NE Balagne.
  - `pieve_calenzana` (6 communes : Calvi, Lumio, Moncale, Zilia, Montegrosso, Calenzana) — doyenne_balagne. Note pédagogique Calvi+arrière-pays.
- **Alias** `pieve_balagne → pieve_aregno` dans `pieve_aliases.json` v3.
- Script `scripts/phase_strat_d_phase2_splits.py` (création/rename pieves + recalcul polygones via shapely).
- Script `scripts/phase_strat_d_phase2_retag_sites.py` (retag 99 sites + PIP fallback).

### Changed
- **Rename** `pieve_balagne` → `pieve_aregno` (14 communes centre-Balagne : Île-Rousse, Monticello, Corbara, Algajola, Santa-Reparata, Pigna, Aregno, Sant'Antonino, Lavatoggio, Cateri, Avapessa, Nessa, Feliceto, Muro). Nessa 2B175 + Muro 2B173 nouveaux dans aregno (= les "2 communes extra" de l'audit Cowork PIP=34 vs declared=32).
- `pieve_vico` réduite (12 → 7 communes : Marignana, Balogna, Vico, Arbori + Renno+Letia+Murzo migrés sorroinsu).
- `pieve_sorroinsu` réduite (7 → 4 communes : Guagno, Orto, Poggiolo, Soccia).
- `pieve_cinarca` (9 communes : Coggia migré sagone, base v1 = 10 → -1 net = 9).
- **99 sites retag** (83 INSEE direct + 10 PIP fallback + 6 no-op).

### Cas particuliers Q-2 / Q-3
- Q-2 `san_pietro_letia` (Letia 2A141) retag `pieve_celavo → pieve_vico` (cohérence commune INSEE migrée).
- Q-3 `tour_d_isolella_sette_navi` (INSEE Renno 2A258 mais géo côte sud Ajaccio) conserve `pieve_ornano`. Dette `TOUR-ISOLELLA-INSEE-DISCORDANCE-001` ouverte.

### Notes
- Voie (b) patch direct du dérivé maintenue (cohérence Phase 1 + évite régression 4 zombies mapping v1).
- Total **47 → 51 pieves** (typo brief 52 corrigée).
- Anomalie détectée à auditer : `pont_genois_de_piedipartino` (INSEE 2B231 Pigna ≠ nom Piedipartino). Dette `PIEVE-PIEDIPARTINO-INSEE-DISCORDANCE-001` ouverte.

### Arbitrages internes 2026-05-18
- Q-1 : 47 → 51 pieves confirmé
- Q-2 : san_pietro_letia retag commune INSEE
- Q-3 : tour_isolella conservé + dette
- Q4 : Speloncato/Costa/Mausoléo/Pioggiola → ostriconi, Lumio → calenzana
- Q7 : multipolygon Scandola préservé pour pieve_piana

### Reference
- `docs/em-mairie/operations/PIEVES_SPLITS_VICO_BALAGNE_AUDIT_2026-05-18.md` (draft Cowork)
- `docs/em-mairie/operations/ADR-001-pieves-doctrine.md` (Stratégie D)

---

## [Stratégie D Phase 1 — Containment fix] — 18 mai 2026

### Added
- Pieve `pieve_biguglia` (11 communes, doyenne_du_golo) — split `pieve_mariana`
- Pieve `pieve_altiani` (3 communes, doyenne_cortenais) — split `pieve_rogna`
- Containment check post-build dans `scripts/build_pieves_polygons.py` (`--strict-containment` mode)
- Alias `pieve_mariana → pieve_castagniccia` dans `pieve_aliases.json` (v2)
- Mapping amont `_drafts/pieves_communes_mapping_v3_stratD_2026-05-17.json` (2 pieves_added + 29 transferts + 1 rename)
- Script `scripts/phase_strat_d_patch_derive.py` (patch direct dérivé Voie b)
- Script `scripts/phase_strat_d_retag_sites.py` (retag 42 sites = 28 brief + 13 ghost rescue + 1 revert)

### Changed
- `pieve_mariana` renommée `pieve_castagniccia` (7 communes restantes nord-Cortenais : Asco, Castifao, Castiglione, Moltifao, Piedigriggio, Popolasca, Prato-di-Giovellina)
- `pieve_nebbiu` réduite (8 communes migrées : 6 → patrimonio, 2 → balagne)
- `pieve_rogna` réduite (3 communes migrées → altiani)
- `pieve_balagne` enrichie (+4 communes : 2 ex-mariana + 2 ex-nebbiu)
- `pieve_patrimonio` recalculée (6 communes ex-nebbiu)
- 42 sites retag (pieve_slug + doyenne_contemporain_slug cohérents) : 28 brief + 13 ghost rescue (sites pieve_mariana hors brief, PIP géo) + 1 revert (`san_cervone_valle_d_alesani` pieve_bozio/cortenais → pieve_alesani/PO suite arbitrage interne Q3 option B)
- Compteurs : 45 → 47 pieves total

### Fixed
- 29 mismatches commune ↔ pieve ↔ doyenné majoritaire (audit Cowork 2026-05-17) → 0 dans le scope traité
- Dette `PATRIMOINE-PIEVE-MARIANA-MEGA-FUSION-001` fermée (split résout les 4 catégories d'écarts mariana)

### Notes
- **Voie (b) patch direct du dérivé adoptée** : la voie (a) régénération propre via `build_pieves_polygons.py` produit aujourd'hui 4 pieves zombies (giovellina/caccia/ampugnani/campoloro) du mapping v1 désynchronisé + perte `pieve_zicavo` + `pieve_patrimonio` sous-représentée. Hors scope Strat D Phase 1.
- **Escalade priorité `PIEVE-MAPPING-AMONT-DESYNCHRO-001` Moyenne → HAUTE** : PR cleanup mapping amont obligatoire en phase ultérieure (rappel interne 2026-05-17).
- Compteurs visuels légèrement différents de prod pour `pieve_nebbiu` (17→9), `pieve_patrimonio` (9→6) — acceptable Phase 1 beta, à corriger via PR cleanup amont.

### Arbitrages internes
- Q1 (28 sites) : confirmé
- Q2 (Vezzani 2B347 inclusion altiani) : NON, conservé pieve_venaco
- Q3 (san_cervone_valle_d_alesani revert) : option B (pieve_alesani/PO)
- Q4 (note castagniccia) : version Cowork validée

### Reference
- `docs/em-mairie/operations/PIEVES_STRATEGIE_D_PHASE1_BRIEF_CODE_2026-05-17.md`
- `docs/em-mairie/operations/ADR-001-pieves-doctrine.md` (Stratégie D actée)
- `docs/em-mairie/operations/PIEVES_CONTAINMENT_AUDIT_2026-05-17.md` (audit programmatique)

---

## [Non publié] — Fix sticker doyenné figé sur drill cross-doyenné N2→N3 (17 mai 2026)

### fix
- **Sticker doyenné re-render au cross-doyenné** (`onPieveClickV2` dans `patrimoine.html`) : quand un utilisateur entre N3 via clic sur une pieve dont le `doyenne_contemporain_majoritaire` est différent du doyenné N2 courant (ex : N2 Golo → clic `pieve_mariana` qui est majoritaire Cortenais), `currentDoyenneSlug` était correctement mis à jour par B5 mais le sticker top-right restait figé sur l'ancien doyenné. Gap doctrine `BP-FIX-RATTACHEMENT-COMPLET-001` (cohérence pieve+doyenné dans toute mutation). Fix : appel `_renderDoyenneSticker(currentDoyenneSlug, ..., 3)` quand l'ancien et le nouveau diffèrent (`attempt=3` force le fallback data-driven immédiat sans 3 rAF retries inutiles, le nouveau mini n'étant jamais dans le DOM en N2).

---

## [Non publié] — Audit Cowork Phase B : 17 orphelins + 18 cross-doyennés retag selon géo (17 mai 2026)

### fix
- **Cat 1 — 17 sites orphelins retag** (commit `18cd606`) : tous les sites avec `doyenne_contemporain_slug=null` issus de l'audit MCP du 15 mai sont retag (pieve + doyenné) selon géo réelle. Doctrine interne : géo prime sur orthodoxie historique pour Phase 1 beta. Méthode : `shapely.contains` pour chaque coord vs polygones pieves + doyennés. Script reproductible `scripts/retag_orphans.py`. **PATRIMOINE-ORPHANS-INVISIBLES-001 réduite 18 → 1 résiduel** (`cap_corse_extreme_nord` orphan transcommunal Cap, légitime documenté).
- **Cat 2 — 18 sites cross-doyennés retag** (commit `0872308`) : sites avec mismatch `pieve.doyenne_contemporain_majoritaire ≠ site.doyenne_contemporain_slug` corrigés selon géo :
  - 10 non-mariana cohérents (pieve géo + doyenné géo = doyenné majoritaire)
  - 4 mariana géo HORS polygone mariana → retag vers vraie pieve géo (`pieve_casinca`, `pieve_casacconi`, `pieve_balagne` ×2)
  - 4 cas A option interne (incohérence pieve.majoritaire vs doyenné géo acceptée, géo prime) : `san_quilicu_lama`/`santa_maria_urtaca` → nebbiu/golo ; `san_cervone_valle_d_alesani`/`pont_genois_d_altiani` → rogna/PO
  - 10 mariana in_pv=True conservés (exception Mariana mega-fusion, refactor via Cowork)
- **2 cas suspendus option D** (tag inchangé, dettes ouvertes) : `tour_de_farinole` (coord en mer probable à 700m frontière pieve), `casteddu_bastelica` (doute homonymie nom=Bastelica PTV vs géo Cortenais).

### docs
- 3 dettes nouvelles ouvertes :
  - `FARINOLE-COORD-DOUTE-001` (coord centroïde commune mais point hors polygones doyenné)
  - `CASTEDDU-BASTELICA-COORD-DOUTE-001` (audit toponymique/coord à faire)
  - `PATRIMOINE-PIEVE-MARIANA-MEGA-FUSION-001` (mega-pieve héritage fusions caccia→giovellina→mariana, refactor via Cowork + ADR ; `doyennes_visibles` manque cortenais en bonus)
- 1 dette mise à jour : `PATRIMOINE-ORPHANS-INVISIBLES-001` (18 → 1 résiduel `cap_corse_extreme_nord`)
- Doctrine actée en interne 2026-05-17 : Tellux n'est pas un atlas Casta strict, géo prime sur orthodoxie historique pour Phase 1 beta, refactor doctrinal possible à un stade ultérieur.

### scripts
- `scripts/retag_orphans.py` : retag des 17 sites orphelins (Cat 1)
- `scripts/retag_cross_doyennes.py` : retag des 18 sites cross-doyennés (Cat 2)

---

## [Non publié] — Renommage axe `edifices_romans` → `patrimoine_religieux` (15 mai 2026)

### refactor
- **Renommage axe `patrimoine_religieux`** : identifiant interne `edifices_romans` renommé en `patrimoine_religieux` dans tout le front (data + scripts). Champ `categorie` mis à jour de `'Édifice roman'` à `'Patrimoine religieux'`. Périmètre : `docs/data/sites_patrimoine.json` (314 occurrences), `docs/data/sites_corse.json` (316 occ.), scripts dépréciés, documentation. Zéro impact runtime — axe consommé génériquement par `patrimoine.html`. Ferme dette `EDIFICES-ROMANS-RENAME-001` (tracée Sprint 1).

---

## [Non publié] — Clôture série fix N3 patrimoine (15 mai 2026)

### feat
- **Implémentation niveau 3 patrimoine.html** (PR #577, 14 mai) : drill-down pieve depuis vue N2 doyenné, breadcrumb 3 segments cliquable (Corse › Doyenné › Pieve), bookmarking URL hash 3 niveaux (`#doyenne/pieve`), sticker doyenné top-right en N3, bouton retour pieve, fix `PATRIMOINE-HASH-DEEPLINK-CADRAGE-001` (cadrage map sur deeplink), CDN Leaflet.markercluster 1.5.3 (initial, retiré PR #579 cf. ci-dessous).

### fix (série lots 1-12 audit visuel interne, 14-15 mai 2026)
- **PR #579/#580** : Retrait clustering Leaflet.markercluster (résidus visuels N3 au changement de région). Remplacé par `L.layerGroup()` natif. Projet revient à zéro dépendance externe.
- **PR #581/#582** : Résolution conflits homonymie pieves (3 cibles : `pieve_verde`, `pieve_rogna`, `pieve_sartene`). 23 retags vers slugs disambiguïsés par doyenné (`*_prunelli_taravo_valinco`, `*_extreme_sud`, `*_plaine_orientale`, `*_ajaccio`).
- **PR #583/#584** : Cleanup `patrimonio_paese` (1 doublon supprimé, conservation `san_martino_de_patrimonio` église romane).
- **PR #585/#586** : Rattachements lot 1 (8 sites pieve+doyenné). Pattern `BP-FIX-RATTACHEMENT-COMPLET-001` formalisé.
- **PR #587/#588** : Lot 2 (15 retags inversion `pieve_rogna` + 1 suppression doublon `pont_d_altiani`).
- **PR #589/#590** : Lot 3 doyenné Cap (9 retags + investigation `pieve_pino` conservée).
- **PR #591/#592** : Lot 4 doyenné Golo (7 retags + suppression polygone `pieve_ampugnani` fusion NE Orezza).
- **PR #593/#594** : Lot 5 doyenné Balagne (Pont Ponte Leccia → pieve_caccia + suppression doublon `tour_de_la_pietra_ile_rousse`).
- **PR #595/#596** : Lot 6 doyenné Cortenais (10 retags + fix nom `santa_restitude_corte_niolu_versant` double parenthèse).
- **PR #597/#598** : Lot 7 doyenné Vico (4 retags).
- **PR #599/#600** : Lot 8 doyenné Ajaccio (2 retags pattern PR 4 incomplet).
- **PR #601/#602** : Lot 9 doyenné PTV (16 retags option simplifiée, `pieve_verde_PTV` orphelinée).
- **PR #603/#604** : Lot 10 doyenné Extrême-Sud (16 retags, `pieve_verde_extreme_sud` orphelinée).
- **PR #605/#606** : Lot 11 doyenné Plaine Orientale (3 fusions polygones anti-conflit homonymie : `pieve_bozio`→`pieve_alesani`, `pieve_campoloro`→`pieve_moriani`, `pieve_verde`→`pieve_fiumorbo` ; 19 retags + 2 polygones supprimés).
- **PR #607/#608** : Lot 12 doyenné Cap compléments (4 retags : `tour_de_giraglia_ilot` + `anneaux_du_cap_corse` → `pieve_rogliano` ; `tour_de_la_mortella` + `barrage_padula` → `pieve_nebbiu`).

### docs (cette PR)
- 2 BPs formalisées en suivi interne :
  - `BP-FIX-RATTACHEMENT-COMPLET-001` : cohérence `pieve_slug` + `doyenne_contemporain_slug` dans toute PR rattachement
  - `BP-FUSION-POLYGONE-ARBITRAGE-001` : fusion polygone admise sous arbitrage interne Phase A + template plan technique
- 1 dette fermée : `PATRIMOINE-HASH-DEEPLINK-CADRAGE-001` (résolue PR #577)
- 3 dettes nouvelles ouvertes :
  - `PATRIMOINE-PIEVE-NEBBIU-CHEVAUCHE-GOLO-CAP-001` (polygone large couvre 2 doyennés)
  - `PATRIMOINE-DETROIT-BONIFACIO-ENTREE-MANQUANTE-001` (entité absente du data, ajout différé en PR dédiée)
  - `PATRIMOINE-PIEVE-CAP-NON-CLIQUABLE-UI-001` (bug visuel non reproductible programmatiquement)

### Bilan compteurs prod post-série fix N3
- **~140 retags `pieve_slug`** cumulés sur 12 lots
- **3 polygones supprimés** : `pieve_ampugnani` (PR #591), `pieve_campoloro` + `pieve_verde` (PR #605) — pieves_polygons.json passe de 47 à 44
- **3 doublons supprimés** : `patrimonio_paese`, `pont_d_altiani`, `tour_de_la_pietra_ile_rousse` — sites_patrimoine.json passe de 544 à 541
- **N3 patrimoine fonctionnel** pour Phase 1 beta : 12 doyennés audités visuellement en interne, slugs pieves consolidés, 0 dépendance externe, drill-down 3 niveaux (N1 Corse → N2 doyenné → N3 pieve) opérationnel
- **2 doyennés signalés "substantiellement propres" en interne** : Balagne (lot 5), Vico (lot 7)

### PRs série fix N3
#577 (impl) + #579/#580, #581/#582, #583/#584, #585/#586, #587/#588, #589/#590, #591/#592, #593/#594, #595/#596, #597/#598, #599/#600, #601/#602, #603/#604, #605/#606, #607/#608 = **31 PRs cumulées** (1 implémentation + 15 paires fix→deploy)

---

## [Non publié] — Clôture Sprint 7 densification + correction rebalance (14 mai 2026)

### docs
- 2 dettes patrimoine ajoutées :
  - `SITES-PATRIMOINE-PIEVES-SOUS-REPRESENTEES-COMPLEMENT-001` (7 pieves restantes < 5 sites : vivario, vallerustie, filosorma, ampugnani, ghisoni, tavagna, giovellina)
  - `SITES-PATRIMOINE-COMMUNES-MULTI-DOYENNES-EGALITE-001` (15 communes en égalité parfaite multi-doyennés : Monte 4-doyennés, 2 cas 2-2 Cervione+Coti-Chiavari, 12 cas 1-1)

### sites_patrimoine.json — rebalance + Sprint 7 (rétrospectif)

**PR #569 — Sprint correction rebalance doyenne_contemporain_slug** :
- Pré-audit cartographique 14 mai a révélé 13 pieves multi-doyennés + 32 communes multi-doyennés
- Décision interne Option B minimaliste : aligner doyenne_contemporain_slug sur majorité claire (≥2:1) commune, skip égalités
- **23 sites migrés** + 1 fix manuel `san_lorenzo_de_ponte_leccia` (commune Lecci → Morosaglia, Ponte-Leccia hameau)
- Distribution doyennés rebalancée :
  - doyenne_du_golo : 66 → 60 (-6, **signal interne allégé**)
  - doyenne_du_cap : 69 → 76 (+7)
  - doyenne_extreme_sud : 88 → 95 (+7)
  - doyenne_cortenais : 54 → 58 (+4)
  - doyenne_plaine_orientale : 54 → 58 (+4)
  - doyenne_balagne : 54 → 56 (+2)
  - 15 communes en égalité skippées (dette dédiée)
- Préservation stricte : slug, lat, lon, sources non touchés

**PR #571 — Sprint 7 densification ciblée pieves sous-rep** :
- Cible Option B interne : 8 pieves < 5 sites
- Doctrine stricte BP-SPRINT4 GPS publié appliquée
- **+1 entrée** : `pont_de_muricciolu_albertacce` (Albertacce, pieve_niolu, GPS publié Médiathèque Corse 42.326036/8.983954, XVIᵉ-XVIIIᵉ génois, arche unique granit alt 852m, emporté tempête Ciaran novembre 2023, inventaire préliminaire Médiathèque Culturelle Corse)
- pieve_niolu : 3 → 5 sites (sortie zone sous-rep)
- 7 pieves restent < 5 sites (dette dédiée)

### Compteurs prod post-Sprint 7
- 544 sites · 13 axes
- 11 ponts historiques (10 → 11)
- doyenne_du_golo allégé -6 sites (signal interne traité)

### PRs Sprint 7
- #569 fix(patrimoine): rebalance doyenne_contemporain_slug (23 sites + 1 fix)
- #571 data(patrimoine): Sprint 7 densification pieve_niolu (+Muricciolu)

---

## [Non publié] — Clôture Sprint 6 paesi d'altura (14 mai 2026)

### docs
- 1 dette patrimoine paesi ajoutée : `SITES-PATRIMOINE-PAESI-D-ALTURA-COMPLEMENT-001` (sous-cible 9/25 assumée scénario B, même doctrine Sprint 4 ponts).

### sites_patrimoine.json (rétrospectif Sprint 6)
- **Création nouvel axe `paesi_d_altura`** dans `_meta.axes_corpus_referentiel` (couleur DA `#A89B8C` Pierre claire)
- 0 → 9 paesi (sprint monolithique, P1 strict)
- Doctrine d'altura validée : exclusion par cross-référence avec axe `tours_genoises` (43 communes-tours exclues)
- Verrou mécanique post-édition : **0 conflit commune-tour détecté**
- Labels représentés : 2 paesi AVF (Plus Beaux Villages de France 2026 : Sant'Antonino, Pigna)
- Sources : Wikipedia FR commune infobox coordonnées (cross-source 9 fetches) + Les Plus Beaux Villages de France 2026 + Mérimée Notes voyage Corse 1840 (Sartène)
- Cible révisée scénario B 25 atteinte à 9/25 = 36% (doctrine « couverture représentative > exhaustivité »)
- Cas frontière arbitrés Phase A en interne :
  - **Piana EXCLU** (AVF officiel mais commune avec Tour Turghiu, doctrine d'altura stricte)
  - **Corte EXCLU** (citadelle militaire historique, hors périmètre paesi d'altura)

### Distribution finale 9 paesi
| Paese | Doyenné | Pieve | Label |
|---|---|---|---|
| Sant'Antonino | doyenne_balagne | pieve_balagne | AVF |
| Pigna | doyenne_balagne | pieve_balagne | AVF |
| Speloncato | doyenne_balagne | pieve_balagne | — |
| Sartène centre | doyenne_extreme_sud | pieve_sartene | — |
| Patrimonio | doyenne_du_cap | pieve_nebbiu | — |
| Aullène | doyenne_extreme_sud | pieve_tallano | — |
| Levie | doyenne_extreme_sud | pieve_carbini | — |
| Bastelica | doyenne_ajaccio | pieve_celavo | — |
| Évisa | doyenne_piana_vico_sari | pieve_vico | — |

### PR Sprint 6
- #565 Sprint 6 paesi d'altura monolithique (+9 paesi, création axe)

---

## [Non publié] — Clôture Sprint 5 archéo + castelli (14 mai 2026)

### docs
- 4 dettes patrimoine archéo ajoutées (Sprint 5 série) :
  `SITES-PATRIMOINE-ARCHEO-ALERIA-V2-APPROFONDIE-001` (multi-composantes : forum, thermes, basilique, nécropoles),
  `SITES-PATRIMOINE-ARCHEO-MARIANA-V2-APPROFONDIE-001` (mithraeum, basilique paléochrétienne, baptistère, palais),
  `SITES-PATRIMOINE-ARCHEO-CITES-ROMAINES-COMPLEMENT-001` (Sagona/Calvi/Centuri antiques skippées Sprint 5b doctrine stricte),
  `SITES-PATRIMOINE-VILLAGES-MEDIEVAUX-DISPARUS-COMPLEMENT-001` (axe non créé Sprint 5c, candidat Saint-Jean-d'Ortolo PA2A000005 sans GPS publié).

### sites_patrimoine.json (rétrospectif Sprint 5 complet)
- **Création nouvel axe `archeo_romaine`** dans `_meta.axes_corpus_referentiel` (couleur DA `#8E2F1F` Porphyre)
- **Création nouvel axe `castelli_oppida`** dans `_meta.axes_corpus_referentiel` (couleur DA `#1F2329` Ardoise)
- **Axe `villages_medievaux_disparus` non créé** (0 candidat passant doctrine stricte GPS publié)
- **7 migrations** :
  - `aleria_antique` : `patrimoine_bati_remarquable` → `archeo_romaine` (préservation stricte gps_locked + priorité étoile + visuel `_tellux_v2`)
  - 6 castelli protohistoriques : `megalithes` → `castelli_oppida` (`alo_bisuje`, `casteddu_bastelica`, `casteddu_caleca`, `casteddu_lozari`, `castellu_araghju`, `cucuruzzu_capula`)
- **Compteur `megalithes` : 70 → 64** (cleanup sémantique, redistribution castelli protohistoriques)
- **1 ajout** : `mariana_antique` (P1 strict, Lucciana 2B148, pieve_mariana, GPS publié 42.53928/9.49597, Mérimée PA00099208)
- Périmètre chronologique : XIIᵉ av. J.-C. — ~1450
- Sources : Mérimée POP (PA + IA), Wikipedia FR, INRAP
- Doctrine `BP-SPRINT4-DOCTRINE-STRICTE-GPS-PUBLIE-001` strictement appliquée → Sprint 5b et 5c vides (cités antiques secondaires + villages désertés sans GPS publié)
- Doctrine interne : Aleria + Mariana = 1 site unique chacun, dettes v2 multi-composantes ouvertes pour exploitation patrimoniale fine ultérieure

### PRs Sprint 5
- #561 Sprint 5a (création 2 axes + 7 migrations + Mariana, structurant)
- Sprint 5b : pas de PR (0 candidat passant doctrine, Sagona/Calvi/Centuri archivés dette)
- Sprint 5c : pas de PR (0 candidat passant doctrine, Saint-Jean-d'Ortolo archivé dette)

---

## [Non publié] — Clôture Sprint 4 ponts historiques (14 mai 2026)

### docs
- 2 dettes patrimoine ponts + 1 dette app (CSS orphelin v8) ajoutées :
  `SITES-PATRIMOINE-PONTS-SOUS-CIBLE-SPRINT4-001` (10/15-20 assumé scénario B),
  `SITES-PATRIMOINE-PONTS-SKIPS-PRECISION-GPS-001` (5 candidats archivés : Zippitoli, Zaglia, Ponti Vecchiu, Trinité, Calzola),
  `APP-CSS-ORPHELIN-PURGE-V8-001` (~90 lignes CSS orphelin résiduel post-purge v8 d'`app.html`, ferme formellement priorité 1 `PROJECT_INSTRUCTIONS_v3.md` du 22 avril 2026).
- 1 bonne pratique ajoutée dans `## Bonnes pratiques issues de sprints` :
  `BP-SPRINT4-DOCTRINE-STRICTE-GPS-PUBLIE-001` (skip sans GPS publié, pas de centroïde commune en P1 pour patrimoine bâti, doctrine Sprint 4b/4c).

### sites_patrimoine.json (rétrospectif Sprint 4 complet, 3 PRs data)
- **Création nouvel axe `ponts_historiques`** dans `_meta.axes_corpus_referentiel`
- Couleur DA v2 `#475569` (gris-bleu ardoise, distinct des 5 couleurs déjà utilisées)
- **0 → 10 ponts** sur la série 3 sprints
- Périmètre chronologique : XIIᵉ pisans + XVᵉ-XVIIIᵉ génois + XIXᵉ+ inclus si Mérimée recensés (axe englobant)
- Distribution finale : 5 P1 strict + 5 P2 latent
- Bassins couverts :
  - **Haute-Corse Sprint 4a** : 8 ponts (Castagniccia + Tavignano + Asco + Golo)
  - **CS-ouest Sprint 4b** : 1 pont (Pianella Ota)
  - **CS-sud Sprint 4c** : 1 pont (Spina-Cavallu Sartène)
- Sources : Mérimée POP (PA*/IA* cross-vérifiés fiche) + Wikipedia FR
- Cible révisée scénario B 15-20 : **10/15 = 67%** (cible basse), doctrine stricte assumée
- 5 candidats skips précision GPS archivés (dette dédiée)
- **Anomalie Altiani PA00099257** (en réalité Viaduc Eiffel Venaco) redressée en route Sprint 4a → bonne ref `PA00099154`
- **Cas Spina-Cavallu** : typologie pisane XIIIᵉ confirmée Wikipedia FR (pas génois malgré la nomenclature courante), élargissement chronologique axe `ponts_historiques` validé ex ante par périmètre incluant pisans

### PRs Sprint 4
- #553 Sprint 4a Haute-Corse (création axe + 8 ponts)
- #555 Sprint 4b CS-ouest (+1 pont Pianella Ota)
- #557 Sprint 4c CS-sud (+1 pont Spina-Cavallu Sartène, clôture série)

---

## [Non publié] — Clôture Sprint 3 tours littorales (13 mai 2026)

### docs
- 7 dettes patrimoine consolidées (Sprint 3 série complète) :
  `SITES-PATRIMOINE-TOURS-PRE-SPRINT3-PIEVE-NULL-001` (4 tours résiduelles),
  `SITES-PATRIMOINE-TOURS-PRE-SPRINT3-INSEE-NULL-001` (4 tours résiduelles),
  `SITES-PATRIMOINE-PIEVE-ATTRIBUTIONS-SUSPECTES-001` (Meria, Olmeta-di-Capocorso, Saint-Florent),
  `SITES-PATRIMOINE-TOURS-CASTELLUCCIO-DOUBLET-001` (audit toponymique),
  `SITES-PATRIMOINE-TOURS-FARINOLE-GPS-PRECIS-001` (centroïde commune),
  `SITES-PATRIMOINE-TOURS-POGGIO-ERSA-MAISON-TOUR-001` (PA2B000009 GPS anomal),
  `SITES-PATRIMOINE-TOURS-MERIMEE-EXHAUSTIF-COMPLEMENT-001` (4 tours résiduelles 66→70).
- 1 bonne pratique tracée dans nouvelle section `## Bonnes pratiques issues de sprints` :
  `BP-SPRINT3B-MAPPING-INTEGRE-INGESTION-001` (mapping `pieve_slug` + `commune_insee` dès ingestion Code, pattern Sprint 3b/3c/3d).

### sites_patrimoine.json (rétrospectif Sprint 3 complet, 5 PRs data + 1 mapping correctif)
- **15 → 66 tours littorales (+51)**
- 4 zones blanches comblées :
  - Balagne : 0 → 11
  - Ajaccio : 1 → 6
  - Extrême-Sud : 1 → 7
  - Plaine Orientale côte est : 0 → 7
- Cap renforcé : 5 → 23
- Piana-Vico-Sari : 4 → 9
- Sources : Mérimée POP (25+ références PA*/IA*) + Wikipedia FR cross-référencées
- Cible brief 70 atteinte à **66/70 = 94%** (4 résiduelles tracées en dette `SITES-PATRIMOINE-TOURS-MERIMEE-EXHAUSTIF-COMPLEMENT-001`)
- Plafond Sprint 3 : 51/55 ajouts consommés (marge 4 reflète sous-densité historique Plaine Orientale, documentée et acceptée)

### PRs Sprint 3
- #541 Sprint 3a Cap+Balagne (+28 tours, mapping non intégré)
- #543 Sprint 3a mapping pieve+INSEE correctif (28 tours patchées + Farinole P1→P2)
- #545 Sprint 3b Ouest+Sud-Ouest (+10 tours, **mapping intégré dès ingestion** — leçon)
- #547 Sprint 3c Extrême-Sud + côte est (+11 tours)
- #549 Sprint 3d complément Plaine Orientale (+2 tours, sous-cible documentée)

---

## [Non publié] — Sprint 2 mégalithes + consolidation dettes (13 mai 2026)

### data — Sprint 2 Phase B mégalithes (PR #538)

- `docs/data/sites_patrimoine.json` : +7 entrées mégalithes + 5 enrichissements existants
  - **Phase 1 (4)** : `tola_di_u_turmentu` (Serra-di-Ferro), `renicciu_coggia` (Coggia), `paomia_i` (Cargèse), `tivulaghju_porto_vecchio` (Porto-Vecchio, Tramoni 2007)
  - **Phase 2 latent (3)** : `casalabriva_contra_maio`, `tremica_casaglione`, `vasculaghju` (centroid commune, `gps_status: centroid_a_preciser`)
  - **Enrichissements** : `palaggiu` (MH PA00099118 + Grosjean BSPF 1972), `statue_menhir_santa_naria` (commune + dimensions + GPS T4T35 secondaire), `tivulaggio_alignement` (commune complétée), `capu_di_logu` (MH PA00099074 + Giraux, anti-doublon A1), `casa_di_l_orca` (Leandri 2012 + PA2B000037 + Wikidata Q17539593, alias Monte Revincu complexe A2)
- Mégalithes total : 63 → 70 (P1=67, P2 latent=3)
- Sites total : 465 → 472
- Anomalies Phase A redressées : A1 (`capu_di_logu` était déjà à Belvédère-Campomoro, pas Bonifacio — doublon évité) et A2 (slug `monte_revincu` déjà pris par sommet géologique, axe `remarquables_geologiques` — `casa_di_l_orca` enrichi à la place)

### docs — Consolidation dettes session 13 mai 2026 (PR docs séparée)

- 6 nouvelles dettes : `SITES-EM-JSON-UNTERMINATED-STRING-001`, `SITES-REFERENCE-JSON-DEPRECATION-001`, `REMARQUABLES-GEOLOGIQUES-DRIFT-001`, `SITES-PATRIMOINE-INSEE-BELVEDERE-CAMPOMORO-001` (A3), `CORPUS-META-AXES-INCOMPLET-001` (A4), `PATRIMOINE-HASH-DEEPLINK-CADRAGE-001` (cadrage map cassé sur navigation hash directe N2, identifiée pendant validation preview PR #538)
- 1 fermeture par invalidation : `SITES-PATRIMOINE-JSON-L13034-001` (audit Code H1 — fichier dev/main JSON valide, cause réelle = sandbox Cowork stale, pattern `OPS-COWORK-SANDBOX-GIT-DRIFT-001`)
- Rappel des 3 dettes ajoutées plus tôt dans la même journée : `OPS-COWORK-SANDBOX-GIT-DRIFT-001`, `SITES-PATRIMOINE-JSON-L13034-001` (immédiatement fermée ci-dessus), `CLEANUP-PATRIMOINE-INSTRUMENTATION-001`

### Cibles non atteintes (notées en dette)

- Cible brief Cowork de 72 mégalithes (Sprint 2) → réalisé 70 sans doublons (A1 + A2 redressés)
- Iconographie : les 7 nouvelles entrées P1 + P2 latent n'ont pas de champ `visuel` rempli (sprint dédié à programmer, mêmes verrous que Sprint 1)

---

## [Non publié] — Sprint 1 patrimoine (13 mai 2026, PRs #536 + #537)

### data

- `docs/data/sites_patrimoine.json` : 54 églises romanes activées Phase 2 → Phase 1 sur l'axe `edifices_romans`
- Axe `edifices_romans` Phase 1 : 27 → 81 entrées (+54)
- Distribution 8-10 par doyenné contemporain (vs précédente : max 5, min 0)
- Zone blanche `doyenne_ajaccio` comblée : 0 → 9 P1
- Critère C3 hybride appliqué : 44 MH classés/inscrits + 10 complément éditorial qualité
- Q2 Bonifacio diversifié : 2 MH gardés, 2 substituts (Porto-Vecchio + Sartène)

### chore

- Restauration de la troncation L.13034 introduite par un bug outil Cowork pendant le commit (entrée `plateau_du_coscione_tellux_v2`, déjà P1, restaurée à l'identique depuis HEAD)

---

## [Non publié] — Consolidation sites EM (13 mai 2026, PRs #529 + #530 + #531)

### data — M1

- Création de `public/data/sites_app.json` (61 sites EM/UTH/thermales consolidés et typés)
- `gps_audit` obligatoire sur 61/61 entrées
- 3 sources auditées (`sites_em`, `points_chauds_radio`, `sites_remarquables`)
- Corrections signalées en interne : `ophi_farinole`, `surv_bonifacio`, `Pietrapola`, `Caldane` (commune corrigée Sainte-Lucie-de-Tallano)
- Suppression de l'entrée fantôme "Lac thermal de Tora" (typo historique Tolla, source inexistante)

### refactor — M2

- `app.html` consomme `sites_app.json` via `loadSitesApp()` (thin wrappers), suppression des 3 sources séparées en frontend

### chore — M3

- Suppression des 3 JSONs obsolètes (`sites_em.json`, `points_chauds_radio_corse.json`, `sites_remarquables_corse.json`)
- Code mort `app.html` retiré (`adaptSiteRemarquable`, `mapSRGranulaire`, `_srLoadPromise`, commentaires orphelins Brief 29/33, ~70 lignes)
- Scripts Python adaptés à `sites_app.json` (`sync_cross_app.py`, `corpus_health_check.py`, `brief_pipeline.py`, `tools/build_sites_app.py`)
- ~74 KB de redondance dataset supprimés

---

## [Non publié] — Fix bug 2e clic patrimoine (13 mai 2026, PR #532)

### Fixed

- `patrimoine.html` : Leaflet `bindPopup()` attache automatiquement un handler `click: _openPopup` (toggle) sur le marker, qui se déclenche au 2e clic APRÈS `marker.openPopup()` piloté par `onSpotClick` et referme la popup immédiatement. Fix : `marker.off('click', marker._openPopup, marker)` après chaque `bindPopup`. Le 2e clic sur un marker patrimoine rouvre désormais sa fiche au lieu de la fermer

### Notes

- Instrumentation `[CLICK-DBG]` / `[BIND-TRACE]` / `[UNBIND-TRACE]` (~30 lignes) laissée en place pour observabilité (dette `CLEANUP-PATRIMOINE-INSTRUMENTATION-001` programmée 5-7 jours post-merge)

---

## [2.10.4] — 2026-05-01

### Changed — Alignement canonique sprint U (PR à venir, sprint `chore/glossaire-canonical-alignment`)

Sprint d'alignement post-livraison du sprint U (`[2.10.3]`) sur la spec canonique du prompt complet. 4 ajustements mineurs sans changement fonctionnel.

**Renommage classe CSS `glossaire.html`** : `.short-anchor` → `.term-short-anchor` (préfixe cohérent avec les `id="term-X"` du sprint T). 25 ancres `<span class="...">` renommées + 1 règle CSS.

**Règle CSS canonique `glossaire.html`** :

```diff
-dl.glossary .short-anchor { display: inline-block; width: 0; height: 0; scroll-margin-top: 80px; }
+dl.glossary .term-short-anchor { display: block; height: 0; visibility: hidden; scroll-margin-top: 80px; }
```

Approche `display: block; visibility: hidden;` plus propre que `inline-block; width: 0;` (pas de risque d'interférence avec le flux inline).

**Ajout `og:image:type` `mairies.html`** : balise `<meta property="og:image:type" content="image/png">` ajoutée après `og:image`. Sémantique propre, certaines plateformes OG en tirent parti.

**Enrichissement texte alt OG/Twitter `mairies.html`** :

```diff
-content="Tellux Corse — Outils mairies pour les 360 communes corses"
+content="Tellux Corse — outils mairies pour les 360 communes corses, cartographie électromagnétique territoriale"
```

Appliqué aux deux balises `og:image:alt` et `twitter:image:alt`. Le texte alt enrichi intègre la signature du projet, cohérent avec la composition visuelle de l'asset variante B.

### Validation

- ✅ Aucune modification du contenu de l'asset `assets/og/mairies_og.{png,svg}`
- ✅ Aucune modification des `<dt id="term-...">` longs ni des `<a class="xref">` du sprint T
- ✅ Aucune modification des autres balises SEO de `mairies.html` (canonical, description, robots, og:type, og:locale, og:site_name, og:url, og:title, og:description, twitter:title, twitter:description)
- ✅ Aucune modification des autres pages
- ✅ Rétro-compat absolue : 119 ids `term-*` (94 longs + 25 courts) toujours présents

---

## [2.10.3] — 2026-05-01

### Added — Asset Open Graph dédié pour `mairies.html` (PR à venir, sprint `feat/og-mairies-slugs-courts-glossaire`)

Asset Open Graph 1200×630 dédié pour `mairies.html`, **variante B « Cartographique avec silhouette Corse »** retenue (recommandation Cowork DA sprint S, drafts dans `Tellux/_drafts/og/`). Composition : fond Pierre `#F5F0E7` avec léger dégradé vers Brume, logo Tellux v14 + wordmark en haut à gauche, silhouette stylisée de la Corse à droite (trait Ocre 2.5 px, 3 marqueurs Maquis discrets Bastia/Ajaccio/Corte non labellisés), signature « Outils mairies — 360 communes corses · Cartographie EM » + URL `tellux.pages.dev/mairies` en bas.

**Fichiers ajoutés** :

- `assets/og/mairies_og.png` (1200×630, ~42 ko, rastérisation cairosvg)
- `assets/og/mairies_og.svg` (4.6 ko, source vectorielle modifiable)

**Critères techniques** : ratio 1.91:1 conforme aux standards Open Graph (Facebook, LinkedIn, Discord, Slack) et Twitter Cards. Poids des PNG bien sous la cible des 200 ko. Aucune dépendance externe.

### Changed — Balises Open Graph et Twitter Cards de `mairies.html`

Balises `<meta>` mises à jour pour pointer vers le nouvel asset au lieu du fallback `assets/logo/favicon_512.png` (1:1) installé au sprint L :

- `og:image` → `https://tellux.pages.dev/assets/og/mairies_og.png`
- `og:image:width` → `1200` (nouveau)
- `og:image:height` → `630` (nouveau)
- `og:image:alt` → `Tellux Corse — Outils mairies pour les 360 communes corses` (au lieu de `Logo Tellux`)
- `twitter:card` → `summary_large_image` (au lieu de `summary`, upgrade pour profiter du format 1.91:1)
- `twitter:image` → `https://tellux.pages.dev/assets/og/mairies_og.png`
- `twitter:image:alt` → `Tellux Corse — Outils mairies pour les 360 communes corses` (nouveau)

Balises `og:type`, `og:locale`, `og:site_name`, `twitter:title`, `twitter:description`, `og:url`, `og:title`, `og:description` du sprint L conservées telles quelles. Le favicon `assets/logo/favicon_512.png` reste utilisé pour son usage natif (favicon navigateur), inchangé.

### Added — Slugs courts complémentaires sur `glossaire.html`

Sprint complémentaire au sprint T (`[2.10.2]`) qui avait livré 94 slugs longs au format `term-{libellé-complet-slug}`. Ce sprint ajoute des slugs courts (sigle seul) pour les 25 entrées au format `SIGLE — Développement`, en complément des slugs longs déjà présents. **Approche additive** : chaque ancre courte est insérée comme `<span id="term-{sigle-slug}" class="short-anchor" aria-hidden="true"></span>` juste avant le `<dt>` correspondant. Aucune modification des `<dt id="term-...">` longs ni des `<a class="xref" href="#term-...">` du sprint T.

**Statistiques** : 25 slugs courts ajoutés sur 25 entrées éligibles, 0 collision détectée.

**Exemples produits** :

| Sigle | Slug court | Slug long (préservé, sprint T) |
|---|---|---|
| `IRSN` | `term-irsn` | `term-irsn-institut-de-radioprotection-et-de-surete-nucleaire` |
| `ANFR` | `term-anfr` | `term-anfr-agence-nationale-des-frequences` |
| `ASNR` | `term-asnr` | `term-asnr-autorite-de-surete-nucleaire-et-de-radioprotection` |
| `IGRF` | `term-igrf` | `term-igrf-international-geomagnetic-reference-field` |
| `ICNIRP` | `term-icnirp` | `term-icnirp-international-commission-on-non-ionizing-radiation-protection` |
| `EDF SEI` | `term-edf-sei` | `term-edf-sei-systemes-energetiques-insulaires` |

**Rétro-compatibilité absolue** : les 73 liens `<a class="xref" href="#term-{slug-long}">` du sprint T continuent de fonctionner. Les slugs courts ne servent qu'au partage d'URL externe (`https://tellux.pages.dev/glossaire.html#term-irsn` plus court que la version longue).

### Changed — CSS `glossaire.html`

Une règle CSS ajoutée :

```css
dl.glossary .short-anchor { display: inline-block; width: 0; height: 0; scroll-margin-top: 80px; }
```

Ancres `<span class="short-anchor">` invisibles (largeur et hauteur zéro), avec `scroll-margin-top` cohérent avec celui des `<dt[id]>` du sprint T pour aligner le scroll vers ancre.

### Validation

- ✅ Asset `mairies_og.png` (43 ko) et `.svg` (4.6 ko) intégrés dans `assets/og/`.
- ✅ Balises OG/Twitter de `mairies.html` mises à jour ; `og:type`, `og:locale`, `og:site_name`, `og:url`, `og:title`, `og:description`, `twitter:title`, `twitter:description` du sprint L préservées.
- ✅ 25 ancres courtes créées dans `glossaire.html`, 0 collision (ni avec les ids `letter-X`, ni avec les ids `term-{long}`, ni entre slugs courts).
- ✅ Rétro-compatibilité totale : 119 ids `term-*` au total (94 longs + 25 courts), 73 hrefs `#term-{long}` du sprint T toujours valides, 0 lien cassé.
- ✅ Aucune modification des `<dt id="term-...">` longs ni des `<a class="xref">` du sprint T.
- ✅ Aucune modification des autres balises SEO de `mairies.html` (canonical, description, robots).
- ✅ Aucune modification des autres pages (transparence, retractations, etc.).

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
- Section 1 reformulée pour retirer toute mention publique de cible de financement (cohérence avec la doctrine éditoriale post-cycle audit Phase D : pas de mention publique d'attribution conditionnelle). Après reformulation : « Le projet est mis à disposition publique via tellux.pages.dev. »
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
- **Open Graph et Twitter Cards** : enrichissement des meta tags dans le `<head>`. Ajout `og:type`, `og:locale` (`fr_FR`), `og:site_name`, `og:image`, `og:image:alt` et les 4 balises `twitter:card`/`title`/`description`/`image`. Image temporaire : `assets/logo/favicon_512.png` (512×512, ratio 1:1) avec `twitter:card` en `summary` (cohérent avec ratio carré). Asset Open Graph dédié 1200×630 (1.91:1) à produire en session dédiée — non créé d'autorité dans ce sprint.
- **Hiérarchie h1** : audit confirme un seul `<h1>` (l.436 « Outils administratifs · Communes corses »), hiérarchie h1 → h2 → h3 propre. Aucune modification requise.

**Notes** :

- La régression SEO apparente sur preview Cloudflare (92 → 61) est un faux positif : les URL preview portent un `X-Robots-Tag: noindex` automatique pour éviter l'indexation des URLs temporaires (audit Lighthouse signale `is-crawlable: Page is blocked from indexing`). À reconfirmer sur prod après merge.
- Anomalies hors périmètre détectées et signalées (non corrigées) : `robots-txt` invalide (présent avant et après), `color-contrast` insuffisant (présent avant et après), CLS et TBT en légère régression à surveiller.

---

## [2.8.3] — 2026-05-01

### Changed — Audit cohérence registre interne des dettes techniques post-cycle audit Phase D (PR à venir, sprint `chore/audit-dettes-coherence-post-phase-d`)

Audit documentaire des dettes techniques pour fermer l'anomalie 4 hors périmètre signalée par la PR [#283](https://github.com/dellahstella/tellux/pull/283) (sprint hygiène repo) et l'anomalie hors périmètre signalée par la PR [#289](https://github.com/dellahstella/tellux/pull/289) (sprint audit EMAG-CRUSTAL).

Modifications cosmétiques appliquées :

- **Fix wording `WDMAM-NAMING-001`** (note de fermeture, section « Dettes fermées récemment ») : la note décrivait un pattern « bbox-dynamique reconstruit à chaque activation » qui ne correspondait plus à l'état actuel du code après le rollback de la PR #190. La note précise désormais le rollback vers la bbox fixe `[[41.3, 8.5], [43.1, 9.65]]` et la raison du rollback (URL dynamique manquant le `renderingRule EMAG2_Color_Scale` rendant l'image transparente), avec renvoi vers le commentaire `app.html:2092-2097`.
- **Actualisation terminologique IRSN → ASNR** sur 2 occurrences de la dette `RADON-DATASET-COVERAGE-001` (description et condition de déblocage), formulation `ASNR (anciennement IRSN)` selon la doctrine appliquée par les sprints `audit-D1`, `audit-D1bis`, `audit-D1ter`. Préserve la traçabilité historique vers les fiches data.gouv.fr publiées sous le slug IRSN tout en utilisant le nom d'autorité actuel.

Pas de fermeture, recadrage ou ouverture de dette dans ce sprint. Les arbitrages non triviaux sont remontés dans la description de la PR pour décision interne.

---

## [2.8.2] — 2026-05-01

### Changed — Fermeture de la dette `EMAG-CRUSTAL-AUDIT-001` après audit (PR à venir, sprint `chore/audit-emag-crustal-fermeture`)

Investigation conduite sur `app.html` pour confirmer ou infirmer la duplication potentielle entre les couches `emag` et `crustal`. Verdict : couches fonctionnellement distinctes, pas de redondance. Aucune modification de code applicatif requise. La dette est déplacée en section « Dettes fermées récemment » du suivi interne avec note d'audit détaillée.

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

Hors périmètre validé en interne : footers de `mairies.html`, `cadre-scientifique.html`, `methode-et-limites.html`, `guide-utilisation.html` non modifiés dans ce sprint, à arbitrer ultérieurement si besoin.

---

## [2.8.0] — 2026-05-01

### Changed — Terminologie ASNR sur les mentions d'actualité (PR [#274](https://github.com/dellahstella/tellux/pull/274), [#278](https://github.com/dellahstella/tellux/pull/278), [#280](https://github.com/dellahstella/tellux/pull/280))

Alignement de la terminologie « ASNR » (active depuis le 1ᵉʳ janvier 2025, suite à la fusion ASN+IRSN) sur l'ensemble des mentions IRSN d'actualité non millésimées du site public et du code applicatif. Les ~16 occurrences IRSN restantes sont toutes des références à des datasets explicitement millésimés 2018 (cartographie radon, décret 2018-434, NCRP 94, noms de colonne CSV `radon_class_IRSN`) et sont conservées en l'état.

- Sprint audit-D1 (PR [#274](https://github.com/dellahstella/tellux/pull/274)) : 7 occurrences contemporaines remplacées dans `index.html` (×5), `methode-et-limites.html` (×2), `guide-utilisation.html` (×2), `transparence.html` (×1).
- Sprint audit-D1bis (PR [#278](https://github.com/dellahstella/tellux/pull/278)) : 5 mentions d'actualité corrigées dans `cadre-scientifique.html` (×3 : sections 1, 4.1, 6.3) et `app.html` (×2 : footer fonctionnel L.1184 et `epistemic_note` de `calcGammaAmbient` L.4274).
- Sprint audit-D1ter (PR [#280](https://github.com/dellahstella/tellux/pull/280)) : 2 résiduels dans `app.html` (commentaire L.3992 « BRGM + ASNR + IGN BD TOPO » ; href L.1184 `https://teleray.irsn.fr` → `https://teleray.asnr.fr`, vivacité 200 OK confirmée par curl).

### Changed — Audit Phase D, fixes structurants landing (PR [#274](https://github.com/dellahstella/tellux/pull/274))

- Compteur antennes du bloc statistiques hero d'`index.html` aligné sur le chiffre exact daté `~960 sites ANFR` (avril 2026), avec mention en infobulle `title=` « plus de 3000 antennes individuelles ».
- Footer d'`index.html` enrichi avec l'identification légale requise par la LCEN.
- Ancre `#contact` d'`index.html` enrichie d'un libellé explicite identifiant le porteur du projet Tellux Corse.

### Added — Section « Cadres éthiques de référence » sur la page Transparence (PR [#276](https://github.com/dellahstella/tellux/pull/276))

Nouvelle section 4 dans `transparence.html` détaillant l'articulation envisagée avec la Charte de la donnée et de l'IA Corse (21 principes en 9 titres) et le Guide de bonne pratique IA Smart Isula (12 bonnes pratiques). Articulation préfigurée par les pratiques actuelles déjà visibles sur le site (MIT, RLS, polices auto-hébergées, pas de tracker). Renumérotation des sections actuelles 4 et 5 en 5 et 6.

### Added then Removed — Section « Inscription territoriale » sur la landing (PR [#276](https://github.com/dellahstella/tellux/pull/276) puis [#281](https://github.com/dellahstella/tellux/pull/281))

Cas particulier signalé pour clarté du lecteur : une section `#inscription-territoriale` a été ajoutée à `index.html` par la PR [#276](https://github.com/dellahstella/tellux/pull/276) (entre `#projet` et `#ressources`, 3 cartes empilées détaillant l'articulation institutionnelle), puis retirée par la PR [#281](https://github.com/dellahstella/tellux/pull/281) sur décision éditoriale (sobriété de la landing publique, la cohérence narrative institutionnelle est portée par les dossiers internes). Bilan net pour la version `[2.8.0]` : section absente du site public. Le draft markdown source (`_drafts/audit-D1/section_spdiac_landing.md`, untracked) est conservé localement pour usage potentiel ultérieur (par exemple page À propos dédiée).

---

## [2.7.0] — 2026-04-27

### Removed — Retrait des modules patrimoine et agronomie du dépôt public (PR `refactor/audit-transparence-corpus-public`)

- Suppression de `patrimoine.html` et `agronomie.html`. Les deux fichiers existaient dans le dépôt public sans être liés depuis la landing ; ils sont retirés à l'occasion de l'audit de transparence du 27 avril 2026 pour aligner le périmètre public sur la phase 1 effectivement publiée (cartographie EM, outils communaux, corpus). Contenus conservés en interne pour réactivation éventuelle dans une phase ultérieure.
- Mise à jour en cascade : `index.html` (bloc état d'avancement, références bibliographiques, sources territoire), `README.md`, `ROADMAP.md` (section périmètre, sections Phase 2/3/4 consolidées en une note neutre, renumérotation), `ARCHITECTURE.md`, `app.html` (lien biblio redirigé vers `corpus.html`).
- Anonymisation des mentions nominatives dans la documentation interne.
- Reformulation des cibles de financement dans les contextes publics.
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
- Notes méthodologiques : `docs/em-mairie/data-sources/postes_sources_corse_notes.md`, `eoliennes_corse_notes.md`, `points_chauds_radio_corse_notes.md`

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
- Notes méthodologie sources : `docs/em-mairie/data-sources/radon_communes_level3_corse_notes.md`, `docs/em-mairie/data-sources/tdf_emitters_corse_notes.md`
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
