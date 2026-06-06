# Tellux — Harness headless du moteur

Exécution programmatique des fonctions `calc*` du moteur Tellux à des entrées arbitraires (GPS, options), via Playwright qui charge `app.html` en mode headless et appelle les globales depuis Node.js. **L'extraction P0 (moteur Node.js autonome) n'est pas requise** — le harness est l'option B intermédiaire de l'audit blindage (`_drafts/AUDIT_BLINDAGE_FAISABILITE_2026-06-06.md` §1.2).

Le harness est le véhicule pour :
- **WS2 sensibilité** : varier `EXPERT_WEIGHTS` / `EXPERT_BOUNDS` en sandbox **sans modifier les constantes `GELE-001` de prod** (la fonction `computeExpertComposite` accepte ces paramètres en argument).
- **WS2 validation RF** : comparer `calcRF(lat, lon)` aux 30 mesures certifiées ANFR/EXEM.
- **WS3 non-régression** : vérifier qu'aucun changement de code ou de données n'a fait dériver les sorties du moteur sur les 25 points de référence de la fixture.

`app.html` n'est jamais modifié. Les constantes `GELE-001` / `NCRP-001` ne sont jamais touchées.

---

## Installation

Depuis la racine du repo :

```bash
cd tests/blindage-harness
npm install
npx playwright install chromium
```

Total : ~150 Mo (Chromium + Playwright Node). `node_modules` est ignoré par `.gitignore`.

---

## Usage

### Non-régression sur les 25 points

```bash
node tests/blindage-harness/non-regression.mjs
```

Compare la sortie de `calcAll_v2(lat, lon, options)` à `tests/fixtures/known-values-pre-extraction.json` pour les 25 points capturés le 2026-04-26 (révision `a76ebce`).

**Reproductibilité :**
- `setRuntimeState({ curKp, chargeFacteur })` force les globales runtime à l'état capturé.
- `freezeTime: fixture.captured_at` patche `Date` dans la page pour que `calcSq(lat)` (app.html:3012, lecture directe de `new Date()`) retourne les mêmes valeurs qu'à la capture.

**Champs ignorés** (cf. `notes_de_capture` de la fixture) :
- `metadata.timestamp`
- `metadata.kp_snapshot.timestamp`
- `metadata.kp_snapshot.value`

**Variables d'environnement :**

| Var | Défaut | Effet |
|---|---|---|
| `HARNESS_URL` | `http://127.0.0.1:3779/app.html` (serveur local) | URL externe à utiliser à la place du serveur local |
| `HARNESS_PORT` | `3779` | Port du serveur local |
| `HARNESS_HEADFUL` | `0` | Si `1`, lance Chromium visible |
| `HARNESS_BOOT_TIMEOUT_MS` | `30000` | Timeout pour le boot du moteur |
| `HARNESS_FREEZE_TIME` | — | ISO date à figer pour `Date` |
| `NUMERIC_EPS` | `1e-9` | Tolérance numérique du diff |
| `LIMIT_POINTS` | `0` (tous) | Limite aux N premiers points |
| `VERBOSE` | `0` | Si `1`, affiche aussi les PASS |

Sortie : exit code `0` si tout PASS, `1` si DIFF ou ERR, `2` si erreur fatale du harness.

### Playground (exemples WS2)

```bash
node tests/blindage-harness/playground.mjs rf-residuals
node tests/blindage-harness/playground.mjs sensitivity
```

- `rf-residuals` : calcule `predicted - measured` (en V/m) sur les 30 mesures certifiées EXEM/ANFR de `public/data/cartoradio_certified_corse.json`.
- `sensitivity` : sweep `EXPERT_WEIGHTS` sur 5 combinaisons × 5 points représentatifs. Lit les constantes `GELE-001` **en read-only** (pour affichage), puis passe des poids explicites à `computeExpertComposite` (sans modifier le défaut).

---

## API du harness

```javascript
import { createHarness } from './tests/blindage-harness/harness.mjs';

const harness = await createHarness({
  // — Tous optionnels —
  url: 'http://127.0.0.1:3779/app.html',  // ou ex. 'https://tellux.pages.dev/app.html'
  port: 3779,                              // port local (ignoré si url externe)
  headless: true,                          // false pour debug visuel
  bootTimeoutMs: 30000,                    // timeout boot moteur
  freezeTime: '2026-04-26T08:46:55.403Z',  // optionnel : fige Date dans la page
});

// ─── Appels du moteur ────────────────────────────────────────────────────────

const v2 = await harness.calcAll_v2(41.92, 8.74, { altitude_m: 5 });
// → objet complet retourné par calcAll_v2 :
//   { domains: { magnetic: {static, elf}, rf, ionizing }, context, metadata }

const composite = await harness.computeExpertComposite(
  v2,
  { M: 0.3, RF: 0.5, I: 0.2 },              // poids custom (sweep)
  { ELF_nT: [0, 1000], RF_uW_m2: [0, 1000], GAMMA_nSv_h: [50, 250] }, // bornes
);
// → { index, normalized, weights, bounds, inputs, epistemic_note, under_review: true }

// Sans args = fallback sur EXPERT_WEIGHTS_DEFAULT / EXPERT_BOUNDS_DEFAULT (GELE-001)
const compositeDefault = await harness.computeExpertComposite(v2);

// ─── Inspection / contrôle d'état ────────────────────────────────────────────

const defaults = await harness.getExpertDefaults();
// → { weights: { M, RF, I }, bounds: { ... }, epistemic_note } — read-only

await harness.setRuntimeState({ curKp: '2.0', chargeFacteur: 0.9130434 });
// → réassigne les `let` globaux dans le script-scope de app.html
//   (les bindings `let` n'étant pas attachés à `window`, on assigne par
//   leur nom nu via page.evaluate)

const state = await harness.getRuntimeState();
// → { curKp, chargeFacteur, WMM_GRID_length, HTA_SEGMENTS_DATA_length,
//     POSTES_SOURCES_length, EOLIENNES_DATA_length, USE_ELF_V2, USE_BT_SEGMENTS }

// ─── Évaluation libre ────────────────────────────────────────────────────────

const ks = await harness.evalInPage(() => Object.keys(window).filter(k => k.startsWith('calc')));
// → ['calcAll', 'calcAll_v2', 'calcRF', 'calcSq', ...]

// ─── Diagnostics console navigateur ──────────────────────────────────────────

const diag = harness.diagnostics();
// → { consoleErrors: [...], consoleWarns: [...] }
//   Les errors de CORS sur fetches externes (RTE, BGS AQU) sont attendues en
//   local — elles déclenchent les fallbacks Kp dans calcExternalCorr.

// ─── Fermeture ──────────────────────────────────────────────────────────────

await harness.close();
```

