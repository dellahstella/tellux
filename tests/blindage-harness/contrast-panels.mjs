// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Garde-fou contraste des panneaux flottants (Playwright)
// Création : 2026-08-31 · chantier « outillage adaptateurs + contraste »
// ═══════════════════════════════════════════════════════════════════════════
//
// POURQUOI CE SCRIPT EXISTE
// -------------------------
// Les panneaux flottants du chrome carte sont peuplés en JS avec des styles
// INLINE qui référencent des tokens de design (--ardoise, --ardoise-clair,
// --tx3, --pierre-ombre). Rien ne garantit qu'un couple texte/fond y reste
// lisible : ce sont des chaînes HTML assemblées à la main, hors de toute revue
// de feuille de style, et posées au-dessus d'un fond de carte.
//
// Cas réel (2026-08-31, PR #1148) : la jauge crustale sortait sa valeur
// principale à un contraste de 1,07 — invisible. Le défaut préexistait et n'a
// été vu que parce qu'un humain a regardé au bon moment.
//
// Ce script transforme ce mode d'échec « invisible jusqu'à ce qu'on regarde »
// en échec mesuré et reproductible.
//
// THÈME UNIQUE DEPUIS LE 2026-08-31
// ---------------------------------
// Ce script mesurait initialement DEUX thèmes (clair + sombre). Le mode sombre
// d'app.html a été retiré le 2026-08-31 (arbitrage Soleil, Cran C : il stylait
// le chrome UI mais pas le fond de carte, raster clair fixe). La mesure porte
// donc désormais sur le thème unique et servi. La sonde de parité des tokens
// clair/sombre a disparu avec lui — elle n'avait plus d'objet.
// ⚠️ Les tokens ci-dessus ne sont toujours PAS thématisés : si un thème
// alternatif revient un jour, ce script devra rebasculer en multi-thèmes et les
// cliquets être re-dérivés. C'est la seule raison de rouvrir ce fichier.
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
// Sonde CONTRASTE EFFECTIF (bloquante). Pour chaque panneau de la liste PANELS :
//   parcourt les éléments porteurs de texte visible, résout l'arrière-plan
//   effectif en compositant les fonds des ancêtres (alpha compris) jusqu'à
//   opacité 1, et calcule le ratio WCAG 2.1.
//   Seuils : 4,5:1 en texte normal, 3:1 en grand texte (>= 24 px, ou >= 18,66 px
//   gras) — définition WCAG, pas un seuil maison.
//   Si la pile d'ancêtres n'atteint jamais l'opacité 1 (cas du panneau posé sur
//   la carte), on composite sur BASE_TONE. Le champ `base_fallback_used` du
//   rapport dit exactement quels nœuds sont concernés, pour que l'approximation
//   reste auditable.
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
//
// ÉLARGISSEMENT DU 2026-09-01 (dette A11Y-CONTRAST-APP-PANELS-002, volet 3)
// ------------------------------------------------------------------------
// Les 5 panneaux d'origine laissaient un ANGLE MORT : `#expert-panel` portait
// trois violations de classe critique (2,59:1) qu'aucun check ne voyait, et le
// cliquet à 0/0 se lisait comme « plus rien nulle part ». Découvert en marge de
// la PR #1164, en mesurant à la main. Cinq surfaces sont ajoutées ici, dont le
// POPUP AU CLIC — probablement la surface la plus vue de l'application, et
// jamais mesurée jusqu'à ce jour.
//
// `requis: true` = surface dont l'absence fait ÉCHOUER le check. Sans ce
// marqueur, ajouter un panneau qui ne s'ouvre jamais donnerait un faux vert :
// zéro nœud mesuré, zéro violation, check content. Même raisonnement que le
// plancher de couverture plus bas, mais par surface au lieu du total.
const PANELS = [
  { sel: '#crustal-gauge-panel', nom: 'Jauge crustale' },
  { sel: '#tellux-legends-context', nom: 'Légendes contextuelles (Zone 2)' },
  { sel: '#legende', nom: 'Panneau « ? »' },
  { sel: '#conditions-bar', nom: 'Barre de conditions' },
  { sel: '.hdr', nom: 'En-tête' },
  // min_noeuds (2026-09-02) : `requis: true` seul ne protège que contre ZÉRO nœud. Trouvé en CI
  // le jour même de la clôture : le popau a rendu 1 SEUL nœud sur son premier point (démarrage à
  // froid), et `!p.noeuds` (1 est truthy) l'aurait laissé passer sans broncher si le max sur les
  // 4 points avait aussi été dégradé partout — corrigé côté mesure (cf. plus bas, noeuds = max
  // des 4 points), mais un plancher PAR SURFACE ferme le trou pour de bon : un rendu qui tourne
  // très en dessous de son plein effectif connu échoue, même s'il n'est pas littéralement vide.
  // Seuils = ~50-70% du plein effectif mesuré à plusieurs reprises le 2026-09-02, marge pour la
  // variation naturelle du contenu conditionnel sans laisser passer un rendu clairement dégradé.
  { sel: '.leaflet-popup-content', nom: 'Popup au clic (carte)', requis: true, min_noeuds: 15 },
  { sel: '#expert-panel', nom: 'Panneau Expertise', requis: true, min_noeuds: 12 },
  { sel: '#expert-bandeau', nom: 'Bandeau Expertise', requis: true, min_noeuds: 4 },
  { sel: '#myplace-modal', nom: 'Modale « Mon lieu »', requis: true, min_noeuds: 6 },
  { sel: '#cform', nom: 'Contribution terrain', requis: true, min_noeuds: 8 },
];

