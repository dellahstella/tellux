#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère SITES_CONSOLIDATION_AUDIT.md à partir de sites_corse_v1.json + log."""
import json
from collections import Counter
from datetime import date

ROOT = '/sessions/busy-awesome-mayer/mnt/Tellux/_drafts'
TODAY = date.today().isoformat()

with open(f'{ROOT}/sites_corse_v1.json') as f:
    d = json.load(f)
with open(f'{ROOT}/SITES_DEDUPLICATION_LOG.json') as f:
    log = json.load(f)

sites = d['sites']
meta = d['_meta']

# Stats
total = len(sites)
ph1 = [s for s in sites if s['phase_publication'] == 1]
ph2 = [s for s in sites if s['phase_publication'] == 2]
by_axe = Counter(s['axe_corpus'] for s in sites)
by_axe_p1 = Counter(s['axe_corpus'] for s in ph1)
by_axe_p2 = Counter(s['axe_corpus'] for s in ph2)
with_insee = sum(1 for s in sites if s.get('commune_insee'))
with_doy = sum(1 for s in sites if s.get('doyenne_contemporain_slug'))
with_pieve = sum(1 for s in sites if s.get('pieve_slug'))
with_visuel = sum(1 for s in sites if s.get('illustre'))
with_priorite = sum(1 for s in sites if s.get('priorite'))
total_doublons = sum(len(v['aliases_merged']) for v in log['mappings'].values())

NATURAL_TRANSCOMMUNAL = {'Aiguilles de Bavella','Anneaux du Cap Corse','Capu Bianchi — extrême nord Cap Corse',
    'Désert des Agriate','Gorges du Spelunca','Monte Cinto',"Monte d'Oro",'Monte Renoso','Monte San Petrone',
    'Plateau du Coscione','Forêt de Vizzavona','Défilé de Lancône','Casa di u Banditu','Mamucci menhirs',
    'Monte Genova mégalithes'}

orphans = [s for s in sites if not s.get('commune_insee')]
orph_intent = [s for s in orphans if s['axe_corpus'] == 'diocese_medieval']
orph_natural = [s for s in orphans if s['nom'] in NATURAL_TRANSCOMMUNAL]
orph_to_resolve = [s for s in orphans if s['axe_corpus'] != 'diocese_medieval' and s['nom'] not in NATURAL_TRANSCOMMUNAL]

# Doublons priorité = sites avec 3+ alias
big_dedups = [(slug, info) for slug, info in log['mappings'].items() if len(info['aliases_merged']) >= 2]

md = []
md.append(f"# SITES_CONSOLIDATION_AUDIT — Tellux Corse")
md.append(f"")
md.append(f"**Date :** {TODAY}")
md.append(f"**Auteur :** Cowork (pipeline `consolidate_sites.py`)")
md.append(f"**Brief :** Stop Point §6.1 validé 2026-05-06 — production étapes 2-10")
md.append(f"")
md.append(f"## 1. Synthèse")
md.append(f"")
md.append(f"- **Total sites canoniques :** {total}")
md.append(f"- **Phase 1 (exposée patrimoine.html) :** {len(ph1)}")
md.append(f"- **Phase 2 (latente, churches_corse) :** {len(ph2)}")
md.append(f"- **Doublons fusionnés :** {total_doublons} (sur 602 entrées brutes en entrée)")
md.append(f"- **Couverture commune INSEE :** {with_insee}/{total} ({with_insee*100//total}%)")
md.append(f"- **Couverture doyenné contemporain :** {with_doy}/{total} ({with_doy*100//total}%)")
md.append(f"- **Couverture pieve médiévale :** {with_pieve}/{total} ({with_pieve*100//total}%)")
md.append(f"- **Sites illustrés (visuel présent) :** {with_visuel}/{total}")
md.append(f"- **Sites prioritaires (mode Découverte) :** {with_priorite}/{total}")
md.append(f"")
md.append(f"## 2. Inventaire des sources d'entrée")
md.append(f"")
md.append(f"| Source | Localisation | Entrées brutes | Statut |")
md.append(f"|--------|--------------|----------------|--------|")
md.append(f"| `SITES_PATRIMOINE` (inline) | `patrimoine.html` ligne 164 | 124 | ✅ intégrée |")
md.append(f"| `SITES_REFERENCE.json` | racine repo | 115 | ✅ intégrée |")
md.append(f"| `sites_corse` Supabase | DB | 115 | ✅ mirror exact de SITES_REFERENCE.json — fusion automatique |")
md.append(f"| `churches_corse` Supabase | DB | 314 | ✅ intégrée (291 en Phase 2 latente) |")
md.append(f"| `patrimoine_corse` Supabase | DB | 39 | ✅ intégrée (Tours, Châteaux, Thermes, Ponts, Mines) |")
md.append(f"| `sites_remarquables_corse.json` | `public/data/` | 10 | ✅ intégrée avec sémantique EM préservée |")
md.append(f"| `mega_studies` Supabase | DB | 83 | ⊘ exclue (corpus bibliographique, pas des sites) |")
md.append(f"")
md.append(f"## 3. Catégories canonisées (Q2 arbitré 2026-05-06)")
md.append(f"")
md.append(f"| axe_corpus | Catégorie display | Nb total | Phase 1 | Phase 2 |")
md.append(f"|-----------|-------------------|---------:|--------:|--------:|")
DISPLAY = {
    'megalithes': 'Mégalithique',
    'remarquables_geologiques': 'Site naturel remarquable',
    'patrimoine_bati_remarquable': 'Patrimoine bâti remarquable',
    'edifices_romans': 'Édifice roman',
    'diocese_medieval': 'Diocèse historique',
    'hydrauliques': 'Hydraulique',
    'tours_genoises': 'Tour génoise',
    'chateaux_medievaux': 'Château médiéval',
    'patrimoine_divers': 'Patrimoine',
}
for axe, n in by_axe.most_common():
    md.append(f"| `{axe}` | {DISPLAY.get(axe, axe)} | {n} | {by_axe_p1.get(axe, 0)} | {by_axe_p2.get(axe, 0)} |")
