# CONTRAT D'ITÉRATION — Reprise audit `mairie.html`

> À placer dans le dossier du chantier. Lu avec `PROTOCOLE_AUTO_ITERATION.md`.

```
CHANTIER  : Reprise audit mairie.html — onglets non testés
AXE       : app
GÉNÉRATEUR: Code
ÉVALUATEUR: Code (session fraîche, mode Playwright)
```

## OBJECTIF (1 phrase)

Valider en production les **trois onglets non testés** de l'outil mairies — génération de courrier (export Word), checklist, cadre légal — sur la base canonique, après l'interruption due au crash MCP.

## DANS LE PÉRIMÈTRE

- Onglet **Génération de courrier** (export Word `.docx`).
- Onglet **Checklist**.
- Onglet **Cadre légal**.
- **Non-régression** de l'onglet *Fiche commune* (360 communes, ANFR live) déjà validé : vérifier qu'il marche toujours, sans le re-auditer en détail.

## HORS PÉRIMÈTRE

- Refonte UI, nouvelles fonctionnalités, autres pages (`patrimoine.html`, `app.html`).
- Toute modification non strictement nécessaire à corriger un défaut détecté par l'évaluateur.

## CRITÈRES D'ACCEPTATION

Rubrique §5.1 du protocole (Fonctionnalité 0.35 / Non-régression 0.30 / Craft 0.20 / Robustesse 0.15) **plus** les spécificités falsifiables ci-dessous.

**Génération de courrier (Word) :**
- Sélectionner une commune déclenche un export `.docx` qui se télécharge réellement.
- Le `.docx` est valide (ouvrable, non corrompu) et contient les bonnes données de la commune sélectionnée (nom, identifiants ANFR, etc.).
- Aucune erreur console pendant la génération.

**Checklist :**
- Les items s'affichent.
- Les cases cochées persistent au sein de la session ; l'état reste cohérent après navigation entre onglets.

**Cadre légal :**
- Le contenu se charge entièrement.
- Les références / liens sont présents et la navigation entre sections fonctionne.

**Non-régression :**
- *Fiche commune* charge toujours les 360 communes avec données ANFR live, sans erreur console.

## PARAMÈTRES DE BOUCLE

```
SEUIL DE RÉUSSITE : 7.0 / 10 (pondéré)
MAX ITÉRATIONS    : 8
ESCALADE          : plateau (Δ < 0.3 sur 3 itérations)  → stop + RAPPORT_FINAL.md
                    OU instabilité MCP / crash session  → stop + rapport immédiat
```

## NOTE PLAYWRIGHT — capture du téléchargement Word

L'export `.docx` est un téléchargement : l'évaluateur doit capter l'événement `download`, pas seulement cliquer.

```js
const [ download ] = await Promise.all([
  page.waitForEvent('download'),
  page.click('#export-courrier'),   // sélecteur réel à confirmer
]);
const path = await download.path();          // fichier reçu ?
const name = download.suggestedFilename();    // se termine par .docx ?
// Ouvrir/valider le .docx (ex. unzip + lecture de word/document.xml)
// et vérifier la présence du nom de la commune sélectionnée.
```

> Si le crash MCP d'origine venait de l'export Word lui-même (génération lourde côté client), le flaguer en **Robustesse** et le noter dans le feedback plutôt que de relancer la boucle à l'aveugle.
