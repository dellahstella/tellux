// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Garde-fou contraste des panneaux flottants (Playwright)
// Création : 2026-08-31 · chantier « outillage adaptateurs + contraste »
// ═══════════════════════════════════════════════════════════════════════════
//
// POURQUOI CE SCRIPT EXISTE
// -------------------------
// Le mode sombre d'app.html n'est PAS une inversion de palette. Le bloc
// `[data-theme="dark"]{ --tx:…; --bg:…; }` redéfinit ses deux tokens avec des
// valeurs STRICTEMENT IDENTIQUES à celles de `:root` — c'est un no-op. Tout le
// mode sombre repose sur ~24 correctifs manuels `[data-theme="dark"] X{…}`.
// Conséquence : tout composant qui utilise --ardoise / --ardoise-clair / --tx3
// / --pierre-ombre s'affiche en couleurs CLAIRES sur fond sombre, jusqu'à ce
// que quelqu'un écrive le correctif suivant à la main.
//
// Cas réel (2026-08-31, PR #1148) : la jauge crustale, dont les contenus sont
// générés en JS avec des styles INLINE référençant ces tokens, sortait sa
// valeur principale en #1F2329 sur fond #1A1D25 — contraste 1,07. Invisible.
// Le défaut préexistait et n'a été vu que parce qu'un humain a regardé.
//
// Ce script transforme ce mode d'échec « invisible jusqu'à ce qu'on regarde »
// en échec mesuré et reproductible.
//
// POURQUOI PAS axe-core
// ---------------------
// axe-core (@axe-core/playwright, règle `color-contrast`) a été essayé en
// premier, et écarté sur MESURE, pas sur principe : sur app.html il renvoie
// 0 violation, 0 passe et 1 « incomplete » — il n'évalue rien. Les panneaux
// flottent au-dessus d'un canvas Leaflet et ont des fonds semi-transparents ;
// axe ne sait pas résoudre l'arrière-plan effectif et abandonne l'arbre. Un
// check qui ne teste rien est pire qu'absent : il rassure à tort. La
// dépendance a donc été retirée.
//
// CE QUE FAIT CE SCRIPT À LA PLACE
// --------------------------------
// Sonde A — CONTRASTE EFFECTIF (bloquante). Pour chaque panneau de la liste
//   PANELS, dans les deux thèmes : parcourt les éléments porteurs de texte
//   visible, résout l'arrière-plan effectif en compositant les fonds des
//   ancêtres (alpha compris) jusqu'à opacité 1, et calcule le ratio WCAG 2.1.
//   Seuils : 4,5:1 en texte normal, 3:1 en grand texte (>= 24 px, ou >= 18,66 px
//   gras) — définition WCAG, pas un seuil maison.
//   Si la pile d'ancêtres n'atteint jamais l'opacité 1 (cas du panneau posé sur
//   la carte), on composite sur BASE_TONE, déclaré par thème ci-dessous. Le
//   champ `base_fallback_used` du rapport dit exactement quels nœuds sont
//   concernés, pour que l'approximation reste auditable.
//
// Sonde B — PARITÉ DES TOKENS (informative). Liste les tokens de design dont
//   la valeur calculée est IDENTIQUE en clair et en sombre. Ne fait pas
//   échouer : c'est l'inventaire de la dette, pour que le prochain qui ouvre
//   le sujet n'ait pas à la re-dériver.
//
// SORTIE : JSON sur stdout. Exit 0 si aucune violation, 2 sinon.
//
// USAGE :
//   cd tests/blindage-harness
//   node contrast-panels.mjs
//   APP_URL=https://tellux.pages.dev/app.html node contrast-panels.mjs
//   CONTRAST_HEADFUL=1 node contrast-panels.mjs      # debug visuel
// ═══════════════════════════════════════════════════════════════════════════

import { chromium } from 'playwright';
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize, resolve as pathResolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const REPO_ROOT = pathResolve(__filename, '..', '..', '..');

const PORT = Number(process.env.CONTRAST_PORT) || 3782;
const HEADLESS = process.env.CONTRAST_HEADFUL !== '1';
const BOOT_TIMEOUT_MS = Number(process.env.CONTRAST_BOOT_TIMEOUT_MS) || 45_000;
const APP_URL_OVERRIDE = process.env.APP_URL;

// Panneaux audités. Volontairement limité au CHROME FLOTTANT de la carte —
// c'est là que vit le mode d'échec (styles inline générés en JS, fond
// semi-transparent, tokens non thématisés). Le contenu long des pages
// documentaires est hors périmètre : il est en CSS statique et n'a pas de
// mode sombre du tout.
const PANELS = [
  { sel: '#crustal-gauge-panel', nom: 'Jauge crustale' },
  { sel: '#tellux-legends-context', nom: 'Légendes contextuelles (Zone 2)' },
  { sel: '#legende', nom: 'Panneau « ? »' },
  { sel: '#conditions-bar', nom: 'Barre de conditions' },
  { sel: '.hdr', nom: 'En-tête' },
];

