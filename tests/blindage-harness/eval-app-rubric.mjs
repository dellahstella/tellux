// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Évaluateur Axe APP (Playwright, rubrique §5.1 PROTOCOLE_AUTO_ITERATION)
// Création : 2026-06-09 · feat/app-rubric-harness
// ═══════════════════════════════════════════════════════════════════════════
//
// Évalue app.html VIVANTE contre la rubrique Axe APP du protocole
// d'auto-itération. Ce script EST l'évaluateur — il critique uniquement,
// ne corrige pas. Il s'exécute en contexte FRAIS (lancement séparé du pas
// de génération), de manière sévère.
//
// SÉPARATION GÉNÉRATEUR / ÉVALUATEUR (§2 du protocole) : ce fichier ne doit
// JAMAIS être appelé par le générateur dans la foulée d'une édition. Il
// tourne dans un sous-process distinct, avec un prompt de session distinct.
//
// RUBRIQUE §5.1 — codée verbatim, pas inventée :
//   • Fonctionnalité      0.35
//   • Non-régression      0.30
//   • Craft / UX          0.20
//   • Robustesse          0.15
//   Seuil : 7.0 / 10 pondéré.
//
// CHECKS FALSIFIABLES §5.1 — codés tels qu'écrits, pas étendus :
//   1. Boot : 9 couches chargent
//   2. Init JS ne se déclenche qu'une fois (bug connu = 3x → flag Robustesse)
//   3. Indice Tellux dual visible (format `P{n} N{m}`)
//   4. Toggle légende fonctionne (Brief 49)
//   5. Drill-down poupée russe s'ouvre/ferme (Brief 47)
//   6. Filtre côtier isLand() rejette antennes en mer
//   7. Dashboard conditions affiche 4 sections (Kp / atmo / charge / terrain)
//   8. Console : zéro erreur rouge au boot + après interaction
//
// SORTIE : JSON sur stdout — { rubrique, score_pondere, threshold_met, fails }
// Exit code : 0 si score >= 7.0, sinon 2 (cohérent avec gate §10).
//
// USAGE :
//   cd tests/blindage-harness
//   node eval-app-rubric.mjs                       # serveur statique local
//   APP_URL=https://tellux.pages.dev/app.html \
//     node eval-app-rubric.mjs                     # mode prod (sans local)
//   EVAL_HEADFUL=1 node eval-app-rubric.mjs        # debug visuel chromium
// ═══════════════════════════════════════════════════════════════════════════

import { chromium } from 'playwright';
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize, resolve as pathResolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { installSupabaseCache } from './supabase-cache.mjs';

const __filename = fileURLToPath(import.meta.url);
const REPO_ROOT = pathResolve(__filename, '..', '..', '..');

const DEFAULT_PORT = Number(process.env.EVAL_PORT) || 3780;
const DEFAULT_HEADLESS = process.env.EVAL_HEADFUL !== '1';
const BOOT_TIMEOUT_MS = Number(process.env.EVAL_BOOT_TIMEOUT_MS) || 45_000;
const INTERACT_DELAY_MS = Number(process.env.EVAL_INTERACT_MS) || 1500;
const APP_URL_OVERRIDE = process.env.APP_URL;

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

// ─── Static server (utilisé quand APP_URL n'est pas fourni) ────────────────

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

// ─── Boot detection (signaux app.html du moteur calc*) ─────────────────────

// WMM_GRID retirée de ce gate le 2026-09-04 (brief AR, suite) : app.html ne la charge plus au
// boot (chargement paresseux, activateExpertMode()) — ce script n'active jamais le mode
// Expertise, donc booted resterait false indéfiniment sinon (mesuré : score_pondere 5.8/10,
// booted=false, 0/9 couches, avant ce retrait). La question séparée de savoir si WMM_grid
// doit continuer à compter comme une des « 9 couches » de PROBE_LAYERS_COUNT plus bas — ce
// n'est pas un vrai calque visuel, à la différence des 8 autres — reste ouverte (cf. rapport
// _drafts/DIAGNOSTIC_WMM_CALCUL_SANS_SURFACE_BRIEF_AR_2026-09-04.md, non committé) ; ce
// correctif-ci ne fait que réparer le boot, pas retoucher le barème.
const BOOT_READY_FN = function () {
  try {
    if (typeof calcAll_v2 !== 'function') return false;
    if (!Array.isArray(HTA_SEGMENTS_DATA) || HTA_SEGMENTS_DATA.length === 0) return false;
    if (!SEGMENT_GRID || typeof SEGMENT_GRID !== 'object') return false;
    return true;
  } catch (_e) {
    return false;
  }
};

