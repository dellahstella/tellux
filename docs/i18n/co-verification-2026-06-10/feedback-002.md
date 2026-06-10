# feedback-002 — Évaluation itération 2 (réponse à feedback-001)

> Session ÉVALUATEUR (Cowork, fraîche), 2026-06-10. Note la production it. 2 du générateur
> contre `contrat.md` (rubrique §5.2 transposée LANGUE) et le suivi des 3 reproches de
> feedback-001. Critique uniquement, ne corrige pas. Posture sévère (PROTOCOLE §2).

## Verdict

**Score pondéré : 7.2 / 10 → au-dessus du seuil (7.0). PASSE.**
**Mais léger recul vs it. 1 (7.6).** L'itération a corrigé le bug bloquant (`merria`) et étendu
massivement la couverture — c'est du vrai progrès. Le revers : pour gonfler la couverture, la
norme « vérifié » a glissé. Un sous-ensemble des nouvelles formes « vérifié » sont des **flexions
verbales mappées sur l'id du lemme qui ne se rejouent PAS par forme exacte** — c'est l'erreur
**symétrique** de `merria` (sur-revendication au lieu de sous-revendication), et elle échoue
au check #1 du contrat. À corriger avant la remise au natif et avant tout merge.

## Suivi des 3 reproches de feedback-001

| # | Reproche | État |
|---|---|---|
| 1 | **Bloquant `merria`** (faux négatif) | **CORRIGÉ.** `merria`/`merrie` → `vérifié` id 27910 (rejoué OK). `nav_mairies`, `footer_mairies` désormais `vérifié`. Bon réflexe : le re-test par forme exacte des flags « absent » a aussi durci la passe (`statu` faux-sens, `sensore`, `betone`, `staticu`… ajoutés). |
| 2 | **Mots de contenu dans `skip_extra`** | **~80 %.** `apre`/`entrite`/`lasciate`/`adopra`/`vulete`/`aduprata` sortis du skip. Mais restent skippés des mots de contenu : `aperta`, `sarà`, `mumentu`, `rimette` (+ `vostra`/`altru`, plus grammaticaux). **2 chaînes `vérifié` reposent encore sur `aperta` skippé** : `cform_note_ph`, `geo_check1`. |
| 3 | **Couverture** | **Fortement étendue** (68→217 vérifié, 1 à confirmer) — mais voir réserve majeure ci-dessous sur la *qualité* de cette extension. |

## Checks falsifiables exécutés

| Check | Résultat |
|---|---|
| Scripts rejoués | OK — **217 vérifié / 89 flaggé / 1 à confirmer**, 307 total, 365 formes vérifiées, 79 flags. Cohérent TSV/REVUE. |
| 307/307 + FR intact | OK (`app.html` toujours non modifié). |
| Chevauchement vérifié∩flaggé | **aucun** (vérifié). |
| Guillemets courbes app.html | OK — aucun. |
| Rejeu INFCOR formes-lemmes `vérifié` | `apre`→3982 ✓, `tubatura`→54019 ✓, `cartugrafia`→9066 ✓, `merria`→27910 ✓. **Solides.** |
| **Rejeu INFCOR formes fléchies `vérifié`** | **`vulete` (52311), `mittite` (28308), `entrite` (16109), `lasciate` (25130) → réponse VIDE par forme exacte.** 4/4 testées échouent au rejeu. **Faux positifs au sens du check #1.** |
| Rejeu flags « absent » | `betone`, `sensore` etc. : OK absents (échantillon). Côté flags sain. |
| Flag `statu` (faux-sens) | **Raison incomplète** : le livrable dit « id 46249 = bustier, pas statut ». Or `statu` exact renvoie AUSSI 46415, 46813 (« statu »), 15440 (« statu di casa »), 46425 (« statutu »). Flagger reste prudent (OK), mais la **raison ne lit que le 1er résultat** — même cause racine que l'erreur `merria`. |

## Réserve majeure — la couverture est gonflée par inférence de lemme