// Couches à activer pour que les panneaux existent réellement dans le DOM.
// Sans ça le script vérifierait des conteneurs vides et passerait à tort.
const LAYER_BUTTONS = ['b-crustal', 'b-ant', 'b-res'];

// ─── Points de clic du popup (2026-09-01) ──────────────────────────────────
// POURQUOI PLUSIEURS POINTS
// Le popup colore plusieurs de ses éléments par TERNAIRE sur la valeur calculée
// au point cliqué (score de perturbation, score d'activité naturelle, écart Δ,
// classe radon). Un seul clic n'exerce donc QU'UNE branche de chaque couleur :
// le compte de violations dépend de l'endroit où l'on clique, et un « 0 » sur un
// point ne dit rien des autres. Constaté en direct le 2026-09-01 — deux
// coordonnées corses ordinaires faisaient apparaître, sur le SCORE PRINCIPAL en
// 14 px gras, des violations que le point de test ne montrait pas.
// C'est la même famille de défaut que l'angle mort qui a motivé l'élargissement :
// le check ne mesure que ce qu'il exerce.
//
// CHOIX DES POINTS — chacun a été retenu parce qu'il exerce, à la date de sa mesure, une branche
// que les autres ne couvrent pas sur AU MOINS un des deux scores (perturbation, activité) ; ce
// n'est pas un échantillon au hasard. Revérifié en direct le 2026-09-02 (clôture du chantier,
// après le retrait du radon) — colonnes = score affiché / couleur RENDUE, pas déduites :
//   42,00/9,05  perturbation 5/5 (#8E2F1F porphyre) · activité 3/5 (#92400e brun)
//   41,60/9,28  perturbation 3/5 (#8A5E22 ocre — la branche corrigée par le lot 3)
//   42,55/9,45  perturbation 5/5 (dup. pt1) · activité 0/5 (#626774 neutre)
//   42,70/9,40  perturbation 1/5 (#3F5B3A vert, fusionné avec le niveau 2 depuis le lot 3)
//               · activité 0/5 (dup. pt3)
// Ce point 42,70/9,40 a perdu sa justification d'origine ("radon classe 2, branche Ocre") : la
// classe radon a disparu du popup avec le retrait du radon (#1172), qui a aussi fait fusionner
// les niveaux 1 et 2 de la perturbation en une seule couleur (#1175) — la branche qu'il ciblait
// n'existe donc plus SOUS CETTE FORME. Gardé quand même, PAS retiré sans discussion (réduire
// l'échantillonnage silencieusement est précisément le mode d'échec documenté par ce chantier) :
// c'est aujourd'hui le SEUL point des quatre à produire une perturbation de niveau 1 — utile si
// la fusion des niveaux 1/2 est un jour reconsidérée, et son activité à 0/5 sert de doublon de
// confirmation pour la branche neutre plutôt que d'apporter une couverture propre. Une
// justification plus modeste que l'originale, mais réelle — pas inventée pour combler le vide.
// ⚠️ Les scores exacts par point dépendent de facteurs live (proximité HTA, correction Kp quand
// NOAA répond) et peuvent glisser d'une session à l'autre sans que la MESURE DE CONTRASTE (qui ne
// dépend que de la couleur rendue contre le fond, pas du chiffre exact) en soit affectée — vérifié
// stable sur 2 mesures consécutives le 2026-09-02, mais à revérifier si ce fichier est rouvert
// après un changement des seuils de branche (perturbHumain/activNat) ou du jeu de données HTA.
// ⚠️ BRANCHES ENCORE NON EXERCÉES, à documenter plutôt qu'à laisser croire à une couverture
// complète : activité 4/5, et toutes les branches de deltaCol (vert/ocre/porphyre — les 4 points
// rendent tous "—", aucun n'a de contribution terrain assez proche pour produire un delta réel).
// Coût mesuré (2026-09-01, local) : script à 1 point ~21 s -> à 4 points ~31 s,
// soit ~+3,3 s par point ajouté. Round-trip Playwright par point (clic + attente
// POPUP_WAIT_MS + sonde), pas la sonde elle-même. Déterminisme vérifié (2 runs
// consécutifs -> même décompte 12 critique + 5 AA).
const POPUP_POINTS = [
  [42.00, 9.05],
  [41.60, 9.28],
  [42.55, 9.45],
  [42.70, 9.40],
];
const POPUP_WAIT_MS = Number(process.env.CONTRAST_POPUP_WAIT_MS) || 2600;

