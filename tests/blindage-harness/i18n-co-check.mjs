// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Vérificateur i18n corsu (bêta) · feat/i18n-corsu-beta
// Création : 2026-06-10
// ═══════════════════════════════════════════════════════════════════════════
//
// Vérifie les 3 invariants de la passe i18n CO :
//   1. FR INTACT par défaut : app.html sans ?lang=co → lang="fr", chrome FR,
//      AUCUNE chaîne corse visible, pas de hook __telluxI18n.
//   2. CO via ?lang=co : lang="co", chrome corse (échantillon de sondes),
//      compteur applied === total (0 chaîne sautée = 0 drift FR),
//      zéro erreur console.
//   3. PAS DE BOUTON PUBLIC : aucun lien/bouton vers ?lang=co dans le DOM FR.
//
// Ce check est COMPLÉMENTAIRE à eval-app-rubric.mjs (rubrique §5.1, FR) —
// il ne remplace pas la non-régression FR, il vérifie l'additivité CO.
//
// SORTIE : JSON sur stdout. Exit 0 si tous les checks passent, sinon 2.
//
// USAGE :
//   cd tests/blindage-harness
//   node i18n-co-check.mjs
//   EVAL_HEADFUL=1 node i18n-co-check.mjs     # debug visuel
// ═══════════════════════════════════════════════════════════════════════════

import { chromium } from 'playwright';
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize, resolve as pathResolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { installSupabaseCache } from './supabase-cache.mjs';

const __filename = fileURLToPath(import.meta.url);
const REPO_ROOT = pathResolve(__filename, '..', '..', '..');

const PORT = Number(process.env.I18N_CHECK_PORT) || 3781;
const HEADLESS = process.env.EVAL_HEADFUL !== '1';
const BOOT_WAIT_MS = Number(process.env.I18N_CHECK_BOOT_MS) || 12_000;

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

function startStaticServer(root, port) {
  return new Promise((resolve, reject) => {
    const server = http.createServer(async (req, res) => {
      try {
        const u = new URL(req.url, `http://${req.headers.host || '127.0.0.1'}`);
        let pathname = decodeURIComponent(u.pathname);
        if (pathname.endsWith('/')) pathname += 'index.html';
        const fp = normalize(join(root, pathname));
        if (!fp.startsWith(normalize(root))) {
          res.writeHead(403);
          res.end('forbidden');
          return;
        }
        const data = await readFile(fp);
        const mime = MIME[extname(fp).toLowerCase()] || 'application/octet-stream';
        res.writeHead(200, { 'Content-Type': mime, 'Access-Control-Allow-Origin': '*' });
        res.end(data);
      } catch {
        res.writeHead(404);
        res.end('not found');
      }
    });
    server.on('error', reject);
    server.listen(port, '127.0.0.1', () => resolve(server));
  });
}

// Échantillon de sondes CO : [sélecteur, attendu FR, attendu CO]
const SAMPLE = [
  [".hdr-actions button[onclick='toggleMethodology()']", 'Méthodologie', 'Metodulugia'],
  [".hdr-actions a[href='patrimoine.html']", 'Patrimoine (bêta)', 'Patrimoniu (beta)'],
  ['#b-hot', 'Champ composite', 'Campu cumpostu'],
  ['#b-failles', 'Failles tectoniques', 'Faglie tettoniche'],
  ['.cform-title', 'Contribution terrain', 'Cuntribuzione di terrenu'],
  ['.tx-footer-brand', 'Tellux Corse', 'Tellux Corsica'],
  ['#glossary-title', 'Glossaire & guides', 'Glussariu è guide'],
];

async function inspect(page) {
  return await page.evaluate((sample) => {
    const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
    const texts = sample.map(([sel]) => {
      const el = document.querySelector(sel);
      return el ? norm(el.textContent) : null;
    });
    return {
      lang: document.documentElement.lang,
      title: document.title,
      texts,
      i18nHook: typeof window.__telluxI18n !== 'undefined' ? window.__telluxI18n : null,
      // Bouton/lien public vers ?lang=co ?
      publicToggle: !!document.querySelector("a[href*='lang=co'], button[data-lang='co']"),
    };
  }, SAMPLE);
}

const result = {
  timestamp: new Date().toISOString(),
  checks: {},
  fails: [],
};