// ─── Sondes par check (§5.1) ────────────────────────────────────────────────

// Probe — Boot : compte les couches du moteur Tellux.
// Le protocole §5.1 énumère 9 couches : HTA, WMM grid, ANFR antennes,
// mesures certifiées, TDF, Radon, postes sources, éoliennes, hotspots U/Th.
// Noms de globals confirmés par lecture app.html :
//   HTA_SEGMENTS_DATA, WMM_GRID, TDF_EMITTERS, POSTES_SOURCES,
//   EOLIENNES_DATA, POINTS_CHAUDS_RADIO, MESURES_CERTIFIEES,
//   RADON_L3_INSEE_SET (Set communes niveau 3).
// Les antennes ANFR sont chargées via loadAnt() Supabase et exposées
// uniquement via un global window.__telluxLayers si présent (hook de
// debug optionnel, cf. §8 protocole) — sinon comptage des markers Leaflet.
const PROBE_LAYERS_COUNT = function () {
  const layers = {
    HTA_segments: Array.isArray(HTA_SEGMENTS_DATA) ? HTA_SEGMENTS_DATA.length : null,
    WMM_grid: Array.isArray(WMM_GRID) ? WMM_GRID.length : null,
    TDF_emitters: typeof TDF_EMITTERS !== 'undefined' && Array.isArray(TDF_EMITTERS) ? TDF_EMITTERS.length : null,
    postes_sources: typeof POSTES_SOURCES !== 'undefined' && Array.isArray(POSTES_SOURCES) ? POSTES_SOURCES.length : null,
    eoliennes: typeof EOLIENNES_DATA !== 'undefined' && Array.isArray(EOLIENNES_DATA) ? EOLIENNES_DATA.length : null,
    hotspots_uth: typeof POINTS_CHAUDS_RADIO !== 'undefined' && Array.isArray(POINTS_CHAUDS_RADIO) ? POINTS_CHAUDS_RADIO.length : null,
    mesures_certifiees: typeof MESURES_CERTIFIEES !== 'undefined' && Array.isArray(MESURES_CERTIFIEES) ? MESURES_CERTIFIEES.length : null,
    radon_communes_L3: (typeof RADON_L3_INSEE_SET !== 'undefined' && RADON_L3_INSEE_SET && typeof RADON_L3_INSEE_SET.size === 'number') ? RADON_L3_INSEE_SET.size : null,
  };
  // ANFR antennes : préférer le hook de debug si exposé, sinon le compteur
  // du status header (nOnshore est stocké dans le label).
  let antennesAnfr = null;
  if (typeof window !== 'undefined' && window.__telluxLayers && typeof window.__telluxLayers.antennes_anfr === 'number') {
    antennesAnfr = window.__telluxLayers.antennes_anfr;
  } else {
    const hdr = document.querySelector('#hdr-status, .hdr-status, [data-status]');
    const txt = hdr ? hdr.textContent || '' : '';
    const m = txt.match(/(\d{3,5})\s*antennes/i);
    antennesAnfr = m ? Number(m[1]) : null;
  }
  layers.ANFR_antennes = antennesAnfr;
  const loadedCount = Object.values(layers).filter(v => typeof v === 'number' && v > 0).length;
  return { layers, loadedCount };
};

// Probe — Init JS unique : compte combien de fois la fonction `bootApp` (ou
// équivalent d'initialisation principale) a été appelée. Sur app.html, il
// n'y a pas de compteur natif → on instrumente côté page après chargement.
// Cette sonde est best-effort ; si on ne peut pas instrumenter, on retourne
// `null` (interprétation : pas de signal négatif).
const PROBE_INIT_COUNT_NULL = null; // Hook absent → null. Voir flag explicite ci-dessous.

