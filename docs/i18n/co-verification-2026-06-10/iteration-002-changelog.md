# Itération 002 — réponse du GÉNÉRATEUR au feedback-001

> Le générateur relit feedback-NNN.md et reprend la production (PROTOCOLE §4).
> Ce fichier documente ce qui a changé. Le générateur ne note pas son travail —
> la re-notation revient à l'évaluateur (feedback-002.md).

## Reproches traités

### 1. BLOQUANT — `merria` faux négatif (corrigé)
`merria` était flaggé « non attesté » sur la foi d'une requête du **radical** `merra`
(= houe). La requête sur la **forme exacte** `merria` renvoie l'entrée INFCOR **id 27910 =
« mairie » (n.f. pl. merrie)**. Corrigé : `merria`/`merrie` retirés des flags, ajoutés aux
formes vérifiées (27910).

**Généralisation demandée par l'évaluateur — faite** : re-test de **tous** les flags « absent »
par forme EXACTE (via l'outil navigateur, `web_fetch` étant rate-limité). Résultat : `merria`
était le **seul** faux négatif ; `faglia`, `gradiente`, `intonacu`, `bluchettu`, `generà`,
`prutoni`, `acquisizione` re-confirmés absents par forme exacte. Le re-test a aussi révélé des
**faux négatifs/sens non détectés en passe 1** désormais flaggés (`statu` = « bustier » et non
« statut » → faux-sens ; `sensore`, `betone`, `staticu`, `ozzionale`, `emettitori`… absents).

### 2. `skip_extra` absorbait des mots de contenu (corrigé)
Les verbes mis à tort en `skip` (`vulete`, `apre`, `entrite`, `lasciate`, `adopra`,
`aduprata`, `attivate`…) en ont été retirés et **vérifiés individuellement** :
`vulè` 52311, `apre` 3982, `entre` 16109, `lascià` 25130, `adoprà` 21539, `attivà` 5229,
`mette` 28308, `nutà` 3236, `stabule` 46551, `nome` 30925. `skip_extra` ne contient plus que
des mots-outils, acronymes, marques, unités et emprunts.

### 3. Couverture (étendue)
La méthode navigateur (non rate-limitée, écriture des résultats dans le DOM) a permis de
vérifier l'essentiel du lexique restant. **Avant : 68 vérifié / 25 flaggé / 214 à confirmer.
Après : 217 vérifié / 89 flaggé / 1 à confirmer** (365 formes vérifiées, 79 motifs de flag).
La seule chaîne « à confirmer » porte sur le sens « corsi d'acqua » (cours d'eau).

## Garde-fous (inchangés / re-vérifiés)
- **FR intact** : clés + colonne FR identiques à `HEAD:app.html` (contrôle auto, re-passé).
- **Aucune valeur inventée** : les 89 flaggées conservent la proposition du modèle, marquée
  NON VÉRIFIÉE ; les formes régulières non lemmatisées sont signalées comme telles (et non
  présentées comme attestées).
- `app.html` toujours non édité (bandeau via relais Code).

## Note d'honnêteté pour l'évaluateur
La hausse de « flaggé » (25 → 89) n'est pas une régression : le re-test par forme exacte a
**augmenté la sévérité** (beaucoup de termes techniques/scientifiques et de formes dérivées ne
sont pas dans une base de langue générale comme INFCOR). C'est conforme à la doctrine :
non confirmable → flaggé, jamais deviné. Un contrôle natif + terminologie Cunsigliu/CdC reste
l'étape qualifiée.