// ─── Balayage déterministe des branches de #conditions-bar (2026-09-03, brief U) ────────────
// POURQUOI
// La barre de conditions colore ses puces par TERNAIRE sur des valeurs LIVE (Kp NOAA, Dst Kyoto,
// charge RTE, orage/ducting Open-Meteo). Le check ne mesurait donc que la branche que l'activité
// géomagnétique du moment voulait bien lui montrer. Deux conséquences, constatées et non
// théoriques :
//   • ANGLE MORT DURABLE — la branche `--warn` du badge Kp (2 <= Kp < 5) n'a JAMAIS été exercée
//     tant que curKp restait à « — » (Promise.all all-or-nothing de loadNOAA, corrigé le
//     2026-09-03 par le brief P/#1198). Le jour où le Kp s'est peuplé, la violation est apparue
//     — préexistante, jamais mesurée, à 2,91 (sous le seuil critique de 3,0).
//   • CHECK NON DÉTERMINISTE — la même PR #1204 a eu un run ROUGE (Kp 2, branche ocre) puis des
//     runs VERTS (Kp < 2, branche verte) sans qu'une ligne ne change. Un check dont la couleur
//     dépend du Soleil ne protège rien : il est vert la plupart du temps et rouge au hasard.
//
// COMMENT
// Un stub de `fetch` posé AVANT le boot (addInitScript), INERTE tant que `__telluxCondFixture`
// vaut null — la passe principale ci-dessous mesure donc toujours la page telle qu'elle est
// servie, réseau réel compris, exactement comme avant. Après cette passe, on renseigne la
// fixture puis on RÉ-INVOQUE les vraies fonctions de production (loadNOAA, loadDst,
// loadLightning, loadMeteo, loadChargeReseau, updateCondSummaries, syncBadges) : aucune logique
// de branche n'est réimplémentée ici, donc rien à faire dériver le jour où un seuil change.
// Ce qui est balayé est la SURFACE DÉJÀ AU PÉRIMÈTRE (#conditions-bar dans son état de
// production, replié) — ce n'est pas un élargissement, c'est la couverture des branches d'une
// surface qui y était déjà.
//
// CE QUE ÇA NE COUVRE TOUJOURS PAS
// `#conditions-bar-details` (le tiroir déplié) reste hors mesure : replié en production, il est
// en display:none et walk() ne le voit pas. Il porte 16 violations préexistantes MESURÉES le
// 2026-09-03 — 15 de la famille --tx-mica (#74706A à 4,33 sur --tx-pierre : .cond-key ×10,
// légende de sparkline ×3, .ci-tier ×2) + 1 de --tx3 sur --bg3 (« (JSON) » à 4,37) — toutes
// indépendantes des branches de couleur (présentes jusque dans le scénario « calme »). Les
// intégrer ici ferait tomber le check sur une dette d'une AUTRE famille, dont la remédiation
// touche un token gelé (A11Y-CONTRAST-001) : lot séparé, à arbitrer, pas à mélanger.
const COND_SCENARIOS = [
  // Chaque scénario est choisi pour exercer des branches que les autres ne couvrent pas.
  // Colonnes = entrées brutes servies aux vrais loaders, pas des couleurs attendues.
  { nom: 'calme',   kp: 1.2, bz: 3.0,  dens: 2.0,  flux: 3,   dst: -10, ducting: false, orageProb: 5,  orage: false, conso: 120 },
  { nom: 'modéré',  kp: 3.4, bz: -2.0, dens: 8.0,  flux: 40,  dst: -40, ducting: true,  orageProb: 35, orage: false, conso: 280 },
  { nom: 'actif',   kp: 4.5, bz: -2.0, dens: 8.0,  flux: 40,  dst: -40, ducting: true,  orageProb: 35, orage: false, conso: 280 },
  { nom: 'tempête', kp: 7.5, bz: -9.0, dens: 22.0, flux: 500, dst: -80, ducting: false, orageProb: 80, orage: true,  conso: 340 },
];
// Plancher par scénario — même raison que `min_noeuds` sur les surfaces requises : un scénario
// qui ne rend plus rien doit ÉCHOUER, pas rapporter zéro violation. 10 = l'effectif réel de la
// barre repliée (5 puces × clé/valeur), mesuré le 2026-09-03.
const COND_MIN_NOEUDS = 10;

