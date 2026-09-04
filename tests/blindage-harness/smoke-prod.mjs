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

// WMM_GRID retirée de ce gate le 2026-09-04 (brief AR, suite) : jamais une dépendance réelle de
// calcAll_v2 (seul updateIgrfWmmDiff(), panneau Expert, la lit) ; app.html ne la charge plus au
// boot depuis le même correctif (chargement paresseux, activateExpertMode()) — ce script ne
// bascule jamais ce mode, donc le condition ci-dessous timeoutait pour rien avant ce retrait
// (WARNING seul, cf. checkRoute() plus bas — jamais un échec bloquant, vérifié avant retrait).
const BOOT_READY_FN = function () {
  try {
    if (typeof calcAll_v2 !== 'function') return false;
    if (!Array.isArray(HTA_SEGMENTS_DATA) || HTA_SEGMENTS_DATA.length === 0) return false;
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

// ─── R1 hero-map : rendu réel ET visible (anti-régression contraste prod) ───
// Le hero map de la landing (#lp-hero-map) est un SVG construit en différé
// (requestIdleCallback) à partir de /public/data/corse_hero_geo.json. Régression
// cible : panneau « quasi uniformément sombre » (carte non rendue, ou rendue mais
// sans contraste sur le panneau #2a2f37). Détection = structure (SVG + zones +
// points + visible) ET pixels (écart-type de luminance du panneau).
// Calibré 2026-06-22 sur prod : sain stdev≈6.0 ; panneau plat (SVG retiré)
// stdev≈1.6 → seuil 3.0 (marge des 2 côtés). Hero masqué < 769px → viewport desktop.
const HERO_STDEV_MIN = Number(process.env.SMOKE_HERO_STDEV_MIN) || 3.0;
const HERO_ZONES_MIN = Number(process.env.SMOKE_HERO_ZONES_MIN) || 50;
const HERO_POINTS_MIN = Number(process.env.SMOKE_HERO_POINTS_MIN) || 5;

// Analyse la luminance d'un élément : screenshot (CSS appliqué) re-décodé par le
// navigateur via un canvas → moyenne / écart-type / fraction de pixels « clairs ».
async function analyzeLuminance(page, sel) {
  const b64 = (await page.locator(sel).first().screenshot()).toString('base64');
  return page.evaluate(async (b) => {
    const img = new Image();
    await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = 'data:image/png;base64,' + b; });
    const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d'); ctx.drawImage(img, 0, 0);
    const d = ctx.getImageData(0, 0, c.width, c.height).data;
    const n = d.length / 4; let sum = 0, sumSq = 0, bright = 0;
    for (let i = 0; i < d.length; i += 4) { const L = 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]; sum += L; sumSq += L * L; if (L > 80) bright++; }
    const mean = sum / n; const variance = sumSq / n - mean * mean;
    return { w: img.width, h: img.height, mean: +mean.toFixed(1), stdev: +Math.sqrt(Math.max(0, variance)).toFixed(2), bright_fraction: +(bright / n).toFixed(4) };
  }, b64);
}

async function checkHeroMap(context) {
  const page = await context.newPage();
  const res = { route: '/', element: '#lp-hero-map', svg: false, zones: 0, points: 0, visible: false, lum: null, ok: false, problems: [], warnings: [] };
  try {
    const resp = await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: NAV_TIMEOUT });
    if (!resp || resp.status() !== 200) res.problems.push(`/ HTTP ${resp ? resp.status() : 'null'}`);
    // Build différé : attendre le SVG (requestIdleCallback timeout 1200 + fetch).
    const built = await page.waitForSelector('#lp-hero-map svg.lp-corse-svg', { timeout: 15_000 }).then(() => true).catch(() => false);
    res.svg = built;
    if (!built) {
      res.problems.push('hero map non construit (SVG #lp-hero-map svg.lp-corse-svg absent) — panneau vide/invisible');
    } else {
      const m = await page.evaluate(() => {
        const svg = document.querySelector('#lp-hero-map svg.lp-corse-svg');
        const r = svg.getBoundingClientRect(); const st = getComputedStyle(svg);
        return {
          zones: document.querySelectorAll('#lp-hero-map .lp-corse-zone').length,
          points: document.querySelectorAll('#lp-hero-map .lp-corse-pt').length,
          visible: r.width > 0 && r.height > 0 && st.display !== 'none' && st.visibility !== 'hidden' && parseFloat(st.opacity || '1') > 0.05,
        };
      });
      res.zones = m.zones; res.points = m.points; res.visible = m.visible;
      if (!m.visible) res.problems.push('hero SVG présent mais non visible (display/visibility/opacity/taille)');
      if (m.zones < HERO_ZONES_MIN) res.problems.push(`hero zones radon=${m.zones} < ${HERO_ZONES_MIN} (carte non rendue ?)`);
      if (m.points < HERO_POINTS_MIN) res.problems.push(`hero points RF=${m.points} < ${HERO_POINTS_MIN}`);
      await page.waitForTimeout(700); // laisser le fade-in 'in' se poser
      res.lum = await analyzeLuminance(page, '#lp-hero-map');
      if (res.lum && res.lum.stdev < HERO_STDEV_MIN) {
        res.problems.push(`hero « quasi uniformément sombre » : écart-type luminance ${res.lum.stdev} < ${HERO_STDEV_MIN} (défaut de contraste / carte non rendue)`);
      }
    }
    res.ok = res.problems.length === 0;
  } catch (e) {
    res.problems.push('exception hero: ' + String(e).slice(0, 160));
    res.ok = false;
  } finally {
    await page.close();
  }
  return res;
}

const browser = await chromium.launch({ headless: true });
// Viewport desktop : le hero map est masqué < 769px (media query), inutile mobile.
const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
const routes = [];
for (const r of ROUTES) routes.push(await checkRoute(context, r));
const hero = await checkHeroMap(context);
await browser.close();

const ok = routes.every((r) => r.ok) && hero.ok;
const warnings_total = routes.reduce((n, r) => n + r.warnings.length, 0) + hero.warnings.length;
console.log(JSON.stringify({ base: BASE, ok, warnings_total, routes, hero }, null, 2));
process.exit(ok ? 0 : 1);