md.append(f"")
md.append(f"**Renommages effectués (Q2) :**")
md.append(f"")
md.append(f"- `Site remarquable` (5 entrées SITES_PATRIMOINE) → `Patrimoine bâti remarquable` / axe `patrimoine_bati_remarquable`")
md.append(f"- `Remarquable` (29 SP + 34 SR) → `Site naturel remarquable` / axe `remarquables_geologiques`")
md.append(f"- Toutes les variantes `B — Édifice roman tardif` etc. unifiées sous `Édifice roman` / axe `edifices_romans`")
md.append(f"- `Pont génois`, `Thermalisme`, `Patrimoine & Ressources`, `Patrimoine` unifiés sous `Patrimoine` / axe `patrimoine_divers`")
md.append(f"")
md.append(f"## 4. Déduplication")
md.append(f"")
md.append(f"**Stratégie appliquée :**")
md.append(f"")
md.append(f"1. Matching primaire : nom normalisé identique (lowercase, sans accents, sans articles `de/du/la/saint/santa/san`)")
md.append(f"2. Matching secondaire : distance GPS ≤ 150 m + axes compatibles (matrice `AXIS_COMPAT`)")
md.append(f"3. Priorité de source décroissante : `SITES_PATRIMOINE > sites_remarquables_corse > patrimoine_corse > SITES_REFERENCE/sites_corse_supabase > churches_corse`")
md.append(f"4. Fusion enrichissante : tout champ non rempli sur le site canonique est complété par les alias")
md.append(f"5. Toutes les sources d'origine listées dans `sources_originales[]`")
md.append(f"6. Mapping complet alias → canonique persisté dans `_drafts/SITES_DEDUPLICATION_LOG.json`")
md.append(f"")
md.append(f"**Résultats :**")
md.append(f"")
md.append(f"- 602 entrées brutes consolidées en {total} sites canoniques ({total_doublons} doublons éliminés)")
md.append(f"- Couples ↔ confirmés : SITES_PATRIMOINE ∩ SITES_REFERENCE (~90), SITES_REFERENCE ≡ Supabase mirror (115), SITES_PATRIMOINE B-Édifice roman ∩ churches_corse (~18), SITES_PATRIMOINE ∩ patrimoine_corse Tours (~4)")
md.append(f"- Aucun doublon trouvé entre `sites_remarquables_corse` et les autres sources (corpus 100% spécifique)")
md.append(f"")
if big_dedups:
    md.append(f"**Sites avec 2+ alias fusionnés (échantillon 10) :**")
    md.append(f"")
    md.append(f"| Slug canonique | Nom | Sources fusionnées | Aliases |")
    md.append(f"|----------------|-----|--------------------|---------|")
    for slug, info in big_dedups[:10]:
        srcs = ', '.join(info['sources_canoniques'])
        aliases = '; '.join(f"{a['nom_alias']} ({a['reason']}, d={a['distance_m']}m)" for a in info['aliases_merged'][:3])
        md.append(f"| `{slug}` | {info['nom_canonique']} | {srcs} | {aliases} |")
    md.append(f"")