// Couches à activer pour que les panneaux existent réellement dans le DOM.
// Sans ça le script vérifierait des conteneurs vides et passerait à tort.
const LAYER_BUTTONS = ['b-crustal', 'b-ant', 'b-res'];

// Fond de repli quand la pile d'ancêtres n'atteint jamais l'opacité 1 (panneau
// posé sur le canvas Leaflet). Valeurs prises sur le fond réellement rendu :
// Esri Light Gray en clair, et la teinte du panneau lui-même en sombre.
const BASE_TONE = { light: [245, 240, 231], dark: [26, 29, 37] };

// Tokens dont la parité clair/sombre est inventoriée par la sonde B.
const TOKENS_AUDITES = [
  '--tx', '--bg', '--tx3', '--ardoise', '--ardoise-clair',
  '--pierre-ombre', '--mica', '--border', '--tx-ardoise', '--tx-pierre',
];

const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.geojson': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.woff2': 'font/woff2', '.ico': 'image/x-icon',
};

function startStaticServer(root, port) {
  return new Promise((resolve, reject) => {
    const server = http.createServer(async (req, res) => {
      try {
        const u = new URL(req.url, `http://${req.headers.host || '127.0.0.1'}`);
        let pathname = decodeURIComponent(u.pathname);
        if (pathname.endsWith('/')) pathname += 'index.html';
        const fp = normalize(join(root, pathname));
        if (!fp.startsWith(normalize(root))) { res.writeHead(403); res.end('forbidden'); return; }
        const data = await readFile(fp);
        res.writeHead(200, {
          'Content-Type': MIME[extname(fp).toLowerCase()] || 'application/octet-stream',
          'Access-Control-Allow-Origin': '*',
        });
        res.end(data);
      } catch (_e) { res.writeHead(404); res.end('not found'); }
    });
    server.on('error', reject);
    server.listen(port, '127.0.0.1', () => resolve(server));
  });
}

// ─── Sonde A — exécutée DANS la page ───────────────────────────────────────
// Tout le calcul vit côté page : getComputedStyle n'est fiable que là, et on
// évite un aller-retour par nœud (les panneaux en comptent plusieurs dizaines).
const PROBE_CONTRAST = function ([panels, baseTone]) {
  const parseRgb = (s) => {
    const m = String(s).match(/-?[\d.]+/g);
    if (!m || m.length < 3) return null;
    return [Number(m[0]), Number(m[1]), Number(m[2]), m.length > 3 ? Number(m[3]) : 1];
  };
  // Composition alpha standard (source OVER destination), canal par canal.
  const over = (src, dst) => {
    const a = src[3];
    return [
      src[0] * a + dst[0] * (1 - a),
      src[1] * a + dst[1] * (1 - a),
      src[2] * a + dst[2] * (1 - a),
      1,
    ];
  };
  const relLum = (c) => {
    const f = c.slice(0, 3).map((v) => {
      const x = v / 255;
      return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2];
  };
  const ratio = (a, b) => {
    const l1 = Math.max(relLum(a), relLum(b));
    const l2 = Math.min(relLum(a), relLum(b));
    return (l1 + 0.05) / (l2 + 0.05);
  };

  const results = [];
  for (const panel of panels) {
    const root = document.querySelector(panel.sel);
    if (!root) { results.push({ panel: panel.nom, sel: panel.sel, etat: 'absent' }); continue; }
    const rs = getComputedStyle(root);
    if (rs.display === 'none' || rs.visibility === 'hidden') {
      results.push({ panel: panel.nom, sel: panel.sel, etat: 'masqué' });
      continue;
    }
    const nodes = [];
    const walk = (el) => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return;
      // On ne mesure que les éléments qui portent EUX-MÊMES du texte visible
      // (un conteneur hérite d'une couleur qu'il n'utilise pas).
      const ownText = Array.from(el.childNodes)
        .filter((n) => n.nodeType === 3 && n.textContent.trim().length > 0)
        .map((n) => n.textContent.trim()).join(' ');
      if (ownText) {
        const r = el.getBoundingClientRect();
        if (r.width > 0 && r.height > 0) nodes.push({ el, cs, texte: ownText.slice(0, 40) });
      }
      for (const child of el.children) walk(child);
    };
    walk(root);

    const items = [];
    for (const n of nodes) {
      const fg = parseRgb(n.cs.color);
      if (!fg) continue;
      // Arrière-plan effectif : on empile les fonds en remontant les ancêtres
      // jusqu'à atteindre l'opacité 1.
      let acc = null, fallback = true;
      for (let el = n.el; el; el = el.parentElement) {
        const bg = parseRgb(getComputedStyle(el).backgroundColor);
        if (!bg || bg[3] === 0) continue;
        acc = acc === null ? bg : over(acc, bg);
        if (acc[3] >= 0.999) { fallback = false; break; }
      }
      const base = [baseTone[0], baseTone[1], baseTone[2], 1];
      const bgFinal = acc === null ? base : (fallback ? over(acc, base) : acc);
      const fgFinal = fg[3] < 1 ? over(fg, bgFinal) : fg;

      const px = parseFloat(n.cs.fontSize) || 16;
      const poids = parseInt(n.cs.fontWeight, 10) || 400;
      // Définition WCAG du « grand texte » : >= 24 px, ou >= 18,66 px en gras.
      const grand = px >= 24 || (px >= 18.66 && poids >= 700);
      const seuil = grand ? 3.0 : 4.5;
      const r = ratio(fgFinal, bgFinal);
      items.push({
        texte: n.texte,
        ratio: Math.round(r * 100) / 100,
        seuil,
        grand_texte: grand,
        px: Math.round(px * 10) / 10,
        couleur: n.cs.color,
        fond_effectif: `rgb(${bgFinal.slice(0, 3).map((v) => Math.round(v)).join(', ')})`,
        base_fallback_used: fallback,
        ok: r >= seuil,
      });
    }
    results.push({
      panel: panel.nom, sel: panel.sel, etat: 'mesuré',
      noeuds: items.length,
      violations: items.filter((i) => !i.ok),
    });
  }
  return results;
};