// Stub de fetch — posé au boot, silencieux tant qu'aucune fixture n'est armée.
const INSTALL_COND_FIXTURE = function () {
  window.__telluxCondFixture = null;
  const F = {
    plasma: (s) => [['time_tag', 'density', 'speed', 'temperature'],
                    ['2026-09-03 12:00:00.000', String(s.dens), '450', '100000']],
    mag: (s) => [['time_tag', 'bx', 'by', 'bz'],
                 ['2026-09-03 12:00:00.000', '1', '1', String(s.bz)]],
    protons: (s) => [{ time_tag: '2026-09-03T12:00:00Z', flux: s.flux, energy: '>=10 MeV' }],
    kp: (s) => [{ time_tag: '2026-09-03T12:00:00Z', kp_index: s.kp, estimated_kp: s.kp }],
    dst: (s) => [{ time_tag: '2026-09-03T12:00:00Z', dst: String(s.dst) }],
    rte: (s) => ({ short_term: [{ values: [{ value: s.conso }] }] }),
    meteo: (s) => ({
      current: {
        surface_pressure: s.ducting ? 1030 : 1012,
        relative_humidity_2m: s.ducting ? 30 : 70,
        temperature_2m: 22, precipitation: 0, wind_speed_10m: 5,
        weather_code: s.orage ? 95 : 1,
      },
      hourly: { thunderstorm_probability: new Array(24).fill(s.orageProb) },
    }),
  };
  const vrai = window.fetch.bind(window);
  window.fetch = function (url, opts) {
    const s = window.__telluxCondFixture;
    const u = String(url);
    let body = null;
    if (s) {
      if (u.includes('plasma-7-day')) body = F.plasma(s);
      else if (u.includes('mag-7-day')) body = F.mag(s);
      else if (u.includes('integral-protons')) body = F.protons(s);
      else if (u.includes('planetary_k_index')) body = F.kp(s);
      else if (u.includes('kyoto-dst')) body = F.dst(s);
      else if (u.includes('rte-france')) body = F.rte(s);
      else if (u.includes('api.open-meteo.com')) body = F.meteo(s);
    }
    if (body !== null) {
      return Promise.resolve(new Response(JSON.stringify(body), {
        status: 200, headers: { 'Content-Type': 'application/json' },
      }));
    }
    return vrai(url, opts);
  };
};

