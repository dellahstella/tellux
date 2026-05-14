# Tellux — Dettes techniques ouvertes

**Dernière mise à jour :** 13 mai 2026 (clôture série Sprint 3 tours littorales) — ajout 7 dettes patrimoine consolidées : `SITES-PATRIMOINE-TOURS-PRE-SPRINT3-PIEVE-NULL-001` (4 tours résiduelles), `SITES-PATRIMOINE-TOURS-PRE-SPRINT3-INSEE-NULL-001` (4 tours résiduelles), `SITES-PATRIMOINE-PIEVE-ATTRIBUTIONS-SUSPECTES-001` (Meria, Olmeta, Saint-Florent), `SITES-PATRIMOINE-TOURS-CASTELLUCCIO-DOUBLET-001` (audit toponymique), `SITES-PATRIMOINE-TOURS-FARINOLE-GPS-PRECIS-001` (centroïde commune), `SITES-PATRIMOINE-TOURS-POGGIO-ERSA-MAISON-TOUR-001` (PA2B000009, GPS anomal), `SITES-PATRIMOINE-TOURS-MERIMEE-EXHAUSTIF-COMPLEMENT-001` (4 tours résiduelles 66→70). Création section `## Bonnes pratiques issues de sprints` avec 1 entrée : `BP-SPRINT3B-MAPPING-INTEGRE-INGESTION-001`. Précédente : 13 mai 2026 (Sprint 2 Phase B mégalithes + finalisation dettes) — ajout 6 dettes : `SITES-EM-JSON-UNTERMINATED-STRING-001`, `SITES-REFERENCE-JSON-DEPRECATION-001`, `REMARQUABLES-GEOLOGIQUES-DRIFT-001`, `SITES-PATRIMOINE-INSEE-BELVEDERE-CAMPOMORO-001` (anomalie A3 Cowork Phase A), `CORPUS-META-AXES-INCOMPLET-001` (anomalie A4 Cowork Phase A), `PATRIMOINE-HASH-DEEPLINK-CADRAGE-001` (cadrage map cassé sur navigation hash directe N2, identifiée pendant validation preview PR #538). Fermeture par invalidation : `SITES-PATRIMOINE-JSON-L13034-001` (audit Code H1, le fichier `sites_patrimoine.json` côté dev/main est JSON valide ; cause réelle = sandbox Cowork stale, pattern `OPS-COWORK-SANDBOX-GIT-DRIFT-001`). Précédente : 13 mai 2026 (Sprint M1/M2/M3 sites_app.json + fix patrimoine 2e clic PR #532) — ajout 3 dettes absentes du fichier : `OPS-COWORK-SANDBOX-GIT-DRIFT-001`, `SITES-PATRIMOINE-JSON-L13034-001`, `CLEANUP-PATRIMOINE-INSTRUMENTATION-001`. Aucune modification des dettes existantes. Précédente : 12 mai 2026 (Sprint micro-data cleanup post-Sprints-A/B/C) — Item 1 doublon `san_andrea` déjà accompli au Sprint B (PR #486+#487, `git mv` = rename, pas copie ; 0 fichier subsistant dans `docs/assets/visuels/san_andrea*` vérifié dans 5 worktrees actifs). Item 2 résolu : 12 slugs whitelist drifts corrigés dans `sites_patrimoine.json` + `sites_corse.json` (commit `48e3556`, illustre False→True + visuel `.png` complet). Nouvelle dette `WHITELIST-ILLUSTRE-FLAG-DRIFT-001` ouverte + résolue dans le même sprint. Pipeline `consolidate_sites.py` not run (déprécié Sprint A), édit manuel cohérent. Précédente : 12 mai 2026 (Sprint C cleanup worktrees OPS) — nettoyage des 2 résiduels mentionnés au brief : worktree root libéré (`git checkout --detach origin/main`, branche `fix/patrimoine-audit-phase-b` supprimée), worktree `hungry-austin-0b60a4` admin nettoyé (`git worktree remove --force`, branche `claude/hungry-austin-0b60a4` supprimée). Worktrees passe de 7 à 5 actifs. Dette `OPS-WORKTREE-CREATION-001` **partiellement résolue** (résiduels admin nettoyés, directory `hungry-austin-0b60a4/` orpheline sur disque comme attendu — Permission denied pendant CWD agent actif). Précédente : 12 mai 2026 (Sprint B data légers) — résolution de 2 dettes patrimoine : `ALERIA-RUINE-FICHE-V3-KEY-MISMATCH-001` (commit `db4074a`, fiche_v3_slug aligné `'aleria_ruine'` → `'aleria_antique'` dans sites_patrimoine.json + sites_corse.json) et `SAN-ANDREA-PIEDICROCE-SOURCE-INTROUVABLE-001` (nouvelle dette ouverte + résolue, commit `866cf86`, archivage des 4 visuels via `git mv` vers `_drafts/visuels_archive/` après hypothèse γ Soleil retenue — erreur exploration Cowork, recherche web exhaustive 6+ sources fiables 12 mai sans résultat). Whitelist reste à 33. Précédente : 12 mai 2026 (Sprint A pipeline réparation, option (b)) — découverte STOP A : `consolidate_sites.py` est obsolète (pas à réparer), `sites_patrimoine.json` est la SOURCE CANON runtime (et non `sites_corse.json` qui est DEPRECATED target 2026-06-05). Actions : (1) `consolidate_sites.py` déprécié explicitement (commit `7565563`, docstring + `sys.exit(2)`), (2) `sync_cross_app.py --apply` exécuté (commit `26fb064`, 28 divergences `sites_em.json` propagées depuis canonical), (3) 2 dettes reformulées/fermées : `PIPELINE-DRIFT-SITES-PATRIMOINE-001` → reformulée `CONSOLIDATE-SITES-PY-OBSOLETE-001` (basse priorité) ; `PIPELINE-DRIFT-SITES-EM-CORSE-001` → **FERMÉE** par sync_cross_app. Nouvelle dette ouverte `PIPELINE-DATA-ARCHITECTURE-DOC-001` (architecture data à documenter pour éviter re-diagnostic à chaque sprint). Précédente : 12 mai 2026 (Sprint micro-data réintégration orphelins) — réintégration de 9 sites orphelins à `sites_patrimoine.json` (commit `6094c11`, corpus Phase 1 passe 171→180) + promotion 9 slugs à `ILLUSTRATED_SPOTS` (commit `312dffe`, whitelist 24→33). Override `plateau_du_coscione` → `doyenne_extreme_sud` + `pieve_verde` dans `SPOT_DOYENNE_OVERRIDES.json`. SKIP `san_andrea_de_piedicroce` (absent canonical, brief séparé futur). **Dette `PIPELINE-DRIFT-SITES-PATRIMOINE-001` escaladée moyenne → HAUTE** (14 sites perdus cumulés en 2 mois, patches manuels itératifs). Mise à jour `ILLUSTRATED-WHITELIST-DRIFT-001` (drift 100→33 sous contrôle éditorial). `MONTE-GENOVA-NATURAL-VISUEL-001` confirmée OUVERTE (audit visuels 2026-05-12 : 0 variante `_naturel` en filesystem). Précédente : 11 mai 2026 (Sprint app-ui-polish, Items 1+2a partiels) — Item 1 ✓ : barre conditions permanente `#conditions-bar` (5 chips Kp/Réseau/Live/Orage/Contribs + accordéon 4 sections), panel `?` slim (légende EM seule). Item 2a partiel : 2 corrections GPS sites géophys (`capu_rossu` recadré sur pic 42.225/8.573, `reserve_de_scandola` aligné sur canonical 42.36072/8.56127). 2 sites skip faute source externe (`barrage_padula`, `min_argentella`) — à re-sourcer brief séparé. 2 sites confirmés OK (`calanques_de_piana` sur D81, `reserve_de_scandola` péninsule). Nouvelle dette `PIPELINE-DRIFT-SITES-EM-CORSE-001` ouverte (même cause racine que `PIPELINE-DRIFT-SITES-PATRIMOINE-001`). Items 2b (refactor popup geophys UTH-pattern) et 3 (popup calc Tellux viewport) en attente. Précédente : 11 mai 2026 (Sprint complément post-curation-N1) — Items 1/2/3 du brief précédent traités : étoile priorité unique sur `aleria_antique` (15 drops total : 13 brief + 2 drift cirque_de_bonifato/plateau_du_coscione côté `sites_corse.json`), Poggio Venaco rename + `.png` cosmétique, override `cap_corse_extreme_nord` → `doyenne_du_cap`. Item 4 (T4 régression panel aleria) classé NOMINAL après investigation chaîne `applyHash → onSpotClick → openPopup` (popup s'ouvre, pas le panel — by design, le panel s'ouvre via bouton "Ouvrir la fiche" dans la popup). Nouvelle dette `VISUEL-EXT-COSMETIC-001` ouverte (228 sites au total sans extension `.png`, sans impact runtime). `PIPELINE-DRIFT-SITES-PATRIMOINE-001` confirmée OUVERTE (toutes les modif data Items 1+2 ont dû éditer les 2 fichiers — preuve vivante du drift). Précédente : 11 mai 2026 (Sprint curation N1) — ajout de 3 nouvelles dettes ouvertes : `PIPELINE-DRIFT-SITES-PATRIMOINE-001` (drift 479 canonical → 453 publié, 22 sites perdus identité inconnue), `MONTE-GENOVA-NATURAL-VISUEL-001` (variante "sans mégalithes" à produire), `ALERIA-RUINE-FICHE-V3-KEY-MISMATCH-001` (bug latent fallback). Mise à jour `ILLUSTRATED-WHITELIST-DRIFT-001` (whitelist 12→24, drift 96→24 sous contrôle). 4 sites naturels Phase 1 (anneaux_du_cap_corse, massif_du_haut_asco, monte_d_oro, monte_renoso) ajoutés manuellement à `sites_patrimoine.json` (commit `18de84e`). Suppression des 9 fiches v3 doyennés de `fiches_patrimoine.json` (`aleria_antique` conservée, commit `7264151`). Précédente : 11 mai 2026 (Sprint dettes post-Phase-B) — résolution de 3 dettes supplémentaires : `DOYENNE-ILLUSTRATIONS-OBSOLETE-001` (S6, commit `bf3415c`, Option A commentaires actualisés), `HASH-SPOT-SEUL-001` (S7, commit `396947e`, `applyHash` étendu single-segment spot), et `SITES-COORDS-COTIERES-VERIFICATION-001` (commit `a966511`, audit GPS + commune pour `capu_di_logu`, `tour_de_capo_di_muro`, `u_paladinu`). Création sous-ticket `OPS-CODE-WORKTREE-ISOLATION-FLAG-001` (investigation cause racine `OPS-WORKTREE-CREATION-001` : worktrees auto-créés par desktop app hardcoded, remediation = usage CLI exclusif). Cleanup 7 worktrees + 6 branches orphelines (commit `c2c7ada`). Précédente : 11 mai 2026 (Sprint Phase B post-audit Cowork patrimoine.html) — résolution de 3 dettes via branche `fix/patrimoine-audit-phase-b-v2` : `SITES-NAME-NULL-001` (suppression doublon `menhirs_du_rizzanese`, commit `7f8f592`), `N2-ILLUSTRATED-SHARED-MARKER-001` (créée + résolue, fix solution A symétrique enter/exit, commit `5f1b480`), `N2-SPOT-CLICK-PROPAGATION-001` (créée + résolue, `L.DomEvent.stopPropagation` sur marker/pieve clicks, commit `4b077f4`). Création de 5 nouvelles dettes ouvertes : `HASH-SPOT-SEUL-001` (S7), `DOYENNE-ILLUSTRATIONS-OBSOLETE-001` (S6), `ILLUSTRATED-WHITELIST-DRIFT-001` (S5), `OPS-WORKTREE-CREATION-001` (14 worktrees parasites + violation doctrine), `SITES-COORDS-COTIERES-VERIFICATION-001` (3 sites lon<8.85 à investigater). Précédente : 6 mai 2026 (Brief 29 app.html migration sites_corse.json) — ajout 4 nouvelles dettes consolidation `PATRIMOINE-BASTIA-PIEVES-SOUS-ATTRIBUEES`, `SITES-CORSE-HAMEAUX-CHURCHES-INSEE-001`, `SITES-CORSE-TOPONYMES-LOCAUX-001`, `TOUR-AGNELLO-GPS-DISCORDANCE-001` (audits Cowork à programmer post-Brief 29). Statut `PATRIMOINE-ORPHANS-INVISIBLES-001` actualisé (43 sites invisibles vs 18 avant Brief 28, lié à l'élargissement de corpus et résorbable via `_drafts/SPOT_DOYENNE_OVERRIDES.json`). Précédente : 6 mai 2026 (Brief 28 patrimoine.html migration sites_corse.json) — ajout `PATRIMOINE-CLICK-CONFLICTS-001` (conflits zones de clic miniatures/polygones, identifié Brief 27) et `PATRIMOINE-LOAD-PERF-001` (3 fetches au boot, sérialisation polygones derrière sites_corse.json). Précédente : 5 mai 2026 (Brief 17 Phase A + B) — résolution `PATRIMOINE-PIEVES-39-VS-47-CASTA-001` via livraison Cowork v2 (`pieves_communes_mapping_v2_canonicite_casta.json`) : 8 pieves Casta restaurées + 39 transferts de communes appliqués par le pipeline. Sortie `pieves_polygons.json` passe de 39 à 47 pieves. Phase A préservée : `PATRIMOINE-ORPHANS-INVISIBLES-001` en voie d'éclaircissement via `_drafts/SPOT_DOYENNE_OVERRIDES.json`. Précédente : 4 mai 2026 (Brief 9 patrimoine drill-down niveau 2) — ajout de `PATRIMOINE-PIEVES-39-VS-47-CASTA-001` (périmètre 39 pieves alignées Brief 2 vs 47 Casta canoniques, 8 pieves implicitement absorbées ou sans rattachement clair). Précédente : 4 mai 2026 (Brief 8 patrimoine révisé) — actualisation des deux entrées `PATRIMOINE-TILES-ZOOM-001` et `PATRIMOINE-ORPHANS-INVISIBLES-001` pour refléter le pivot patrimoine.html sur les 10 doyennés contemporains du diocèse d'Ajaccio (vision macro Soleil 2026-05-04, drill-down 2 niveaux retiré, ~105 spots invisibles dans la nav v1). Précédente : 1ᵉʳ mai 2026 (soir, post sprints J et L) — recensement de 4 dettes nouvelles issues de l'audit Lighthouse du sprint L (`mairies.html`) : `ROBOTS-TXT-001`, `A11Y-CONTRAST-001`, `MAIRIES-CLS-TBT-001`, `MAIRIES-REDIRECTS-001`. Précédente : 1ᵉʳ mai 2026 (soir) — audit cohérence post-cycle audit Phase D : fix wording note de fermeture `WDMAM-NAMING-001` (rollback bbox-dynamique → bbox fixe par PR #190 désormais reflété correctement) ; actualisation terminologique IRSN → ASNR (anciennement IRSN) sur 2 occurrences de la dette `RADON-DATASET-COVERAGE-001` (description + condition de déblocage) selon doctrine D1bis. Précédente : 1ᵉʳ mai 2026 — fermeture EMAG-CRUSTAL-AUDIT-001 par audit (verdict : `emag` et `crustal` fonctionnellement distincts, pas de redondance, voir notes en section "Dettes fermées récemment"). Précédente : 27 avril 2026 (soir) — ajout CAPTEURS-WEB-API-001 (magnétomètre indisponible dans les navigateurs depuis Chrome M116, août 2023 ; module différé d'une éventuelle phase ultérieure couvrant une app Android native). Précédente : 27 avril 2026 — fermeture WDMAM-NAMING-001 (fusion EMAG2/WDMAM en couche unique bbox-dynamique). Précédente : 26 avril 2026 (soir) — ajout RADON-DATASET-COVERAGE-001 (couverture partielle du dataset radon 2B vs décret 2018-434, identifiée lors de l'audit préparatoire aux envois aux institutions). 26 avril 2026 — ajout des dettes CONTRIB-SCHEMA-001 (incohérence schéma stockage contributions, identifiée lors du fix Android PR #154), RADON-CLASS-DUPLICATE et HELPERS-INLINE-CONSTS (issues de la cartographie d'extraction du moteur, `docs/tellux-engine-extraction-plan.md`). 25 avril 2026 — consolidation semaine 21-25 avril : enrichissement BT-CALIBRATION-001 (priorité Haute, mesures ratios ×57 à ×210), nouvelle dette EMAG-CRUSTAL-AUDIT-001 (Cowork Session B), précisions PR # sur les fermetures ELF-CALIB-001/WMM-CROSSCHECK-001/BDFORET-V2-001/ELF-VECTOR-001/BT-ELF-001, ajout en fermées récemment de SUPABASE-COMMUNE-FIELD-001 (PR #137) et ANTENNES-REFRESH-001 (PR #138), liens démarches externes sur TÉLÉ-001/HTA-TENSION-001/RADIO-AERO-001 (lettres envoyées 28-29 avril 2026). 25 avril — ajout RTE-OPENDATA-001. 24 avril — ajout RADON-L3-UNIFICATION-001 + WDMAM-NAMING-001.

Ce document liste les dettes techniques ouvertes identifiées dans l'application Tellux. Chaque dette fait l'objet d'un identifiant pérenne, d'une description factuelle et d'une condition de déblocage documentée. Aucune de ces dettes ne bloque la publication de la phase 1.

---

## Dettes actives

### GELÉ-001 — Constantes Expert gelées

**Description :** Les pondérations du mode Expertise (`w_M`, `w_RF`, `w_I`) et les bornes de normalisation (`EXPERT_BOUNDS_DEFAULT`) sont fixées à titre provisoire. Elles sont documentées comme telles dans l'interface (bandeau permanent du mode Expertise) et dans le code (commentaire « GELÉ — GELÉ-001 »).

**Priorité :** Haute

**Condition de déblocage :** Relecture méthodologique par un physicien tiers qualifié et validation explicite des constantes.

---

### NCRP-001 — Fond naturel terrestre gelé

**Description :** La composante terrestre de `calcGammaAmbient` (formule NCRP 94) est provisoirement gelée, en attente de validation méthodologique externe.

**Priorité :** Haute

**Condition de déblocage :** Lié à GELÉ-001.

---

### TÉLÉ-001 — API Téléray ASNR

**Description :** L'intégration en temps réel du réseau Téléray (débit de dose gamma) n'est pas réalisée. La composante ionisante actuelle repose sur la classification radon officielle en vigueur et la composante cosmique altitudinale via IGN RGE Alti.

**Priorité :** Moyenne

**Condition de déblocage :** En attente d'un retour de l'organisme concerné sur les conditions d'accès à l'API.

**Démarche externe :** lettre ASNR direction Téléray envoyée le 28 avril 2026 (cf. `ROADMAP.md` section « Suivi des sollicitations institutionnelles »).

---

### HTA-TENSION-001 — Voltage des lignes HTA

**Description :** Le dataset Supabase `hta_lines` ne comporte pas de champ voltage/tension permettant de différencier HTA 20 kV et HTB 63/90/225 kV. `calcMagneticELF_v2` applique un courant uniforme de 225 A (option de repli documentée).

**Priorité :** Moyenne

**Condition de déblocage :** Enrichissement du dataset via migration SQL ou accès à une source de données tension par segment.

**Démarche externe :** lettre EDF SEI direction Corse envoyée le 29 avril 2026 (cf. `ROADMAP.md` section « Suivi des sollicitations institutionnelles »). Lien transverse avec `BT-CALIBRATION-001` (la même lettre sollicite des caractéristiques techniques utiles à la recalibration BT).

---

### ELF-TRIPH-001 — Correction triphasée approximée

**Description :** La correction triphasée appliquée au calcul Biot-Savart ELF utilise un coefficient `k=0.5` approximé au-delà de 20 m. La géométrie réelle des pylônes (espacement des phases) n'est pas modélisée par segment.

**Priorité :** Faible

**Condition de déblocage :** Accès à des données géométriques pylône par pylône, ou modèle statistique validé.

---

### BT-CALIBRATION-001 — Cancellation insuffisante du modèle Biot-Savart sur lignes BT torsadées

**Description :** Le calcul des segments BT (basse tension, lignes torsadées) dans `calcMagneticELF_v2` utilise actuellement la même formule Biot-Savart et correction triphasée `k = 0.5` que les lignes HTA. Or cette correction est calibrée sur la géométrie pylône HTA (phases espacées de 1-3 m). Appliquée telle quelle aux câbles BT torsadés (phases espacées d'environ 1 cm), elle produit une cancellation très insuffisante. Audit post-merge PR #71 (2026-04-22) : ratios v2.5 (HTA seul) vs v2.6 (HTA + BT segments) sur 4 villes corses :

| Zone | v2.5 (nT) | v2.6 (nT) | Ratio |
|---|---:|---:|---:|
| Bastia centre | 160 | 33 592 | ×210 |
| Calvi | 208 | 26 654 | ×128 |
| Porto-Vecchio | 367 | 21 047 | ×57 |
| Ajaccio centre | 219 | 14 253 | ×65 |

Pour Ajaccio : 5 038 segments BT contribuent 14 134 nT, soit deux ordres de grandeur au-dessus des mesures urbaines typiques (50-300 nT documentés dans la littérature). Cause racine probable : décroissance attendue 1/d² ou 1/d³ au lieu de 1/d, et facteur de cancellation dépendant fortement de la géométrie torsadée des conducteurs BT. État actuel du code : le calcul BT par segments est désactivé (flag `USE_BT_SEGMENTS = false` dans `app.html`), et le proxy `BT_ZONES` legacy reste actif.

**Priorité :** Haute (impact ordre de grandeur en zone urbaine si activation prématurée)

**Condition de déblocage :** Recalibration du modèle BT par session dédiée. Trois leviers envisagés :
- Recalibration paramétrique (coefficient `k` BT distinct, cap par segment, distance minimale)
- Modèle statistique de densité BT par tuile
- Modèle Biot-Savart adapté aux câbles torsadés basse tension (1/d² ou 1/d³)

La validation physique préalable (littérature ou mesures terrain) est un prérequis.

**Lien transverse :** la lettre EDF SEI envoyée le 29 avril 2026 (cf. `ROADMAP.md` section « Suivi des sollicitations institutionnelles ») sollicite les caractéristiques techniques (tension, configuration des conducteurs, courants nominaux) qui éclaireraient cette calibration.

---

### RADIO-AERO-001 — Radiométrie aérienne

**Description :** L'intégration des données de radiométrie aérienne BRGM pour affiner la composante ionisante est non réalisée. Aucun flux WMS, WFS ou téléchargement public de ces données n'a été identifié lors de l'audit 2026-04-21.

**Priorité :** Faible

**Condition de déblocage :** En attente d'un retour de l'organisme concerné sur les conditions de mise à disposition de ces données.

**Démarche externe :** lettre BRGM direction régionale Corse envoyée le 29 avril 2026 (cf. `ROADMAP.md` section « Suivi des sollicitations institutionnelles »). La lettre sollicite également l'accès aux flux WFS géologie Corse et aux campagnes spectrogamma.

---

### BDFORET-GRANULARITE-001 — Granularité BD Forêt

**Description :** La couche Forêts publiques ONF actuellement intégrée ne permet pas de distinguer les essences (feuillus, conifères, maquis). La version BD Forêt V3 avec détail par essence n'est pas disponible en WMS raster stable.

**Priorité :** Faible

**Condition de déblocage :** Stabilisation de la version BD Forêt V3 en production, ou rasterisation locale d'une extraction shapefile.

---

### CORPUS-PILIERS-001 — Relecture corpus Pilier A et Pilier B post-migration Biot-Savart

**Description :** Le corpus scientifique interne a été scindé le 2026-04-21 en deux piliers distincts : Pilier A (14 fiches scientifiques S1-S14, en attente de relecture méthodologique externe par un physicien) et Pilier B (20 fiches patrimoine gamifiées P1-P20). Les fiches avaient initialement été formulées avec un modèle ELF basé sur 8 axes simplifiés. Depuis la migration Biot-Savart réel sur réseau HTA complet (avril 2026), le taux de validation de chaque fiche peut évoluer significativement.

**Historique.** Cette dette a été initialement identifiée sous l'ID `H1-H88-ELF-001` (formulation antérieure à la scission). L'ID est reformulé en `CORPUS-PILIERS-001` le 2026-04-23 pour refléter la structure post-scission. La correspondance H-numéro → fiche S ou P reste consultable dans le corpus interne.

**Priorité :** Haute

**Condition de déblocage :** Session dédiée de relecture par pilier, avec recalcul des corrélations et mise à jour du corpus interne. Pilier A : à prioriser dans le cadre de la relecture méthodologique externe. Pilier B : peut attendre l'obtention d'un financement dédié.

---

### MIGN-001 — Appelants legacy `calcAll`

**Description :** Un petit nombre d'appelants legacy de `calcAll` ne transmettent pas les paramètres `commune_info` et `altitude_m` introduits lors de la migration v2. Comportement non bloquant : les valeurs par défaut sont utilisées.

**Priorité :** Faible

**Condition de déblocage :** Session dédiée de nettoyage (non bloquant).

---

### MESURES-EM-BASCULE-001 — Bascule deux boutons couche Mesures EM

**Description :** La couche Mesures EM unifiée (mergée 2026-04-23) regroupe deux datasets hétérogènes dans un seul bouton UI : contributions citoyennes (layer `lCon`, clusterisé, Supabase `contributions`) et mesures certifiées ANFR/EXEM (layer `lCert`, non-clusterisé, `public/data/cartoradio_certified_corse.json`). À terme, quand le volume des certifiées dépassera environ 100 entrées (actuellement 30), la distinction visuelle entre les deux strates devra passer par deux boutons distincts pour permettre à l'utilisateur de filtrer l'un sans l'autre.

**Priorité :** Faible (non bloquant tant que le volume certifiées reste inférieur à ~100)

**Condition de déblocage :** dépassement du seuil de ~100 mesures certifiées OU feedback utilisateur signalant la confusion entre les deux strates OU session UI dédiée identifiant d'autres besoins de filtrage.

---

### RADON-L3-UNIFICATION-001 — Unification des deux sources radon (GeoJSON polygones vs JSON L3 INSEE)

**Description :** Tellux maintient actuellement deux sources de données radon indépendantes pour la Corse. D'une part, `public/data/radon_zones_corse.geojson` (253 polygones communaux officiels ASNR, 216 cat.3 + 37 cat.2) est consommé par la couche cartographique `lRadon` via `buildRadonLayer()` (introduit par la PR #130 du 24 avril 2026 — intégration ; l'unification proprement dite reste pendante). D'autre part, `public/data/radon_communes_level3_corse.json` (28 communes explicites + règle « tout 2A classé cat.3 », 152 communes théoriques cat.3 uniquement) est consommé par `loadRadonCommunesL3()` → `isCommuneRadonL3()` → `calcRadonPotential()` pour booster la classe du score composite lorsque la commune cliquée est officiellement classée. Les deux sources pointent vers le même décret (2018-434, arrêté du 27 juin 2018) mais ont des couvertures différentes : le GeoJSON est exhaustif (253 communes cat.2+cat.3 aux frontières réelles), le JSON L3 utilise un proxy (règle départementale 2A + liste 2B partielle, cat.3 seulement). Risque de divergence documentaire : une commune 2B cat.2 du GeoJSON n'apparaîtra pas dans `isCommuneRadonL3()`.

**Priorité :** Faible (aucun bug fonctionnel ; les deux flux cohabitent proprement. Dette documentaire : une seule source canonique serait plus propre à long terme)

**Condition de déblocage :** Session dédiée d'unification avec (1) test d'équivalence quantitatif — les 216 cat.3 du GeoJSON couvrent-ils bien les 124 communes 2A intégrales + 28 communes 2B listées dans le JSON L3 actuel, sans régression ? Quels INSEE sont dans l'un mais pas l'autre ? (2) refonte de `isCommuneRadonL3()` pour lire depuis un index INSEE extrait du GeoJSON au chargement (via `loadRadonCommunesFromGeoJSON()` — un seul fetch partagé avec la couche cartographique). (3) suppression de `public/data/radon_communes_level3_corse.json`, de `loadRadonCommunesL3()`, des constantes `RADON_L3_INSEE_SET`, `RADON_L3_NAME_SET`, `RADON_L3_SOURCE`, `RADON_2A_APPLIES_ALL`, et de la fonction `normCommuneName()` si elle n'est utilisée que par ce flux. (4) vérification que le composite `calcRadonPotential` continue de booster correctement la classe à 3 sur un clic dans une commune 2A et sur un clic dans une commune 2B listée. Zone concernée : `app.html` uniquement (fichier data à supprimer en parallèle).

---

### RTE-OPENDATA-001 — Demande de cadrage RTE différée post-financement

**Description :** La lettre RTE Open Data v1 (rédigée 22 avril 2026, recadrée 25 avril 2026) sollicitait trois éléments auprès de la direction Open Data RTE : confirmation de stabilité des flux eco2mix utilisés actuellement par Tellux (endpoint `digital.iservices.rte-france.com/open_api/consumption/v1/short_term?sandbox=true`), validation de l'usage non commercial public d'eco2mix sandbox dans le contexte cartographique Tellux, orientation sur d'éventuels jeux de données Corse-spécifiques RTE susceptibles de remplacer le profil horaire estimé du modèle local de repli. Décision 2026-04-25 : envoi différé. Le canal officiel RTE passe par un formulaire de contact ODRÉ (`opendata.reseaux-energies.fr`) limité aux messages courts, inadapté à une demande structurée multi-points. L'envoi formel est reporté à la phase post-financement, dans un cadre institutionnel adapté (structure dédiée, courrier sur en-tête, canal direction Open Data RTE direct). En attendant, Tellux continue d'utiliser eco2mix sandbox dans le respect du quota officiel (50 000 appels API par utilisateur et par mois, mentionné dans les CGU ODRÉ). Aucune action technique requise côté Tellux. Lien interne : la lettre v1 est archivée hors du repo public ; une version recadrée sera produite pour l'envoi post-financement. Lien transverse : `chargeFacteur` (variable consommée par `calcMagneticELF_v1` / `calcMagneticELF_v2` dans `app.html`) repose actuellement sur cet endpoint sandbox, avec fallback profil horaire local en cas d'échec.

**Priorité :** Faible (différée, non bloquante — le flux sandbox actuel est fonctionnel)

**Condition de déblocage :** Post-obtention d'un financement Phase 1 (FEDER ou équivalent). Reformulation de la lettre v1 dans un cadre institutionnel adapté au canal direction RTE.

---

### CONTRIB-SCHEMA-001 — Incohérence du schéma de stockage des contributions (Mesure technique vs Capteurs appareil)

**Description :** Les deux flux d'écriture vers la table Supabase `contributions` stockent la valeur de mesure dans deux unités différentes. Le flux « Mesure technique » (formulaire `cform`) convertit la valeur saisie en nT et stocke `unite='nT'` quel que soit le choix de l'utilisateur (`app.html` lignes 4866-4868 et 4873). Le flux « Capteurs appareil » (`ctab-cap`) stocke la valeur brute renvoyée par l'API Magnetometer en µT et stocke `unite='µT'` (`app.html` lignes 7120-7121). La colonne `valeur` mélange donc deux unités selon la provenance de la contribution, ce qui complique l'agrégation, les comparaisons et toute requête SQL transversale. Identifiée lors de l'audit du 26 avril 2026 ayant conduit à la PR #154 (fix affichage magnétomètre). La dette est masquée côté affichage par la fonction `formatMagneticField` (introduite par la PR #154) qui lit `c.unite` comme unité canonique, mais le schéma reste incohérent au niveau stockage.

**Priorité :** Faible (masquée côté affichage, sans bug fonctionnel direct)

**Condition de déblocage :** Harmoniser le pipeline d'écriture pour que les deux flux convergent sur une même unité de stockage (a priori nT). Migration Supabase à prévoir pour normaliser les contributions historiques flux B (multiplier `valeur` par 1000 sur les lignes où `unite='µT'`, puis passer `unite` à `nT`).

---

### RADON-CLASS-DUPLICATE — Doublon du mapping `RADON_CLASS_BY_LITHOLOGY` dans `app.html`

**Description :** Le mapping `RADON_CLASS_BY_LITHOLOGY` (correspondance lithologie → classe radon 1/2/3) est défini en deux endroits dans `app.html` : dans `calcSubstrateContext` (ligne ~3939) et dans `calcRadonPotential` (ligne ~4102). Risque de dérive entre les deux copies si l'une est mise à jour sans l'autre. Le contenu actuel est identique et stable. Identifiée le 26 avril 2026 lors de la cartographie d'extraction du moteur (`docs/tellux-engine-extraction-plan.md` section 6.7).

**Priorité :** Faible (cosmétique, contenu actuel identique)

**Condition de déblocage :** Centraliser le mapping en un seul export (`data/radon-classification.js` ou équivalent) lors de l'extraction du moteur. Référence : `docs/tellux-engine-extraction-plan.md` section 6.7.

---

### HELPERS-INLINE-CONSTS — Constantes physiques inline dans le moteur de calcul

**Description :** Plusieurs constantes physiques sont définies inline dans le corps de fonctions du moteur de calcul de `app.html`, recréées à chaque appel et non testables en isolation. Liste identifiée le 26 avril 2026 lors de la cartographie du moteur (`docs/tellux-engine-extraction-plan.md` section 6.8) :
- `MU0_OVER_2PI` dans `calcBiotSavartSegment` (ligne ~3350)
- `METERS_PER_DEG_LAT` dans `calcBiotSavartSegment` et `calcBiotSavartSegmentVec` (lignes ~3090 et 3130)
- `METERS_PER_DEG_LON` dans `calcBiotSavartSegment` et `calcBiotSavartSegmentVec` (lignes ~3091 et 3131)
- `RIVER_PTS` dans `calcSubstrateContext`

**Priorité :** Faible (sans impact runtime significatif, mais nuit à la testabilité et à la lisibilité du code)

**Condition de déblocage :** Hisser ces constantes au niveau module lors de l'extraction du moteur. Référence : `docs/tellux-engine-extraction-plan.md` section 6.8.

---

### RADON-DATASET-COVERAGE-001 — Couverture partielle du dataset radon Corse vs décret 2018-434

**Description :** Le dataset `public/data/radon_communes_level3_corse.json` liste 28 communes corses explicitement classées en zone 3 par le décret 2018-434 / arrêté du 27 juin 2018 (14 en Corse-du-Sud, 14 en Haute-Corse). En réalité, l'arrêté classe environ 194-209 communes en zone 3 sur l'ensemble du territoire corse : la totalité du département 2A (124 communes, classement intégral confirmé par l'arrêté annexe IV) + environ 70 à 85 communes du département 2B (estimation faute d'extraction exhaustive). Couverture pratique du modèle Tellux : la règle départementale `RADON_2A_APPLIES_ALL` (`app.html` ligne 4050) reconnaît automatiquement les 124 communes 2A par préfixe INSEE, donc la couverture 2A est complète. La couverture 2B reste à environ 17-20% (14 communes listées sur 70-85 attendues), ce qui constitue une dette réelle. Identifiée le 26 avril 2026 lors de l'audit du dataset radon en préparation des envois aux institutions. Les notes méthodologiques `docs/data-sources/radon_communes_level3_corse_notes.md` (datées 20 avril 2026) documentent déjà l'incomplétude (« dataset amorce fiable, à compléter ») et listent les sources de complétion (data.gouv.fr ASNR (anciennement IRSN), Legifrance annexe IV, cartographie ASNR interactive).

**Priorité :** Moyenne (impact direct sur la fidélité du score radon en Haute-Corse, sans bug fonctionnel — la classe par défaut estimée par lithologie reste appliquée pour les communes non listées explicitement)

**Condition de déblocage :** Compléter le dataset avec les communes 2B manquantes en téléchargeant le dataset radon ASNR (anciennement IRSN) sur data.gouv.fr depuis un environnement non bloqué, puis joindre les codes INSEE et centroïdes officiels via API BAN ou COG INSEE 2016. Référence : `docs/data-sources/radon_communes_level3_corse_notes.md` section 6 (méthodologie de complétion phase 2).

---

### ROBOTS-TXT-001 — Fichier `robots.txt` invalide

**Description :** Lighthouse SEO signale un échec `robots-txt | robots.txt is not valid` sur `mairies.html` (audit du 1ᵉʳ mai 2026, sprint L). Anomalie présente avant et après le sprint L, hors périmètre des chantiers SEO traités. Le fichier `robots.txt` actuel (s'il existe à la racine du déploiement Cloudflare Pages) ne respecte pas la spécification attendue par Lighthouse, ou n'est pas présent / pas correctement servi.

**Priorité :** Faible

**Condition de déblocage :** Audit du `robots.txt` actuel en production (vérifier sa présence et son contenu à `https://tellux.pages.dev/robots.txt`). Création ou correction conforme à la spécification, en autorisant l'indexation des pages publiques (`index.html`, `app.html`, `mairies.html`, `cadre-scientifique.html`, `transparence.html`, `methode-et-limites.html`, `guide-utilisation.html`, `mentions-legales.html`, `donnees-vie-privee.html`, `retractations.html`). Vérification post-correction via Lighthouse SEO.

---

### A11Y-CONTRAST-001 — Contraste de couleurs insuffisant

**Description :** Lighthouse Accessibility signale un échec `color-contrast | Background and foreground colors do not have a sufficient contrast ratio` sur `mairies.html` (audit du 1ᵉʳ mai 2026, sprint L). Anomalie présente avant et après le sprint L. La localisation exacte du composant fautif n'a pas été identifiée dans le sprint L (sortie Lighthouse non détaillée à ce niveau). Probablement applicable à d'autres pages éditoriales du site partageant la même DA v2.

**Priorité :** Moyenne (accessibilité, conformité WCAG 2.1 AA)

**Condition de déblocage :** Audit ciblé des contrastes texte/fond sur les pages publiques avec un outil dédié (axe-core, Stark, Lighthouse Accessibility détaillé). Identification des composants concernés et recalibration de la palette DA v2 si nécessaire. La palette racine est gelée (variables `--ardoise`, `--pierre`, `--mica`, `--brume`, `--maquis`, `--ocre`, `--porphyre`, `--tyrrhenien`) mais les usages spécifiques par composant peuvent être ajustés sans toucher aux variables racines.

---

### MAIRIES-CLS-TBT-001 — Régressions CLS et TBT post-lazy load `pdfmake`

**Description :** Le sprint L (lazy load `pdfmake`, PR [#293](https://github.com/dellahstella/tellux/pull/293) + [#294](https://github.com/dellahstella/tellux/pull/294)) a introduit deux régressions Lighthouse mineures sur `mairies.html` : Cumulative Layout Shift (CLS) 0.131 → 0.186 et Total Blocking Time (TBT) 130 ms → 400 ms. Les deux métriques restent sous les seuils critiques (CLS < 0.25 = needs improvement, pas poor ; TBT < 600 ms acceptable) mais sont dégradées par rapport à l'état avant lazy load. Cause probable : le lazy load déclenche un layout shift au moment de l'injection dynamique du script et un blocage runtime au premier clic sur « Télécharger PDF ».

**Priorité :** Faible (à surveiller)

**Condition de déblocage :** Investigation des causes (réservation de hauteur fixe pour le bouton « Télécharger PDF » pendant la phase « Préparation du PDF… » pour éviter le shift, hydration de pdfmake en arrière-plan dès l'ouverture de l'onglet « Générer un courrier » au lieu d'attendre le clic). Patch correctif si une régression sensible est détectée par les utilisateurs ou si une remontée Lighthouse ultérieure aggrave la situation.

---

### MAIRIES-REDIRECTS-001 — Redirections multiples détectées par Lighthouse

**Description :** Lighthouse Performance signale `Avoid multiple page redirects | Est savings of 880 ms` sur `mairies.html` (audit du 1ᵉʳ mai 2026, sprint L, présent avant et après le sprint). Probablement liée à la redirection automatique HTTP→HTTPS, à la canonical Cloudflare ou à une redirection `mairies` → `mairies.html` (cf. preview Lighthouse sur `tellux.pages.dev/mairies` qui ressort en `tellux.pages.dev/mairies` final après redirect). Audit à conduire pour confirmer la chaîne exacte.

**Priorité :** Faible

**Condition de déblocage :** Audit DevTools Network avec « disable cache » sur `https://tellux.pages.dev/mairies.html` pour identifier la chaîne de redirections. Optimisation possible via le fichier `_redirects` Cloudflare Pages ou la configuration `wrangler.jsonc` si applicable. Vérification post-correction via Lighthouse Performance.

---

### CAPTEURS-WEB-API-001 — Mesure auto magnétomètre indisponible dans les navigateurs

**Description :** L'onglet « Capteurs appareil » du formulaire de contribution (`#ctab-cap` dans `app.html`) ne peut pas accéder au magnétomètre du téléphone via l'API web `Magnetometer` (Generic Sensor API). Chrome a retiré le flag `enable-generic-sensor-extra-classes` en M116 (août 2023) par mesure anti-fingerprinting, et `typeof Magnetometer === 'undefined'` retourne désormais `true` sur Chrome Android grand public, indépendamment du code Tellux. Aucune piste viable côté web (TWA, PWA, polyfill, autre navigateur Android grand public) n'a été identifiée — confirmé par recherche du 27 avril 2026. Lié à `CONTRIB-SCHEMA-001` (la chaîne `capCheckSupport` exige déjà le magnétomètre natif et refuse le fallback `DeviceOrientation`, qui n'expose que des angles non-EM ; voir audit du 27 avril 2026, 6 contributions polluées dépiautées).

**Impact :** L'onglet reste présent dans l'UI (architecture en place pour une future app native), mais il affiche un bandeau d'indisponibilité honnête expliquant la cause (politique navigateur Chrome) et la perspective (module phase 2 du projet). Le bouton « Démarrer l'enregistrement » est désactivé proprement via `capCheckSupport` (ligne 7012) et le style `.cap-btn-primary:disabled` existant. Wording UI corrigé par PR du 27 avril 2026 (commit `fix: honnêteté UI onglet capteurs appareil`). Renvoi vers l'onglet « Mesure technique » manuel pour les contributions Phyphox / Sensor Kinetics.

**Priorité :** Différée — phase 2 (post-financement). Pas un bug Tellux, pas de fix possible côté web.

**Condition de déblocage :** Développement d'une application Android native (Kotlin + bridges natifs + UI dédiée) ou wrapper Capacitor/Tauri avec plugin natif. Module à inscrire dans un dossier de candidature financement (FEDER) sous « infrastructure scientifique ». Estimation initiale : 4-6 semaines de développement. La couche logique JS de capture (`capStartLiveReadings`, `capStartRecording`, `capSubmitMeasurement`) reste fonctionnelle pour le jour où une app native injectera les valeurs nT mesurées dans la même structure de contribution.

---

### PATRIMOINE-TILES-ZOOM-001 — Fond carte CARTO disparu après zoom in (audit UX #2, non reproductible)

**Description :** Audit UX #2 (4 mai 2026) a observé visuellement la disparition du fond de carte CARTO sur `https://tellux.pages.dev/patrimoine` après zoom in déclenché par clic cluster (screenshot `ss_7327svjjr`). Tentative de reproduction Brief 7 sur le code dev/main actuel : tiles testées à tous les niveaux de zoom 9 à 19 (toutes chargent avec succès, `naturalWidth=512`, status HTTP 200), inspection panes (`tilePane` `opacity:1`, `visibility:visible`, `z-index:200`), test clic cluster (cluster « 11 » Sartène : zoom 9→11, 8 tiles chargées correctement). Hypothèses A (maxZoom dépassé), B (URL pattern), C (pane masque), D (overlay couvrant) toutes écartées. Configuration tile : `https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png`, `subdomains:'abcd'`, `maxZoom:19`, className `tlx-tiles` (filtre sépia). Identique en local et sur prod. Branche `fix/patrimoine-tiles-zoom` clôturée sans commit. Mise à jour 4 mai 2026 (Brief 8 révisé) : pivot patrimoine.html sur 11 doyennés contemporains avec fill plein opaque qui masque entièrement le fond de carte au niveau 1 ; le bug initial concernait spécifiquement le drill-down post-clic cluster, lui-même retiré dans le Brief 8 révisé (pas de zoom auto, pas de drill-down 2 niveaux). Les nouvelles couches doyennés peuvent toutefois interagir différemment avec le tilePane et re-déclencher le symptôme.

**Priorité :** Faible (à monitorer)

**Condition de déblocage :** Re-observer post-Brief 8 révisé (vision macro doyennés). Si re-observé en prod, rouvrir investigation avec : niveau de zoom exact, navigateur + OS + DPI, capture DevTools Network filtrée sur `cartocdn`, séquence d'actions précise.

---

### PATRIMOINE-ORPHANS-INVISIBLES-001 — Spots orphans non illustrés invisibles dans nav v1

**Statut actualisé 2026-05-06 (Brief 28/29) :** corpus passé de 124 → 191 sites Phase 1 (+67 nouveaux sites issus de la consolidation Cowork 4 sources). Sur les 191 sites P1, **~43 restent invisibles** post-migration : 51 sont sans `doyenne_contemporain_slug` (orphans intentionnels — diocèses abstraits, naturels transcommunaux, churches Phase 2 partiel, toponymes locaux) et l'intersection illustrés ∪ overrides ne les rapatrie pas tous. Le mécanisme d'override `_drafts/SPOT_DOYENNE_OVERRIDES.json` (Brief 17 Phase A) reste actif et la résorption progressive continue au fil des audits. La dette reste ouverte avec un nouveau périmètre 191 (vs 124).

**Statut antérieur 2026-05-05 (Brief 17 Phase A)** — mécanisme d'override actif via `_drafts/SPOT_DOYENNE_OVERRIDES.json`. Soleil peut rattacher manuellement chaque orphan à un doyenné (et optionnellement à une pieve) au fil des sessions, sans modifier le pipeline ni le mapping Cowork. Le runtime `patrimoine.html` charge le fichier au boot et applique les overrides : les markers correspondants apparaissent au drill-down niveau 2 du doyenné cible.

**Description :** Sur les 191 spots Phase 1 du corpus consolidé `sites_corse.json` (Brief 28), une partie reste invisible dans la navigation. Critères : 123 illustrés affichés au niveau 1 (whitelist `ILLUSTRATED_SPOTS` + champ `illustre=true`) ; 5 spots-diocèse (slug commençant par `diocese_`) exclus ; sites sans `doyenne_contemporain_slug` invisibles au niveau 2 (51 orphans intentionnels). L'intersection des trois critères laisse ~43 sites invisibles aujourd'hui (vs 18 avant Brief 28 — l'élargissement du corpus a temporairement augmenté le pool). Liste exacte loggée au boot via `console.log('[Tellux patrimoine] Spots non illustrés masqués: …')` (DevTools, pas user-facing). Note : la formulation pré-Brief 28 (124 spots, ~105 invisibles) est obsolète.

**Priorité :** Moyenne (mécanisme actif, remplissage progressif)

**Condition de déblocage :** Remplissage progressif de `_drafts/SPOT_DOYENNE_OVERRIDES.json` au fil des audits patrimoine (Soleil arbitre commune par commune). Levier complémentaire : génération d'illustrations Nano Banana pour rapatrier des spots dans `ILLUSTRATED_SPOTS` (visibilité niveau 1 directe). La résolution complète de la dette est définie comme : tous les ~105 spots sont soit illustrés, soit overridés, soit explicitement classés "non visibles intentionnellement".

---

### PATRIMOINE-PIEVES-39-VS-47-CASTA-001 — Périmètre pieves alignées sur 39 (vs 47 Casta canoniques)

**Statut : RÉSOLU 2026-05-05 (Brief 17 Phase B)** — Cowork a livré `_drafts/pieves_communes_mapping_v2_canonicite_casta.json` qui restaure les 8 pieves Casta absorbées (Casacconi, Tavagna, Filosorma, Mezzana, Luri, Celavo, Talcini, Aleria) via 39 transferts de communes depuis les pieves v1 vers les pieves v2 nouvellement créées. Le pipeline `scripts/build_pieves_polygons.py` détecte automatiquement le fichier v2 et l'applique en extension du v1. Sortie `docs/data/pieves_polygons.json` : passe de 39 à **47 pieves** (canonicité Casta complète). 3 cas ambigus de la livraison Cowork v2 (Pino → Luri, Galéria → Filosorma, Ghisonaccia → Aleria) sont appliqués par défaut selon les choix Cowork ; ajustables ultérieurement via `_drafts/PIEVE_OVERRIDES.json` si Soleil arbitre différemment.

**Description (historique) :** Le mapping pieves Cowork v1 livré le 4 mai 2026 couvrait 39 pieves alignées sur le manifest `PATRIMOINE_POLYGONS.pieves` du Brief 2. Cinq pieves Casta étaient implicitement absorbées dans des voisines (Casacconi, Tavagna, Filosorma, Mezzana, Cap-Corse-Luri) ; trois autres sans rattachement clair (Celavo, Talcini, Aleria). La livraison v2 du 5 mai 2026 restaure les 8 pieves manquantes, distinguant explicitement la canonicité médiévale Casta des regroupements contemporains.

---

### PATRIMOINE-CLICK-CONFLICTS-001 — Conflits zones de clic patrimoine.html niveau 1 et 2

**Description :** Au niveau 1, les miniatures doyennés (`L.divIcon` `iconSize:[120,96]`) chevauchent visuellement les polygones doyennés et certains markers spots, créant des clics ambigus selon la zone précise. Au niveau 2, le `bringToFront()` des doyennés voisins (Brief 10, ligne ~949 `enterNiveau2View`) clippe visuellement les pieves débordantes mais capte aussi les clics au-dessus de ces portions, masquant les pieves multi-doyennés. Les couches polygones legacy `dioceseLayer` et `pieveLayer` (lignes 558-559) sont construites depuis `PATRIMOINE_POLYGONS` inline mais jamais attachées au map post-Brief 8 — consommation mémoire pour rien (~22 kB JSON parsé, layers Leaflet créés mais dormants).

**Priorité :** Basse

**Condition de déblocage :** Audit UX dédié (mesure des taux de clics ambigus par zone), arbitrage entre rétention `bringToFront()` Brief 10 (clipping visuel) vs précédence pieves Brief 12 (clics multi-doyennés). Si retrait de `dioceseLayer`/`pieveLayer` legacy : suppression aussi de `PATRIMOINE_POLYGONS` inline ligne 270 (~22 kB) car plus aucun consommateur. Identifiée Brief 27 (2026-05-06).

---

### PATRIMOINE-LOAD-PERF-001 — Chargement séquentiel polygones + sites au boot

**Description :** Le boot patrimoine.html effectue désormais 3 fetches : `sites_corse.json` (~329 kB), `doyennes_polygons.json` (~183 kB), `pieves_polygons.json` (~585 kB). Brief 28 a chaîné les polygones après `sitesReady` (await dans les `.then()`) pour éviter le race sur `markersBySlug`, mais cela sérialise les 2 fetches polygones derrière le fetch sites — TTI augmenté inutilement. La construction synchrone de tous les polygones (10 doyennés + 47 pieves V2 + couches legacy `dioceseLayer`/`pieveLayer` dormantes) intervient au boot, alors que les pieves ne sont visuellement utiles qu'au premier drill-down (clic doyenné).

**Priorité :** Basse

**Condition de déblocage :** Audit Lighthouse Time-to-Interactive avant/après. Pistes : (1) parallélisation `Promise.all([loadSitesPatrimoine(), loadDoyennesPolygons(), loadPievesPolygons()])` puis init markers une fois sitesReady, (2) lazy-load `pieves_polygons.json` au premier drill-down vs eager au boot (économie ~585 kB upfront), (3) compression Brotli côté Cloudflare (déjà actif par défaut, à vérifier sur les `_headers`). Identifiée Brief 28 (2026-05-06).

---

### PATRIMOINE-BASTIA-PIEVES-SOUS-ATTRIBUEES — Doyenné de Bastia avec une seule pieve attribuée

**Description :** Le doyenné contemporain de Bastia (`doyenne_de_bastia`) ne contient qu'une seule pieve médiévale (Bastia, 1 commune fallback cercle 5 km) dans le mapping `pieves_communes_mapping_v2_canonicite_casta.json` Brief 17. Suspect au regard de la couverture territoriale réelle du doyenné (qui englobe le bassin bastiais + microrégions adjacentes). Probable sous-attribution lors du mapping Cowork v2 — d'autres pieves Casta (Mariana, Casinca, Nonza...) pourraient légitimement être incluses ou partiellement attribuées via ratios `doyennes_appartenance[]` (Brief 12 multi-appartenance pieves).

**Priorité :** Basse

**Condition de déblocage :** Mission Cowork ultérieure pour audit du mapping pieves → doyenné Bastia, croisement avec sources historiques (Casta, Doyenné contemporain Diocèse Ajaccio). Si confirmation sous-attribution : livraison `_drafts/PIEVE_DOYENNES_OVERRIDES.json` avec attributions multi-doyennés ajustées + ré-exécution `scripts/build_pieves_polygons.py`. Identifiée Brief 29 (2026-05-06).

---

### SITES-CORSE-HAMEAUX-CHURCHES-INSEE-001 — Hameaux Phase 2 churches sans INSEE résolu

**Description :** Sur les 288 sites Phase 2 latents (corpus `churches_corse` Moracchini-Mazel intégré par Brief 27), environ **17 sites de hameaux** n'ont pas de `commune_insee` résolu dans `sites_corse.json`. Le mapping commune Moracchini-Mazel utilise des toponymes locaux (Lieu-dit, Hameau, Cuvée) qui ne matchent pas le référentiel INSEE 5 chiffres. Ces sites sont actuellement absents de `pieve_slug`, `diocese_medieval_slug` et `doyenne_contemporain_slug`. Tant que la Phase 2 n'est pas ouverte au runtime patrimoine.html (filter `phase_publication === 1` actuel), pas d'impact UX immédiat. Mais bloquera l'ouverture Phase 2 future.

**Priorité :** Basse (Phase 2 latente)

**Condition de déblocage :** Override JSON `_drafts/CHURCHES_HAMEAUX_INSEE_OVERRIDES.json` à livrer avant ouverture Phase 2. Cowork ou audit manuel pour résoudre chaque hameau vers son INSEE de commune mère via croisement Moracchini-Mazel + IGN BDTopo + Wikipedia toponymes corses. Identifiée Brief 29 (2026-05-06).

---

### SITES-CORSE-TOPONYMES-LOCAUX-001 — Mégalithes Phase 1 au toponyme local sans INSEE

**Description :** Sur les 191 sites Phase 1 du corpus consolidé, environ **12 mégalithes** sont décrits par un toponyme local (Castaldu, Pacciunituli, Ciutulaghja, Manzavinu, etc.) sans `commune_insee` résolu. Le mapping nominal échoue car ces toponymes ne correspondent pas à des noms de communes INSEE (souvent des lieux-dits ou ravins archéologiques). Conséquence : ces 12 sites sont sans `doyenne_contemporain_slug` ni `pieve_slug`, donc invisibles au niveau 2 patrimoine.html (orphans). Comportement actuel cohérent (orphans intentionnels), mais résolution améliorerait la couverture niveau 2 de ~5%.

**Priorité :** Basse

**Condition de déblocage :** Croisement `lat/lon` × GeoJSON contours communes IGN (BDTopo ou OpenAddresses) → résolution point-in-polygon pour rattacher chaque toponyme local à sa commune INSEE mère. Livraison `_drafts/MEGALITHE_TOPONYME_INSEE_OVERRIDES.json`. Alternativement, override manuel par Soleil au fil des sessions via `_drafts/SPOT_DOYENNE_OVERRIDES.json`. Identifiée Brief 29 (2026-05-06).

---

### TOUR-AGNELLO-GPS-DISCORDANCE-001 — 3 coordonnées coexistantes pour Tour d'Agnello

**Description :** Lors de la consolidation Brief 27, le pipeline `consolidate_sites.py` a détecté que **3 coordonnées GPS coexistent** dans les sources d'origine pour la Tour d'Agnello (Cap Corse) : (a) `SITES_PATRIMOINE` inline `[42.x, 9.y]`, (b) `patrimoine_corse` Supabase `[42.x', 9.y']`, (c) `tours_genoises` autre référence `[42.x'', 9.y'']`. La fusion automatique a retenu la priorité de source (cf. matrice `AXIS_COMPAT` du pipeline) mais l'écart entre les 3 GPS dépasse le seuil de proximité 150 m (sites donc non fusionnés en doublon, 1 seul retenu). Risque : le site retenu n'est pas nécessairement le plus précis ; les 2 autres ont été éliminés sans audit terrain.

**Priorité :** Basse

**Condition de déblocage :** Audit GPS dédié pour Tour d'Agnello : (1) cross-check avec sources de référence externes (Wikipedia FR, Megalithic Portal, IGN GeoPortail), (2) éventuel relevé GPS terrain, (3) mise à jour `sites_corse.json` via `gps_audit` + ré-exécution pipeline avec coordonnée canonique unique, (4) documentation dans `gps_audit_changes` du `_meta`. Identifiée Brief 29 (2026-05-06).

---

### ILLUSTRATED-WHITELIST-DRIFT-001 — Risque de désynchro `ILLUSTRATED_SPOTS` vs visuels effectifs

**Description :** La constante `ILLUSTRATED_SPOTS` (Set hardcodé dans `patrimoine.html`) liste les slugs dont les markers doivent apparaître en N1 macro-vue. Toute évolution de corpus (ajout/retrait de visuels) doit être manuellement synchronisée avec ce Set, sinon dérive entre HTML et data. Évolution chronologique :
- Brief Phase B 2026-05-11 : retrait 2 slugs invalides → whitelist 14 → 12
- Sprint curation N1 2026-05-11 : Item 6 ajout 12 nouveaux → whitelist 12 → 24
- **Sprint micro-data 2026-05-12 : promotion 9 slugs orphelins → whitelist 24 → 33**

Drift sous-jacent au 12 mai 2026 : `sites_patrimoine.json` contient ~100 sites avec `illustre: true` mais seuls 33 sont en N1 (curation éditoriale manuelle). 66 sites Phase 1 + `illustre=true` + visuel physique présent mais hors whitelist (Croisement B audit 2026-05-12). Pas d'auto-detection de la dérive.

**Priorité :** Basse.

**Condition de déblocage :** (a) Soit dériver `ILLUSTRATED_SPOTS` à la volée depuis `sites_patrimoine.json` (champ `illustre: true` + audit `priorite`), (b) soit ajouter un script de check CI qui valide la cohérence entre le Set et la liste effective des visuels. Identifiée Phase A Cowork (2026-05-11) symptôme S5. **Statut sprint micro-data 2026-05-12 : whitelist 12→24→33, drift 100→33 toujours ouvert mais sous contrôle éditorial (tri par batches postérieurs planifiés).**

---

### PIPELINE-DRIFT-SITES-PATRIMOINE-001 — REFORMULÉE → voir `CONSOLIDATE-SITES-PY-OBSOLETE-001`

**Statut au 12 mai 2026 (Sprint A pipeline réparation) :** dette **mal nommée**, reformulée et fermée.

Investigation STOP A du Sprint A a révélé que le « drift `sites_corse.json` → `sites_patrimoine.json` » n'est PAS un drift à corriger :

- `sites_corse.json` est **DEPRECATED** (header `_DEPRECATED` depuis Brief 33 split 2026-05-06, target suppression 2026-06-05). Il N'est PAS la source canon runtime.
- `sites_patrimoine.json` **EST la source canon runtime** depuis Brief 33 split. Édité directement via `scripts/brief_pipeline.py` ou briefs ciblés.
- Les 14 « réintégrations manuelles » des sprints curation N1 + micro-data étaient en réalité l'**application correcte** du canonical actuel — pas des patches contre un pipeline cassé.

La vraie dette résiduelle est : **`scripts/consolidate_sites.py` est obsolète et inexécutable** (paths sandbox + sources Supabase non versionnées). Cf. nouvelle dette `CONSOLIDATE-SITES-PY-OBSOLETE-001` ci-dessous.

**Action 2026-05-12 :** dépréciation explicite de `consolidate_sites.py` (commit `7565563`, docstring de tête + `sys.exit(2)` au boot, code historique conservé pour référence).

**Statut :** **FERMÉE — REFORMULÉE** comme `CONSOLIDATE-SITES-PY-OBSOLETE-001`.

---

### CONSOLIDATE-SITES-PY-OBSOLETE-001 — Script pipeline obsolète à supprimer ou réécrire

**Constat (12 mai 2026, Sprint A pipeline réparation) :**

`scripts/consolidate_sites.py` est obsolète :
- **Paths hardcodés sandbox** (`/sessions/busy-awesome-mayer/mnt/Tellux/...`, `/sessions/busy-awesome-mayer/mnt/outputs/...`) non applicables en local
- **Sources d'entrée non versionnées** dans le repo public : `outputs/churches_dump.json`, `outputs/patrimoine_dump.json` (Supabase dumps externes)
- **Sortie `_drafts/sites_corse_v1.json`** jamais consommée en runtime — le pipeline conçu pour reconstruire `sites_corse.json` (lui-même deprecated)
- **Pipeline conceptuellement remplacé** par l'architecture Brief 33 split : `sites_patrimoine.json` édité directement via briefs ciblés, `sites_em.json` synchronisé via `sync_cross_app.py`

**Action en cours (sprint A) :** déprécié explicitement (commit `7565563`) avec :
- Docstring de tête détaillé documentant l'architecture data actuelle
- Bloc `if __name__ == '__main__': sys.exit(2)` au boot avec message d'erreur
- Code historique conservé pour référence

**Priorité :** Basse. Le script ne nuit plus (exit immédiat si exécuté). Pas de bénéfice immédiat à le supprimer.

**Condition de déblocage (si on veut nettoyer définitivement) :** Vérifier qu'aucun workflow CI/CD ou doc externe ne référence le script, puis supprimer + retirer les références dans `DETTES_TECHNIQUES.md`. Pas urgent.

**Statut :** OUVERT (basse priorité, sera nettoyé avec la suppression de `sites_corse.json` target 2026-06-05).

---

### PIPELINE-DATA-ARCHITECTURE-DOC-001 — Documentation architecture data manquante

**Constat (12 mai 2026, Sprint A) :**

L'architecture data Tellux post-Brief 33 split (2026-05-06+) n'est documentée nulle part de manière centralisée. Les agents (humain et Code) doivent reconstruire le diagnostic à chaque sprint touchant aux fichiers data. Cf. STOP A du Sprint A pipeline réparation : initial diagnostic erroné « sites_corse.json canonical » alors que `sites_patrimoine.json` est la vraie source canon.

**Architecture data réelle à documenter quelque part :**

- **`docs/data/sites_patrimoine.json`** : SOURCE CANON runtime pour `patrimoine.html`. Édité directement via :
  - Briefs ciblés Soleil (corrections GPS, ajouts/retraits sites)
  - `scripts/brief_pipeline.py` (patches automatiques depuis brief markdown)
- **`docs/data/sites_em.json`** : dérivé EM consommé par `app.html` layer `sitesRemarq`. Synchronisé depuis Patrimoine via :
  - `scripts/sync_cross_app.py --apply` (propage lat/lon/gps_*/commune_nom/doyenne_contemporain_slug/pieve_slug)
- **`docs/data/sites_corse.json`** : **DEPRECATED** (header `_DEPRECATED` Brief 33 split, target suppression 2026-06-05). Ne plus consulter ni modifier.
- **`scripts/consolidate_sites.py`** : OBSOLÈTE (cf. `CONSOLIDATE-SITES-PY-OBSOLETE-001`). Ne pas exécuter.
- **`scripts/brief_pipeline.py`** : ACTIF, paths relatifs OK.
- **`scripts/sync_cross_app.py`** : ACTIF, paths relatifs OK, fonctionne en local.

**Action requise :**

- (a) Soit créer un fichier dédié `docs/PIPELINE_DATA_ARCHITECTURE.md` (option propre, documentation séparée des dettes)
- (b) Soit enrichir le préambule de `DETTES_TECHNIQUES.md` avec un encadré architecture
- (c) Soit enrichir `CLAUDE.md` local pour Code (audience principale du diagnostic récurrent)

**Priorité :** Moyenne. Bénéfice : éviter de re-diagnostiquer l'architecture à chaque sprint touchant aux data.

**Statut :** OUVERT.

---

### MONTE-GENOVA-NATURAL-VISUEL-001 — Visuel "sans mégalithes" requis pour monte_genova

**Description :** Sprint curation N1 (Item 2 du brief) demandait de pointer le champ `visuel` de `monte_genova` vers une variante "sans mégalithes" (image naturelle du Monte Genova sans le contenu archéologique). Audit filesystem : seul `monte_genova_tellux_v2.png` (+ 3 dérivés `_full.webp`, `_medium.webp`, `_thumb.webp`) existe dans `docs/assets/visuels/`. Aucune variante candidate (`_naturel_`, `_sans_megalithes`, etc.) trouvée.

**Priorité :** Basse (cosmétique, visuel actuel reste valide).

**Condition de déblocage :** Soleil produit le visuel "naturel sans mégalithes" via workflow DA v2 dans une session séparée, puis micro-PR data pour wirer le nouveau fichier dans le champ `visuel` de l'entrée `monte_genova` de `sites_corse.json` + propagation pipeline vers `sites_patrimoine.json`. Identifiée sprint curation N1 (2026-05-11), Item 2 skip après STOP A.

**Statut :** OUVERT.

---

### PIPELINE-DRIFT-SITES-EM-CORSE-001 — Drift `sites_em.json` vs `sites_corse.json` — RÉSOLUE

**Statut au 12 mai 2026 (Sprint A pipeline réparation) :** **FERMÉE**.

**Diagnostic révisé après Sprint A STOP A :** Le drift constaté avait deux composantes :
1. Drift `sites_em.json` vs `sites_corse.json` : non pertinent car `sites_corse.json` est DEPRECATED (cf. doctrine Brief 33 split). Pas un drift à corriger.
2. Drift `sites_em.json` vs `sites_patrimoine.json` (vrai canonical runtime) : **28 divergences** détectées par `scripts/sync_cross_app.py --dry-run` 2026-05-12.

**Résolution 2026-05-12 (commit `26fb064`) :**
- Exécution `scripts/sync_cross_app.py --apply` (outil déjà fonctionnel localement)
- 28 divergences propagées Patrimoine (source canon) → EM
- Champs propagés : lat, lon, gps_locked, gps_lock_reason, gps_audit, gps_source, commune_nom, doyenne_contemporain_slug, pieve_slug
- Backup automatique : `_drafts/sites_em.backup_sync_cross_app_2026-05-12.json`
- Vérification post-apply : `python3 scripts/sync_cross_app.py --dry-run` retourne **0 divergence**

**Note de régression apparente :** `reserve_de_scandola` voyait sa coord em `(42.36072, 8.56127)` (alignée sprint app-ui-polish sur l'ancien `sites_corse.json` deprecated) écrasée par patrim `(42.3589, 8.5615)`. Drift de 200m vers le sud — toujours sur la péninsule UNESCO. Si réalignement souhaité, brief data dédié pour modifier patrimoine.json (le canonical) puis re-sync.

**Sites SKIP du sprint app-ui-polish toujours à re-sourcer** (hors scope de cette dette, à traiter dans un brief séparé) :
- `barrage_padula` : coord (42.62806, 9.32278) probablement erronée (Saint-Florent au lieu de Fium'Orbu sud-est)
- `min_argentella` : (42.225, 8.573) à confirmer côte ouest Calenzana/Crovani

**Statut :** **FERMÉE**.

---

### PIEVE-STATUES-MENHIRS-CLEANUP-FINAL-001 — Retrait final pieve_statues_menhirs prod — RÉSOLUE

**Constat (13 mai 2026)** : malgré l'archivage supposé Sprint U1, le slug `pieve_statues_menhirs` était encore dans `sites_patrimoine.json` + `sites_corse.json` en prod, avec 4 fichiers visuels actifs dans `docs/assets/visuels/`. Le slug n'a jamais représenté un site réel (résidu d'exploration toponymique abandonnée).

**Cause probable** : pipeline `consolidate_sites.py` (réparé Sprint A) non re-run après l'archivage Sprint U1, OU archivage Sprint U1 incomplet (ne couvrait que la whitelist HTML, pas les JSON ni les visuels filesystem).

**Action 13 mai 2026 (commit `73cfeb3`)** : retrait complet :
- 4 visuels archivés via `git mv` vers `_drafts/visuels_archive/` (rename 100%, historique préservé : `_tellux_v2.png` + 3 webp dérivés)
- Entrée canonical `sites_corse.json` supprimée (479 → 478 sites)
- Entrée publié `sites_patrimoine.json` supprimée (466 → 465 sites)
- Whitelist `ILLUSTRATED_SPOTS` HTML : pieve_statues_menhirs déjà absent (jamais promu N1), no-op

**Intouché** : références `spot_ids` dans `PATRIMOINE_POLYGONS` const `patrimoine.html` (L420) — préservées pour nomenclature pievale historique (Nebbiu / nebbiu). Au runtime, le rendu se base sur `sites_patrimoine.json` async, pas sur ces métadonnées.

**Statut** : **RÉSOLUE**.

---

### DESERT-DES-AGRIATE-DISAPPEAR-N2-001 — desert_des_agriate disparaît en N2 drill-down — RÉSOLUE

**Constat (13 mai 2026, audit Soleil whitelist refonte)** : `desert_des_agriate` apparaît correctement en N1 (whitelist `ILLUSTRATED_SPOTS`) mais disparaît lors du drill-down N2 du doyenné qui le contient.

**Cause racine identifiée (Sprint K 13 mai 2026)** : hypothèse (b) confirmée — `doyenne_contemporain_slug` était `null` côté JSON canonical + publié, donc absent du `SPOT_TO_DOYENNE` map runtime, donc non ajouté à `spotsLevel2ByDoyenne` LayerGroup N2. Le filtre N2 strict ne fait pas de fallback point-in-polygon runtime (cf Brief 28/33 split, mapping pré-calculé Cowork).

**Résolution (Sprint K commit `9422dc3`)** : rattachement programmatique via point-in-polygon des 48 orphelins Phase 1. `desert_des_agriate` (42.68, 9.10) → unique match `doyenne_du_golo` → `doyenne_contemporain_slug` rempli dans les 2 JSON. Désormais visible en drill-down doyenne_du_golo.

**Effet collateral positif** : 47 autres sites Phase 1 dans la même situation rattachés en même temps (aiguilles_de_bavella, vizzavona, gorges_du_tavignano, etc.). Volumétrie sites Phase 1 sans doyenne_contemporain_slug : 48 → ~0.

**Statut** : **RÉSOLUE**.

---

### SITES-GEOPHYS-TOOLTIP-OVERFLOW-001 — Tooltip sr-icon débordait viewport — RÉSOLUE

**Constat (13 mai 2026, diagnostic Soleil live)** : la couche "sites géophysiques remarquables" de `app.html` utilise `bindTooltip` (non `bindPopup`) avec classe `tellux-sr-tooltip` sur 48 markers `sr-icon`. Au clic sur un marker en bord de carte (ex. `Anneaux du Cap Corse` lat 43.17 en haut), le tooltip s'affichait à `y=-203` (totalement hors viewport top). Tooltip étroit (~120px) et long (~350px) en format colonne sur certains viewports, sans bouton close ni autopan.

**Origine** : fix Sprint app-ui-polish ne couvrait que `delta-popup` (calc Tellux), pas les tooltips géophys. Le diagnostic Code de l'époque ("sr-icon utilise bindTooltip, pas bindPopup → pas de popup à refactorer") était techniquement vrai mais incomplet.

**Résolution (Sprint flash 13 mai 2026, commit `11981cd`)** : Option A retenue (fix minimal CSS + autopan listener) :
- CSS `.tellux-sr-tooltip` enrichi : `max-height: 60vh; overflow-y: auto;` (en plus du `max-width: 300px; white-space: normal` déjà présents). Empêche tooltip très long de déborder verticalement.
- JS listener `tooltipopen` ajouté sur chaque sr-icon marker : `setTimeout 50ms` puis `getBoundingClientRect`, si `r.y < 80` → `map.panBy([0, r.y - 80])` (pan vers le sud), si `r.bottom > viewport-20` → pan vers le nord. Mimique autoPanPadding de Leaflet bindPopup.

**Effet** : tous les markers sr-icon désormais lisibles quelle que soit leur position viewport, y compris bord nord (Anneaux Cap), bord sud (Bonifacio), bord ouest/est. Pas de régression sur autres couches (delta-popup, postes, points chauds, etc.).

**Statut** : **RÉSOLUE**.

---

### PONT-ZIPPITOLI-DISPARU-DESCRIPTION-001 — Pont de Zippitoli disparu 2023, description marker à enrichir

**Constat (13 mai 2026, Sprint K)** : le site `pont_de_zippitoli_disparu_2023` (commune Zigliara, vallée du Taravo, doyenne_prunelli_taravo_valinco) est un pont génois disparu en 2023 (crue ou démolition probable selon le slug). Rattaché doyenne_prunelli_taravo_valinco via point-in-polygon Sprint K, mais sa description marker actuelle ne mentionne pas le statut "disparu".

**Action requise** : au prochain pass éditorial sur les descriptions patrimoine, enrichir la description avec :
- Statut "disparu en 2023"
- Contexte historique (pont génois, vallée du Taravo)
- Éventuelle source / photo d'archive si disponible

**Priorité** : 3 (basse). Pas bloquant, donnée géolocalisée valable comme repère historique.

**Statut** : OUVERT.

---

### VISUELS-A-REGENERER-FILITOSA-TOLLA-LOZARI-001 — 3 visuels patrimoine à régénérer en session DA v2

**Constat (13 mai 2026, audit Soleil post-Sprint U3) :** 3 visuels patrimoine identifiés par Soleil comme à régénérer dans une session DA v2 future :

- `filitosa` : cadrage à reprendre
- `lac_de_tolla` : statues géantes en arrière-plan WTF
- `casteddu_lozari` : hyperréaliste, hors DA v2

**Statu quo prod :** visuels actuels conservés visibles en N1 illustré (restent dans `ILLUSTRATED_SPOTS` whitelist). Pas de retrait temporaire whitelist. Régénération à planifier dans un sprint Soleil production externe ultérieur.

**Priorité :** 2 (moyenne). Pas bloquant Phase 1, esthétique seulement.

**Statut :** OUVERT.

---

### VISUEL-EXT-COSMETIC-001 — Champ `visuel` sans extension `.png`

**Constat (11 mai 2026, audit Code sprint complément) :**
105 sites dans `sites_patrimoine.json` + 123 sites dans `sites_corse.json` ont un champ `visuel` qui ne se termine pas par `.png`. Le runtime (`_illustrationUrl`) strip `.png` puis append `_medium.webp` — **l'extension n'a aucun impact sur le rendu**. Pattern cosmétique data, pas un bug.

**Priorité :** basse. À normaliser via pipeline `consolidate_sites.py` quand celui-ci sera réparé (cf. `PIPELINE-DRIFT-SITES-PATRIMOINE-001`). Pas d'action ad hoc.

**Statut :** OUVERT, non bloquant.

---

### WHITELIST-ILLUSTRE-FLAG-DRIFT-001 — Incohérence `illustre` côté JSON vs whitelist HTML — RÉSOLUE

**Constat (12 mai 2026, quick-check post-Sprints A/B/C) :**
12 slugs présents dans `ILLUSTRATED_SPOTS` (whitelist HTML `patrimoine.html`) avaient `illustre: false` côté JSON `sites_patrimoine.json` + champs `visuel` tronqués (sans `.png`) ou `null`. Côté `sites_corse.json` (canonical-deprecated) : `illustre: true` OK mais `visuel` sans extension `.png` (cosmétique).

Slugs concernés : `aiguilles_de_bavella`, `barrage_alesani`, `barrage_de_calacuccia`, `barrage_du_rizzanese`, `barrage_padula`, `cap_corse_extreme_nord`, `desert_des_agriate`, `lac_de_creno`, `lac_de_nino`, `monte_cinto`, `monte_san_petrone`, `monte_stello`.

**Impact runtime : nul.** N'affectait pas le rendu (whitelist HTML précède la data, et `_illustrationUrl` strip toujours `.png` puis append `_<size>.webp` — extension cosmétique sans impact rendu, cf dette `VISUEL-EXT-COSMETIC-001`).

**Origine probable :** sprints curation N1 + orphans ont promu en whitelist HTML sans propager le flag côté JSON. Drift accumulé.

**Résolution (12 mai 2026, commit `48e3556`) :** 12 slugs corrigés dans les 2 fichiers via script Python idempotent (`illustre: true` + `visuel` complet avec `.png`). Mapping résolu via audit filesystem (95× `_tellux_v2.png` convention principale + 4× `_v1.png` fallback). Pipeline `consolidate_sites.py` NOT run (déprécié Sprint A), édit manuel cohérent.

**Action préventive proposée :** pipeline ou check CI qui valide la cohérence whitelist HTML ↔ flag JSON. Si un slug est dans `ILLUSTRATED_SPOTS`, il doit avoir `illustre: true` côté data. Lien avec `ILLUSTRATED-WHITELIST-DRIFT-001` (drift global 100→33 sous contrôle éditorial).

**Statut :** **RÉSOLUE**.

---

### SAN-ANDREA-PIEDICROCE-SOURCE-INTROUVABLE-001 — Visuels orphelins archivés faute de source — RÉSOLUE

**Constat (12 mai 2026, Sprint B Item 2) :**
Le slug `san_andrea_de_piedicroce` avait 4 visuels physiques présents dans `docs/assets/visuels/` (`_tellux_v2.png`, `_full.webp`, `_medium.webp`, `_thumb.webp`) mais absent de `sites_corse.json` ET `sites_patrimoine.json`. Présumé église romane Castagniccia. Brief Sprint B Item 2 a tenté la réintégration au canonical avec recherche web.

**Recherche web exhaustive 12 mai 2026 sur 6+ sources fiables :**
- `corse-romane.eu` (référence patrimoine roman corse, 204 chapelles cataloguées) : page `piedicroce-andrea-y/` retourne **404**, homepage ne liste pas Piedicroce
- `visit-corsica.com`, `castagniccia.fr`, `corseweb.corsica`, `pozzodiborgo.com` : aucune mention d'une chapelle Sant'Andrea à Piedicroce
- Wikipedia FR : pas d'article spécifique

**Constats :**
- L'église principale de Piedicroce est **baroque XVIIᵉ siècle** (1684-1696, plus vieil orgue de Corse 1619), pas romane
- Sant'Andrea en Corse = autres communes (Biguglia, Castellare di Casinca, Cotone, Orcino, Bozio, Granaggiolo, Loreto-di-Casinca) **mais pas Piedicroce**

**3 hypothèses, arbitrage Soleil :**
- (α) Source privée Cowork non accessible : **écartée**
- (β) Visuel mal nommé (église baroque renommée erronément Sant'Andrea) : **écartée**
- (γ) Erreur / exploration abandonnée Cowork : **RETENUE**

**Résolution (commit `866cf86`) :** archivage des 4 fichiers visuels via `git mv` vers `_drafts/visuels_archive/` (historique git préservé via rename 100%). Pas de suppression — traçabilité conservée pour le travail Cowork. Si une source apparaît un jour, restauration possible.

**Statut :** **RÉSOLUE** par archivage.

---

### ALERIA-RUINE-FICHE-V3-KEY-MISMATCH-001 — `fiche_v3_slug` invalide dans `aleria_antique` — RÉSOLUE

**Statut au 12 mai 2026 (Sprint B Item 1) :** **RÉSOLUE** par alignement clé.

Le site `aleria_antique` avait `fiche_v3_slug: "aleria_ruine"` dans `sites_patrimoine.json` mais la clé réelle dans `fiches_patrimoine.json` est `aleria_antique`. Le lookup `fiches[site.fiche_v3_slug]` retournait null, le fallback `site.slug` masquait le bug (carte postale s'affichait par accident).

**Fix appliqué (commit `db4074a`)** : option (a) — aligner `fiche_v3_slug` sur la clé réelle.
- `sites_patrimoine.json` : `'aleria_ruine'` → `'aleria_antique'`
- `sites_corse.json` : `None` → `'aleria_antique'` (propagation cohérence canonical, le champ existait mais était null)

Clé `aleria_antique` dans `fiches_patrimoine.json` inchangée (1 fiche restante post sprint Phase B). Le lookup direct fonctionne maintenant, plus de fallback masqué.

---

### PATRIMOINE-DOYENNE-MARKER-MISMATCH-001 — 2 sites Phase 1 illustrés rattachés à un doyenné qui ne contient pas leur coord — RÉSOLUE

**Constat (12 mai 2026, Sprint U2 audit transcommunaux) :**
2 sites Phase 1 illustrés s'affichaient en N2 dans un doyenné cible mais leur coord GPS tombait dans un autre doyenné polygon. Effet UX confusant : l'utilisateur drillait dans doyenné X, voyait le marker Y, mais Y appartenait éditorialement à doyenné Z.

| Slug | Coord initiale | Doyenné naturel (PIP) | Doyenné cible (éditorial) |
|---|---|---|---|
| `plateau_du_coscione` | (41.88, 9.07) | prunelli_taravo_valinco | doyenne_extreme_sud |
| `foret_de_tartagine` | (42.46, 8.985) | cortenais | doyenne_balagne |

**Origine :** Le mapping `SPOT_TO_DOYENNE` utilise le champ pré-calculé `doyenne_contemporain_slug` (Brief 28 / Brief 33 split), pas un point-in-polygon runtime. Le décalage entre coord et doyenné cible était invisible à l'œil mais incohérent géographiquement. Pour `plateau_du_coscione`, le champ JSON était `null` + override compensatoire dans `_drafts/SPOT_DOYENNE_OVERRIDES.json`. Pour `foret_de_tartagine`, le champ JSON pointait sur balagne mais la coord tombait dans cortenais polygon.

**Résolution (12 mai 2026, commit `d2cac55` branche `fix/patrimoine-doyenne-marker-placement-2026-05-12`) :** option (a) Soleil — repositionner les markers vers des coords qui tombent dans le doyenné cible polygon, sans inventer une localisation arbitraire (vérification point-in-polygon programmatique + plausibilité géographique).

- `plateau_du_coscione` : (41.88, 9.07) → (41.83, 9.10) zone Quenza/Coscione sud, ~6 km au sud (plateau s'étend jusqu'à Aullène 41.79). `doyenne_contemporain_slug` null → `doyenne_extreme_sud`. `pieve_slug` null → `pieve_tallano` (pieve naturelle PIP). Override `SPOT_DOYENNE_OVERRIDES.json` retiré (redondant).
- `foret_de_tartagine` : (42.46, 8.985) → (42.475, 8.96) zone Mausoléo/Vallica, ~1.5 km nord-ouest. `doyenne_contemporain_slug` `doyenne_balagne` inchangé, `pieve_slug` `pieve_balagne` inchangé.

**Statut :** **RÉSOLUE** par repositionnement data cohérent.

---

### DOYENNE-EDITORIAL-MISMATCH-RENOSO-DORO-001 — Renoso + Oro initialement ciblés Golo (erreur éditoriale) — RÉSOLUE

**Constat (12 mai 2026, Sprint U2 STOP B audit transcommunaux) :**
`monte_renoso` (sommet 2352 m, commune réelle Ghisoni) et `monte_d_oro` (sommet 2389 m, commune réelle Vivario) avaient `doyenne_contemporain_slug = doyenne_du_golo` dans `sites_corse.json` + `sites_patrimoine.json`. Géographiquement insoluble : le doyenné du Golo couvre le bassin versant du fleuve Golo (nord-est Corse, Cinto, Niolu, Castagniccia–Bastia, bbox lat 42.34–42.74) ; les sommets Renoso (lat 42.06) et d'Oro (lat 42.14) sont sur d'autres bassins versants centraux. Aucun point géographiquement crédible sur ces massifs ne tombe dans golo polygon (écart 22–30 km).

**Origine :** Erreur de classification éditoriale initiale Cowork — probable confusion zone Golo-fleuve vs zone Golo-sommet ou ciblage par défaut sur un doyenné nord. Le champ `commune_nom = "Monte"` pour ces 2 sites est aussi probablement erroné (Monte est une commune Casinca lat ~42.65), à corriger dans un sprint commune-INSEE séparé (hors scope U2).

**Arbitrage Soleil (12 mai 2026) :** option (iii) — re-cibling formel selon bassin versant réel, garder coord. Évite (i) coord arbitraire dans Golo (visuellement absurde, sommet 2000+m projeté sur plaine) et (ii) override informel laissé dormant.

**Résolution (12 mai 2026, commit `d2cac55` branche `fix/patrimoine-doyenne-marker-placement-2026-05-12`) :**
- `monte_renoso` : `doyenne_du_golo` → `doyenne_plaine_orientale` (bassin Fium'Orbu, commune Ghisoni). `pieve_slug` `pieve_casacconi` → `pieve_ghisoni` (pieve naturelle PIP). Coord (42.06, 9.13) inchangée.
- `monte_d_oro` : `doyenne_du_golo` → `doyenne_cortenais` (bassin Tavignano, commune Vivario). `pieve_slug` `pieve_casacconi` → `pieve_vivario` (pieve naturelle PIP). Coord (42.14, 9.10) inchangée.

**Statut :** **RÉSOLUE** par re-cibling éditorial. Cohérence rattachement bassin versant restaurée.

---

### OPS-WORKTREE-CREATION-001 — Worktrees parasites créés par agents Claude Code

**État au 11 mai 2026 :**
- 14 worktrees actifs dans `.claude/worktrees/` (toutes directories présentes physiquement sur disque, non-prunable).
- 12 branches pointées indépendamment + 2 detached HEADs reachable.
- 2 branches orphelines sans commit propre vs dev :
  - `fix/spot-illustres-disparu` (HEAD 69bb6bb, antérieur PR #420) — vide, pointée par worktree `distracted-cohen-9850e9`.
  - `fix/patrimoine-audit-phase-b` initial (HEAD 4621a1a) — vide, créée par tentative Cowork puis abandonnée suite blocage FUSE.
- 9 branches `claude/*` créées automatiquement par agents Claude Code en mode worktree-isolation (pointent toutes vers `f1ce4d2`/`2789698`/`18f371e` — commits anciens). Aucun travail unique.

**Doctrine projet :** « jamais worktree » (PROJECT_INSTRUCTIONS_v3). Violation systématique par Claude Code en mode agentic. Cause racine probable : flag `worktree-isolation` actif par défaut dans la CLI Code.

**Audit détaillé sprint dettes post-Phase-B (11 mai 2026) :**

7 branches `claude/*` recensées (vs 9 estimées initialement) — vérification `git log origin/dev..claude/<branche> --oneline` :

| Branche | HEAD | Commits ahead dev | Statut audit |
|---|---|---|---|
| `claude/bold-cannon-75df9e` | `f1ce4d2` | 0 | Vide, safe delete |
| `claude/dreamy-bose-c3e3ee` | `f1ce4d2` | 0 | Vide, safe delete |
| `claude/hopeful-almeida-0f3f86` | `f1ce4d2` | 0 | Vide, safe delete |
| `claude/hungry-austin-0b60a4` | `2789698` | 0 | Vide, safe delete (mais worktree associée = CWD agent courant) |
| `claude/musing-herschel-2603b1` | `f1ce4d2` | 0 | Vide, safe delete |
| `claude/pensive-murdock-652a9a` | `18f371e` | 0 | Vide, safe delete |
| `claude/brave-poincare-28cbc7` | `fd5f309` | **2** | ⚠️ À ARBITRER — 2 commits uniques |

**Anomalie `claude/brave-poincare-28cbc7`** — 2 commits uniques détectés :

```
fd5f309 fix(patrimoine): corriger race condition markers non cliquables après N1→N2→N1
df717c2 fix(mobile): déplacer bouton accordéon mob-toggle de left vers right
```

Le commit `fd5f309` est très probablement une **tentative antérieure du symptôme S1 Phase A** (résolu sprint 2026-05-11 commit `5f1b480` solution A symétrique enter/exit, cf. ci-dessous `N2-ILLUSTRATED-SHARED-MARKER-001` fermée récemment). Diff vs `origin/dev` massif (suppressions visuels webp + .gitignore + ROADMAP + app.html -88 lignes) car branche basée sur état du repo très ancien. À supprimer dès validation prod du fix `5f1b480`, OU à conserver archivage pour comparaison historique. Arbitrage Soleil requis.

**Branches orphelines hors `claude/*`** identifiées au STOP 1 sprint Phase B, toujours présentes (non nettoyées) :
- `fix/spot-illustres-disparu` (HEAD `69bb6bb`, 0 ahead dev) — worktree `distracted-cohen-9850e9`
- `fix/patrimoine-audit-phase-b` initial (HEAD `4621a1a`, 0 ahead dev) — pointée par worktree racine `C:/Users/lucas/Documents/Claude/Projects/Tellux` (ne peut PAS être `worktree remove`, nécessite checkout dev d'abord)

**Action requise :**
- Arbitrage Soleil sur réglage CLI Code pour désactiver worktree-isolation. → **Résolu par investigation** (cf. ci-dessous + sous-ticket `OPS-CODE-WORKTREE-ISOLATION-FLAG-001`).
- Brief ops séparé pour nettoyage : `git worktree remove` explicite sur les 14 worktrees, puis `git branch -D` sur les 11 branches orphelines après audit individuel. → **Partiellement traité** sprint dettes 2026-05-11 (7 worktrees + 6 branches supprimés, cf. ci-dessous post-sprint cleanup section).
- À traiter avant prochain sprint Code pour éviter récidive.

**Investigation cause racine (sprint dettes 2026-05-11) :**

Via agent `claude-code-guide` cross-référé avec docs officielles Anthropic (https://code.claude.com/docs/en/desktop.md section "Work in parallel with sessions") :

> "For Git repositories, each session gets its own isolated copy of your project using Git worktrees, so changes in one session don't affect other sessions until you commit them."

**Diagnostic :** la création automatique de worktrees `.claude/worktrees/<random-name>/` à chaque session est une **propriété intrinsèque hardcodée du desktop app Claude Code**. PAS un flag configurable. Aucun moyen de la désactiver côté desktop.

**Cleavage CLI vs desktop :**
- **CLI Claude Code** (`claude`, `claude --continue`) : pas de worktree automatique. N'en crée que si argument explicite `--worktree` passé.
- **Desktop app Claude Code** : chaque session = 1 worktree dédié, automatique, non-désactivable.

**Setting `worktree.baseRef`** (le seul existant) : dans `.claude/settings.json` ou `settings.local.json`, contrôle UNIQUEMENT la ref de base depuis laquelle le worktree branche (`"fresh"` default = `origin/<default-branch>`, `"head"` = HEAD local). Ne contrôle PAS la création elle-même.

**Doctrine Anthropic vs Tellux :**
- **Anthropic :** worktrees recommandés pour sessions parallèles (design pattern).
- **Tellux PROJECT_INSTRUCTIONS :** « jamais worktree ».
- **Incompatibilité irréconciliable** côté desktop app.

**Remediation :**
1. Migrer à 100% sur **CLI Claude Code** pour ce projet (`claude` / `claude --continue` depuis le repo principal).
2. Prohiber l'usage du desktop app sur ce repo (cf. CLAUDE.md à enrichir).
3. Optionnel : ajouter `.claude/settings.json` avec `"worktree.baseRef": "head"` pour limiter le drift si desktop app utilisé en dépannage.

**Priorité :** Moyenne (non bloquant Phase B, mais pollution disque + traçabilité git dégradée). Réduite par investigation : le comportement est documenté/connu, la remediation est connue.

**Condition de déblocage :** Arbitrage Soleil sur flag `worktree-isolation` + brief ops cleanup. Identifiée Phase B sprint (2026-05-11), enrichie sprint dettes post-Phase-B (audit détaillé branches `claude/*` + identification anomalie `brave-poincare`).

**Post-sprint cleanup exécuté Sprint C OPS 2026-05-12 :**

- ✅ **Worktree root libéré** : `git -C <root> checkout --detach origin/main` (branche `main` était squattée par `sweet-buck-7ccde0`, donc detached HEAD au lieu de checkout main). Branche `fix/patrimoine-audit-phase-b` supprimée (`was 4621a1a`).
- ✅ **Worktree `hungry-austin-0b60a4` admin nettoyé** : `git worktree remove --force` réussi côté admin. Directory physique `Permission denied` au rm (mon CWD agent en cours). Branche `claude/hungry-austin-0b60a4` supprimée (`was 2789698`). Pattern identique à `brave-poincare-28cbc7` du sprint dettes post-Phase-B (commit `c2c7ada`).

**État worktrees post-cleanup Sprint C (5 actifs) :**
- `C:/Users/lucas/Documents/Claude/Projects/Tellux` (root, detached HEAD `c02e129` origin/main, libéré)
- `.claude/worktrees/inspiring-fermat-d69ee2` (branche `dev`, agent Code actif)
- `.claude/worktrees/inspiring-snyder-b363e6` (branche `refactor/app-fetch-sites-corse-json`, conservé)
- `.claude/worktrees/magical-heisenberg-32429b` (detached HEAD, conservé)
- `.claude/worktrees/sweet-buck-7ccde0` (branche `main`, conservé)
- `.claude/worktrees/youthful-borg-c042ec` (branche `data/reconciliation-sites-corse`, conservé)

**Dette `OPS-WORKTREE-CREATION-001` : PARTIELLEMENT RÉSOLUE.** Les 2 résiduels du brief (root + hungry-austin) sont nettoyés côté admin. Reste : 3 worktrees `refactor/*`, `data/*`, `magical-heisenberg` qui sont vraisemblablement encore actifs (autres sessions Code ou branches en cours). À auditer dans un brief séparé si nécessaire. Le sous-ticket `OPS-CODE-WORKTREE-ISOLATION-FLAG-001` reste ouvert (doctrine CLI exclusif).

---

### OPS-CODE-WORKTREE-ISOLATION-FLAG-001 — Désactivation création auto worktrees desktop app

**Sous-ticket de `OPS-WORKTREE-CREATION-001`.**

**Description :** L'app desktop Claude Code crée automatiquement et de façon non-désactivable un git worktree sous `.claude/worktrees/<random-name>/` à chaque session ouverte (cf. https://code.claude.com/docs/en/desktop.md section "Work in parallel with sessions"). Le projet Tellux a une doctrine « jamais worktree » (PROJECT_INSTRUCTIONS), incompatible avec ce comportement.

**Conclusion investigation 2026-05-11 :** aucun flag, env var, ou setting (autre que `worktree.baseRef` qui contrôle juste la ref de base) ne permet de désactiver la création automatique côté desktop app. Le seul moyen de respecter la doctrine projet est d'utiliser exclusivement le **CLI Claude Code** pour ce repo et de prohiber le desktop app.

**Priorité :** Basse (workaround connu : usage CLI exclusif).

**Condition de déblocage :**
1. **Court terme** : enrichir `.claude/CLAUDE.md` (instructions Claude Code locales du projet) avec mention explicite « usage CLI uniquement, desktop app prohibé sur ce repo ». À traiter dans brief séparé.
2. **Moyen terme** : si Anthropic ouvre un flag de désactivation dans une release future, mettre à jour `.claude/settings.json` du projet. Surveiller release notes CLI Claude Code.
3. **Long terme** : si la doctrine projet évolue ou si Anthropic rend obligatoire le desktop, réconcilier les doctrines.

Identifiée sprint dettes post-Phase-B (2026-05-11), suite à investigation de la cause racine `OPS-WORKTREE-CREATION-001`.

---

### ARCHIVE-BRANCH-BRAVE-POINCARE-001 — Tentative antérieure fix race N1↔N2

Branche `claude/brave-poincare-28cbc7` (HEAD `fd5f309`) contient une tentative antérieure non-mergée de fix sur "race condition markers non cliquables après N1→N2→N1". Notre fix S1 solution A (commit `5f1b480`, prod 11 mai 2026 via PR #470) résout le même symptôme avec approche symétrique enter/exit. Branche conservée pour comparaison si edge-case réapparaît. À supprimer si > 6 mois sans rappel.

Worktree associée `brave-poincare-28cbc7` supprimée 11 mai 2026 (detached HEAD `2789698` indépendant de la branche `claude/brave-poincare-28cbc7` à `fd5f309`, donc safe).

**Statut :** ARCHIVÉE, non bloquant. Reminder à 11 novembre 2026 pour décision suppression définitive.

---

### GPS-AUDIT-BRGM-001 — Indices uranium Cortenais/Venaco — coord BRGM non publiques

**Description :** L'entrée `uth_cortenais_venaco` (slug app `CORTENAIS_VENACO`) de `points_chauds_radio_corse.json` repose sur le rapport BRGM 1979 (`79-RDM-070-FE`, « Les minéralisations intragranitiques de la Corse »), qui décrit des indices d'autunite et torbernite (phosphates secondaires d'uranium) dans des filons hydrothermaux du Cortenais sans publier de coordonnées GPS précises. La coordonnée actuelle 42.29/9.152 (precision_coord `communal`) est un centroïde géographique cohérent entre Corte et Venaco, validée en clôture M1 (2026-05-13) faute de meilleure source publique.

**Priorité :** Basse

**Condition de déblocage :** Audit dédié BRGM InfoTerre (portail public `infoterre.brgm.fr`) pour récupérer les coordonnées précises des indices d'autunite/torbernite, ou consultation du rapport `79-RDM-070-FE` archivé. Mise à jour de l'entrée `uth_cortenais_venaco` de `public/data/sites_app.json` (lat/lon + `gps_source` + `gps_audit` + éventuellement `precision_coord` → `ponctuel`).

**Identifiée :** clôture M1 sites_app.json (2026-05-13).

---

### GPS-AUDIT-BRGM-002 — Indices uranium Balagne Giussani — coord BRGM non publiques

**Description :** L'entrée `uth_balagne_giussani` (slug app `BALAGNE_GIUSSANI`) repose sur le rapport BRGM 1980 (`80-RDM-003-FE`, « Activités minières en Corse »), qui mentionne le Giussani comme secteur à anomalies radioactives dans les granites de la Balagne intérieure. Coordonnée actuelle 42.529/9.02 (precision_coord `communal`) = centroïde Giussani (4 communes : Olmi-Cappella, Pioggiola, Mausoléo, Vallica). Validée en clôture M1 (2026-05-13) faute de coord publique précise.

**Priorité :** Basse

**Condition de déblocage :** Idem GPS-AUDIT-BRGM-001 — consultation InfoTerre ou rapport `80-RDM-003-FE` archivé. Mise à jour de l'entrée `uth_balagne_giussani` de `public/data/sites_app.json`.

**Identifiée :** clôture M1 sites_app.json (2026-05-13).

---

### GPS-AUDIT-BRGM-003 — Source thermale de Guitera — émergence Taravo non publiée

**Description :** L'entrée `source_thermale_guitera` (THERMAL_SOURCES_CORSE) repose sur la coord du village de Guitera-les-Bains (41.88/9.07, alt 621 m, CP 20153), récupérée auprès de la Communauté de communes Pieve de l'Ornano et du Taravo. La source thermale réelle émerge au bord du Taravo, mais le point d'émergence exact n'est pas publié sur les sources web consultées (Wikipedia, pieveornano.fr, corseweb.corsica). La station thermale est fermée depuis plusieurs années (status `fermee_depuis_plusieurs_annees`). Coordonnée acceptée en clôture M1 (2026-05-13) en `precision_coord: secteur`.

**Priorité :** Basse

**Condition de déblocage :** Audit dédié — consultation BRGM `RP-55916-FR` (« Inventaire des sources thermominérales de Corse ») disponible sur infoterre.brgm.fr, ou recherche IGN Géoportail pour le toponyme « Bagni di Vutera ». Mise à jour `source_thermale_guitera` (lat/lon + `gps_source` + `precision_coord` → `ponctuel` ou `exacte`).

**Identifiée :** clôture M1 sites_app.json (2026-05-13).

---

### OPS-COWORK-SANDBOX-GIT-DRIFT-001 — Désynchronisation git sandbox Cowork vs repo Windows réel

**Description :** L'environnement bash sandbox Cowork se désynchronise du repo Windows réel sur certaines sessions : index git corrompu (erreur « uses C? extension »), `.git/index.lock` 0-byte impossible à supprimer en mode supervisé, fichiers HTML vus tronqués alors que le fichier Windows est complet. Pattern observé 3 fois le 13 mai 2026 (M3 + fix patrimoine + diagnostic environnement). Cause probable : `git rm -r .` accidentel stagé dans une session antérieure + mount sandbox désynchronisé. Workaround opérationnel : Code local Windows reprend la suite (stash / reset / re-branche depuis `origin/dev`).

**Priorité :** Moyenne (impacte la productivité Cowork mais le workaround Code local est fiable)

**Condition de déblocage :** Investigation environnement Cowork (permissions mount sandbox, comportement de l'index git entre sessions). Possiblement une issue à remonter à Anthropic support. Pattern à documenter dans `COWORK.md` pour accélérer le diagnostic futur.

**Identifiée :** 13 mai 2026 (M3 + fix patrimoine PR #532, 3 occurrences distinctes dans la même journée).

---

### CLEANUP-PATRIMOINE-INSTRUMENTATION-001 — Retrait instrumentation `[CLICK-DBG]` dans `patrimoine.html`

**Description :** Les instrumentations `[CLICK-DBG]`, `[BIND-TRACE]`, `[UNBIND-TRACE]` ajoutées le 13 mai 2026 dans `patrimoine.html` (~30 lignes au total) pour diagnostiquer le bug 2e clic Leaflet toggle sont encore présentes en prod. Le fix toggle a été mergé en PR #532 le 13 mai. L'instrumentation génère du bruit en DevTools console et alourdit légèrement le code, sans impact fonctionnel.

**Priorité :** Faible (non bloquant, bruit console uniquement)

**Condition de déblocage :** 5-7 jours de stabilité prod du fix PR #532 sans nouveau symptôme. Retrait des ~30 lignes `[CLICK-DBG]` / `[BIND-TRACE]` / `[UNBIND-TRACE]` de `patrimoine.html` via `grep -n "CLICK-DBG\|BIND-TRACE\|UNBIND-TRACE" patrimoine.html` puis suppression ciblée.

**Identifiée :** 13 mai 2026 (merge PR #532 fix patrimoine 2e clic Leaflet toggle).

---

### SITES-EM-JSON-UNTERMINATED-STRING-001 — `sites_em.json` signalé corrompu (audit cross-axes Cowork)

**Description :** Audit cross-axes Cowork du 13 mai 2026 a signalé une "unterminated string" dans `sites_em.json` lors d'une tentative de `json.load`. Or `sites_em.json` n'existe plus dans le repo : il a été supprimé par M3 (PR #531, `chore(m3): remove obsolete sites_em / points_chauds_radio / sites_remarquables JSONs`) au profit de `public/data/sites_app.json` consolidé. La référence Cowork est donc probablement obsolète (sandbox vue antérieure à M3), mais à vérifier par reproductibilité côté Windows post-resync.

**Priorité :** Faible (fichier supposé inexistant, à confirmer)

**Condition de déblocage :** Reproductibilité confirmée côté Windows (fresh checkout dev) + investigation si oui. Probable même cause que `OPS-COWORK-SANDBOX-GIT-DRIFT-001`.

**Identifiée :** 13 mai 2026 (audit cross-axes Cowork session Sprint 2 Phase A).

---

### SITES-REFERENCE-JSON-DEPRECATION-001 — `SITES_REFERENCE.json` racine 115 sites historiques sans axes modernes

**Description :** `SITES_REFERENCE.json` à la racine du repo (33 KB, 115 sites) porte un schéma historique pré-refonte (champ `type` string, pas d'`axe_corpus` / `phase_publication` / `gps_audit`). Source antérieure au pivot patrimoine de mai 2026, possible source de confusion pour les nouveaux consommateurs et risque de drift silencieux par rapport au canonical `docs/data/sites_patrimoine.json`.

**Priorité :** Faible

**Condition de déblocage :** Audit usage (`grep -r "SITES_REFERENCE" --include="*.py" --include="*.js" --include="*.html"`), choix entre archivage `_drafts/` ou intégration formelle dans le pipeline moderne via sprint dédié.

**Identifiée :** 13 mai 2026 (audit Code Sprint 2 Phase B post-merge).

---

### REMARQUABLES-GEOLOGIQUES-DRIFT-001 — Divergence d'effectifs entre runs Cowork sur axe `remarquables_geologiques`

**Description :** Axe `remarquables_geologiques` de `sites_patrimoine.json` observé à 4 entrées dans un run Cowork du 12 mai 2026, puis 17 entrées dans un autre du 13 mai 2026 (audit cross-axes Phase A). Source de la divergence non identifiée (probable run Code silencieux entre les deux, ou session Cowork parallèle non tracée). Risque de confusion sur la doctrine d'ingestion de cet axe.

**Priorité :** Faible (axe minoritaire en termes d'effectif comparé aux `edifices_romans` et `megalithes`)

**Condition de déblocage :** `git log --oneline -- docs/data/sites_patrimoine.json` filtré sur les modifications portant sur l'axe `remarquables_geologiques` depuis le 1er mai 2026 ; reconstruction de l'historique d'ingestion ; documentation de la source canonique.

**Identifiée :** 13 mai 2026 (audit cross-axes Cowork session Sprint 2 Phase A).

---

### SITES-PATRIMOINE-INSEE-BELVEDERE-CAMPOMORO-001 — INSEE divergent sur `capu_di_logu` (anomalie A3 Cowork)

**Description :** L'entrée `capu_di_logu` de `docs/data/sites_patrimoine.json` porte `commune_insee: "2A041"` (source initiale) alors que le code INSEE officiel actuel de Belvédère-Campomoro est `2A035` (COG INSEE 2024). Anomalie A3 identifiée par Cowork pendant Phase A Sprint 2. Non corrigée dans la PR data Sprint 2 Phase B (hors périmètre, risque de cascade si d'autres entrées portent aussi `2A041` à tort, audit cross-source nécessaire).

**Priorité :** Faible (donnée erronée localisée mais sans impact runtime aujourd'hui ; risque de pollution si propagation)

**Condition de déblocage :** `grep -n "2A041" docs/data/sites_patrimoine.json` (et autres fichiers `docs/data/*.json`) pour mesurer la propagation. Audit cross-source COG INSEE officiel vs sources utilisées en historique. Patch ciblé `2A041` → `2A035` après confirmation.

**Identifiée :** 13 mai 2026 (anomalie A3 audit Cowork Sprint 2 Phase A).

---

### CORPUS-META-AXES-INCOMPLET-001 — `_meta.axes_corpus_referentiel` incomplet dans `sites_patrimoine.json` (anomalie A4 Cowork)

**Description :** Le bloc `_meta.axes_corpus_referentiel` de `docs/data/sites_patrimoine.json` ne liste pas tous les axes effectivement présents dans le fichier : notamment `remarquables_geologiques` (cf. dette `REMARQUABLES-GEOLOGIQUES-DRIFT-001`) est porté par des entrées sans être déclaré dans le référentiel `_meta`. Source de confusion potentielle pour les consommateurs qui valident la cohérence d'un import par référence au `_meta`.

**Priorité :** Faible

**Condition de déblocage :** Refresh manuel de `_meta.axes_corpus_referentiel` à partir des `axe_corpus` distincts effectivement présents dans `sites`, ou script de regen idempotent. Vérifier qu'aucun consommateur ne dépend de l'absence des axes manquants comme signal de non-existence.

**Identifiée :** 13 mai 2026 (anomalie A4 audit Cowork Sprint 2 Phase A).

---

### PATRIMOINE-HASH-DEEPLINK-CADRAGE-001 — Cadrage map cassé sur navigation hash directe N2

**Description :** Navigation directe via URL hash (`patrimoine.html#<doyenne_slug>`) vers un doyenné N2 crée les markers DOM (ex. 25 markers observés sur `#piana_vico_sari`) mais n'effectue pas le cadrage de la carte sur ces markers — viewport reste centré ailleurs, thumbnail latérale vide. Le drill-down via clic depuis la vue N1 fonctionne normalement. Reproductible en prod actuelle (pré-existant Phase B), confirmé lors de la validation preview PR #538 (Chrome MCP, 13 mai 2026). Cause probable : la chaîne `applyHash() → drillDown()` ne déclenche pas `map.fitBounds(layer.getBounds())` en queue, ou l'appel est joué avant que les markers soient ajoutés à la couche. À comparer avec le chemin clic-N1 qui fonctionne.

**Priorité :** Faible (UX dégradée sur deeplink uniquement, contournable par drill-down depuis N1)

**Condition de déblocage :** Tracer la chaîne `applyHash → drillDown` vs chaîne clic-N1, identifier le point de divergence, ajouter le `fitBounds` manquant ou réordonner l'appel. Estimation 1-2 lignes de fix.

**Identifiée :** 13 mai 2026 (validation preview PR #538 Sprint 2 Phase B, Chrome MCP sur `#piana_vico_sari`).

---

### SITES-PATRIMOINE-TOURS-PRE-SPRINT3-PIEVE-NULL-001 — 4 tours pré-Sprint 3 sans `pieve_slug`

**Description :** 4 tours présentes avant la série Sprint 3 (tours littorales) n'ont jamais reçu d'attribution `pieve_slug` et n'ont pas été enrichies au passage des sprints 3a/3b/3c/3d. État post-Sprint 3d (commit `47816b1`) : `tour_d_agnello_cap_corse`, `tour_de_capo_di_muro`, `tour_de_giraglia_ilot`, `tour_de_la_mortella`. Le chiffre était de 6 tours avant Sprint 3 ; `tour_d_isolella_sette_navi` et `tour_genoise_chiappa` ont été enrichies incidemment en Sprint 3b et 3c respectivement (mapping cohérent commune → pieve appliqué au passage de la commune voisine ingérée).

**Priorité :** Faible (4 tours sur 66, pieve_slug non bloquant pour l'affichage N2 qui repose sur `doyenne_contemporain_slug`)

**Condition de déblocage :** Audit ciblé des 4 slugs résiduels, lookup commune → pieve via référentiel Casta canonique (sources `tellux-corpus-internal`). Mini-PR data dédiée (~30 min Cowork ou Code). Vérifier au passage attributions suspectes existantes (cf. `SITES-PATRIMOINE-PIEVE-ATTRIBUTIONS-SUSPECTES-001`).

**Identifiée :** 13 mai 2026 (audit Cowork session Sprint 3a + persistance post-clôture Sprint 3d).

---

### SITES-PATRIMOINE-TOURS-PRE-SPRINT3-INSEE-NULL-001 — 4 tours pré-Sprint 3 sans `commune_insee`

**Description :** 4 tours présentes avant la série Sprint 3 (tours littorales) sans `commune_insee` peuplé. État post-Sprint 3d : `tour_d_agnello_cap_corse`, `tour_de_capitello_castelluccio`, `tour_de_giraglia_ilot`, `tour_de_la_mortella`. Overlap fort avec `SITES-PATRIMOINE-TOURS-PRE-SPRINT3-PIEVE-NULL-001` (3 tours communes : agnello, giraglia_ilot, mortella). `tour_de_turghiu_capo_rosso` a été enrichie INSEE 2A212 en Sprint 3b (sortie de la dette). Le brief clôture mentionnait 2 tours initiales, l'état exact reste 4 résiduelles.

**Priorité :** Faible

**Condition de déblocage :** Lookup INSEE COG officiel depuis le champ `commune_nom` existant pour les 4 slugs. Traitement Cowork ou Code (< 30 min). Idéalement traité conjointement avec `SITES-PATRIMOINE-TOURS-PRE-SPRINT3-PIEVE-NULL-001`.

**Identifiée :** 13 mai 2026 (audit Cowork session Sprint 3a + persistance post-clôture Sprint 3d).

---

### SITES-PATRIMOINE-PIEVE-ATTRIBUTIONS-SUSPECTES-001 — Attributions `pieve_slug` à vérifier (3 cas)

**Description :** Audit Cowork Sprint 3a a remonté 3 attributions `pieve_slug` suspectes pré-existantes dans `sites_patrimoine.json` :
- **Meria** : `pieve_sorroinsu` erronée (devrait probablement être `pieve_luri` selon référentiel Casta — Meria est dans le Cap Corse côte est, zone pieve_luri historiquement)
- **Olmeta-di-Capocorso** : doublon entre `pieve_nebbiu` et `pieve_nonza` selon les entrées du JSON (côte ouest Cap Corse → `pieve_nonza` retenu Sprint 3a pour la nouvelle Tour de Negro, mais cohérence cross-corpus à vérifier)
- **Saint-Florent** : `pieve_balagne` suspect (Saint-Florent est plutôt rattaché à `pieve_nebbio` historiquement)

**Priorité :** Faible (anomalies non bloquantes pour le rendu N2, qui repose sur `doyenne_contemporain_slug`)

**Condition de déblocage :** Cross-check référentiel Casta canonique (corpus interne `tellux-corpus-internal`) vs attribution effective JSON. Mini-PR data dédiée correction si confirmé.

**Identifiée :** 13 mai 2026 (audit Cowork session Sprint 3a Phase A).

---

### SITES-PATRIMOINE-TOURS-CASTELLUCCIO-DOUBLET-001 — Doublet toponymique Castelluccio

**Description :** Deux entrées potentiellement homonymes dans le corpus tours littorales :
- `tour_de_capitello_castelluccio` (Sprint 3a pré-existant, côte est golfe Ajaccio, lat 41.90424 / lon 8.79912, doyenne_ajaccio — mais sans commune_insee, cf. dette INSEE-NULL)
- `tour_de_castellucio_ajaccio` (créée Sprint 3b, côte ouest Ajaccio entre Sanguinaires et Capitello, lat 41.87556 / lon 8.58778, commune Ajaccio, INSEE 2A004, pieve_ajaccio)

Castelluccio (variante de *castellaccio*, "petit château fort") est un toponyme répandu en Corse. Les deux sites sont **probablement distincts géographiquement** (écart ~15 km en longitude, deux côtes du golfe d'Ajaccio), mais l'audit toponymique formel cross-référence Mérimée + IGN n'a pas été effectué. Sprint 3b a choisi de créer la nouvelle entrée en assumant la distinction.

**Priorité :** Faible (cas isolé, pas de cascade)

**Condition de déblocage :** Audit toponymique cross-référence Mérimée POP + Wikipedia FR + cartes IGN. Si distincts confirmés : ajouter note de désambiguïsation dans la `description` des deux entrées. Si doublon : fusionner et garder le slug le plus fidèle à la source primaire.

**Identifiée :** 13 mai 2026 (Sprint 3b Phase A audit).

---

### SITES-PATRIMOINE-TOURS-FARINOLE-GPS-PRECIS-001 — Tour de Farinole GPS centroïde commune

**Description :** Tour de Farinole reclassée P1 → P2 latent en Sprint 3a Phase B mapping (Option A arbitrée Soleil). GPS actuel = centroïde commune Farinole (42.7333, 9.3333), `precision_coord: ±2km`, `gps_status: centroid_a_preciser`, `gps_audit: commune_centroid_2026-05-13`. Mérimée PA00125391 référencé mais pas exploité pour GPS précis lors de l'ingestion Sprint 3a.

**Priorité :** Faible

**Condition de déblocage :** Recherche GPS précis via Mérimée POP fiche détaillée PA00125391, ou Wikipedia FR fiche dédiée Tour de Farinole si existe, ou Wikidata QID Tour de Farinole. Si GPS précis trouvé : promotion P2 → P1, mise à jour `gps_audit`, retrait `precision_coord` et `gps_status`.

**Identifiée :** 13 mai 2026 (Sprint 3a Phase B mapping, Option A Soleil).

---

### SITES-PATRIMOINE-TOURS-POGGIO-ERSA-MAISON-TOUR-001 — Maison-tour Poggio Ersa PA2B000009 skip Sprint 3a

**Description :** Maison-tour Poggio Ersa (Mérimée PA2B000009) skippée Sprint 3a Phase A pour GPS anomal. La 1ère extraction Wikipedia donnait lat 42.81583, incompatible avec Ersa (extrême nord du Cap Corse, lat attendu ~43.0+). Distincte de `tour_de_poggio_ersa` (PA2B000369) ingérée Sprint 3a avec GPS proche du hameau Poggio sur Ersa.

**Priorité :** Faible

**Condition de déblocage :** Recherche GPS exploitable pour PA2B000009 (Wikipedia FR fiche dédiée si existe, ou consultation Mérimée détaillée Ersa). Si GPS trouvé compatible Ersa : ajout dédié en P1 ou P2 latent selon précision, avec note de distinction vs `tour_de_poggio_ersa` (PA2B000369).

**Identifiée :** 13 mai 2026 (Sprint 3a Phase A skip + persistance audit).

---

### SITES-PATRIMOINE-TOURS-MERIMEE-EXHAUSTIF-COMPLEMENT-001 — Sprint complément 66 → 70 tours

**Description :** Cible brief Sprint 3 = 70 tours littorales. Atteint **66/70 = 94%** sur les 4 sprints de la série (3a Cap+Balagne, 3b Ouest+Sud-Ouest, 3c Extrême-Sud+côte est, 3d complément Plaine Orientale). Marge plafond 4 ajouts non consommée (51/55) reflète la sous-densité historique de la Plaine Orientale, documentée et acceptée (zone marécageuse insalubre jusqu'au XIXe, peuplement côtier tardif, défense génoise moins concentrée). Confirmation empirique par recherche Wikipedia Option B exhaustive Sprint 3d sur 5 communes côte est = 0 candidat additionnel.

**Priorité :** Faible (Phase 1 acceptable à 94%)

**Condition de déblocage :** Sprint Cowork dédié exploration **Mérimée POP exhaustive** (filtres + scrolling complet base Mérimée Corse, recherche structurée "tour" + département 2A/2B), focalisé sur sous-zones encore minoritairement couvertes ou tours non listées dans la synthèse Wikipedia. À reconsidérer si dossier FEDER OS1.2 nécessite exhaustivité visuelle patrimoine pour démonstration.

**Identifiée :** 13 mai 2026 (clôture série Sprint 3 à 66/70 documentée).

---

## Bonnes pratiques issues de sprints

### BP-SPRINT3B-MAPPING-INTEGRE-INGESTION-001 — Mapping `pieve_slug` + `commune_insee` intégré dès l'ingestion

**Contexte initial :** Sprint 3a a livré 28 tours avec `pieve_slug=null` et `commune_insee=null`, nécessitant un sprint correctif (mapping Cowork + PR #543) pour peupler les champs structurants. Cette seconde passe a révélé 5 dettes data-quality pré-existantes (4 cas dont 3 attributions suspectes) et coûté environ 3 h de travail supplémentaire.

**Acquis Sprint 3b et maintenu Sprint 3c + 3d :** Code peuple `pieve_slug` et `commune_insee` **dès l'ingestion en Phase A**, en utilisant comme référentiel :
1. La distribution `pieve_slug` effective extraite du JSON (post-Sprint 3a = 47 pieves canoniques Casta)
2. La table commune → pieve cohérente cross-corpus (lookup direct sur les entrées existantes par `commune_nom`)
3. Le lookup INSEE COG officiel pour les communes sans entrée existante

Le mapping est validé par Soleil au **POINT DE VALIDATION A** (Phase A), avant édition. Résultat sur 3 sprints consécutifs : 10/10 (3b) + 11/11 (3c) + 2/2 (3d) tours avec champs structurants peuplés, zéro seconde passe nécessaire.

**Pattern à réutiliser pour les sprints data patrimoine futurs :**
1. Phase A inclut systématiquement extraction du référentiel `pieve_slug` effectif depuis `sites_patrimoine.json`
2. Détection automatique des ambiguïtés commune → pieve (communes mappées à plus d'une pieve) → remontée pour arbitrage Soleil
3. Communes nouvelles (pas dans le référentiel actuel) → arbitrage Soleil obligatoire avant édition (avec proposition pieve_slug par voisinage géographique)
4. Phase B vérification post-édition : compteurs `tours sans pieve_slug` et `tours sans commune_insee` doivent matcher **exactement** les dettes pré-existantes (pas de nouvelle entrée null)
5. Si la commune nouvelle n'a pas d'entrée dans le corpus, l'INSEE COG peut être trouvé via Wikipedia FR commune (toujours présent dans l'infobox) ou via la base INSEE COG officielle

**Applicable à :** tous les sprints futurs touchant `sites_patrimoine.json` (Sprint 4 ponts génois, Sprint 5 archéo romain/médiéval, Sprint 6 paesi, Sprint 7 vernaculaire, sprints complémentaires).

**Origine :** Sprint 3a (situation problème, mapping différé en PR #543), Sprint 3b (acquis, PR #545), Sprint 3c (maintenu, PR #547), Sprint 3d (maintenu, PR #549).

---

## Dettes fermées récemment

- **SITES-PATRIMOINE-JSON-L13034-001** (13 mai 2026, audit Code H1 Sprint 2 Phase B) — **fermée par invalidation**. La virgule trailing supposée ligne 13034 signalée par Cowork pendant M3 est invalidée par audit Code locale : `docs/data/sites_patrimoine.json` côté `origin/dev` et `origin/main` est JSON valide (`python -m json.tool` exit 0), 13 051 lignes / 446 867 chars, tail propre `}`, `]`, `}`. La virgule trailing observée par Cowork n'existe pas dans le fichier réel — la cause racine est la désynchronisation du sandbox Cowork (pattern `OPS-COWORK-SANDBOX-GIT-DRIFT-001`). La dette créée plus tôt le 13 mai 2026 est donc immédiatement clôturée sans patch nécessaire.
- **SITES-COORDS-COTIERES-VERIFICATION-001** (11 mai 2026, commit `a966511` branche `chore/patrimoine-dettes-post-phase-b`) — résolue par audit GPS + correction commune pour les 3 sites côtiers identifiés. `capu_di_logu` (lat 41.6212→41.62585, lon 8.8424→8.84461, commune Bonifacio→Belvédère-Campomoro, description actualisée vers plateau golfe Valinco) ; `tour_de_capo_di_muro` (lat 41.719→41.7500, lon 8.664→8.6767, commune null→Coti-Chiavari) ; `u_paladinu` (GPS inchangé 41.7313/8.8325 confirmé légitime, commune null→Serra-di-Ferro). Pieve/doyenne_contemporain_slug non touchés (rebalancing pipeline `consolidate_sites.py` séparé si Soleil souhaite).
- **HASH-SPOT-SEUL-001** (11 mai 2026, commit `396947e` branche `chore/patrimoine-dettes-post-phase-b`) — symptôme S7 Phase A. `applyHash` étendu pour accepter `#<spot-slug>` single-segment : si le segment est un slug de site connu (`markersBySlug`), résolution doyenné via `SPOT_TO_DOYENNE.get(spot)` + pieve via `SPOT_TO_PIEVE_V2.get(spot)`, puis pipeline standard (enter N2 + sticker pieve + popup spot). `syncHashToUrl` canonicalise le hash final vers `#doy/pieve/spot`. Cas non couverts (doy seul, doy/pv, doy/pv/spot, segment inconnu) inchangés.
- **DOYENNE-ILLUSTRATIONS-OBSOLETE-001** (11 mai 2026, commit `bf3415c` branche `chore/patrimoine-dettes-post-phase-b`) — symptôme S6 Phase A. Commentaires obsolètes (`5/10 doyennes` faux, doctrine fallback typographique périmée) actualisés à 3 endroits dans `patrimoine.html` (L761, L877, L953) pour refléter l'état post-PR #460 : 9 doyennés actifs, 4 entrées recyclage diocèse indispensables (illustration_path retiré de polygons.json), 5 entrées dédiées redondantes (conservées en défense en profondeur). Mapping inchangé fonctionnellement. Option A « minimum invasif » retenue.
- **SITES-NAME-NULL-001** (11 mai 2026, commit `7f8f592` branche `fix/patrimoine-audit-phase-b-v2`) — résolue par suppression de l'entrée `menhirs_du_rizzanese` (doublon de `rizzanese_frati_sora` selon audit Phase A Cowork, lat 41.648/lon 8.828 vs canonique 41.6468/8.9478, name=null vs `Menhirs du Rizzanese`). Symptôme S2 Phase A. Corpus passe de 168 à 167 sites P1.
- **N2-ILLUSTRATED-SHARED-MARKER-001** (créée + résolue 11 mai 2026, commit `5f1b480` branche `fix/patrimoine-audit-phase-b-v2`) — symptôme S1 Phase A. 9 markers illustrés étaient invisibles/inclickables en N2 (un par doyenné contemporain sauf 5 ILLUSTRATED_SPOTS sans rattachement doyenné). Cause racine : marker Leaflet partagé entre `spotsIllustratedLayer` (N1) et `spotsLevel2ByDoyenne` (N2). Le `map.removeLayer(spotsIllustratedLayer)` du setTimeout 250ms dans `enterNiveau2View` détache le marker du DOM même s'il appartient encore au LG N2 actif. Fix solution A symétrique enter/exit : re-attache individuelle dans setTimeout enter + detach individuel avant `spotsIllustratedLayer.addTo(map)` en exit. Liste markers affectés : citadelle_de_calvi, citadelle_de_corte, lac_de_nino, bastia_citadelle, couvent_d_orezza, bonifacio_remparts, cargese_grec_latin, lac_de_creno, aleria_antique.
- **N2-SPOT-CLICK-PROPAGATION-001** (créée + résolue 11 mai 2026, commit `4b077f4` branche `fix/patrimoine-audit-phase-b-v2`) — symptôme S3 Phase A. Le clic marker spot et clic polygone pieve propageaient leur événement aux handlers parents (polygones doyenné/pieve sous-jacents), causant des transitions N1→N2 indésirables et des bascules de breadcrumb incorrectes. Fix : `marker.on('click', (ev) => onSpotClick(..., ev))` + `poly.on('click', (ev) => onPieveClickV2(..., ev))`, avec `if (ev) L.DomEvent.stopPropagation(ev)` en tête des deux handlers. `onDoyenneClick` non touché (légitime à propager). 4 chemins testés : N1 spot, N2 spot, N2 pieve, miniature N2.

- **EMAG-CRUSTAL-AUDIT-001** (1ᵉʳ mai 2026) — fermée par audit (verdict : couches fonctionnellement distinctes). Investigation conduite sur `app.html` après que la portion « wdmam » de la dette ait été implicitement résolue par la fermeture de `WDMAM-NAMING-001` le 27 avril 2026. Constats : la couche `emag` (l.2098) est un `L.imageOverlay` raster régional Corse pointant sur l'endpoint NOAA NCEI EMAG2v3 ImageServer (`gis.ngdc.noaa.gov/arcgis/rest/services/EMAG2v3/ImageServer/exportImage`) avec bbox `[[41.3, 8.5], [43.1, 9.65]]` et `renderingRule={"rasterFunction":"EMAG2_Color_Scale"}` ; la couche `crustal` (l.2657-2700+) est un `L.layerGroup` vectoriel construit à partir du tableau hardcodé `CRUSTAL_REFS` (5 entrées : Bangui, Kursk, Vredefort, Ries, Chicxulub) avec 5 cercles + 5 markers divIcon, accompagné d'un panneau Leaflet Control `topright` (`_crustalGauge`) qui combine la valeur EMAG2v3 locale au centre carte (via `fetchEMAG2()`) avec les 5 références mondiales en barres logarithmiques. Datasets différents (raster EMAG2v3 régional vs 5 références hardcodées mondiales), mécanismes différents (raster ImageServer NOAA vs vectoriel Leaflet local), finalités différentes (overlay régional Corse vs panneau comparatif pédagogique mondial). Les deux couches peuvent être superposées (chacune a son propre flag dans `ACTIVE`) ; le panneau comparatif `crustal` *utilise* EMAG2v3 (complémentarité, pas redondance). Aucune modification de code requise. Note : un rollback du pattern bbox-dynamique introduit en PR #190 (commenté l.2092-2097) a depuis remis `wmsEmag` en bbox fixe — incohérence de note avec la fermeture WDMAM-NAMING-001 qui décrit un pattern bbox-dynamique. Hors périmètre de cet audit, à arbitrer dans un sprint ultérieur si harmonisation souhaitée.
- **WDMAM-NAMING-001** (27 avril 2026, PR phase 2 groupe 3) — résolue par fusion. La couche `b-wdmam` (« EMAG2 mondial » dynamique) et la couche `b-emag` (EMAG2v3 bbox Corse fixe) chargeaient toutes deux le même endpoint NOAA NCEI EMAG2v3 ImageServer. La fusion supprime `b-wdmam` et conserve `wmsEmag` en imageOverlay régional Corse à bbox fixe `[[41.3, 8.5], [43.1, 9.65]]`. Note historique : un pattern bbox-dynamique reconstruit à chaque activation avait été initialement introduit avec cette fermeture (PR phase 2 groupe 3) puis rollbacké par la PR #190 vers la bbox fixe pour des raisons de stabilité (le raccord cassé en prod — l'URL dynamique manquait notamment le `renderingRule EMAG2_Color_Scale` rendant l'image transparente). Cf. commentaire `app.html:2092-2097`. Identifiants `wmsWDMAM`, `togWDMAM`, `LEGEND_HTML.wdmam`, `#b-wdmam`, `.on-wdmam`, `showLegend('wdmam', ...)` tous supprimés du code. Conséquence collatérale : la portion « wdmam » de `EMAG-CRUSTAL-AUDIT-001` est aussi résolue (la triple couche emag/wdmam/crustal est ramenée à deux couches distinctes — EMAG2v3 régional et 5 références mondiales pédagogiques). Op-row d'opacité de `b-emag` retirée (incompatible avec le pattern de recréation à l'activation initialement envisagé, conservée en l'état après rollback).
- **ANTENNES-REFRESH-001** (24 avril 2026, PR #138) — workflow GitHub Actions de refresh mensuel des données antennes ANFR. Créée et fermée le même jour par Cowork Session A. Script `scripts/build_antennes_par_commune_corse.py`, sortie `public/data/antennes_par_commune_corse.json`, documentation `docs/operations/refresh-antennes.md`.
- **SUPABASE-COMMUNE-FIELD-001** (24 avril 2026, PR #137) — colonne `code_insee_commune` ajoutée à la table Supabase `contributions` pour permettre la jointure commune dans la Fiche commune `mairies.html`. Créée et fermée le même jour par Cowork Session A. Script de remplissage `scripts/fix_supabase_commune_insee.py`.
- **INTL-CRUSTAL-001** (23 avril 2026) — module de calibration crustale mondiale réimplémenté en EM pur. Tableau `CRUSTAL_REFS` (5 entrées : Bangui, Kursk, Vredefort, Ries, Chicxulub) avec `name`, `lat`, `lon`, `nT`, `radius_km`, `type`, `source`, `desc`. Couche Leaflet opt-in `crustal` (bouton `b-crustal`, désactivée par défaut) avec 5 cercles d'emprise + 5 markers divIcon. Panneau comparatif Leaflet Control `topright` : valeur EMAG2v3 locale au centre carte, 5 barres log(|nT|) des références mondiales, ligne "Centre carte" distincte. Aucun site patrimoine ; vérification anti-pollution passée (grep 17 termes negatif). Palette DA v2 gelée : Porphyre négatives, Ocre positives. Voir section « Module comparaison anomalies crustales mondiales » (archive ci-dessous).
- **CSS-HARMONISATION-001** (23 avril 2026) — aliases courts déjà ajoutés en amont (commit `66fd6ce`) ; 4 variables hardcodées renommées sémantiquement dans `:root` de `app.html` (`--tx2`→`--ardoise-clair`, `--bg2`→`--pierre-ombre`, `--acc2`→`--maquis-clair`, `--acc3`→`--maquis-pale`, ~137 occurrences) ; `Georgia` retiré du fallback `--font-display` (Fraunces self-hosted depuis PR #83). `DM Sans`/`DM Mono` déjà absents.
- **ELF-VECTOR-001** (21 avril 2026, PR #71) — sommation vectorielle 2D implémentée dans `calcMagneticELF_v2`
- **BT-ELF-001** (21 avril 2026, PR #71) — infrastructure BT asynchrone implémentée (calcul désactivé temporairement, voir `BT-CALIBRATION-001`)
- **ELF-CALIB-001** (21 avril 2026, PR #69) — vérification des seuils visuels post-migration Biot-Savart, conservation des seuils 150/300/500 nT (Scénario A)
- **WMM-CROSSCHECK-001** (21 avril 2026, PR #67) — WMM 2025 cross-check intégré via grille précalculée (851 points, 124 KB, résolution 0.05°), affichage Mode Expertise « Écart IGRF/WMM », validation 3 points témoins (Ajaccio, Bastia, Monte Cinto)
- **BDFORET-V2-001** (21 avril 2026, PR #67, fermeture partielle) — couche Forêts publiques ONF intégrée via WMS IGN `FORETS.PUBLIQUES`. La granularité essences/forêts privées reste pendante via `BDFORET-GRANULARITE-001`.
- **SUPABASE-INSERT-001** (22 avril 2026) — policies INSERT permissives `WITH CHECK (true)` remplacées sur `contributions` et `orientations_contributions`. Migration `005_security_hardening.sql` : validation GPS mondiale (lat/lon), `note`/`commentaire` ≤ 500 chars, `azimut` 0-360, `site_id` non vide, rate limiting 10 contributions/heure par `session_id` via `check_contribution_rate_limit()`. Advisors Supabase : 0 alerte résiduelle. Limite connue : rate limit contournable en changeant de session_id (protection anti-spam naïf, non anti-attaquant déterminé).

---

## Principes

- Chaque dette porte un identifiant pérenne `XXX-YYY-NNN` pour traçabilité.
- La priorité reflète l'impact sur la qualité du modèle et non l'urgence opérationnelle.
- Une dette n'est fermée qu'après implémentation validée et mise à jour du corpus correspondant.
- Les dettes gelées (`GELÉ-001`, `NCRP-001`) attendent une validation méthodologique externe avant implémentation.

*Fin du document.*