// ─── Sonde B — parité des tokens ───────────────────────────────────────────
const PROBE_TOKENS = function (noms) {
  const lire = () => {
    const cs = getComputedStyle(document.documentElement);
    const out = {};
    for (const n of noms) out[n] = cs.getPropertyValue(n).trim();
    return out;
  };
  const avant = document.documentElement.getAttribute('data-theme');
  document.documentElement.removeAttribute('data-theme');
  const clair = lire();
  document.documentElement.setAttribute('data-theme', 'dark');
  const sombre = lire();
  if (avant) document.documentElement.setAttribute('data-theme', avant);
  else document.documentElement.removeAttribute('data-theme');
  const identiques = noms.filter((n) => clair[n] && clair[n] === sombre[n]);
  return { clair, sombre, identiques };
};

// ─── Orchestration ─────────────────────────────────────────────────────────

async function main() {
  let server = null;
  let appUrl = APP_URL_OVERRIDE;
  if (!appUrl) {
    server = await startStaticServer(REPO_ROOT, PORT);
    appUrl = `http://127.0.0.1:${PORT}/app.html`;
  }

  const browser = await chromium.launch({ headless: HEADLESS });
  // newContext() explicitement : newPage() direct suffit ici, mais on garde la
  // même forme que les autres harnais du dossier.
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  const rapport = { url: appUrl, themes: {}, tokens: null };

  try {
    await page.goto(appUrl, { waitUntil: 'domcontentloaded', timeout: BOOT_TIMEOUT_MS });
    // Boot : on attend que la couche crustale soit constructible (le bouton
    // existe dès le HTML, mais tog() a besoin du JS initialisé).
    await page.waitForFunction(() => typeof window.tog === 'function', { timeout: BOOT_TIMEOUT_MS });
    await page.waitForTimeout(4000);

    // Activer les couches pour que les panneaux soient réellement peuplés.
    await page.evaluate((ids) => {
      for (const id of ids) {
        const b = document.getElementById(id);
        if (b && !/\bon-/.test(b.className)) b.click();
      }
    }, LAYER_BUTTONS);
    await page.waitForTimeout(3000);
    // Refermer le tiroir des couches : il recouvre la moitié droite et n'est
    // pas ce qu'on audite.
    await page.evaluate(() => {
      const a = document.querySelector('.layers-accordion');
      if (a) a.classList.remove('open');
      const t = document.getElementById('legende-toggle');
      // Ouvrir le « ? » pour que son contenu soit mesurable.
      if (t && document.getElementById('legende-content')
          && getComputedStyle(document.getElementById('legende-content')).display === 'none') t.click();
    });
    await page.waitForTimeout(1200);

    rapport.tokens = await page.evaluate(PROBE_TOKENS, TOKENS_AUDITES);

    for (const theme of ['light', 'dark']) {
      await page.evaluate((t) => {
        if (t === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
        else document.documentElement.removeAttribute('data-theme');
      }, theme);
      await page.waitForTimeout(800);
      // Playwright sérialise PROBE_CONTRAST et l'exécute dans la page — même
      // convention que les autres harnais du dossier (sondes déclarées en
      // haut de fichier, appelées via page.evaluate).
      rapport.themes[theme] = await page.evaluate(
        PROBE_CONTRAST,
        [PANELS, BASE_TONE[theme]],
      );
    }
  } finally {
    await browser.close();
    if (server) server.close();
  }

  const violations = [];
  for (const [theme, panneaux] of Object.entries(rapport.themes)) {
    for (const p of panneaux) {
      for (const v of (p.violations || [])) violations.push({ theme, panel: p.panel, ...v });
    }
  }

  // ─── Cliquet (ratchet) ───────────────────────────────────────────────────
  // app.html porte AUJOURD'HUI une dette de contraste antérieure à ce script
  // (cf. le no-op du bloc [data-theme="dark"] documenté en tête de fichier).
  // Un check qui échoue dès son premier jour serait ignoré en une semaine.
  // On le rend donc utile immédiatement sans exiger la refonte de palette :
  // les plafonds ci-dessous sont calés sur la mesure du jour, et le check
  // tombe dès qu'un chiffre AUGMENTE. Ce sont des cliquets — ils ne doivent
  // JAMAIS être remontés pour faire passer une PR ; la seule direction
  // autorisée est vers le bas, au fur et à mesure des corrections.
  //
  //   critique = ratio < 3,0  → texte illisible ou quasi (le cas de la jauge
  //                             crustale corrigé le 2026-08-31 était à 1,07)
  //   aa       = ratio >= 3,0 mais sous le seuil WCAG applicable
  const MAX_CRITIQUE = Number(process.env.CONTRAST_MAX_CRITIQUE ?? 0);
  const MAX_AA = Number(process.env.CONTRAST_MAX_AA ?? 0);
  const critiques = violations.filter((v) => v.ratio < 3.0);
  const aa = violations.filter((v) => v.ratio >= 3.0);

  const noeudsMesures = Object.values(rapport.themes).flat().reduce((s, p) => s + (p.noeuds || 0), 0);

  const depassements = [];
  // Plancher de couverture — AVANT les cliquets, et pour la même raison qu'axe-core a été
  // écarté : un check qui ne mesure rien passe au vert et rassure à tort. Les cliquets sont des
  // MAJORANTS ; si les panneaux ne se peuplaient pas (Supabase indisponible en CI, boot trop
  // lent, sélecteur renommé), le compte de violations tomberait à zéro et le check passerait
  // en n'ayant rien testé. Ce plancher rend ce scénario bruyant.
  // Référence : 204 nœuds mesurés en local le 2026-08-31, sur 5 panneaux × 2 thèmes.
  const MIN_NOEUDS = Number(process.env.CONTRAST_MIN_NOEUDS ?? 50);
  if (noeudsMesures < MIN_NOEUDS) {
    depassements.push(`couverture insuffisante : ${noeudsMesures} nœuds mesurés < plancher ${MIN_NOEUDS}`
      + ' — les panneaux ne se sont probablement pas peuplés, le résultat n\'est pas exploitable');
  }
  if (critiques.length > MAX_CRITIQUE) {
    depassements.push(`critique : ${critiques.length} > plafond ${MAX_CRITIQUE}`);
  }
  if (aa.length > MAX_AA) {
    depassements.push(`aa : ${aa.length} > plafond ${MAX_AA}`);
  }

  const sortie = {
    outil: 'contrast-panels',
    date_utc: new Date().toISOString(),
    url: rapport.url,
    resume: {
      violations: violations.length,
      critique: critiques.length,
      aa: aa.length,
      plafond_critique: MAX_CRITIQUE,
      plafond_aa: MAX_AA,
      plancher_noeuds: MIN_NOEUDS,
      depassements,
      panneaux_mesures: (rapport.themes.light || []).filter((p) => p.etat === 'mesuré').length,
      noeuds_mesures: noeudsMesures,
      // Sonde B : tokens dont la valeur est identique en clair et en sombre.
      // Informatif — c'est l'inventaire de la dette de thématisation.
      tokens_identiques_clair_sombre: rapport.tokens.identiques,
    },
    violations_critiques: critiques,
    violations_aa: aa,
    detail: rapport.themes,
    tokens: rapport.tokens,
  };
  process.stdout.write(JSON.stringify(sortie, null, 2) + '\n');
  process.exitCode = depassements.length > 0 ? 2 : 0;
}

main().catch((e) => {
  process.stdout.write(JSON.stringify({ outil: 'contrast-panels', erreur: String(e && e.stack || e) }, null, 2) + '\n');
  process.exitCode = 1;
});