md.append(f"## 5. Audit GPS — corrections appliquées")
md.append(f"")
for ga in meta['gps_audit_changes']:
    md.append(f"### `{ga['slug']}`")
    md.append(f"")
    md.append(f"- **Changement :** {ga['change']}")
    md.append(f"- **Ancien GPS :** ({ga['from'][0]}, {ga['from'][1]})")
    md.append(f"- **Nouveau GPS :** ({ga['to'][0]}, {ga['to'][1]})")
    md.append(f"- **Source :** OSM / Wikidata Capu Bianchi (audit Tellux 2026-05-06)")
    md.append(f"- **Décision :** Q3 Stop Point §6.1, déplacé à la pointe physique extrême nord")
    md.append(f"- **Renommage :** `Cap Corse extrême nord` → `Capu Bianchi — extrême nord Cap Corse`")
    md.append(f"- **Vérification non-confusion :** distinct de la Tour d'Agnello et de l'île Giraglia (voir §6)")
    md.append(f"")
md.append(f"## 6. Cas ambigus rencontrés")
md.append(f"")
md.append(f"### 6.1 Discrepance GPS Tour d'Agnello (à arbitrer dans une session ultérieure)")
md.append(f"")
md.append(f"Trois coordonnées différentes coexistent pour la \"Tour d'Agnello\" :")
md.append(f"")
md.append(f"| Source | Lat | Lon | Distance vs Capu Bianchi |")
md.append(f"|--------|-----|-----|--------------------------|")
md.append(f"| `patrimoine_corse` Supabase id=2 | 42.973 | 9.355 | ~5,2 km SW |")
md.append(f"| `SITES_REFERENCE` id correspondant | 42.973 | 9.415 | ~3,7 km SE |")
md.append(f"| GPS de référence cité par Soleil 2026-05-06 | 43.00917 | 9.4225 | ~2,7 km E |")
md.append(f"")
md.append(f"La pipeline a fusionné les deux premiers (matching nom). La référence Soleil n'est pas dans le corpus actuel.")
md.append(f"**Action recommandée :** audit GPS dédié Tour d'Agnello dans une prochaine session avec source documentée (BRGM Mérimée, OSM, photo-aérienne).")
md.append(f"")
md.append(f"### 6.2 Hameaux et lieux-dits dans `churches_corse` non résolus en INSEE")
md.append(f"")
md.append(f"Plusieurs églises sont localisées sur des hameaux (Vizzavona, Pietrapola, Folelli, Sagone, Lozari, Castelluccio…) qui ne sont pas des communes INSEE distinctes.")
md.append(f"Le `lieu` est conservé dans `commune_nom` mais `commune_insee = null`.")
md.append(f"**Action recommandée Phase 2 :** override JSON manuel (`_drafts/sites_corse_overrides.json`) à compléter avant ouverture Phase 2 churches.")
md.append(f"")
md.append(f"### 6.3 Sites mégalithiques sans toponyme communal")
md.append(f"")
md.append(f"Une vingtaine de mégalithes du `SITES_REFERENCE.json` portent des noms en corse ancien sans rattachement communal explicite (Scalsa Murta, U Cantonu, U Paladinu, Sposata, Tappa torre…).")
md.append(f"**Action recommandée :** audit ponctuel par croisement coordonnées GPS / contour communal (futur point-in-polygon avec contours communes Corse — non disponible v1).")
md.append(f"")
md.append(f"## 7. Orphans `commune_insee = null` (synthèse)")
md.append(f"")
md.append(f"Total : {len(orphans)} orphans sur {total} sites ({len(orphans)*100//total}%).")
md.append(f"")
md.append(f"**Catégorisation :**")
md.append(f"")
md.append(f"- **{len(orph_intent)} intentionnels — Diocèses historiques** : abstractions géographiques (Ajaccio, Aleria, Mariana, Sagone, Nebbio). `commune_insee = null` est correct, le centroïde GPS est conservé.")
md.append(f"- **{len(orph_natural)} sites naturels transcommunaux** : Aiguilles de Bavella, Désert des Agriate, Gorges du Spelunca, Monte Cinto/d'Oro/Renoso/San Petrone, Plateau du Coscione, Forêt de Vizzavona, Défilé de Lancône, Capu Bianchi, Anneaux du Cap Corse, Casa di u Banditu, Mamucci, Monte Genova mégalithes. Sites légitimement transcommunaux ou marins.")
md.append(f"- **{len(orph_to_resolve)} à résoudre manuellement** : voir §6.1, §6.2, §6.3 ci-dessus. Liste exhaustive dans `_drafts/SITES_DEDUPLICATION_LOG.json` (champ `notes`).")
md.append(f"")
md.append(f"## 8. Liste exhaustive des {len(orph_to_resolve)} orphans à résoudre")
md.append(f"")
md.append(f"| Nom | axe_corpus | Sources | Action recommandée |")
md.append(f"|-----|-----------|---------|---------------------|")
for s in orph_to_resolve:
    sources = ', '.join(s['sources_originales'])
    if 'churches_corse' in s['sources_originales']:
        action = 'Override JSON hameau→commune'
    elif 'patrimoine_corse' in s['sources_originales']:
        action = 'Audit BRGM/Mérimée + override'
    else:
        action = 'Point-in-polygon contour commune (Phase 2)'
    md.append(f"| {s['nom']} | `{s['axe_corpus']}` | {sources} | {action} |")