// Probe — Indice Tellux (score unique depuis ADR-064/brief T, 2026-09-03).
// Corrigé 2026-09-04 (brief AT, arbitrage Soleil) : le protocole §5.1 énonce
// encore le format historique `P{n} N{m}` (double score) — cette moitié a
// été retirée du popup par ADR-064, « Activité naturelle » n'y est plus
// affichée nulle part (cf. rapport _drafts/RAPPORT_BRIEF_AT_ACTIVNAT_DOUBLE_
// COMPTAGE_2026-09-04.md). L'ancienne sonde cherchait ce texte mort ET
// retombait, faute de le trouver, sur un sélecteur générique
// (`.leaflet-popup-content`, qui matche dès qu'un popup existe, quel que
// soit son contenu) — elle passait donc sans jamais vérifier qu'un score
// s'affiche réellement. Vérifié en direct sur tellux.pages.dev/app : le DOM
// réel est `<div style="font-weight:700...">🔴 5/5</div>` PUIS, dans un
// <div> frère séparé, le libellé « Perturbation » — l'ancien regex
// `Perturbation\s+\d\/5` ne pouvait de toute façon jamais matcher cet ordre.
// La sonde vérifie maintenant directement le bloc `font-weight:700` du
// popup (celui que rend phHeaderHTML, app.html) pour un chiffre suivi de
// `/5` — le score qui existe réellement aujourd'hui. Nom de fonction et clé
// `indice_dual`/`check:'indice_dual'` conservés tels quels (compatibilité
// des consommateurs du JSON de sortie), même si « dual » ne décrit plus ce
// qui est mesuré.
//
// L'indice n'est calculé qu'APRÈS un clic sur la carte (handler map.on
// 'click' déclenche calcAll_v2 + rendu popup avec indice). On simule un
// clic sur un point land plausible (Ajaccio centre).
async function probeIndiceDual(page) {
  // Cliquer sur Ajaccio (un point land sûr) via les coords Leaflet.
  // Plus fiable qu'un clic pixel au centre map (qui peut tomber en mer).
  try {
    const clicked = await page.evaluate(() => {
      try {
        if (typeof map === 'undefined' || !map || typeof map.fireEvent !== 'function') return false;
        const latlng = L.latLng(41.92, 8.74); // Ajaccio centre
        const point = map.latLngToContainerPoint(latlng);
        map.fireEvent('click', { latlng, containerPoint: point, layerPoint: point });
        return true;
      } catch (_e) { return false; }
    });
    if (clicked) {
      await page.waitForTimeout(INTERACT_DELAY_MS);
    }
  } catch (_e) { /* on continue */ }

  // Cible le bloc réel du score (phHeaderHTML, app.html) plutôt qu'un texte
  // générique — pas de repli sur `.leaflet-popup-content` seul : sans chiffre
  // `/5` dedans, ce n'est pas un score, même si un popup est bien ouvert.
  try {
    const scoreEl = page.locator('.leaflet-popup-content div[style*="font-weight:700"]').first();
    const visible = await scoreEl.isVisible({ timeout: 800 }).catch(() => false);
    if (!visible) return { matched: null };
    const txt = await scoreEl.textContent().catch(() => '');
    const scoreVisible = /\d\s*\/\s*5/.test(txt || '');
    return { matched: scoreVisible ? 'perturbation_score' : null, score_text: txt || null };
  } catch (_e) {
    return { matched: null };
  }
}

// Probe — toggle de légende. Sélecteur confirmé : #legende-toggle (cf. app.html l.1151).
async function probeLegendToggle(page) {
  const candidates = [
    '#legende-toggle',
    '#legend-toggle',
    '[data-action="toggle-legend"]',
  ];
  for (const sel of candidates) {
    try {
      const el = page.locator(sel).first();
      if (await el.count() === 0) continue;
      await el.click({ timeout: 2000 });
      await page.waitForTimeout(INTERACT_DELAY_MS);
      return { selector: sel, clicked: true };
    } catch (_e) { /* essayer suivant */ }
  }
  return { selector: null, clicked: false };
}

