# Plan de renommages et refontes des pièves Tellux

**Date** : 2026-05-17
**Statut** : arbitrages Soleil **actés 2026-05-17** (4 reco Cowork validées + arbitrage complémentaire)
**Référence doctrinale** : `ADR-001-pieves-doctrine.md`
**Source audit** : 47 pièves de `docs/data/pieves_polygons.json` + 541 sites de
`docs/data/sites_patrimoine.json`

---

## AMENDEMENT 2026-05-17 — exécution en session Code

État data au moment de l'exécution : **45 pièves** (pas 47 ; `pieve_campoloro` + `pieve_verde_PTV` supprimés post-rédaction de ce plan). Suite à la vérification de cohérence pré-rename par Code :

- **A1 `pieve_verde`** : décision révisée SUPPRESSION → **CONSERVATION (option C)**. Le polygone est valide (Bavella/Zonza/Levie sud) et 9 sites le référencent — pas une entrée fantôme. Actions : `diocese_medieval=Aleria` + retag 2 sites mistagged vers `pieve_carbini` + 2 sites côte est conservés (dette `PATRIMOINE-PIEVE-VERDE-COTE-EST-NON-RATTACHEE-001`).
- **R-1 `pieve_bastia` → `pieve_lota`** : **ANNULÉ Phase 1 beta**. `pieve_bastia` actuel = 1 commune (Bastia ville), Lota historique exclut explicitement Bastia ville. Rename aurait été factuellement faux. Dette `PIEVE-BASTIA-PERIMETRE-RESIDUEL-001` ouverte pour refonte post-FEDER.
- **R-4 `pieve_mariana` → `pieve_piana_di_mariana`** : **ANNULÉ Phase 1 beta**. `pieve_mariana` actuel = 24 communes (plaine + Castagniccia), pas 8 attendues. Rename trompeur sur le périmètre étendu. Problème = redécoupage, pas rename. Déféré post-FEDER. Dette `PATRIMOINE-PIEVE-MARIANA-MEGA-FUSION-001` amendée.
- **R-3 `pieve_ajaccio` → `pieve_gulfo_d_aiacciu`** : **EXÉCUTÉ** (commit `6b5d461`). 11 sites retag, alias hash en place (commit `73b6aae`).
- **A+ ghost `pieve_sartene_plaine_orientale`** : **DÉJÀ RÉSOLU dans dev** avant exécution. `castidetta` tagué `pieve_sartene` correctement, slug fantôme absent.

`pieve_aliases.json` final ne contient qu'**1 entrée** (`pieve_ajaccio` → `pieve_gulfo_d_aiacciu`) au lieu des 3 prévues.

---

## 0. Note sur le brief amont

Le brief Cowork mentionne *« pieve_mariana = agrégat post-fusions
(caccia → giovellina → mariana), doyenne_majoritaire calculé = cortenais »*.

**Vérification factuelle** des données prod le 2026-05-17 :

- `pieve_caccia` et `pieve_giovellina` existent toujours **comme pièves
  distinctes** (Sagone, doyenne_cortenais) ;
- les transferts v2 documentés dans `pieves_polygons.json` envoient
  `caccia` et `giovellina` vers `pieve_talcini`, **pas vers `pieve_mariana`** ;
- `pieve_mariana` a au contraire **perdu** 6 communes au profit de
  `pieve_casacconi` ;
- `pieve_mariana` actuel : 8 sites, communes Lucciana (3), Borgo (2),
  Bastia (1), Furiani (1), Poggio-d'Oletta (1) ; doyenné majoritaire des
  sites = **`doyenne_du_golo`** (7/8), pas cortenais.

Le territoire actuel de `pieve_mariana` est donc **cohérent géographiquement**
(plaine de Mariana + frange nord). Le problème identifié est un **problème
de nom**, pas de découpage : collision avec le diocèse Mariana et avec le
site archéologique romain de Mariana près de Lucciana. Cf. section 2.3.

Si Soleil parlait d'une version antérieure (avant le mapping v2 Brief 17),
le diagnostic visait la bonne intuition mais la donnée a déjà bougé.

---

## 1. Phase QW — Quick Wins mécaniques (N1→N5)

À exécuter en bloc, sans arbitrage. Aucun renommage de slug, aucun
retag de sites. Risque nul sur les hash URL et les liens externes.

### QW-1 — Régénérer le compteur de stats

