// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Blindage harness (Playwright wrapper around app.html)
// Création : 2026-06-06 · feat/blindage-harness
// ═══════════════════════════════════════════════════════════════════════════
//
// Permet d'exécuter les fonctions calc* du moteur Tellux à des GPS et options
// arbitraires, en mode headless, SANS extraction préalable du moteur.
//
// app.html est chargé en lecture seule via une page Playwright/Chromium ; les
// fonctions globales du moteur (calcAll_v2, computeExpertComposite, ...) sont
// appelées par page.evaluate() et leurs sorties typées sont sérialisées en
// JSON puis renvoyées au harness.
//
// Stratégie de chargement :
//   - Le harness lance un serveur HTTP statique local (Node http) sur la
//     racine du repo, puis Chromium navigue vers /app.html.
//   - Mode dégradé : si une URL externe est fournie (HARNESS_URL), elle est
//     utilisée à la place (ex: https://tellux.pages.dev/app.html). Utile pour
//     reproduire l'état prod sans dépendre du working tree local.
//
// État runtime reproductible :
//   - Les globales mutables curKp / chargeFacteur sont écrites avant chaque
//     appel via setRuntimeState({curKp, chargeFacteur}). Sans cela, les
//     valeurs ELF et metadata.kp_snapshot dépendent du dernier fetch NOAA/EDF.
//
// ⚠ Le harness ne modifie ni app.html ni les constantes gelées (GELE-001 /
// NCRP-001). L'objectif est d'exécuter le moteur tel quel, à des entrées
// arbitraires, sans toucher le code.
// ═══════════════════════════════════════════════════════════════════════════

import { chromium } from 'playwright';
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize, resolve as pathResolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { installSupabaseCache } from './supabase-cache.mjs';

const __filename = fileURLToPath(import.meta.url);
const HARNESS_DIR = pathResolve(__filename, '..');
const REPO_ROOT = pathResolve(HARNESS_DIR, '..', '..');

const DEFAULT_PORT = Number(process.env.HARNESS_PORT) || 3779;
const DEFAULT_HEADLESS = process.env.HARNESS_HEADFUL !== '1';
const DEFAULT_BOOT_TIMEOUT_MS = Number(process.env.HARNESS_BOOT_TIMEOUT_MS) || 30000;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.geojson': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.woff2': 'font/woff2',
  '.ico': 'image/x-icon',
};

// ─── Static file server (only used when HARNESS_URL not set) ─────────────────

function startStaticServer(root, port) {
  return new Promise((resolve, reject) => {
    const server = http.createServer(async (req, res) => {
      try {
        const u = new URL(req.url, `http://${req.headers.host || '127.0.0.1'}`);
        let pathname = decodeURIComponent(u.pathname);
        if (pathname.endsWith('/')) pathname += 'index.html';
        const fp = normalize(join(root, pathname));
        const rootN = normalize(root);
        if (!fp.startsWith(rootN)) {
          res.writeHead(403);
          res.end('forbidden');
          return;
        }
        const data = await readFile(fp);
        const mime = MIME[extname(fp).toLowerCase()] || 'application/octet-stream';
        res.writeHead(200, { 'Content-Type': mime, 'Access-Control-Allow-Origin': '*' });
        res.end(data);
      } catch (_e) {
        res.writeHead(404);
        res.end('not found');
      }
    });
    server.on('error', reject);
    server.listen(port, '127.0.0.1', () => resolve(server));
  });
}

// ─── Boot detection ──────────────────────────────────────────────────────────

const BOOT_CHECK_FN = function () {
  // Returns true when the engine is loaded and ready to evaluate calcAll_v2
  // against arbitrary GPS coordinates. We check the presence of:
  //   - the function calcAll_v2 (the orchestrator)
  //   - HTA_SEGMENTS_DATA populated (loaded from Supabase hta_lines)
  //   - SEGMENT_GRID built (depends on HTA_SEGMENTS_DATA)
  // The Supabase fetch can take 5-15s on cold start.
  // WMM_GRID retirée d'ici le 2026-09-04 (brief AR, suite) : n'a jamais été une dépendance de
  // calcAll_v2 — seule updateIgrfWmmDiff() (panneau Expert, cross-check invisible) la lit.
  // app.html ne la charge plus au boot (chargement paresseux, déclenché par activateExpertMode())
  // ; ce harnais n'active jamais le mode Expertise, donc WMM_GRID resterait indéfiniment null si
  // ce gate n'était pas retiré — timeout garanti sur un signal qui ne mesure rien de réel ici.
  try {
    if (typeof calcAll_v2 !== 'function') return false;
    if (!Array.isArray(HTA_SEGMENTS_DATA) || HTA_SEGMENTS_DATA.length === 0) return false;
    if (!SEGMENT_GRID || typeof SEGMENT_GRID !== 'object') return false;
    return true;
  } catch (_e) {
    return false;
  }
};

// ─── Harness factory ─────────────────────────────────────────────────────────