// Probe — drill-down poupée russe (Brief 47). On ne valide que la PRÉSENCE
// d'un mécanisme drill-down (popup, modale, panel détaillé) après clic.
async function probeDrillDown(page) {
  const candidates = [
    '.leaflet-popup-content',
    '.drill-down-panel',
    '[data-drill-down]',
    '.modal-overlay.open',
  ];
  for (const sel of candidates) {
    try {
      if (await page.locator(sel).count() > 0) {
        return { selector: sel, present: true };
      }
    } catch (_e) { /* */ }
  }
  return { selector: null, present: false };
}

// Probe — filtre côtier des antennes offshore. Le protocole §5.1 parle de
// `isLand()` mais app.html a migré vers un filtre `commune` (PR #756) :
// les antennes sans rattachement commune sont considérées offshore et
// rejetées du rendu. La sonde vérifie le MÉCANISME (count antennes
// effectivement rendues) plutôt que la fonction nommée.
//
// IMPORTANT (correction 2026-06-10) : on NE demande PAS `offshore > 0`.
// État nominal post-backfill = 0 offshore (toutes les antennes Corse ont
// un code_insee_commune résolu via polygones IGN + fallback reverse-géocode
// BAN). La sonde valide :
//   (a) la logique de catégorisation lit la source de vérité (hook publié,
//       compteurs cohérents avec le rendu) ;
//   (b) aucune antenne réelle n'est masquée (onshore = total ANFR Corse).
// La sonde DOIT passer avec offshore = 0. Une régression future qui
// re-introduirait des antennes "offshore" sera signalée comme info, pas
// comme fail — sauf si onshore chute (vrai signal de masquage erroné).
async function probeIsLandFilter(page) {
  return await page.evaluate(() => {
    try {
      // 1) Si la fonction historique isLand existe encore (ancien chemin) →
      //    on la vérifie sur 1 point mer + 1 point land.
      if (typeof isLand === 'function') {
        const sea = isLand(42.5, 9.9);
        const land = isLand(42.0, 9.05);
        return { method: 'isLand', sea_off: sea, land_ajaccio: land,
                 ok: sea === false && land === true };
      }
      // 2) Sinon : vérifier le filtre par `commune` côté Supabase / loadAnt.
      //    Le hook publie nOnshore (rendu) et nOffshore (rejeté). Le critère
      //    de passage est : la logique a tourné (compteurs présents) ET
      //    onshore > 0 (aucune antenne réelle masquée). offshore peut être 0
      //    (état nominal post-backfill INSEE) ou > 0 (régression à signaler).
      if (typeof window !== 'undefined' && window.__telluxLayers &&
          typeof window.__telluxLayers.antennes_anfr === 'number' &&
          typeof window.__telluxLayers.antennes_offshore === 'number') {
        const onshore = window.__telluxLayers.antennes_anfr;
        const offshore = window.__telluxLayers.antennes_offshore;
        return {
          method: 'commune_filter (hook)', onshore, offshore,
          // PASS si la logique a publié des compteurs cohérents ET au moins
          // une antenne onshore réelle. offshore = 0 = nominal post-backfill.
          ok: onshore > 0,
          // Info : tag "nominal" si offshore = 0 (état attendu après pipeline),
          // "regression" si offshore > 0 (signale qu'une antenne réelle pourrait
          // être incorrectement masquée — à investiguer hors sonde).
          state: offshore === 0 ? 'nominal' : 'regression-suspecte',
        };
      }
      // 3) Fallback : examiner le texte du status header pour repérer un
      //    compteur d'antennes onshore filtrées.
      const hdr = document.querySelector('#hdr-status, .hdr-status');
      const txt = hdr ? hdr.textContent || '' : '';
      const m = txt.match(/(\d{3,5})\s*antennes/i);
      if (m) {
        // S'il y a un compteur, on considère qu'un filtre a tourné même
        // si on ne peut pas distinguer offshore vs onshore.
        return { method: 'count_only', onshore: Number(m[1]), ok: Number(m[1]) > 0 };
      }
      return { method: 'none', ok: false };
    } catch (e) {
      return { method: 'error', error: String(e), ok: false };
    }
  });
}