---

## État de référence (non-régression)

Au `2026-06-06` sur la branche `feat/blindage-harness`, avec `setRuntimeState` (curKp + chargeFacteur) + `freezeTime` (Date capturée) :

```
Résultat : 0 PASS · 25 DIFF · 0 ERR  (sur 25 points)
```

Les 25 écarts sont **strictement les mêmes 2 champs par point**, **identiques pour les 25 points** :

| Champ | Drift | Diagnostic |
|---|---|---|
| `domains.magnetic.elf.source` | `"…+ 0 segments BT réels +…"` vs `"…+ BT_ZONES proxy +…"` | Label de boot-state. À la capture, `BT_SEGMENTS_DATA` était chargé mais `USE_BT_SEGMENTS = false` (hotfix `BT-CALIBRATION-001`) → label « 0 segments BT réels ». En local, `bt_lines` ne charge pas dans le timeout boot → fallback `BT_ZONES proxy`. **La sortie numérique ELF est identique**, seule l'étiquette descriptive diffère. |
| `domains.ionizing.gamma.epistemic_note` | `"…Téléray IRSN…"` vs `"…Téléray ASNR…"` | **Évolution du code source post-capture.** L'ASNR est l'entité issue de la fusion ASN + IRSN (cf. `transparence.html` §7). Quelqu'un a mis à jour la chaîne dans `app.html` entre la révision `a76ebce` (2026-04-26) et l'état courant. Drift volontaire et tracé éditorialement. |

**Aucun écart numérique** sur les 25 points. Le moteur reproduit exactement les valeurs capturées une fois le runtime state (curKp, chargeFacteur) et l'horloge (Date) figés.

Les écarts sont **signalés en sortie de test (exit code 1)** et **ne sont pas masqués** dans `IGNORED_PATHS`. La fixture n'est pas modifiée pour faire passer — un écart reste un signal.

---

## Architecture

```
tests/blindage-harness/
├── package.json           # devDep : playwright ^1.49
├── harness.mjs            # API du harness (createHarness, etc.)
├── non-regression.mjs     # boucle de comparaison sur la fixture
├── playground.mjs         # exemples WS2 (RF résiduels + sensibilité)
└── README.md              # ce fichier
```

- **Aucune modification de `app.html`** ni des constantes `GELE-001` / `NCRP-001`.
- **`node_modules/` gitignoré** (cf. `.gitignore` ligne 43, pattern relatif).
- **Le harness lance un serveur HTTP statique local** (Node `http`, racine du repo) pour servir `app.html` au navigateur Chromium. Désactivable en passant `url: 'https://tellux.pages.dev/app.html'`.

---

## Limites connues

- **Boot dépend de fetches Supabase et Cloudflare** : ~5-10 s sur cold start. Si le réseau Supabase est lent, augmenter `bootTimeoutMs`.
- **CORS externes en local** : les fetches vers `rte-france.com`, `geomag.bgs.ac.uk` et autres sont bloqués par CORS quand on charge depuis `127.0.0.1`. Le moteur retombe sur ses fallbacks (Kp pour `calcExternalCorr`, `BT_ZONES` proxy pour ELF BT). Pour tester avec les services externes, charger depuis `https://tellux.pages.dev/app.html` (`HARNESS_URL=https://tellux.pages.dev/app.html node non-regression.mjs`).
- **`calcSq(lat)` lit `new Date()` directement** (app.html:3012) — contredit la note §6.10 du plan d'extraction qui affirmait l'absence de dépendance temporelle. Le harness expose `freezeTime` pour cette raison.
- **`BT_SEGMENTS_DATA` peut ne pas charger** dans le timeout par défaut → fallback `BT_ZONES proxy`. Affecte seulement l'étiquette `source`, pas la sortie numérique.

---

## Pourquoi pas Phase 0 (extraction Node) tout de suite ?

L'extraction du moteur vers `lib/tellux-engine.js` est conçue (cf. `docs/em-mairie/tellux-engine-extraction-plan.md`, 347 lignes) mais conditionnée à plusieurs prérequis non encore réunis (retour physicien Santoni, volume contributions niveau 1, bande passante Soleil). Ce harness est l'**enabler intermédiaire** : il rend la testabilité automatisée et la sensibilité possibles **sans attendre P0**, sans toucher au moteur, et reste compatible avec une migration ultérieure vers un runner de tests natif (`node:test`) une fois le moteur extrait.