La doctrine du contrat est explicite : « vérifié = mot **attesté** (id INFCOR) » + check #1
« rejouer par forme exacte → confirmer l'id ». Or l'extension it. 2 mappe des **flexions** (impératifs
2pl, conjugaisons) sur l'id de l'infinitif sans que la forme exacte soit dans la base :
`vulete`→`vulè`, `entrite`→`entre`, `lasciate`→`lascià`, `mittite`→`mette`. La colonne SOURCE
affiche « INFCOR 52311 » comme si la forme exacte était attestée — elle ne l'est pas.

Ce n'est **pas de l'hallucination** (les lemmes existent, les flexions sont régulières et
plausibles) — mais c'est une **sur-revendication non déclarée** qui contredit la doctrine et le
check. C'est exactement le biais que la boucle générateur/évaluateur doit attraper : pour faire
monter le chiffre « 217 », la barre a baissé. Le spot-check donne 4/4 flexions verbales testées
non rejouables → la classe entière est suspecte (auditer aussi `pusate`, `staccate`, `marcate`,
`nutati`, `alluntanate`, `spartite`, `attivate`…).

## Notes par critère

- **Couverture — 7.5 (0.25).** Gros gain réel sur les noms/adjectifs/pluriels (rejouables). Réserve : ~10-15 flexions verbales non rejouables comptées « vérifié ».
- **Qualité & fiabilité sources — 7.0 (0.25).** `merria` corrigé, passage à la forme exacte = bon. Mais lecture 1er-résultat-seulement persiste (`statu`) et inférence de lemme.
- **Traçabilité — 6.5 (0.15).** La majorité des id rejouent ; mais un sous-ensemble de `vérifié` ne rejoue pas par forme exacte (id cité ≠ forme citée). Atteinte directe au check #1.
- **Honnêteté anti-hallucination — 6.5 (0.20).** Rien d'inventé, flags prudents. Mais labelliser « vérifié » des flexions non attestées par forme exacte = sur-revendication vs doctrine (le non-confirmable-direct devrait être « à confirmer » ou noté). Recul net vs it. 1 (8.5), où la posture était conservatrice.
- **Défendabilité dossier — 8.5 (0.15).** Inchangé, solide : bêta, FR fait foi, native review fléchée, changelog transparent.

**Calcul :** 7.5·0.25 + 7.0·0.25 + 6.5·0.15 + 6.5·0.20 + 8.5·0.15 = **7.2 / 10**.

## Corrections demandées (it. 3 — légères, sans nouveau quota)

1. **Distinguer attesté-direct vs flexion-inférée.** Pour toute forme dont le rejeu exact est vide
   (flexions verbales : `vulete`, `mittite`, `entrite`, `lasciate`, + audit `pusate`/`staccate`/
   `marcate`/`nutati`/`alluntanate`/`spartite`/`attivate`…) : soit la marquer explicitement
   « vérifié (flexion du lemme X attesté id Y) » dans SOURCE/note, soit la rétrograder « à confirmer ».
   Ne pas afficher « INFCOR <id> » seul, qui implique une attestation directe fausse au rejeu.
2. **Compléter la raison du flag `statu`** : mentionner que `statu` exact renvoie plusieurs entrées
   (46415, 46813, `statutu` 46425) ; le faux-sens « bustier » n'est qu'une des acceptions. Vérifier
   au passage les autres flags rédigés sur le 1er résultat seul.
3. **Finir le ménage `skip_extra`** : sortir `aperta`, `mumentu`, `rimette`, `sarà` (re-vérifier
   `cform_note_ph`, `geo_check1` qui dépendent d'`aperta`).

## Suite protocole

Score ≥ seuil → **SUCCÈS** maintenu, mais **recul de 0.4 vs it. 1** : signal que l'extension a
été poussée au prix de la rigueur. La correction #1 est la priorité — elle ne demande pas de
re-quota INFCOR (re-tag/note sur formes déjà identifiées) et restaurerait l'honnêteté de la passe
au niveau it. 1 tout en gardant le gain de couverture sur les formes réellement rejouables.
Si it. 3 traite #1–#3, je table sur ~8.0+. Pas de plateau : trajectoire saine si la rigueur revient.