Dans `pieves_polygons.json`, `stats.pieves_count` annonce 44 ; la liste
contient 47. Régénérer via `scripts/build_pieves_polygons.py` ou patcher
manuellement à 47. Vérifier aussi `total_communes` (360 annoncé), à
recalculer.

### QW-2 — Corriger le mojibake d'affichage

```
pieve_sartene    : name "SartÃƒÆ'Ã‚Â¨ne"   → "Sartène"
pieve_sorroinsu  : name "SorroinsÃƒÆ'Ã‚Â¹" → "Sorroinsù"
```

Source probable du bug : double encodage CP1252 → UTF-8 dans le mapping
amont. À refixer dans la source, pas seulement dans le JSON dérivé.

### QW-3 — Renseigner `diocese_medieval` pour les 3 pièves orphelines

```
pieve_cauro   → "Ajaccio"
pieve_talavo  → "Ajaccio"
pieve_verde   → "Aleria"   (cohérent avec son polygone réel et avec sa
                            mention dans la déclaration v2)
```

Référence Casta : les trois relèvent du Sud médiéval (Ajaccio pour les deux
premières, Aleria pour Verde).

### QW-4 — Décider du sort de `pieve_verde`

Deux options :
- **(a)** la supprimer : 0 commune, 0 site, entrée fantôme. Mais le
  polygone existe peut-être encore et représente une portion de territoire
  réelle (rive droite du Tavignano).
- **(b)** la réhydrater : compléter son mapping communal et son tag site.

`[ARBITRAGE 1]` — supprimer ou réhydrater ? Recommandation Cowork :
**(a) suppression** si Phase 1 beta ; **(b) réhydratation** si Tellux
ambitionne une couverture exhaustive du sud-est dans la Phase 2 patrimoine.

### QW-5 — Normaliser le préfixe « Pieve di / d' »

8 entrées portent le préfixe dans `name`, 39 non. Conformément à
l'ADR-001 §2.4.4, le **préfixe est retiré partout** dans `name` :

```
"Pieve di Mezzana"   → "Mezzana"
"Pieve di Celavo"    → "Celavo"
"Pieve di Tavagna"   → "Tavagna"
"Pieve di Casacconi" → "Casacconi"
"Pieve di Filosorma" → "Filosorma"
"Pieve di Luri"      → "Luri"
"Pieve di Talcini"   → "Talcini"
"Pieve d'Aleria"     → "Aleria"   (devient redondant avec le diocèse :
                                    cf. R4 ci-dessous, renommage à acter)
```

Les slugs `pieve_*` restent inchangés. Seul le `name` d'affichage bouge.

---

## 2. Phase R — Renommages substantiels

Ces renommages **touchent des slugs**, donc retag des sites et alias hash
URL (cf. ADR-001 §2.5).

### R-1 · `pieve_bastia` → `pieve_lota`  [PROPOSÉ]

**Pourquoi** : Bastia est fondée fin XIVᵉ par les Génois, n'existe pas
comme pieve médiévale Casta. Le territoire (6 communes du sud du Cap)
correspond à la **Pieve di Lota**.

**Périmètre** : inchangé.

**Effet collatéral** : `doyenne_majoritaire_reclassed` du JSON note déjà
que `pieve_bastia` est polygonalement dans `doyenne_du_cap`, pas dans un
hypothétique `doyenne_de_bastia` (qui n'existe pas comme doyenné contemporain
de toute façon). Renommage cohérent.

**Site impacté** : 1 site `pieve_mariana` est en commune de Bastia, ce qui
suggère que Bastia-ville est partagée entre `pieve_lota` (cap, nord) et
`pieve_mariana` (plaine, sud). À vérifier au moment du retag.

### R-2 · Cas `pieve_bonifacio` ↔ `pieve_freto`  [ARBITRAGE 2]

**Situation actuelle** :

```
pieve_bonifacio  10 communes, doy=doyenne_extreme_sud
pieve_freto      14 communes, doy=doyenne_extreme_sud, 14 sites
```

Les deux cohabitent dans le même doyenné, alors que Freto est historiquement
le nom de la pieve médiévale qui contient Bonifacio. Trois options :

- **(2a) Fusion** `pieve_bonifacio` → `pieve_freto`, on ne garde que Freto.
  Plus historique, plus simple, mais on perd la lisibilité « Bonifacio »
  pour le grand public.

- **(2b) Renommer** `pieve_bonifacio` en `pieve_bonifacio_freto` ou
  `pieve_freto_bonifacio` (composé géo lisible). Garde les deux logiques.
  Mais redondance avec `pieve_freto` voisin si on garde aussi celui-ci.