let server = null;
let browser = null;
try {
  server = await startStaticServer(REPO_ROOT, PORT);
  browser = await chromium.launch({ headless: HEADLESS });

  // ── Passe 1 : FR par défaut ──────────────────────────────────────────────
  {
    const page = await browser.newPage();
    await installSupabaseCache(page.context(), { label: 'i18n-co-check:fr' }); // brief BN
    const consoleErrors = [];
    page.on('console', (msg) => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
    page.on('pageerror', (err) => consoleErrors.push(String(err)));
    await page.goto(`http://127.0.0.1:${PORT}/app.html`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(BOOT_WAIT_MS);
    const fr = await inspect(page);
    result.checks.fr = {
      lang: fr.lang,
      lang_ok: fr.lang === 'fr',
      chrome_fr_ok: fr.texts.every((t, i) => t === SAMPLE[i][1]),
      no_corsican: fr.texts.every((t, i) => t !== SAMPLE[i][2]),
      no_i18n_hook: fr.i18nHook === null,
      no_public_toggle: !fr.publicToggle,
      console_errors: consoleErrors.length,
      textes: fr.texts,
    };
    if (!result.checks.fr.lang_ok) result.fails.push({ check: 'fr_lang', detail: `lang=${fr.lang}` });
    if (!result.checks.fr.chrome_fr_ok) result.fails.push({ check: 'fr_chrome', detail: JSON.stringify(fr.texts) });
    if (!result.checks.fr.no_corsican) result.fails.push({ check: 'fr_pollution_co', detail: 'chaîne corse visible en mode FR' });
    if (!result.checks.fr.no_i18n_hook) result.fails.push({ check: 'fr_hook', detail: '__telluxI18n défini en mode FR' });
    if (!result.checks.fr.no_public_toggle) result.fails.push({ check: 'fr_toggle_public', detail: 'lien/bouton ?lang=co trouvé dans le DOM' });
    await page.close();
  }

  // ── Passe 2 : CO via ?lang=co ────────────────────────────────────────────
  {
    const page = await browser.newPage();
    await installSupabaseCache(page.context(), { label: 'i18n-co-check:co' }); // brief BN
    const consoleErrors = [];
    page.on('console', (msg) => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
    page.on('pageerror', (err) => consoleErrors.push(String(err)));
    await page.goto(`http://127.0.0.1:${PORT}/app.html?lang=co`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(BOOT_WAIT_MS);
    const co = await inspect(page);
    // Bruit CORS localhost non représentatif de la prod (même filtre que
    // eval-app-rubric) : on ne compte que les erreurs non réseau.
    const realErrors = consoleErrors.filter((e) =>
      !/CORS|Failed to fetch|net::|ERR_|blocked by CORS|TypeError: NetworkError|access control/i.test(e));
    result.checks.co = {
      lang: co.lang,
      lang_ok: co.lang === 'co',
      title: co.title,
      title_ok: /Palesà l'invisibile/.test(co.title),
      chrome_co_ok: co.texts.every((t, i) => t === SAMPLE[i][2]),
      applied: co.i18nHook ? co.i18nHook.applied : null,
      total: co.i18nHook ? co.i18nHook.total : null,
      skipped: co.i18nHook ? co.i18nHook.skipped : null,
      no_drift: !!co.i18nHook && co.i18nHook.applied === co.i18nHook.total,
      no_public_toggle: !co.publicToggle,
      console_errors: realErrors.length,
      console_errors_detail: realErrors.slice(0, 5),
      textes: co.texts,
    };
    if (!result.checks.co.lang_ok) result.fails.push({ check: 'co_lang', detail: `lang=${co.lang}` });
    if (!result.checks.co.title_ok) result.fails.push({ check: 'co_title', detail: co.title });
    if (!result.checks.co.chrome_co_ok) result.fails.push({ check: 'co_chrome', detail: JSON.stringify(co.texts) });
    if (!result.checks.co.no_drift) {
      result.fails.push({
        check: 'co_drift',
        detail: `applied=${result.checks.co.applied}/${result.checks.co.total} — sautées : ${(result.checks.co.skipped || []).join(', ')}`,
      });
    }
    if (result.checks.co.console_errors > 0) {
      result.fails.push({ check: 'co_console', detail: realErrors.slice(0, 3).join(' | ') });
    }
    await page.close();
  }
} catch (err) {
  result.fails.push({ check: 'harness', detail: String(err) });
} finally {
  if (browser) await browser.close().catch(() => {});
  if (server) server.close();
}

result.ok = result.fails.length === 0;
console.log(JSON.stringify(result, null, 2));
process.exit(result.ok ? 0 : 2);