// Probe — dashboard conditions : sélecteur confirmé `#conditions-bar`.
// Le protocole §5.1 attend 4 sections (Kp solaire, atmo, charge, terrain).
// La sonde recherche les badges/sections sous le container conditions-bar.
async function probeDashboardConditions(page) {
  const containerSel = '#conditions-bar';
  try {
    if (await page.locator(containerSel).count() === 0) {
      return { container: null, sections_found: 0, note: 'pas de #conditions-bar' };
    }
    // Stratégie 1 : compter les badges du résumé
    const badgeCount = await page.locator(`${containerSel} .cond-badge`).count();
    // Stratégie 2 : ouvrir le détail (clic toggle) et compter les sections
    try {
      const toggle = page.locator(`${containerSel} #conditions-bar-toggle, ${containerSel}-toggle`).first();
      if (await toggle.count() > 0) await toggle.click({ timeout: 1500 });
      await page.waitForTimeout(INTERACT_DELAY_MS);
    } catch (_e) { /* */ }
    const detailSectionCount = await page.locator(`${containerSel} #conditions-bar-details > *, ${containerSel} .conditions-section`).count();
    const sections = Math.max(badgeCount, detailSectionCount);
    return { container: containerSel, sections_found: sections, badges: badgeCount, detail_sections: detailSectionCount };
  } catch (_e) {
    return { container: containerSel, sections_found: 0 };
  }
}

// ─── Scoring rubrique §5.1 ──────────────────────────────────────────────────

const RUBRIC_WEIGHTS = {
  fonctionnalite: 0.35,
  non_regression: 0.30,
  craft_ux: 0.20,
  robustesse: 0.15,
};
const THRESHOLD = Number(process.env.EVAL_THRESHOLD) || 7.0;

function scoreFromChecks({ booted, layers, indice, toggleLegend, drillDown, filtreCoter, dashboard, errorsBoot, errorsInteract }) {
  // — Fonctionnalité (0.35) : indice dual + drill-down + toggle légende + filtre côtier
  let fonc = 1;
  const foncSignals = [indice?.matched, toggleLegend?.clicked, drillDown?.present, filtreCoter?.ok].filter(Boolean).length;
  if (foncSignals === 4) fonc = 9;
  else if (foncSignals === 3) fonc = 7;
  else if (foncSignals === 2) fonc = 5;
  else if (foncSignals === 1) fonc = 3;

  // — Non-régression données (0.30) : couches chargées (cible 9) + dashboard 4 sections
  let regr = 1;
  const layerCount = layers?.loadedCount ?? 0;
  const dashSections = dashboard?.sections_found ?? 0;
  if (layerCount >= 9 && dashSections >= 4) regr = 9;
  else if (layerCount >= 9 && dashSections >= 3) regr = 8;
  else if (layerCount >= 7) regr = 6;
  else if (layerCount >= 5) regr = 4;
  else if (layerCount >= 3) regr = 2;

  // — Craft / UX (0.20) : interactions opérationnelles (toggle + drill)
  let craft = 4;
  if (toggleLegend?.clicked && drillDown?.present) craft = 7;
  if (toggleLegend?.clicked && drillDown?.present && indice?.matched) craft = 8;

  // — Robustesse (0.15) : console clean au boot + après interaction
  let robust = 5;
  if (errorsBoot === 0 && errorsInteract === 0) robust = 9;
  else if (errorsBoot === 0 && errorsInteract <= 2) robust = 7;
  else if (errorsBoot <= 2 && errorsInteract <= 2) robust = 5;
  else robust = Math.max(1, 5 - (errorsBoot + errorsInteract));

  // Pondéré
  const weighted =
    fonc * RUBRIC_WEIGHTS.fonctionnalite +
    regr * RUBRIC_WEIGHTS.non_regression +
    craft * RUBRIC_WEIGHTS.craft_ux +
    robust * RUBRIC_WEIGHTS.robustesse;

  return {
    par_critere: {
      fonctionnalite: { note: fonc, poids: RUBRIC_WEIGHTS.fonctionnalite },
      non_regression: { note: regr, poids: RUBRIC_WEIGHTS.non_regression },
      craft_ux: { note: craft, poids: RUBRIC_WEIGHTS.craft_ux },
      robustesse: { note: robust, poids: RUBRIC_WEIGHTS.robustesse },
    },
    score_pondere: Math.round(weighted * 1000) / 1000,
    threshold: THRESHOLD,
    threshold_met: weighted >= THRESHOLD,
  };
}