- **(2c) Statu quo** : on assume que `pieve_bonifacio` représente la zone
  urbaine + littorale et `pieve_freto` l'arrière-pays rural. C'est défendable
  géographiquement. À documenter dans le JSON par un champ
  `note_decoupage` pour ne pas refaire le débat dans 3 mois.

`[ARBITRAGE 2]` — Recommandation Cowork : **(2c) statu quo + note**.
Bonifacio est trop reconnu pour disparaître, et la séparation ville/arrière-pays
a un sens pédagogique.

### R-3 · `pieve_ajaccio` → ?  [ARBITRAGE 3]

**Situation actuelle** :

```
pieve_ajaccio  12 communes, doy=doyenne_ajaccio, 12 sites, diocese Ajaccio
```

Collision triple : nom de ville moderne + nom de diocèse + nom de doyenné.
Casta ne reconnaît pas une pieve « Ajaccio » ; le bassin ajaccien est
historiquement éclaté entre Mezzana (déjà existante, 5 communes), Cinarca
(déjà existante, 8 communes) et la commune-territoire d'Ajaccio.

Trois options :

- **(3a) Redécouper** : absorber les 12 communes dans `pieve_mezzana`,
  `pieve_cinarca`, `pieve_celavo`. Plus orthodoxe, mais nécessite un
  vrai re-mapping communal et casse 12 sites.

- **(3b) Renommer en `pieve_gulfo_d_aiacciu`** (ou `pieve_golfe_d_ajaccio`) :
  garde le territoire actuel, lève la collision avec le diocèse. Conserve
  la lisibilité grand public.

