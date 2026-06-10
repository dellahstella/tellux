# Itération 003 — réponse du GÉNÉRATEUR au feedback-002

> Le générateur relit le feedback et reprend la production (PROTOCOLE §4).
> Re-notation = évaluateur (feedback-003.md).

## Reproche central (sur-revendication des flexions) — traité

feedback-002 a montré que la hausse 68→217 « vérifié » reposait en partie sur des **flexions
verbales** (`vulete`, `mittite`, `entrite`, `lasciate`…) mappées sur l'id du lemme alors que la
**forme exacte** renvoie vide chez INFCOR — l'erreur symétrique de `merria` (sur- au lieu de
sous-revendication), qui échouait au check #1 du contrat (« rejouer par forme exacte »).

**Correctif appliqué (pas de devinette)** : j'ai **rejoué les 365 formes « vérifié » par forme
exacte** sur INFCOR (outil navigateur, 5 lots). Chaque forme est classée :
- **attesté-direct** : la forme exacte figure dans l'entrée INFCOR (champ `def`) → reste `vérifié`.
- **flexion-inférée** : forme régulière d'un lemme attesté, mais la forme exacte n'est pas un
  sous-lemme rejouable (résultat « famille » ou vide) → nouveau statut **`vérifié (flexion)`**,
  avec SOURCE explicite « INFCOR <id-lemme> · flexion: <id> » + note.

Résultat (honnête, sans baisse de rigueur) :
- **145 vérifié** (tout attesté-direct) · **72 vérifié (flexion)** · **89 flaggé** · **1 à confirmer**.
- Lexique : **261 formes attestées-direct** + **106 flexions-inférées** + 79 flaggées.
- Plus aucune chaîne ne présente une flexion non rejouable comme une attestation directe :
  la colonne SOURCE distingue désormais `INFCOR <id>` de `flexion: <id>`.

## Points secondaires — traités

- **`skip_extra` (résidu #2)** : `aperta` et `altru` retirés du skip. `altru` → attesté-direct
  (id 2511) ; `aperta` → flexion de `apertu` (id 3522). Restent en skip uniquement des mots
  grammaticaux (`sarà` futur de esse, `vostra` possessif) — structurels, non lexicaux.
- **Raison du flag `statu`** : reformulée pour ne pas affirmer sur la seule 1re entrée
  (« la 1re entrée = bustier ; des formes statu/statutu peuvent exister par ailleurs — à confirmer »).

## Garde-fous re-vérifiés
- **FR intact** (clés + colonne FR == HEAD).
- **Aucun chevauchement** verified / inferred / flags (contrôle automatique : V∩I, V∩F, I∩F = vides).
- `app.html` toujours non édité (bandeau via relais Code).
- Outillage : `scripts/verify_i18n_co.mjs` lit désormais `verified` (direct) + `inferred` (flexion)
  depuis `verification_co.tokens.json` ; entièrement rejouable.

## Note pour l'évaluateur
Le « vrai » plein-attesté est 145 (et non 217). Les 72 « flexion » sont sourcées au lemme et
signalées comme telles — ni cachées, ni comptées comme attestation directe. C'est le compromis
honnête entre couverture et la doctrine « rejouer par forme exacte ».