/**
 * Create a new harness instance backed by a fresh Chromium page on app.html.
 *
 * @param {object} [opts]
 * @param {string} [opts.url] — explicit URL (overrides local server). If unset,
 *   the harness starts a local Node http server on opts.port and navigates to
 *   http://127.0.0.1:{port}/app.html.
 * @param {number} [opts.port] — port for the local server. Defaults to 3779.
 * @param {boolean} [opts.headless] — Chromium headless mode. Defaults to true.
 * @param {number} [opts.bootTimeoutMs] — how long to wait for the engine to
 *   boot (HTA + WMM + SEGMENT_GRID). Defaults to 30000.
 * @param {string} [opts.freezeTime] — ISO date string. When set, Date is patched
 *   inside the page so that `new Date()`, `Date.now()` and friends always
 *   return this fixed moment. Used to make calcSq() (which reads `new Date()`
 *   directly, app.html:3012) strictly reproducible. The patch is installed
 *   via Playwright's addInitScript so it applies before app.html scripts run.
 * @returns {Promise<object>} harness API.
 */
export async function createHarness(opts = {}) {
  const port = opts.port ?? DEFAULT_PORT;
  const url = opts.url ?? process.env.HARNESS_URL ?? `http://127.0.0.1:${port}/app.html`;
  const headless = opts.headless ?? DEFAULT_HEADLESS;
  const bootTimeoutMs = opts.bootTimeoutMs ?? DEFAULT_BOOT_TIMEOUT_MS;
  const freezeTime = opts.freezeTime ?? process.env.HARNESS_FREEZE_TIME ?? null;

  let server = null;
  if (url.startsWith('http://127.0.0.1') || url.startsWith('http://localhost')) {
    server = await startStaticServer(REPO_ROOT, port);
  }

  const browser = await chromium.launch({ headless });
  const context = await browser.newContext({
    ignoreHTTPSErrors: true,
  });

  // Cache local Supabase (brief BN, 2026-09-05) — posé AVANT toute navigation
  // pour intercepter le premier chargement lui-même, pas seulement les
  // rechargements. opts.cache===false équivaut à TELLUX_HARNESS_CACHE=off
  // pour ce contexte précis (utilisé par loading-path-live-check.mjs) : aucune
  // route posée, réseau réel garanti. Ne touche jamais app.html ni le chemin
  // de chargement réel — cf. commentaire de tête de supabase-cache.mjs pour
  // la conception complète.
  const cacheInfo = opts.cache === false
    ? { disabled: true }
    : await installSupabaseCache(context, opts.cacheOpts);

  // Time-freezing init script — installed in every page of the context BEFORE
  // app.html's scripts run. Replaces Date with a subclass that, when constructed
  // with no arg or called with Date.now(), returns the frozen instant.
  // Keeps the original Date constructor for explicit-arg calls.
  if (freezeTime) {
    const epochMs = new Date(freezeTime).getTime();
    if (!Number.isFinite(epochMs)) {
      throw new Error('createHarness: freezeTime is not a valid ISO date string: ' + freezeTime);
    }
    await context.addInitScript((frozenEpoch) => {
      const _OrigDate = Date;
      const Frozen = function (...args) {
        if (args.length === 0) return new _OrigDate(frozenEpoch);
        // eslint-disable-next-line new-cap
        return new _OrigDate(...args);
      };
      Frozen.now = () => frozenEpoch;
      Frozen.parse = _OrigDate.parse.bind(_OrigDate);
      Frozen.UTC = _OrigDate.UTC.bind(_OrigDate);
      Frozen.prototype = _OrigDate.prototype;
      // Replace global Date (script lexical environment + window prop)
      // eslint-disable-next-line no-global-assign
      Date = Frozen;
      window.Date = Frozen;
    }, epochMs);
  }

  const page = await context.newPage();

  // Capture console errors / warnings for diagnostics.
  const consoleErrors = [];
  const consoleWarns = [];
  page.on('console', (msg) => {
    const t = msg.type();
    if (t === 'error') consoleErrors.push(msg.text());
    else if (t === 'warning') consoleWarns.push(msg.text());
  });
  page.on('pageerror', (err) => consoleErrors.push('pageerror: ' + (err?.message || String(err))));

  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: bootTimeoutMs });
  await page.waitForFunction(BOOT_CHECK_FN, undefined, { timeout: bootTimeoutMs, polling: 250 });

  // ─── Public API ────────────────────────────────────────────────────────────

  const api = {
    /**
     * Call calcAll_v2(lat, lon, options) inside the browser and return the
     * serialized result.
     */
    async calcAll_v2(lat, lon, options = {}) {
      return await page.evaluate(
        ({ lat, lon, options }) => {
          // eslint-disable-next-line no-undef
          return calcAll_v2(lat, lon, options);
        },
        { lat, lon, options }
      );
    },

    /**
     * Call computeExpertComposite(v2, weights?, bounds?). When weights/bounds
     * are omitted, the function falls back to EXPERT_WEIGHTS_DEFAULT /
     * EXPERT_BOUNDS_DEFAULT (GELE-001). Use explicit args for sensitivity
     * sweeps without touching the gel.
     */
    async computeExpertComposite(v2, weights, bounds) {
      return await page.evaluate(
        ({ v2, weights, bounds }) => {
          // eslint-disable-next-line no-undef
          return computeExpertComposite(v2, weights ?? undefined, bounds ?? undefined);
        },
        { v2, weights, bounds }
      );
    },

    /**
     * Read the GELE-001 default constants (read-only inspection — no mutation).
     */
    async getExpertDefaults() {
      return await page.evaluate(() => ({
        // eslint-disable-next-line no-undef
        weights: typeof EXPERT_WEIGHTS_DEFAULT !== 'undefined' ? EXPERT_WEIGHTS_DEFAULT : null,
        // eslint-disable-next-line no-undef
        bounds: typeof EXPERT_BOUNDS_DEFAULT !== 'undefined' ? EXPERT_BOUNDS_DEFAULT : null,
        // eslint-disable-next-line no-undef
        epistemic_note: typeof EXPERT_EPISTEMIC_NOTE !== 'undefined' ? EXPERT_EPISTEMIC_NOTE : null,
      }));
    },

    /**
     * Overwrite the mutable globals curKp / chargeFacteur (used by calcAll_v2
     * indirectly through metadata.kp_snapshot and ELF contributions). Used to
     * reproduce the runtime_state_at_capture of a fixture deterministically.
     *
     * Implementation note : ces deux globales sont déclarées en `let` au
     * top-level d'un <script> de app.html (script scope, PAS attaché à
     * `window`). On les réassigne par leur nom nu dans page.evaluate, ce qui
     * cible bien le binding script-scope (et pas une nouvelle propriété
     * `window.curKp` qui n'aurait aucun effet sur le moteur).
     */
    async setRuntimeState({ curKp, chargeFacteur } = {}) {
      return await page.evaluate(
        ({ newCurKp, newCharge }) => {
          // eslint-disable-next-line no-undef
          if (newCurKp !== undefined) curKp = String(newCurKp);
          // eslint-disable-next-line no-undef
          if (newCharge !== undefined) chargeFacteur = Number(newCharge);
          return {
            // eslint-disable-next-line no-undef
            curKp,
            // eslint-disable-next-line no-undef
            chargeFacteur,
          };
        },
        { newCurKp: curKp, newCharge: chargeFacteur }
      );
    },

    /**
     * Read the current values of curKp / chargeFacteur in the page context.
     */
    async getRuntimeState() {
      return await page.evaluate(() => ({
        // eslint-disable-next-line no-undef
        curKp: typeof curKp !== 'undefined' ? curKp : null,
        // eslint-disable-next-line no-undef
        chargeFacteur: typeof chargeFacteur !== 'undefined' ? chargeFacteur : null,
        // WMM_GRID vaut désormais `null` (pas `undefined`) tant que le mode Expertise n'a pas
        // été activé (chargement paresseux, 2026-09-04, brief AR) — `typeof null` est 'object',
        // donc l'ancien garde-fou `typeof WMM_GRID !== 'undefined'` laissait passer `null` et
        // faisait planter `.length` (TypeError). Array.isArray() couvre correctement les deux cas.
        // eslint-disable-next-line no-undef
        WMM_GRID_length: Array.isArray(WMM_GRID) ? WMM_GRID.length : null,
        // eslint-disable-next-line no-undef
        HTA_SEGMENTS_DATA_length: typeof HTA_SEGMENTS_DATA !== 'undefined' ? HTA_SEGMENTS_DATA.length : null,
        // eslint-disable-next-line no-undef
        POSTES_SOURCES_length: typeof POSTES_SOURCES !== 'undefined' ? POSTES_SOURCES.length : null,
        // eslint-disable-next-line no-undef
        EOLIENNES_DATA_length: typeof EOLIENNES_DATA !== 'undefined' ? EOLIENNES_DATA.length : null,
        // eslint-disable-next-line no-undef
        USE_ELF_V2: typeof USE_ELF_V2 !== 'undefined' ? USE_ELF_V2 : null,
        // eslint-disable-next-line no-undef
        USE_BT_SEGMENTS: typeof USE_BT_SEGMENTS !== 'undefined' ? USE_BT_SEGMENTS : null,
      }));
    },

    /**
     * Evaluate an arbitrary expression inside the page. The function body runs
     * in the page context with access to all globals. Use for one-off
     * inspections.
     *
     * Example:
     *   await harness.evalInPage(() => Object.keys(window).filter(k => k.startsWith('calc')))
     */
    async evalInPage(fn, ...args) {
      return await page.evaluate(fn, ...args);
    },

    /**
     * Return any console errors/warnings captured since the harness started.
     */
    diagnostics() {
      return {
        consoleErrors: [...consoleErrors],
        consoleWarns: [...consoleWarns],
      };
    },

    /**
     * Cleanly shut down browser and local server.
     */
    async close() {
      await page.close({ runBeforeUnload: false }).catch(() => {});
      await context.close().catch(() => {});
      await browser.close().catch(() => {});
      if (server) {
        await new Promise((res) => server.close(() => res()));
      }
    },

    _internal: { page, server, browser, context, url, cacheInfo },
  };

  return api;
}