md.append(f"")
md.append(f"## 9. Schéma JSON cible — version définitive")
md.append(f"")
md.append(f"Champs obligatoires sur tous les sites : `slug`, `nom`, `lat`, `lon`, `categorie`, `axe_corpus`, `phase_publication`, `illustre`, `sources_originales[]`.")
md.append(f"")
md.append(f"Champs optionnels (peuvent être null/empty selon catégorie) : `description`, `commune_insee`, `commune_nom`, `pieve_slug`, `diocese_medieval_slug`, `doyenne_contemporain_slug`, `visuel`, `version_visuel`, `priorite`, `couleur`, `description_em`, `gps_source`, `gps_audit`, `notes`.")
md.append(f"")
md.append(f"**Adaptations vs brief (validées Q4 Stop Point §6.1) :**")
md.append(f"")
md.append(f"- `priorite: bool` ajouté (issu de SITES_PATRIMOINE — utile mode Découverte)")
md.append(f"- `couleur: string?` ajouté (présent dans SITES_REFERENCE et patrimoine_corse — facultatif si runtime calcule depuis `categorie`)")
md.append(f"- `description_em: object?` ajouté (sémantique riche de sites_remarquables_corse — `signature_em`, `impact_modele`, etc. préservée)")
md.append(f"- `gps_audit` au format ISO `YYYY-MM-DD`")
md.append(f"")
md.append(f"## 10. Fichiers livrés")
md.append(f"")
md.append(f"Tous dans `_drafts/` (pas d'intégration runtime sans Brief 28) :")
md.append(f"")
md.append(f"- `_drafts/sites_corse_v1.json` — corpus consolidé final ({total} sites, {meta.get('total_sites',total)} entrées, format JSON compact UTF-8)")
md.append(f"- `_drafts/SITES_DEDUPLICATION_LOG.json` — mapping complet `{{slug_canonique → [aliases]}}` ({len(log['mappings'])} sites avec doublons fusionnés)")
md.append(f"- `_drafts/SITES_CONSOLIDATION_AUDIT.md` — ce fichier")
md.append(f"")
md.append(f"## 11. Prochaines actions (hors périmètre Brief actuel)")
md.append(f"")
md.append(f"1. **Brief 28 (intégration repo)** — Soleil pousse `sites_corse_v1.json` vers `public/data/sites_corse.json`, met à jour `patrimoine.html` pour fetch + filtrer `phase_publication === 1`")
md.append(f"2. **Override JSON hameaux** (à créer) — résoudre les ~17 hameaux churches_corse non rattachables auto à une commune INSEE")
md.append(f"3. **Audit GPS Tour d'Agnello** — arbitrer entre les 3 coords (42.973/9.355, 42.973/9.415, 43.00917/9.4225)")
md.append(f"4. **Polygones communes Corse (GeoJSON)** — pour résoudre par point-in-polygon les ~22 sites SITES_REFERENCE/patrimoine_corse sans toponyme")
md.append(f"5. **Phase 2 enrichissement** — descriptions, visuels, orientations astrales pour les 291 churches latentes (au moment de l'ouverture Phase 2)")
md.append(f"")
md.append(f"---")
md.append(f"")
md.append(f"_Stop Point §6.2 obligatoire avant intégration repo. Soleil arbitre._")

out = f'{ROOT}/SITES_CONSOLIDATION_AUDIT.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))
print(f'Wrote {out} — {sum(len(l) for l in md)} chars / {len(md)} lines')
