# Rapport Brief 39decies - D2 polygones + sync_cross_app

Date : 2026-05-07
Initie par : Soleil "go"
Tache D2 (audit polygone Cortenais) + bonus script sync_cross_app.

## Synthese

| Action | Resultat |
|---|---|
| sync_cross_app.py cree | 220 lignes, 2 modes dry-run/apply |
| Sync initial : divergences detectees | 10 |
| Sync initial : sites synces | 10 (Patrimoine -> EM) |
| D2 audit polygone Cortenais | Hypothese Code "Cortenais deborde" INVALIDEE |
| D2 audit complet 449 sites | 1 vrai DIVERGENT, 8 HORS_POLY connus, 58 NULL_DECL |
| Renommage santa_maria_della_neve_grosseto_prugna_basse -> saint_cesaire_grosseto_prugna | OUI (web confirme Saint Cesaire = vraie eglise romane XIe) |
| Total sites JSON apres D2 | 449 (inchange) |
| Total locked apres D2 | 77 (inchange : 1 lock retire + 1 lock ajoute = 0 net) |

## sync_cross_app.py

Script complementaire au pipeline pour synchroniser les 19 doublons cross-app EM <- Patrimoine. Sync les champs canoniques :
- lat, lon
- gps_locked, gps_lock_reason, gps_audit, gps_source
- commune_nom, doyenne_contemporain_slug, pieve_slug

Premier run (post-Brief 39octies + Brief 39nonies) : 10 divergences detectees, propagees. Causes :
- Champs doyenne_contemporain_slug/pieve_slug ajoutes plus tard cote Patrimoine, pas propages a EM (8 cas)
- Coords micro-divergences post-corrections recentes Patrimoine (barrage_alesani, monte_san_petrone)

Verification post-apply : 0 divergence.

## D2 - audit polygone Cortenais : conclusion

### Cas Code 39octies (3 sites signales)

| Slug | Coords | Doyenne declare | Polygone(s) contenant | Resultat |
|---|---|---|---|---|
| monte_san_petrone | (42.3961, 9.3269) | doyenne_du_golo | doyenne_du_golo | OK coherent |
| casteddu_bastelica | (42.217, 9.255) | doyenne_cortenais | doyenne_cortenais | OK coherent |
| casa_di_u_banditu | (42.5443, 8.9348) | doyenne_balagne | doyenne_balagne | OK coherent |

**L'hypothese Code "polygone Cortenais s'etend trop sur la haute vallee" est INVALIDEE par le data actuel**. Les 3 cas signales sont coherents avec leurs polygones respectifs.

### Audit complet 449 sites Patrimoine

Reverse-geo de chaque site contre les 9 polygones doyennes :

| Statut | Count |
|---|---|
| Coherent (declare = polygone) | 382 |
| **DIVERGENT** (declare != polygone) | **1** |
| HORS polygone (sites cote/ilots/orphans) | 8 |
| NULL declare mais polygone existe | 58 |

### 1 vrai DIVERGENT detecte