// ─── Main ───────────────────────────────────────────────────────────────────

async function main() {
  let server = null;
  let appUrl = APP_URL_OVERRIDE;
  if (!appUrl) {
    server = await startStaticServer(REPO_ROOT, DEFAULT_PORT);
    appUrl = `http://127.0.0.1:${DEFAULT_PORT}/app.html`;
  }

  const browser = await chromium.launch({ headless: DEFAULT_HEADLESS });
  const context = await browser.newContext();
  await installSupabaseCache(context, { label: 'eval-app-rubric' }); // brief BN
  const page = await context.newPage();

  // Tracking des erreurs console — séparés boot vs interaction.
  // CORS errors depuis localhost vers les API externes (RTE, BGS geomag,
  // NOAA SWPC) sont du bruit attendu : en prod sur tellux.pages.dev, le
  // domaine est allowlisté côté API. On les met de côté (env metadata
  // pour audit) mais on ne les compte pas dans le scoring "console clean".
  const CORS_NOISE_RE = /CORS\s+policy|Access.*has been blocked|Failed to load resource.*ERR_FAILED|net::ERR_FAILED/i;
  // Liste des hostnames externes pour lesquels les erreurs net:: ne sont pas
  // imputables à app.html (allowlist remoteOrigin). Documentation.
  const _EXTERNAL_HOSTS_NOISE = [
    'rte-france.com', 'bgs.ac.uk', 'swpc.noaa.gov', 'noaa.gov',
    'iservices.rte', 'geomag', 'teleray', 'asnr', 'irsn',
  ];
  const errorsBoot = [];
  const errorsInteract = [];
  const corsNoise = [];
  let boot_done = false;
  const recordError = (text, meta) => {
    if (CORS_NOISE_RE.test(text)) { corsNoise.push({ text, ...meta }); return; }
    (boot_done ? errorsInteract : errorsBoot).push({ text, ...meta });
  };
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      recordError(msg.text().slice(0, 240), { location: msg.location?.()?.url ?? null });
    }
  });
  page.on('pageerror', (err) => {
    recordError(String(err).slice(0, 240), { pageerror: true });
  });

  const fails = [];
  let booted = false;
  let layers = null;
  let indice = null;
  let toggleLegend = null;
  let drillDown = null;
  let filtreCoter = null;
  let dashboard = null;

  try {
    // domcontentloaded suffit pour démarrer ; les fetchs Supabase / WMM /
    // tuiles continuent en arrière-plan et 'networkidle' ne se déclenche
    // jamais sur une app cartographique vivante (timeout garanti). On attend
    // ensuite le boot moteur via BOOT_READY_FN.
    await page.goto(appUrl, { waitUntil: 'domcontentloaded', timeout: BOOT_TIMEOUT_MS });

    // Dismiss disclaimer overlay (recouvre l'interaction avec la page).
    // Best-effort : le sélecteur peut varier ; on tente plusieurs candidats.
    try {
      const dismissCandidates = [
        '#disclaimer-overlay button:has-text("J\'ai compris")',
        '#disclaimer-overlay button:has-text("OK")',
        '#disclaimer-overlay button:has-text("Accepter")',
        '#disclaimer-overlay .btn-dismiss',
        '#disclaimer-overlay button',
        '.disclaimer-overlay button',
      ];
      for (const sel of dismissCandidates) {
        try {
          const el = page.locator(sel).first();
          if (await el.count() > 0) {
            await el.click({ timeout: 1500 });
            await page.waitForTimeout(500);
            break;
          }
        } catch (_e) { /* try next */ }
      }
      // Fallback : retirer l'overlay du DOM directement si on n'a pas pu cliquer
      await page.evaluate(() => {
        const ov = document.querySelector('#disclaimer-overlay, .disclaimer-overlay');
        if (ov) ov.remove();
      });
    } catch (_e) { /* */ }

    // Attente boot moteur (signaux calcAll_v2 + HTA + WMM + SEGMENT_GRID)
    try {
      await page.waitForFunction(BOOT_READY_FN, null, { timeout: BOOT_TIMEOUT_MS });
      booted = true;
    } catch (_e) {
      fails.push({ check: 'boot', detail: `Moteur calcAll_v2 / HTA_SEGMENTS_DATA / WMM_GRID / SEGMENT_GRID non prêt après ${BOOT_TIMEOUT_MS} ms.` });
    }

    boot_done = true; // tous les console errors qui suivent sont post-boot

    // Sondes (best-effort si pas booted)
    layers = booted ? await page.evaluate(PROBE_LAYERS_COUNT) : { loadedCount: 0, layers: {} };
    if (!layers || layers.loadedCount < 9) {
      fails.push({ check: 'couches', detail: `${layers?.loadedCount ?? 0}/9 couches chargées`, layers: layers?.layers });
    }

    // Ordre important : interactions non destructrices d'abord (legend toggle,
    // filtre côtier). Puis clic-carte qui peut ouvrir un popup. Dashboard en
    // dernier car son toggle change le layout (collapse footer).
    toggleLegend = await probeLegendToggle(page);
    if (!toggleLegend?.clicked) fails.push({ check: 'toggle_legend', detail: 'Toggle légende introuvable ou non cliquable.' });

    filtreCoter = await probeIsLandFilter(page);
    if (!filtreCoter?.ok) fails.push({ check: 'filtre_cotier', detail: `filtre offshore : method=${filtreCoter?.method}, ok=${filtreCoter?.ok}` });

    indice = await probeIndiceDual(page);
    if (!indice?.matched) fails.push({ check: 'indice_dual', detail: 'Indice Tellux (score Perturbation X/5) non visible dans le popup.' });

    drillDown = await probeDrillDown(page);
    if (!drillDown?.present) fails.push({ check: 'drill_down', detail: 'Mécanisme drill-down (popup/modale/panel) non détecté.' });

    dashboard = await probeDashboardConditions(page);
    if ((dashboard?.sections_found ?? 0) < 4) fails.push({ check: 'dashboard_conditions', detail: `${dashboard?.sections_found ?? 0}/4 sections détectées.` });

    if (errorsBoot.length > 0) fails.push({ check: 'console_boot', detail: `${errorsBoot.length} erreurs console au boot.`, errors: errorsBoot.slice(0, 5) });
    if (errorsInteract.length > 0) fails.push({ check: 'console_interact', detail: `${errorsInteract.length} erreurs console après interaction.`, errors: errorsInteract.slice(0, 5) });
  } finally {
    await browser.close();
    if (server) server.close();
  }

  const scoring = scoreFromChecks({
    booted, layers, indice, toggleLegend, drillDown, filtreCoter, dashboard,
    errorsBoot: errorsBoot.length, errorsInteract: errorsInteract.length,
  });

  const result = {
    app_url: appUrl,
    timestamp: new Date().toISOString(),
    rubrique: 'AXE APP §5.1 PROTOCOLE_AUTO_ITERATION',
    booted,
    sondes: {
      couches_chargees: layers?.loadedCount ?? null,
      couches_detail: layers?.layers ?? null,
      indice_dual: indice?.matched ?? null,
      indice_score_text: indice?.score_text ?? null,
      toggle_legend: toggleLegend?.clicked ?? null,
      drill_down: drillDown?.present ?? null,
      filtre_cotier: filtreCoter?.ok ?? null,
      filtre_cotier_method: filtreCoter?.method ?? null,
      dashboard_sections: dashboard?.sections_found ?? null,
      erreurs_console_boot: errorsBoot.length,
      erreurs_console_interact: errorsInteract.length,
      cors_noise_filtered: corsNoise.length,
    },
    scoring,
    fails,
  };

  console.log(JSON.stringify(result, null, 2));
  process.exit(scoring.threshold_met ? 0 : 2);
}

main().catch((err) => {
  console.error('[eval-app-rubric] erreur fatale :', err);
  process.exit(3);
});
