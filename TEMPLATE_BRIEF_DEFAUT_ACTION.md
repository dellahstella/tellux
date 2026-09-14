# TEMPLATE — Brief / Contrat « défaut-action »

> Gabarit de tout nouveau brief ou contrat de chantier. Inverse l'ancien réflexe « STOP partout » : le défaut est l'action, l'arrêt est l'exception (Cran C de `CHARTE_DECISION.md`). Remplacer les `<…>`. Supprimer les sections non pertinentes.

---

## En-tête

- **Chantier** : `<nom>`
- **Cible** : `<Code | Cowork>`
- **À lire au démarrage (§11.4)** : chartes d'axe + `CHARTE_DECISION.md` + `DECISIONS.md` + skills pertinents.
- **Confidentialité** : `<publique | Phase 3 confidentielle (zéro FEDER, gitignored)>`

## Objet

`<1–3 phrases : ce que le chantier doit produire.>`

## Entrées (lecture seule) → Sortie

- **Entrées** : `<fichiers / corpus>`
- **Sortie** : `<chemin>` — `<draft _drafts/ | branche claude/…>`

## Critères d'acceptation falsifiables (rubrique §5.1)

- `<critère mesurable 1>`
- `<critère mesurable 2>`
- **Seuil** : `<§5.1>`

## Gates binaires (échec = Cran C, FAIL immédiat)

- **§10 citations** : `verify_citation.py`, 0 Frankenstein (si corpus/références affichés).
- **Doctrine** : mesure d'abord, pas de mysticisme, pas de bénéfice EM présenté comme acquis.

## Autonomie (défaut = action)

Opère sous `CHARTE_DECISION.md`.

- **Cran A/B** : décide et avance (loggé / signalé). Ne demande pas de validation pour les choix réversibles internes, les itérations, les PR sur `claude/`, l'enchaînement d'un chantier qui PASSE.
- **Ne t'arrête QUE sur Cran C** : merge `main`, déploiement public, échec §10/doctrine, irréversible, changement de scope, dépassement budget, donnée FEDER-facing, repo privé depuis le public, ambiguïté réelle non tranchée.
- **Escalade groupée** : parque les Cran C, va au bout du faisable, présente un seul digest d'arbitrage en fin (décision · contexte · reco · défaut). Pas d'interruption par item.

## Vérification couche non-textuelle (brief de recherche documentaire)

Avant de clore un brief qui conclut sur le contenu d'un document ou d'une source :

- Ai-je vérifié une **couche non-textuelle** en plus du texte brut ? — annotations/
  commentaires (PDF `/Annots`, `.docx word/comments.xml`, suivi de modifications),
  métadonnées, tableaux rendus en image/canvas (non captés par l'extraction texte),
  structure (champs d'un JSON/objet, feuilles masquées d'un tableur).
- Puis-je distinguer « **l'information n'existe pas dans la source** » de
  « **je ne l'ai pas cherchée à cette couche** » ? Si non, ma conclusion négative
  n'est pas fondée — le dire (« non trouvé à la couche texte ; couche X non vérifiée »),
  pas « n'existe pas ».
- Rappel de deux précédents : 18 annotations réelles invisibles à l'extraction texte
  d'un PDF relu (2026-07) ; « UNSCEAR table 5 » citée des mois sans vérifier qu'elle
  contient réellement des coefficients (elle n'en contient pas).

## Capitalisation à la clôture (§11)

- **§11.1** décisions → `DECISIONS.md` (ou « RAS »).
- **§11.2** skill réutilisable → `skill-creator` (proposé en PR).
- **§11.3** patterns / anti-patterns notés.

## Clôture

Deux étages : seuil méthodo atteint ≠ export-ready FEDER. Le chantier s'auto-clôt s'il PASSE (Cran B) ; seuls les Cran C attendent l'arbitrage Soleil dans le digest.
