# PROTOCOLE AUTO-ITÉRATION — TELLUX CORSE

> Règle de workflow lue par **Claude Code** et **Cowork** avant tout chantier à objectif clair.
> Inspiré du `gan-style-harness` (séparation générateur / évaluateur).

---

## 1. Objet

Donner aux agents la capacité de **produire → s'auto-évaluer → réitérer jusqu'à réussite**, de façon autonome, sur les chantiers dont l'objectif a été arbitré en amont. Le but est d'étendre l'autonomie sur les tâches longues sans dérive : la boucle fournit le mécanisme de détection d'erreur qu'un agent solo n'a pas.

Trois axes concernés :
- **Axe APP / innovation** → Claude Code, évaluation **Playwright** (app live).
- **Axe BÂTIMENT (recherche)** → Cowork, évaluation rubrique.
- **Axe AGRONOMIE (recherche)** → Cowork, évaluation rubrique.

---

## 2. Principe non négociable : séparer le générateur de l'évaluateur

Un agent qui construit **et** juge sa propre sortie est un optimiste pathologique : il se félicite et minimise ses bugs. La règle :

- Le **générateur** produit. Il ne note jamais son propre travail.
- L'**évaluateur** tourne dans une **session fraîche**, avec un prompt distinct, et écrit son verdict dans `feedback-NNN.md`.
- L'évaluateur **critique uniquement** — il ne corrige pas, puis ne se félicite pas de ses propres corrections.
- L'évaluateur est volontairement **sévère**. Sur un chantier de **génération** (le générateur vient d'écrire le livrable), valider dès l'itération 1 est suspect → durcir la rubrique. Sur un chantier d'**audit** (code/contenu pré-existant), un pass précoce est normal : l'évaluateur constate, il ne félicite pas un générateur.

Cette séparation reste obligatoire quel que soit le modèle. Elle corrige un biais, pas une limite de capacité.

---

## 3. Contrat d'itération (arbitrage amont — Soleil + Claude briefs)

Avant de lancer la boucle, produire **une page** validée par Soleil. Sans elle, l'évaluateur n'a rien contre quoi noter.

```
CHANTIER : <nom>
AXE : app | bâtiment | agronomie
GÉNÉRATEUR : Code | Cowork
OBJECTIF (1 phrase) : ...
DANS LE PÉRIMÈTRE : ...
HORS PÉRIMÈTRE : ...
CRITÈRES D'ACCEPTATION : voir rubrique §5 + spécificités ci-dessous
SEUIL DE RÉUSSITE : 7.0 / 10 (pondéré)
MAX ITÉRATIONS : 8
CONDITION D'ESCALADE : plateau de score sur 3 itérations → stop + rapport Soleil
```

Soleil arbitre cette page **une seule fois**. Ensuite la boucle est autonome jusqu'à seuil, plateau ou max.

---

## 4. La boucle

```
0.  Lire le contrat d'itération + ce protocole.
1.  GÉNÉRATEUR : produire / corriger. Commit git.
2.  ÉVALUATEUR (session fraîche) : tester contre la rubrique.
       → écrire feedback-NNN.md : score par critère, score pondéré, problèmes précis.
3.  Si score ≥ seuil → SUCCÈS. Stop. Rapport final.
    Si max itérations atteint → stop + escalade.
    Si plateau (Δ < 0.3 sur 3 itérations) → stop + escalade.
    Sinon → GÉNÉRATEUR relit feedback-NNN.md et reprend en 1.
```

Conventions de fichiers, par chantier :
- `contrat.md` — le contrat d'itération.
- `feedback-001.md`, `feedback-002.md`, … — un par cycle.
- `RAPPORT_FINAL.md` — verdict, score final, ce qui reste hors-scope.

Le feedback passe **par fichier**, jamais inline : le générateur le relit au début de chaque itération.

---

## 5. Rubriques par axe

Chaque critère noté 1–10. Score pondéré = Σ(note × poids). Seuil par défaut **7.0**.