`santa_maria_della_neve_grosseto_prugna_basse` (que j'ai diverge Brief 39nonies vers 41.9095/8.803) :
- Declare : doyenne_prunelli_taravo_valinco
- Geo : doyenne_ajaccio
- Cause : coords approximatives Brief 39nonies positionnent le site dans la zone Ajaccio peripherique au lieu de Grosseto-Prugna village reel

### Decision Soleil + action D2

> "Renommer en saint_cesaire_grosseto_prugna + coords centre village"

Justification web : "Santa Maria della Neve" non confirme a Grosseto-Prugna. La vraie eglise romane XIe est **Saint Cesaire** (centre village). Source : Wikipedia, intramuros, mairie Grosseto-Prugna.

Action appliquee :

| Champ | Avant | Apres |
|---|---|---|
| slug | santa_maria_della_neve_grosseto_prugna_basse | saint_cesaire_grosseto_prugna |
| nom | (vide) | Eglise Saint-Cesaire de Grosseto-Prugna |
| lat | 41.9095 | 41.8536 (centre village Grosseto-Prugna selon Wikipedia FR) |
| lon | 8.803 | 8.7933 |
| description | "Eglise romane - Cote golfe Ajaccio - Distincte tour Capitello..." | "Eglise romane XIe siecle - Joyau architectural Grosseto-Prugna - Centre village 400m altitude - Pieve de l'Ornano - Vitrail mosaique Smalti, Vierge polychrome XVIIe, Vierge de marbre XVe" |
| doyenne_contemporain_slug | doyenne_prunelli_taravo_valinco | doyenne_prunelli_taravo_valinco (confirme par reverse-geo) |
| pieve_slug | pieve_ornano | pieve_ornano (confirme par reverse-geo) |
| gps_locked | True (Brief 39nonies) | True (Brief 39decies) |

### 8 HORS_POLY (sites cote/ilots/orphans, deja connus)

Tous sont des cas Cat. 1 (sites en mer) ou orphans Brief 36 R5 :
- couvent_sant_antoni_de_calvi (Calvi peripherie)
- santa_maria_assunta_ajaccio_bazzicacce (Bazzicacce hors centre Ajaccio)
- tour_d_omigna_cargese (Cat. 1 site en mer)
- tour_de_capitello_castelluccio (orphan residuel)
- tour_de_capo_di_muro (RESCUE_ABSENT Code C6)
- tour_de_giraglia_ilot (Cat. 1 ilot Cap Corse)
- tour_de_la_chiappella_rogliano (Cat. 1 site en mer)
- menhirs_du_rizzanese (cree Brief 39septies, coords approx)

Aucune action D2 (deja sur la liste audit terrain Soleil).

### 58 NULL_DECL (doyenne_contemporain_slug=null)

Sites avec coords + polygone valide mais doyenne_contemporain_slug non renseigne. Bonne cible pour un brief futur "bulk fill doyenne_contemporain_slug via reverse-geo". A faire si Soleil le souhaite.

## Garde-fous

- Tous sites Briefs 38-39nonies non concernes inchanges
- 77 sites locked (-1 santa_maria_della_neve_grosseto_prugna_basse renomme = nouveau slug saint_cesaire_grosseto_prugna +1 lock = net 0)
- JSON valide post-Brief 39decies (ce snapshot)
- Backup auto sync_cross_app : `_drafts/sites_em.backup_sync_cross_app_2026-05-07.json`

## Fichiers livres

- `scripts/sync_cross_app.py` - nouveau script sync EM <- Patrimoine
- `docs/data/sites_patrimoine.json` - D3 + D2 appliques (worktree distracted-cohen)
- `docs/data/sites_em.json` - 10 sites synces depuis patrimoine
- `_drafts/sync_cross_app_log_2026-05-07.md` - log apply
- `_drafts/sites_em.backup_sync_cross_app_2026-05-07.json` - backup pre-sync
- `fiches_patrimoine/RAPPORT_BRIEF_39decies_D2_sync_2026-05-07.md` - ce rapport

## Recommandations futures

1. **Lancer sync_cross_app.py apres chaque pipeline brief** pour eviter divergence cumule
2. **Brief futur "bulk doyenne_contemporain_slug"** : 58 sites NULL_DECL a remplir auto
3. **Ne pas ressuscister l'hypothese "Cortenais deborde"** : data actuel confirme polygone OK

## Commande git pour Code (consolidee D1+D3+D2+sync)

```
git checkout -b feat/brief-39decies-D1-D2-D3-sync && \
git add docs/data/sites_patrimoine.json \
        docs/data/sites_em.json \
        docs/data/CROSS_APP_DOUBLONS.md \
        scripts/sync_cross_app.py \
        fiches_patrimoine/RAPPORT_BRIEF_39decies_D3_2026-05-07.md \
        fiches_patrimoine/RAPPORT_BRIEF_39decies_D2_sync_2026-05-07.md \
        _drafts/sync_cross_app_log_2026-05-07.md \
        _drafts/sites_em.backup_sync_cross_app_2026-05-07.json && \
git commit -m 'data+chore(corpus): Brief 39decies — D1 doc cross-app + D2 audit polygones + D3 Monte Revincu + sync_cross_app.py' && \
git push -u origin feat/brief-39decies-D1-D2-D3-sync
```
