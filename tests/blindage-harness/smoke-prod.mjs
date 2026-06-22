// ═══════════════════════════════════════════════════════════════════════════
// Tellux — R1 Smoke-test post-déploiement (prod, LECTURE SEULE)
// ═══════════════════════════════════════════════════════════════════════════
//
// Vérifie que les pages clés de la prod chargent et que les fonctions
// critiques tiennent, APRÈS un déploiement. DÉTECTE et SIGNALE uniquement
// (le workflow ouvre une issue sur échec dur — Cran B) : ne corrige rien,
// aucun rollback, n'écrit jamais sur la prod (read-only).
//
// PHILOSOPHIE Phase A (cf. eval-app-rubric.yml) — éviter les faux positifs :
//   • DUR (ouvre une issue, fait rougir le run) = signaux non ambigus :
//       route ≠ 200, carte Leaflet non montée sur /app, exception de navigation.
//   • WARNING (rapporté, n'ouvre PAS d'issue) = signaux plus flous en CI :
//       boot moteur lent / data muette, erreurs console, pageerror.
//     Promotion en DUR possible après observation de la stabilité CI.
//
// Critères du brief R1 couverts : routes 200, Leaflet monté (dur) ; endpoints
// data (boot moteur) + erreurs console (warning, rapporté).
//
// SORTIE : JSON sur stdout { base, ok, warnings_total, routes[] }. Exit 0 si
// aucun problème DUR, 1 sinon.
// USAGE : SMOKE_BASE=https://tellux.pages.dev node smoke-prod.mjs
// ═══════════════════════════════════════════════════════════════════════════

import { chromium } from 'playwright';

const BASE = (process.env.SMOKE_BASE || 'https://tellux.pages.dev').replace(/\/$/, '');
const ROUTES = ['/', '/app', '/patrimoine', '/mairies'];
const NAV_TIMEOUT = Number(process.env.SMOKE_NAV_TIMEOUT_MS) || 45_000;
const BOOT_TIMEOUT = Number(process.env.SMOKE_BOOT_TIMEOUT_MS) || 60_000;

const CONSOLE_NOISE_RE = /favicon|ERR_BLOCKED_BY_CLIENT|Failed to load resource: the server responded with a status of 404/i;
const DATA_HOSTS = ['supabase.co', 'anfr', 'geo.api.gouv.fr', 'data.geopf.fr', 'geoservices.brgm.fr'];

const BOOT_READY_FN = function () {
  try {
    if (typeof calcAll_v2 !== 'function') return false;
    if (!Array.isArray(HTA_SEGMENTS_DATA) || HTA_SEGMENTS_DATA.length === 0) return false;
    if (!Array.isArray(WMM_GRID) || WMM_GRID.length === 0) return false;
    if (!SEGMENT_GRID || typeof SEGMENT_GRID !== 'object') return false;
    return true;
  } catch (_e) { return false; }
};

async function checkRoute(context, route) {
  const url = BASE + route;
  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];
  const dataHosts = new Set();
  page.on('console', (m) => {
    if (m.type() === 'error') { const t = m.text().slice(0, 200); if (!CONSOLE_NOISE_RE.test(t)) consoleErrors.push(t); }
  });
  page.on('pageerror', (e) => pageErrors.push(String(e).slice(0, 200)));
  page.on('response', (r) => {
    try {
      const h = new URL(r.url()).host;
      if (DATA_HOSTS.some((d) => h.includes(d)) && r.status() < 400) dataHosts.add(h);
    } catch (_e) { /* ignore */ }
  });

  // problems = DUR (fait échouer) ; warnings = SOFT (rapporté seulement).
  const res = { route, url, status: null, ok: false, leaflet: null, booted: null, dataHostsOk: [], consoleErrors: [], pageErrors: [], problems: [], warnings: [] };
  try {
    const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: NAV_TIMEOUT });
    res.status = resp ? resp.status() : null;
    if (res.status !== 200) res.problems.push(`HTTP ${res.status} (attendu 200)`); // DUR

    if (route === '/app') {
      await page.evaluate(() => { const ov = document.querySelector('#disclaimer-overlay,.disclaimer-overlay'); if (ov) ov.remove(); }).catch(() => {});
      res.leaflet = await page.locator('.leaflet-container').first().isVisible({ timeout: 15_000 }).catch(() => false);
      if (!res.leaflet) res.problems.push('carte Leaflet (.leaflet-container) non montée'); // DUR
      res.booted = await page.waitForFunction(BOOT_READY_FN, null, { timeout: BOOT_TIMEOUT }).then(() => true).catch(() => false);
      if (!res.booted) res.warnings.push(`moteur non booté en ${BOOT_TIMEOUT}ms (endpoints data ANFR/Supabase lents/muets ?)`); // WARN
      res.dataHostsOk = [...dataHosts];
      if (res.dataHostsOk.length === 0) res.warnings.push('aucun hôte data joignable (supabase/anfr/geo/brgm)'); // WARN
    }

    res.consoleErrors = consoleErrors.slice(0, 8);
    res.pageErrors = pageErrors.slice(0, 8);
    if (pageErrors.length > 0) res.warnings.push(`${pageErrors.length} erreur(s) JS non rattrapée(s) (pageerror)`); // WARN
    if (consoleErrors.length > 0) res.warnings.push(`${consoleErrors.length} erreur(s) console`); // WARN
    res.ok = res.problems.length === 0; // ok = aucun problème DUR
  } catch (e) {
    res.problems.push('exception navigation: ' + String(e).slice(0, 160)); // DUR
    res.ok = false;
  } finally {
    await page.close();
  }
  return res;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext();
const routes = [];
for (const r of ROUTES) routes.push(await checkRoute(context, r));
await browser.close();

const ok = routes.every((r) => r.ok);
const warnings_total = routes.reduce((n, r) => n + r.warnings.length, 0);
console.log(JSON.stringify({ base: BASE, ok, warnings_total, routes }, null, 2));
process.exit(ok ? 0 : 1);
