# feedback-003 — Évaluation itération 3 (réponse à feedback-002)

> Session ÉVALUATEUR (Cowork, fraîche), 2026-06-10. Note l'it. 3 contre `contrat.md`
> (rubrique §5.2 transposée LANGUE) + suivi des reproches de feedback-002. Critique seule,
> ne corrige pas. Posture sévère (PROTOCOLE §2).

## Verdict

**Score pondéré : 8.0 / 10 → PASSE largement.** Trajectoire : 7.6 (it.1) → 7.2 (it.2) → **8.0 (it.3)**.
Le reproche central de feedback-002 — la sur-revendication des flexions présentées comme
attestation directe — est **structurellement corrigé** : statut dédoublé `vérifié` (forme exacte
listée) vs `vérifié (flexion)` (flexion régulière d'un lemme attesté, SOURCE = `flexion: <id>`).
Le « 217 vérifié » gonflé devient **145 direct + 72 flexion**, honnête. Reste **un défaut de
précision résiduel** dans le re-test (non bloquant) : voir §Réserve.

## Suivi des reproches de feedback-002

| # | Reproche | État |
|---|---|---|
| 1 | Flexions mappées sur l'id du lemme, non rejouables, présentées comme directes | **CORRIGÉ.** `vulete`(52311), `mittite`(28308), `entrite`(16109), `lasciate`(25130) → désormais `vérifié (flexion)` (vérifié : rejeu exact = vide, classement correct). SOURCE affiche `flexion: <id>`, plus d'attestation directe implicite. |
| 2 | Raison du flag `statu` sur le 1er résultat seul | **CORRIGÉ.** Note reformulée : « 1re entrée 46249 = bustier ; des formes statu/statutu peuvent exister par ailleurs — sens à confirmer ». |
| 3 | Résidus `skip_extra` | **CORRIGÉ pour les mots de contenu.** `altru`→DIRECT 2511, `aperta`→FLEXION d'`apertu` 3522. Skip ne garde que du grammatical (`sarà`, `vostra`). |

## Checks falsifiables exécutés

| Check | Résultat |
|---|---|
| Scripts rejoués | OK — **145 vérifié / 72 vérifié(flexion) / 89 flaggé / 1 à confirmer**, 307 total. 261 direct + 106 inferred + 79 flags. |
| 307/307 + FR intact | OK (`app.html` non modifié). |
| Chevauchement verified∩inferred∩flags | **aucun** (3 paires testées). |
| Guillemets courbes app.html | aucun. |
| Rejeu INFCOR `vérifié`(direct) — formes-lemmes & listées | `apre`→3982 ✓, `tubatura`→54019 ✓, `fonti`→18021 ✓ (def « fonte fonti », forme listée), `altru`→2511 ✓. |
| Rejeu INFCOR `vérifié (flexion)` | `vulete`/`mittite`/`entrite`/`lasciate`/`aperta` → vide/forme non listée par exact → classement flexion **correct**. |
| **Rejeu DIRECT « à risque » (pluriels)** | **`campi` (DIRECT 54907) : exact renvoie 8228/8223… PAS 54907.** **`siti` (DIRECT 44828) : exact renvoie 43797 « sete/soif », PAS 44828.** → **2 mauvais classements DIRECT résiduels.** |

## Réserve — défaut de précision du re-test (non bloquant)

Le re-test it. 3 semble avoir marqué `DIRECT` dès que la requête exacte renvoyait **une réponse
non vide**, sans vérifier que l'`unique` renvoyé **== l'id assigné**. Conséquence : les flexions
qui *préfixent* un autre mot (rappel : `part=first` = match par **préfixe**) passent DIRECT à tort :

- `campi` (pluriel de `campu` 54907) → la requête renvoie `campià`/`campione` (8228, 8223…), pas 54907.
- `siti` (pluriel de `situ` 44828) → renvoie `sete/seti/siti` 43797 (« soif »), mot sans rapport.

Ces formes devraient être `vérifié (flexion)` de leur lemme, pas `DIRECT`. Périmètre estimé :
**14 formes DIRECT partagent l'id d'une autre forme** (cf. audit) ; 6 sont des variantes à article
élidé (`l'invisibile`, `un'osservazione`… — inoffensives), les ~8 autres sont des
pluriels/féminins à vérifier (`campi`, `siti` confirmés faux ; `corsa`, `tecnica`, `publiche`,
`rete`, `materiale`, `capisce` à contrôler — certains *peuvent* être des formes réellement listées,
comme `fonti`). C'est une **imprécision de classement**, pas une invention : le lemme et le sens
restent corrects, seul le label direct/flexion est trop optimiste sur ~2-8 formes.

## Notes par critère

- **Couverture — 8.0 (0.25).** Statuage complet, 1 seul « à confirmer ». Le dédoublement ne perd pas de couverture, il l'honnêtise.
- **Qualité & fiabilité sources — 7.5 (0.25).** Re-test exact-form adopté (bien). Mais critère d'acceptation trop lâche (non-vide ≠ id concordant) → `campi`/`siti` DIRECT à tort.
- **Traçabilité — 7.5 (0.15).** SOURCE distingue désormais `flexion: <id>` — gros progrès. Résiduel : 2+ DIRECT citent un id qui ne renvoie pas leur forme exacte.
- **Honnêteté anti-hallucination — 8.5 (0.20).** Le biais central est corrigé ; 145 directs honnêtes vs 217 gonflés. Résidu `campi`/`siti` de bonne foi, mineur.
- **Défendabilité dossier — 9.0 (0.15).** La distinction explicite direct/flexion **renforce** la défendabilité FEDER (on montre précisément ce qui est attesté vs inféré). Bêta, FR fait foi, native review fléchée.

**Calcul :** 8.0·0.25 + 7.5·0.25 + 7.5·0.15 + 8.5·0.20 + 9.0·0.15 = **8.0 / 10**.

## Correction (optionnelle, it. 4 si souhaité — sinon clôture)

Une seule, mécanique : dans le re-test, exiger **`unique` renvoyé == id assigné** (et idéalement
que le token exact figure dans le `def` de l'entrée) avant de classer `DIRECT` ; sinon → `vérifié
(flexion)`. Cela reclasserait `campi`, `siti` et confirmerait/corrigerait les ~6 autres formes à id
partagé. Gain attendu : Qualité-sources et Traçabilité → ~8.5 global. Aucun risque pour le natif
si non fait (il tranche de toute façon), d'où le caractère **non bloquant**.

## Suite protocole

Score ≥ seuil sur 3 itérations avec **trajectoire ascendante saine** (pas de plateau, le creux
it. 2 était dû à une sur-extension, corrigée). Le chantier est **mûr pour clôture** : produire
`RAPPORT_FINAL.md` (verdict 8.0, livrables, hors-scope = relecture native budgétée), puis relais
Code (branche → PR `dev`, pas d'auto-merge) tel que décrit dans `RELAIS_CODE.md`. La correction
optionnelle ci-dessus peut être faite avant la PR ou laissée au natif — au choix de Soleil.