// Fond de repli quand la pile d'ancêtres n'atteint jamais l'opacité 1 (panneau
// posé sur le canvas Leaflet). Valeur prise sur le fond réellement rendu (Esri
// World Light Gray Canvas).
const BASE_TONE = [245, 240, 231];

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

  await page.addInitScript(INSTALL_COND_FIXTURE);

  const rapport = { url: appUrl, panneaux: null, popup_par_point: null, cond_par_scenario: null };
  const POPUP_PANEL = PANELS.find((p) => p.sel === '.leaflet-popup-content');
  const COND_PANEL = PANELS.find((p) => p.sel === '#conditions-bar');
  const scansPopup = [];

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

    // ─── Ouverture des 5 surfaces ajoutées le 2026-09-01 ────────────────────
    // L'ORDRE COMPTE et n'est pas cosmétique :
    //   • le popup au clic AVANT la contribution terrain — `startContribFromFAB()`
    //     arme un handler sur le prochain clic carte ; l'inverse ferait consommer
    //     le clic par le placement de mesure, et le popup ne s'ouvrirait jamais ;
    //   • la contribution EN DERNIER — elle pose un overlay et arme la carte.
    // On pilote l'UI réelle partout où c'est possible (clic carte, ouverture du
    // formulaire par son propre flux). Seule exception : « Mon lieu », dont le
    // chemin UI passe par la géolocalisation ou une recherche d'adresse réseau —
    // on appelle donc sa fonction de rendu avec un résultat de calcul réel, ce
    // qui produit exactement le DOM que rend la production.
    await page.evaluate(async () => {
      const dodo = (ms) => new Promise((r) => setTimeout(r, ms));
      // Fermer la modale de bienvenue par son VRAI bouton — la masquer au
      // style.display fausse toute géométrie ultérieure (piège éprouvé).
      const acc = Array.from(document.querySelectorAll('button'))
        .find((b) => /Accéder à la carte|the map/i.test((b.textContent || '').trim()));
      if (acc) acc.click();
      await dodo(400);
    });

    // 1) Popup au clic — MESURÉ SUR PLUSIEURS POINTS (2026-09-01, cf. POPUP_POINTS).
    // Une seule mesure ne testait qu'une branche de chaque couleur conditionnelle.
    // Ce passage a lieu AVANT l'ouverture de la contribution terrain, qui arme un
    // handler sur le prochain clic carte et détournerait ces clics.
    for (let i = 0; i < POPUP_POINTS.length; i++) {
      const [lat, lon] = POPUP_POINTS[i];
      await page.evaluate(([la, lo]) => {
        if (typeof map !== 'undefined' && map && typeof L !== 'undefined') {
          map.fire('click', { latlng: L.latLng(la, lo) });
        }
      }, [lat, lon]);
      // Marge supplémentaire sur le PREMIER point (2026-09-02) : c'est le tout premier popup
      // jamais ouvert sur la page, juste après boot + modale + boutons de couches — trouvé en CI
      // rendu à 1 seul nœud (contre 26-27 pour les points 2-4) sur un runner visiblement plus
      // lent/froid que ce script ne l'anticipait. Les points suivants n'ont pas ce problème : la
      // page a déjà eu le temps de finir son travail de fond pendant leur propre clic précédent.
      const wait = i === 0 ? POPUP_WAIT_MS + 1500 : POPUP_WAIT_MS;
      await page.waitForTimeout(wait);
      const r = await page.evaluate(PROBE_CONTRAST, [[POPUP_PANEL], BASE_TONE]);
      scansPopup.push({ point: `${lat},${lon}`, ...r[0] });
    }

    await page.evaluate(async () => {
      const dodo = (ms) => new Promise((r) => setTimeout(r, ms));

      // 2) Mode Expertise — panneau + bandeau. activateExpertMode() court-circuite
      //    la modale de consentement, qui n'est pas l'objet de la mesure.
      if (typeof activateExpertMode === 'function') activateExpertMode();
      await dodo(500);

      // 3) Modale « Mon lieu », peuplée avec un calcul réel
      if (typeof openMyPlaceModal === 'function') openMyPlaceModal();
      if (typeof myPlaceRenderSummary === 'function' && typeof calcAll_v2 === 'function') {
        myPlaceRenderSummary({
          lat: 42.00, lon: 9.05, v2: calcAll_v2(42.00, 9.05),
          commune_info: { nom: 'Bastelica' }, n500: 3, n1000: 9,
          hta: { known: true, distance_m: 820 },
        });
      }
      await dodo(400);

      // 4) Contribution terrain — flux réel : armement puis clic de placement
      // ⚠️ TROUVAILLE (2026-09-01) : ce clic déclenche AUSSI le handler normal
      // d'ouverture du popup, en plus du placement de mesure — comportement de
      // PRODUCTION vérifié en direct (map.on('click',…) accumule les handlers,
      // Leaflet ne les rend pas mutuellement exclusifs), pas un artefact de ce
      // script. Le popup mesuré par le probe final serait donc celui de CE point
      // (42.01/9.06), un 5e point non documenté — d'où la reconstruction de
      // l'entrée popup ci-dessous à partir des seuls points de POPUP_POINTS.
      if (typeof startContribFromFAB === 'function') startContribFromFAB();
      await dodo(300);
      if (typeof map !== 'undefined' && map && typeof L !== 'undefined') {
        map.fire('click', { latlng: L.latLng(42.01, 9.06) });
      }
      await dodo(1500);
    });
    await page.waitForTimeout(1500);

    // Mesure unique : app.html n'a plus qu'un thème depuis le 2026-08-31. Aucun
    // attribut `data-theme` n'est posé ni retiré ici — la page est mesurée telle
    // qu'un visiteur la reçoit.
    // Playwright sérialise PROBE_CONTRAST et l'exécute dans la page — même
    // convention que les autres harnais du dossier (sondes déclarées en haut de
    // fichier, appelées via page.evaluate).
    //
    // Le popup EST EXCLU de cet appel : à ce stade, la contribution terrain (étape
    // 4 ci-dessus) l'a rouvert à un point non documenté (cf. son commentaire). Le
    // mesurer ici donnerait un résultat qui dépend d'un effet de bord, pas d'un
    // choix. L'entrée popup est reconstruite juste après, uniquement à partir des
    // POPUP_POINTS mesurés en amont, sur ces points-là et aucun autre.
    const panelsSansPopup = PANELS.filter((p) => p !== POPUP_PANEL);
    rapport.panneaux = await page.evaluate(PROBE_CONTRAST, [panelsSansPopup, BASE_TONE]);

    // ─── Reconstruction de l'entrée popup à partir de scansPopup ────────────
    // noeuds = celui du PREMIER point (POPUP_POINTS[0]) : c'est le point historique
    // du check à un seul point, ce qui garde le nombre comparable aux mesures
    // passées. violations = UNION dédupliquée sur (couleur, taille) — cf. le
    // commentaire de POPUP_POINTS : le texte est exclu de la clé exprès, pour
    // compter un DÉFAUT une fois même s'il apparaît sur plusieurs points.
    if (POPUP_PANEL) {
      // noeuds = MAXIMUM sur les 4 points, pas le premier (2026-09-02, trouvé en clôturant ce
      // chantier : un run CI réel a rendu le POINT 1 à 1 seul nœud — démarrage à froid, premier
      // popup jamais ouvert sur la page, juste après boot + clic modale + boutons de couches —
      // pendant que les points 2 à 4 rendaient normalement 26-27 nœuds chacun. Les VIOLATIONS
      // restaient fiables (unifiées sur les 4 points, un point dégradé n'en cache aucune), mais
      // le nombre de nœuds rapporté — utilisé par le plancher de couverture — serait tombé à 1,
      // masquant une vraie mesure derrière un chiffre d'échec de démarrage. C'est exactement le
      // mode d'échec que ce plancher existe pour attraper, retourné contre lui-même par un choix
      // de conception trop naïf ("le premier point suffit"). Le maximum répond à la question que
      // le plancher pose réellement : au moins un rendu complet a-t-il eu lieu ? — sans se laisser
      // fausser par un point isolé lent à charger.
      const noeudsCandidats = scansPopup.map((s) => s.noeuds || 0);
      const noeudsRetenu = noeudsCandidats.length ? Math.max(...noeudsCandidats) : 0;
      const vues = new Set();
      const violationsUnion = [];
      for (const s of scansPopup) {
        for (const v of (s.violations || [])) {
          const cle = `${v.couleur}|${v.px}`;
          if (vues.has(cle)) continue;
          vues.add(cle);
          violationsUnion.push({ ...v, vu_au_point: s.point });
        }
      }
      rapport.panneaux.push({
        panel: POPUP_PANEL.nom, sel: POPUP_PANEL.sel, etat: 'mesuré',
        noeuds: noeudsRetenu, points_mesures: scansPopup.length,
        noeuds_par_point: noeudsCandidats,
        violations: violationsUnion,
      });
    }

    // ─── Balayage des branches de #conditions-bar (cf. COND_SCENARIOS) ─────
    // A lieu APRÈS la passe principale : elle mesure la page telle qu'elle est
    // servie (fixture inerte), celui-ci force les entrées pour atteindre les
    // branches que la donnée live ne montre pas ce jour-là.
    const scansCond = [];
    for (const sc of COND_SCENARIOS) {
      await page.evaluate(async (s) => {
        // Purge du seul cache de fetchEnv (clés `tc_`), pas de sessionStorage.clear() :
        // d'autres états de page y vivent, les écraser fausserait la mesure suivante.
        try {
          for (const k of Object.keys(sessionStorage)) if (k.startsWith('tc_')) sessionStorage.removeItem(k);
        } catch (_e) { /* stockage indisponible : le stub sert de toute façon la fixture */ }
        window.__telluxCondFixture = s;
        // Vraies fonctions de production, dans l'ordre où la page les appelle.
        if (typeof loadNOAA === 'function') await loadNOAA();
        if (typeof loadDst === 'function') await loadDst();
        if (typeof loadLightning === 'function') await loadLightning();
        if (typeof loadMeteo === 'function') await loadMeteo();
        if (typeof loadChargeReseau === 'function') await loadChargeReseau();
        if (typeof _updateDstUI === 'function') _updateDstUI();
        if (typeof updateCondSummaries === 'function') updateCondSummaries();
        if (typeof syncBadges === 'function') syncBadges();
        // État de PRODUCTION : la barre est repliée au chargement. On le réaffirme
        // au lieu de le supposer — un flux ouvert plus haut pourrait l'avoir dépliée.
        const bar = document.getElementById('conditions-bar');
        const det = document.getElementById('conditions-bar-details');
        if (bar) bar.classList.add('collapsed');
        if (det) det.setAttribute('hidden', '');
      }, sc);
      await page.waitForTimeout(400);
      const r = await page.evaluate(PROBE_CONTRAST, [[COND_PANEL], BASE_TONE]);
      scansCond.push({ scenario: sc.nom, ...r[0] });
    }
    // Remise en veille du stub : plus aucune fixture servie après le balayage.
    await page.evaluate(() => { window.__telluxCondFixture = null; });

    // Une entrée de rapport par scénario, dédupliquée par (couleur, taille) comme
    // pour le popup : un MÊME défaut vu sous trois scénarios se compte une fois.
    const vuesCond = new Set();
    const violationsCond = [];
    for (const s of scansCond) {
      for (const v of (s.violations || [])) {
        const cle = `${v.couleur}|${v.px}`;
        if (vuesCond.has(cle)) continue;
        vuesCond.add(cle);
        violationsCond.push({ ...v, vu_au_scenario: s.scenario });
      }
    }
    rapport.cond_par_scenario = scansCond.map((s) => ({
      scenario: s.scenario, etat: s.etat, noeuds: s.noeuds || 0,
      violations: (s.violations || []).length,
    }));
    rapport.panneaux.push({
      panel: 'Barre de conditions — branches forcées', sel: '#conditions-bar (fixtures)',
      etat: scansCond.every((s) => s.etat === 'mesuré') ? 'mesuré' : 'dégradé',
      // noeuds volontairement à 0 : ces nœuds sont les MÊMES que ceux de « Barre de
      // conditions » plus haut, mesurés sous d'autres entrées. Les compter gonflerait
      // le plancher de couverture sans rien couvrir de plus. Le plancher propre à ce
      // balayage est COND_MIN_NOEUDS, appliqué par scénario ci-dessous.
      noeuds: 0, scenarios_mesures: scansCond.length,
      noeuds_par_scenario: scansCond.map((s) => s.noeuds || 0),
      violations: violationsCond,
    });
  } finally {
    await browser.close();
    if (server) server.close();
  }

  // Décompte par point, publié tel quel dans le rapport pour audit — l'entrée
  // popup elle-même a déjà été reconstruite plus haut (cf. le bloc juste avant
  // `finally`), à partir de ces mêmes scans et d'aucun autre.
  rapport.popup_par_point = scansPopup.map((s) => ({
    point: s.point, noeuds: s.noeuds || 0, violations: (s.violations || []).length,
  }));

  const violations = [];
  for (const p of rapport.panneaux) {
    for (const v of (p.violations || [])) violations.push({ panel: p.panel, ...v });
  }

  // ─── Cliquet (ratchet) ───────────────────────────────────────────────────
  // À sa création (2026-08-31), app.html portait une dette de contraste
  // antérieure à ce script — le check ne pouvait pas partir à 0/0 sans échouer
  // dès son premier jour, ce qui l'aurait fait ignorer en une semaine. Les
  // plafonds étaient donc calés sur la mesure du jour, revus à la baisse au
  // fil des corrections. Résorbée le même jour (dette A11Y-CONTRAST-APP-PANELS-002
  // fermée) : les valeurs par défaut sont maintenant 0/0 (cf. MAX_CRITIQUE/MAX_AA
  // ci-dessous). Le mécanisme de cliquet reste le garde-fou permanent contre
  // toute régression — ces plafonds ne doivent JAMAIS être remontés pour faire
  // passer une PR ; la seule direction autorisée est vers le bas.
  //
  //   critique = ratio < 3,0  → texte illisible ou quasi (le cas de la jauge
  //                             crustale corrigé le 2026-08-31 était à 1,07)
  //   aa       = ratio >= 3,0 mais sous le seuil WCAG applicable
  const MAX_CRITIQUE = Number(process.env.CONTRAST_MAX_CRITIQUE ?? 0);
  const MAX_AA = Number(process.env.CONTRAST_MAX_AA ?? 0);
  const critiques = violations.filter((v) => v.ratio < 3.0);
  const aa = violations.filter((v) => v.ratio >= 3.0);

  const noeudsMesures = rapport.panneaux.reduce((s, p) => s + (p.noeuds || 0), 0);

  const depassements = [];
  // Surfaces requises — ajoutées avec l'élargissement du 2026-09-01. Une surface
  // déclarée `requis` qui ne se mesure pas (absente, masquée, ou vide de texte)
  // fait échouer le check. Sans ça, un sélecteur renommé ou un flux d'ouverture
  // cassé rendrait la surface invisible au contrôle SANS rien signaler : zéro
  // nœud, zéro violation, vert. C'est exactement le mode d'échec qui a laissé
  // `#expert-panel` hors mesure jusqu'au 2026-09-01 — on ne le rejoue pas.
  const surfacesRequises = PANELS.filter((p) => p.requis);
  for (const panel of surfacesRequises) {
    const nom = panel.nom;
    const seuil = panel.min_noeuds ?? 1;
    const p = rapport.panneaux.find((x) => x.panel === nom);
    const noeuds = p && p.etat === 'mesuré' ? (p.noeuds || 0) : 0;
    if (!p || p.etat !== 'mesuré' || noeuds < seuil) {
      depassements.push(`surface requise sous son plancher : « ${nom} » (état : ${p ? p.etat : 'introuvable'}`
        + `${p && p.etat === 'mesuré' ? `, ${noeuds} nœud(s) < ${seuil}` : ''}) — son flux d'ouverture`
        + ' ne fonctionne plus ou rend un état dégradé, le résultat n\'est pas exploitable');
    }
  }
  // Plancher de couverture — AVANT les cliquets, et pour la même raison qu'axe-core a été
  // écarté : un check qui ne mesure rien passe au vert et rassure à tort. Les cliquets sont des
  // MAJORANTS ; si les panneaux ne se peuplaient pas (Supabase indisponible en CI, boot trop
  // lent, sélecteur renommé), le compte de violations tomberait à zéro et le check passerait
  // en n'ayant rien testé. Ce plancher rend ce scénario bruyant.
  // Référence : 204 nœuds mesurés en local le 2026-08-31, sur 5 panneaux × 2 thèmes ;
  // 100 après le retrait du mode sombre ; 192 depuis l'élargissement du 2026-09-01
  // (10 panneaux déclarés, 9 mesurés — Zone 2 reste masquée sans couche contextuelle).
  // Plancher PAR SCÉNARIO du balayage #conditions-bar — un scénario qui ne rend plus la barre
  // (loader renommé, fixture qui ne matche plus une URL, stub court-circuité) rapporterait zéro
  // violation et passerait au vert sans avoir exercé la moindre branche. Exactement le mode
  // d'échec que ce balayage existe pour supprimer : il ne doit pas pouvoir se le réintroduire.
  for (const s of (rapport.cond_par_scenario || [])) {
    if (s.etat !== 'mesuré' || s.noeuds < COND_MIN_NOEUDS) {
      depassements.push(`balayage #conditions-bar sous son plancher : scénario « ${s.scenario} »`
        + ` (état : ${s.etat}, ${s.noeuds} nœud(s) < ${COND_MIN_NOEUDS}) — la barre ne s'est pas`
        + ' peuplée sous fixture, les branches de couleur ne sont pas exercées');
    }
  }
  if (!rapport.cond_par_scenario || rapport.cond_par_scenario.length !== COND_SCENARIOS.length) {
    depassements.push(`balayage #conditions-bar incomplet :`
      + ` ${(rapport.cond_par_scenario || []).length}/${COND_SCENARIOS.length} scénarios mesurés`);
  }
  const MIN_NOEUDS = Number(process.env.CONTRAST_MIN_NOEUDS ?? 75);
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
      panneaux_mesures: rapport.panneaux.filter((p) => p.etat === 'mesuré').length,
      noeuds_mesures: noeudsMesures,
    },
    violations_critiques: critiques,
    violations_aa: aa,
    popup_par_point: rapport.popup_par_point,
    cond_par_scenario: rapport.cond_par_scenario,
    detail: rapport.panneaux,
  };
  process.stdout.write(JSON.stringify(sortie, null, 2) + '\n');
  process.exitCode = depassements.length > 0 ? 2 : 0;
}

main().catch((e) => {
  process.stdout.write(JSON.stringify({ outil: 'contrast-panels', erreur: String(e && e.stack || e) }, null, 2) + '\n');
  process.exitCode = 1;
});