### 5.1 — Axe APP (Code, mode Playwright)

> Tool d'éval : Playwright pilote l'app **vivante**. Il clique, attend le boot, lit la console. Il ne lit pas le code.
> Cible : la base canonique de travail (voir §7 RÈGLE CRITIQUE).

| Critère | Poids | Échelle |
|---|---|---|
| **Fonctionnalité** | 0.35 | 1-3 : feature cassée/absente · 4-6 : happy path OK, cas limites cassent · 7-8 : tout marche, erreurs gérées · 9-10 : robuste sur tous les cas |
| **Non-régression données** | 0.30 | 1-3 : couches manquantes au boot · 4-6 : couches OK mais comptes faux · 7-8 : 9 couches OK, comptes justes · 9-10 : + Indice Tellux dual recalculé correctement |
| **Craft / UX** | 0.20 | 1-3 : layout cassé, pas d'états · 4-6 : marche mais rugueux · 7-8 : poli, responsive · 9-10 : micro-interactions soignées |
| **Robustesse** | 0.15 | 1-3 : erreurs console au boot · 4-6 : warnings · 7-8 : console propre · 9-10 : + pas d'init redondant |

**Checks Playwright concrets (falsifiables) :**
- Boot : les **9 couches** chargent (HTA ~8387 lignes, ANFR antennes ~2820, mesures certifiées 30, TDF 10, Radon, postes sources 21, éoliennes 3, hotspots U/Th 8).
- L'**init JS ne se déclenche qu'une fois** (le bug connu = 3× redondant → à flaguer en Robustesse).
- L'**Indice Tellux dual** s'affiche au format `🟢 P1 N3` (Perturbation 0-5 / Activité naturelle 0-5).
- Le **toggle de légende** fonctionne (Brief 49).
- Le **drill-down « poupée russe »** s'ouvre et se referme (Brief 47).
- Le **filtre côtier `isLand()`** rejette bien les antennes en mer.
- Le **dashboard conditions** affiche ses 4 sections (Kp solaire, atmosphérique, charge réseau, terrain).
- **Console** : zéro erreur rouge au chargement et après interaction.

### 5.2 — Axe BÂTIMENT (Cowork, recherche)

> Limite honnête : la boucle note la **solidité méthodologique**, pas la justesse scientifique finale (= arbitrage Soleil).

| Critère | Poids | Échelle |
|---|---|---|
| **Couverture** | 0.25 | la question est-elle traitée sur tous ses angles ? |
| **Qualité & fraîcheur des sources** | 0.25 | sources primaires/récentes vs agrégateurs/obsolètes |
| **Citations & traçabilité** | 0.15 | chaque affirmation est sourcée et vérifiable |
| **Détection de contradictions** | 0.15 | les désaccords entre sources sont signalés, pas lissés |
| **Défendabilité innovation FEDER** | 0.20 | la prétention d'innovation tient-elle face à un évaluateur de dossier ? |

### 5.3 — Axe AGRONOMIE (Cowork, recherche)

Même squelette que Bâtiment, mêmes poids. Critères de domaine à préciser dans le `contrat.md` du chantier (ex. pertinence pédologie/EM, données terrain corses, saisonnalité).

---

## 6. Conditions d'arrêt (anti-boucle infinie)

- **Seuil atteint** → succès.
- **Max itérations** → stop, `RAPPORT_FINAL.md`, escalade Soleil.
- **Plateau** (amélioration < 0.3 sur 3 itérations) → stop + escalade. Ne pas s'acharner.
- L'évaluateur ne propose **jamais** de correctif puis ne le re-note pas lui-même.
- **Axes recherche — clôture à deux étages** : atteindre le seuil ferme la boucle *méthodologiquement*, mais ne rend pas le livrable exportable. L'export externe / FEDER exige en plus le **gate d'intégrité citations** (§10).

---

## 7. RÈGLE CRITIQUE TELLUX

