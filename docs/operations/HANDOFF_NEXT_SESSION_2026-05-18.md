# Handoff prochaine session Tellux

## Session précédente : 2026-05-18 (sprint pré-FEDER massif)

Récap complet : `docs/operations/ETAT_FIN_SESSION_2026-05-18.md`.

### État final
- 50 pieves, 360 communes, 9 doyennés, 5 aliases v4.
- Pipeline `v7-cleanup-mapping-amont-rebuild-2026-05-18`.
- Override `pieve_bozio` → `doyenne_cortenais` actif.
- 23 sites B-ZONES (polygones au survol).
- Voie-a (rebuild depuis le mapping v4) redevenue viable.
- Phase 1 beta patrimoine : production-grade.

### À surveiller dès la nouvelle session
- **11 pieves reshapées par le rebuild v7** (dette `PATRIMOINE-PIEVES-V7-RESHAPE-INSPECTION-001`) : Soleil doit les inspecter visuellement (delta communes vs baseline v6 — `orezza` 14→29 et `moriani` 5→13 sont les plus gros écarts). Si une forme paraît anormale → corriger `_drafts/pieves_communes_mapping_v4_cleanup_2026-05-18.json` puis relancer `python scripts/build_pieves_polygons.py`. Le baseline pré-rebuild est conservé dans `outputs/baseline_v6_snapshot.json`.
- Dette `MAPPING-PREQW-ORIGIN-UNKNOWN-001` (basse) reste ouverte — origine `pieve_patrimonio` / `pieve_zicavo`.
- 19 pieves sans fiche rédactionnelle (vague 4) : post-FEDER.

### Pistes prochaine session
- Bascule **FEDER OS1.2** (chantier de fond).
- Investigation du diocèse `"?"` résiduel (~104.7 km² dans les stats v7).
- Inspection visuelle des 11 pieves reshapées par Soleil.
- Chantier rédactionnel fiches pieves (post-FEDER).

### Repères techniques pour reprise
- Rebuild pieves : `python scripts/build_pieves_polygons.py` (voie-a, depuis mapping v1+v2+v3+v4). Flag `--strict-mapping` pour faire échouer le build en cas de désync mapping ↔ dérivé.
- Cohérence mapping : `python scripts/validate_mapping.py` (doit être vert : 0 zombie, 0 manquante, 360 communes).
- Scripts one-shot historiques archivés : `scripts/archive/phase_oneshots/`.
- Convention coords : `pieves_polygons.json` / `doyennes_polygons.json` en `[lat, lon]` ; B-ZONES `zone_geometry` en GeoJSON `[lon, lat]`.

### Sessions Code et Cowork
Fermées en fin de session 2026-05-18. Nouvelle session ouverte selon besoin Soleil.