- **(3c) Renommer en `pieve_aiacciu`** (graphie corse) : lève partiellement
  la collision (lecteur sait qu'on parle de la ville, pas du diocèse latin)
  mais reste ambigu pour un lecteur francophone.

`[ARBITRAGE 3]` — Recommandation Cowork : **(3b) `pieve_gulfo_d_aiacciu`**.
Géographique, lisible, casse la collision proprement. Le retag est mécanique
(12 sites).

### R-4 · `pieve_mariana` → ?

Le territoire actuel (Lucciana + Borgo + Furiani + Poggio-d'Oletta, plus 1
site à Bastia) est cohérent et correspond à la **plaine alluviale du
Golo / Tavignano nord**.

Le **problème** est le nom :
- collision avec le diocèse `Mariana` ;
- collision avec le site archéologique romain de Mariana (Canonica) ;
- pieve sera demain accolée à une pieve patrimoniale dédiée au site lui-même.

Trois options motivées :

- **(4a) `pieve_marana`** : graphie italienne archaïque, lève à peine la
  collision visuelle, peu lisible pour un non-spécialiste.

- **(4b) `pieve_piana_di_mariana`** ou `pieve_plaine_de_mariana` : descriptif,
  très lisible, casse la collision diocèse/site. Recommandation Cowork.

- **(4c) `pieve_lucciana_borgo`** : toponymes contemporains des deux plus
  grosses communes du territoire. Très lisible mais perd la charge
  historique. Risque : si Bastia commune entre dans le périmètre, le nom
  devient trompeur.

`[ARBITRAGE 4 — informel]` — Recommandation Cowork : **(4b) `pieve_piana_di_mariana`**
(graphie italo-corse stable, lisible CTC et grand public).

Soleil m'avait demandé une proposition motivée ; je n'en fais pas un
arbitrage bloquant, mais c'est mon choix par défaut si tu ne tranches pas
autrement.

### R-5 · Collisions slug ↔ diocèse résiduelles  [PARTIEL]

Après R-3 et R-4, il reste deux collisions :

```
pieve_aleria   (Pieve d'Aleria, 10 communes) ↔ diocèse Aleria
pieve_nebbiu   (Nebbiu, 30 communes)         ↔ diocèse Nebbiu
```

- **`pieve_aleria`** : le territoire correspond à la pieve médiévale
  d'Aleria (basse plaine orientale, ancienne capitale romaine). Suggestion :
  `pieve_aleria_centro` ou `pieve_aleria_basse` pour distinguer clairement.
  Pas bloquant Phase 1 si on assume la collision.

- **`pieve_nebbiu`** : Nebbiu est à la fois le diocèse médiéval et la
  microrégion contemporaine (Saint-Florent / Patrimonio). Le diocèse Nebbiu
  ne contient qu'une seule pieve dans le JSON (`pieve_nebbiu` elle-même).
  Soit on découpe Nebbiu en pièves Casta (Patrimonio, Tegime, Canari…),
  soit on accepte que Nebbiu = mini-diocèse à 1 pieve. Cf. ADR-001 §4 :
  **déféré Phase 2**.

**Décision Phase 1 beta** : on traite R-5 après FEDER, on documente la
collision dans le JSON via `note_collision_slug`.

---

## 3. Phase D — Redécoupages

### D-1 · Déséquilibre des doyennés (9 vs 2)

`doyenne_balagne` n'a que 2 pièves (Balagne 46 communes + Filosorma 3) ;
`doyenne_cortenais` en a 9. **Pas d'action Phase 1 beta** : on assume
l'asymétrie et on l'explique en méthodologie.

Post-FEDER, redécoupage envisageable de Balagne en 2-3 sous-pièves
(Balagne Déserte, Balagne Aregno, Balagne Pino-Tuani).

### D-2 · `pieve_balagne` (46 communes) trop grosse

Statut idem D-1. **Déféré post-FEDER.**

### D-3 · 3 reclassifications polygonales forcées

```
pieve_bastia    declared=doyenne_de_bastia       actual=doyenne_du_cap
pieve_verde     declared=doyenne_prunelli...     actual=doyenne_extreme_sud
pieve_vivario   declared=doyenne_ajaccio         actual=doyenne_cortenais
```

Action minimale Phase 1 beta : **aligner les `declared` sur les `actual`**
dans le mapping amont (`_drafts/pieves_communes_mapping_v2_canonicite_casta.json`)
puis régénérer. Le JSON dérivé suivra.

`doyenne_de_bastia` n'existe pas comme doyenné contemporain, c'est
probablement un résidu de mapping. À nettoyer en même temps que R-1
(qui renomme la pieve elle-même).

---

## 4. Phase ALIAS — Stabilité des hash URL

Per ADR-001 §2.5, tout renommage de slug introduit une entrée dans
`docs/data/pieve_aliases.json` :

```json
{
  "version": "v1",
  "generated": "2026-05-17",
  "aliases": {
    "pieve_bastia":   "pieve_lota",
    "pieve_ajaccio":  "pieve_gulfo_d_aiacciu",
    "pieve_mariana":  "pieve_piana_di_mariana"
  }
}
```

`patrimoine.html` consomme ce fichier dans `applyHash` initial : si le hash
contient un ancien slug, on redirige vers le nouveau sans casser le partage.

Le fichier d'alias est cumulatif (jamais purgé) jusqu'à la refonte post-FEDER.

---

## 5. Récapitulatif des arbitrages demandés

| Réf            | Question                                       | Décision actée 2026-05-17                                      |
|----------------|------------------------------------------------|----------------------------------------------------------------|
| `[ARBITRAGE 1]`| `pieve_verde` : supprimer ou réhydrater ?      | **Supprimer** (Phase 1 beta)                                   |
| `[ARBITRAGE 2]`| `pieve_bonifacio` vs `pieve_freto`             | **Statu quo + `note_decoupage`** dans le JSON                  |
| `[ARBITRAGE 3]`| Nouveau nom pour `pieve_ajaccio`               | **`pieve_gulfo_d_aiacciu`**                                    |
| `[ARBITRAGE 4]`| Nouveau nom pour `pieve_mariana`               | **`pieve_piana_di_mariana`**                                   |
| `[ARBITRAGE +]`| Ghost slug `pieve_sartene_plaine_orientale`    | **Retag mécanique** du site `castidetta` (à pieve_taravo ou cohérente intérieur Cozzano — Code arbitre géo) |
| Implicite R-1  | `pieve_bastia` → `pieve_lota`                  | **Acté** (reco Cowork validée)                                 |

Code peut donc dérouler les **Phases QW, D-3, R, ALIAS, déférée DOC**
dans l'ordre du §6 ci-dessous, sans nouvel arbitrage.

---

## 6. Ordre d'exécution recommandé

```
1. Phase QW (N1→N5)                — mécanique, ~1h Code
2. Phase D-3 (re-alignement v2)    — ~30 min Code
3. Arbitrages ARBITRAGE 1-4        — Soleil
4. Phase R (renommages actés)      — ~2h Code + retag sites + aliases
5. Phase D-1, D-2, R-5             — DÉFÉRÉ post-FEDER
```

---

**Suite** : `PIEVES_REFACTOR_EXEC_CODE_2026-05-17.md` — liste exécutable
détaillée à destination de Claude Code.