Toujours repartir de la **base de travail canonique** (`tellux_v5_9_AGRONOMIE_COMPLETE.html` ou son successeur dans le dossier réorganisé), **jamais** d'un fichier uploadé ancien — sauf pour en extraire un contenu nouveau à intégrer.

---

## 8. Setup Playwright (axe APP)

Installation (une fois, côté environnement Code) :

```bash
npm init -y
npm install -D @playwright/test
npx playwright install chromium
```

Servir l'app (mono-fichier Leaflet, a besoin du réseau pour les tuiles/WMS) :

```bash
python3 -m http.server 3000   # depuis le dossier contenant la page
```

Squelette d'évaluateur (`eval/check_app.mjs`) — l'évaluateur l'exécute puis note la rubrique §5.1 :

```js
import { chromium } from '@playwright/test';

const URL = process.env.APP_URL || 'http://localhost:3000/app.html';
const errors = [];

const browser = await chromium.launch();
const page = await browser.newPage();
page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });

await page.goto(URL, { waitUntil: 'networkidle' });
await page.waitForTimeout(4000); // laisser les couches charger

// Exemples de sondes — à compléter selon les sélecteurs réels de la page :
const layerCount = await page.evaluate(() =>
  window.__telluxLayers ? Object.keys(window.__telluxLayers).length : null);
const indice = await page.locator('text=/P\\d N\\d/').first().isVisible().catch(() => false);

// Interaction : toggle légende, drill-down poupée russe…
// await page.click('#legend-toggle'); etc.

console.log(JSON.stringify({
  couches_au_boot: layerCount,      // attendu : 9
  indice_dual_visible: indice,      // attendu : true
  erreurs_console: errors,          // attendu : []
}, null, 2));

await browser.close();
```

> Note : exposer un hook de debug léger (ex. `window.__telluxLayers`) dans la page facilite énormément les sondes. À discuter avec Code si absent.

---

## 9. Version allégée — Opus 4.8

Le harness doit se **simplifier** quand le modèle monte (Stage 3) :
- planification en une passe (pas de découpage en sprints),
- génération continue,
- évaluation en **checkpoints** plutôt qu'à chaque micro-étape.

Mais la **séparation générateur / évaluateur (§2) ne disparaît jamais** : c'est un correctif de biais, indépendant de la capacité du modèle.

---

## 10. Gate d'intégrité citations (axes recherche — agronomie & bâtiment)

**Constat (chantier électroculture).** Sur 4 itérations, le score de contenu a progressé mais la fabrication de citations — « citations Frankenstein » : auteur d'un papier, journal/année d'un autre, URL d'un troisième — est revenue à *chaque* itération. Une note de 1–10 ne corrige pas ça : l'évaluateur échantillonne, un « Citations 7/10 » passe le seuil, et le générateur réintroduit de nouvelles fabrications plus vite qu'elles ne sont attrapées une par une. **L'intégrité d'une citation est binaire, pas une dimension de qualité.**

Donc, pour tout chantier recherche, **en plus** de la rubrique §5 :

**Gate pass/fail, par citation.** Une citation passe seulement si ses quatre éléments — auteur, année, titre/journal, DOI ou URL — résolvent vers **le même papier réel**, ET que ce papier soutient effectivement l'affirmation citée. Outil de résolution : connecteur **Consensus** en priorité, sinon DOI/éditeur. **Une seule citation qui échoue = gate échoué.**

**Clôture à deux étages.** Ne jamais confondre :
- *Méthodologiquement clos* = rubrique §5 ≥ seuil. Suffisant pour clore la boucle en interne.
- *Exportable FEDER / externe* = méthodologiquement clos **ET** gate citations à 100 % pass.

Un livrable peut être méthodologiquement clos tout en restant non exportable tant que le gate n'est pas passé. C'est un **verrou**, pas un TODO différable.

**Qui l'exécute.** Le gate tourne dans une tâche évaluateur dédiée (séparation §2 maintenue), après clôture méthodologique. Verdict dans `GATE_CITATIONS.md` : liste exhaustive des références, pass/fail + motif pour chacune. Toute fail repart au générateur.
