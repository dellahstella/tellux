// ═══════════════════════════════════════════════════════════════════════════
// Tellux — cache local Supabase pour les harnais de test (brief BN, 2026-09-05)
// ═══════════════════════════════════════════════════════════════════════════
//
// POURQUOI CE FICHIER EXISTE
// --------------------------
// Diagnostic brief BL (2026-09-05) : 98,7% du trafic Supabase des dernières 24h
// venait de sessions de développement/harnais de test (headless Chrome, Claude
// MSIX, node brut — referers localhost), pas de visiteurs réels. bt_lines/
// hta_lines/antennas_corse sont confirmées statiques (0 écriture enregistrée).
// Chaque exécution de harnais rechargeait ces 3 tables en entier (181 requêtes,
// ≈1,88 Mo compressés) sans jamais réutiliser un téléchargement précédent.
//
// CE QUE CE FICHIER FAIT — ET NE FAIT PAS
// ----------------------------------------
// Intercepte les requêtes réseau (Playwright context.route), PAS le code de
// chargement de app.html — le chemin de chargement réel (fetch, pagination,
// parsing JSON, construction de SEGMENT_GRID/ANFR_GRID) tourne à l'identique,
// que la réponse vienne du cache ou du réseau. app.html n'est jamais modifié.
// Si ce fichier disparaissait demain, rien ne changerait dans l'application —
// seul le volume réseau des tests remonterait.
//
// CE QUI EST MIS EN CACHE, ET CE QUI NE L'EST JAMAIS
// ----------------------------------------------------
// bt_lines, hta_lines, antennas_corse — confirmées statiques (brief BL).
// contributions est EXCLUE EN DUR (règle du brief BN) : table en écriture,
// un cache y donnerait des résultats faux. Toute autre table Supabase que
// app.html viendrait à interroger un jour passe au réseau réel par défaut —
// liste blanche, pas liste noire, pour ne jamais mettre en cache une table
// par erreur d'omission.
//
// CLÉ DE CACHE — LE DÉTAIL QUI COMPTE
// -------------------------------------
// hta_lines pagine par en-tête HTTP `Range` (Range-Unit: items), PAS par
// `offset`/`limit` en paramètre d'URL comme bt_lines/antennas_corse — la même
// URL littérale sert 9 pages différentes du chargement complet. Une clé basée
// sur l'URL seule aurait donc servi la MÊME page neuf fois (le contenu de la
// première requête interceptée, jamais les 8 suivantes) : un bug silencieux,
// invisible à l'exécution (le harnais tourne, les fonctions ne plantent pas),
// qui aurait cassé la fidélité du chargement pour cette seule table sans
// qu'aucun test existant ne le révèle. La clé inclut donc explicitement
// l'en-tête Range quand il est présent (cf. cacheKeyFor ci-dessous).
//
// EMPLACEMENT — HORS DE TOUTE ARBORESCENCE DE TRAVAIL
// -------------------------------------------------------
// %LOCALAPPDATA%\Tellux\harness-supabase-cache\ (ou $XDG_CACHE_HOME/tellux/...
// hors Windows) — chemin utilisateur fixe, pas relatif à un clone : partagé de
// fait par tous les worktrees du poste, sans mécanisme de partage à construire.
// N'entre dans aucun dépôt git (ni public ni privé) : .gitignore et le hook
// pre-commit privé n'ont rien à couvrir, ce chemin ne peut jamais être stagé.
// Surchargeable par TELLUX_HARNESS_CACHE_DIR.
//
// INVALIDATION ET RAFRAÎCHISSEMENT — JAMAIS SILENCIEUX
// ---------------------------------------------------------
// TTL 7 jours par défaut (TELLUX_HARNESS_CACHE_TTL_MS pour surcharger). Un
// TTL borne le risque si ces tables cessaient un jour d'être statiques, sans
// dépendre de quelqu'un qui penserait à vider le cache. Mais un TTL qui expire
// au milieu d'une session ralentit un script sans explication visible si rien
// ne le dit (retour Soleil, revue de conception) — chaque miss/expiration logue
// donc une ligne explicite AVANT de retourner au réseau (le "MISS/expiré"
// dans installSupabaseCache ci-dessous). Les hits (le cas normal, des
// centaines par exécution) ne loguent rien — le silence, ici, c'est le
// chemin rapide qui marche comme prévu.
//
// FORCER LE RECHARGEMENT
// ------------------------
// TELLUX_HARNESS_CACHE=off désactive complètement l'interception (installSupabaseCache
// devient un no-op, aucune route posée) — réseau réel systématique, comme avant
// ce chantier. Utilisé par loading-path-live-check.mjs, qui doit vérifier le
// VRAI chemin de chargement, pas une version mise en cache de celui-ci.
// ═══════════════════════════════════════════════════════════════════════════

import { mkdir, readFile, writeFile, stat } from 'node:fs/promises';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import os from 'node:os';

// Liste blanche stricte — jamais de mise en cache par défaut pour une table
// non listée ici (cf. commentaire ci-dessus, "contributions" en est exclue).
const CACHEABLE_TABLES = new Set(['bt_lines', 'hta_lines', 'antennas_corse']);

const DEFAULT_TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 jours

function defaultCacheDir() {
  if (process.env.TELLUX_HARNESS_CACHE_DIR) return process.env.TELLUX_HARNESS_CACHE_DIR;
  if (process.platform === 'win32') {
    const base = process.env.LOCALAPPDATA || join(os.homedir(), 'AppData', 'Local');
    return join(base, 'Tellux', 'harness-supabase-cache');
  }
  const base = process.env.XDG_CACHE_HOME || join(os.homedir(), '.cache');
  return join(base, 'tellux', 'harness-supabase-cache');
}

function tableFromPath(pathname) {
  // /rest/v1/<table> — segment après /rest/v1/
  const m = pathname.match(/\/rest\/v1\/([^/?]+)/);
  return m ? m[1] : null;
}

// DEUX DÉFAUTS TROUVÉS EN VÉRIFIANT CE CHANTIER (2026-09-05, pas en revue de conception) :
//
// 1) CORS origin figée (LA cause confirmée de "❌ loadAnt erreur: Failed to fetch" —
//    diagnostiqué en direct via page.on('requestfailed') : errorText="net::ERR_FAILED").
//    access-control-allow-origin dans la réponse Supabase d'origine vaut l'origine EXACTE
//    du serveur local qui a fait la requête au moment où l'entrée a été écrite (ex.
//    http://127.0.0.1:3779, port par défaut de createHarness()). La clé de cache n'inclut
//    PAS ce port — volontairement, cf. cacheKeyFor : le cache est partagé entre TOUS les
//    scripts sur disque. Mais eval-app-rubric.mjs tourne sur son propre port fixe (3780,
//    indépendant de createHarness()) : en lisant une entrée écrite par un script tournant
//    sur 3779, l'en-tête rejoué prétend autoriser 3779 alors que la page réelle est sur
//    3780 — Chromium applique bien CORS à une réponse mockée par route.fulfill() (il ne
//    sait pas qu'elle est simulée), et rejette. Solution : ces réponses n'ont plus de
//    frontière de sécurité réelle à faire respecter (page de test locale parlant à
//    elle-même) — les requêtes ici n'utilisent jamais `credentials:'include'` (auth par
//    en-tête Authorization, pas cookie), donc allow-origin:'*' est valide et définitif,
//    quel que soit le port de n'importe quel script présent ou futur.
//
// 2) content-encoding : route.fetch() → response.body() (et donc tout ce qu'on stocke/
//    rejoue) renvoie TOUJOURS le corps déjà DÉCOMPRESSÉ — Playwright décode gzip/br
//    automatiquement en récupérant .body(). Rejouer content-encoding tel quel prétendrait
//    à Chromium qu'il doit encore décoder un corps déjà en clair. Pas confirmé comme la
//    cause du símptome observé ici (l'erreur réseau était bien CORS, pas
//    ERR_CONTENT_DECODING_FAILED), mais reste un mensonge de l'en-tête envers le corps
//    réellement servi — retiré par hygiène/prudence, avant qu'un jour une réponse
//    compressée ne déclenche ce second défaut latent. content-length/transfer-encoding/
//    connection retirés pour la même raison (ne décrivent plus le corps qu'on rejoue, ou
//    sont des en-têtes de bout en bout HTTP/1.1 sans sens pour un serveur simulé) ;
//    set-cookie par hygiène (cookie de session Supabase sans usage pour la page locale).
const UNSAFE_REPLAY_HEADERS = new Set([
  'content-encoding', 'content-length', 'transfer-encoding', 'connection', 'set-cookie', 'keep-alive',
]);

function sanitizeReplayHeaders(headers) {
  const out = {};
  for (const [k, v] of Object.entries(headers || {})) {
    if (!UNSAFE_REPLAY_HEADERS.has(k.toLowerCase())) out[k] = v;
  }
  // Toujours '*', jamais l'origine capturée à l'écriture — cf. point 1) ci-dessus.
  out['access-control-allow-origin'] = '*';
  return out;
}

function cacheKeyFor(url, headers) {
  // Inclut explicitement l'en-tête Range (pagination hta_lines) et Prefer
  // (peut influencer Content-Range dans la réponse) — jamais l'URL seule.
  const u = new URL(url);
  const parts = [
    u.pathname,
    [...u.searchParams.entries()].sort().map(([k, v]) => `${k}=${v}`).join('&'),
    'range=' + (headers['range'] || headers['Range'] || ''),
    'prefer=' + (headers['prefer'] || headers['Prefer'] || ''),
  ].join('|');
  return createHash('sha256').update(parts).digest('hex');
}

async function readCacheEntry(cacheDir, table, key, ttlMs) {
  const file = join(cacheDir, table, key + '.json');
  try {
    const st = await stat(file);
    if (Date.now() - st.mtimeMs > ttlMs) return null; // expiré
    const raw = await readFile(file, 'utf8');
    return JSON.parse(raw);
  } catch {
    return null; // absent ou illisible — traité comme un miss
  }
}

async function writeCacheEntry(cacheDir, table, key, entry) {
  const dir = join(cacheDir, table);
  await mkdir(dir, { recursive: true });
  await writeFile(join(dir, key + '.json'), JSON.stringify(entry), 'utf8');
}

/**
 * Installe l'interception de cache sur un BrowserContext Playwright.
 * No-op si TELLUX_HARNESS_CACHE=off (aucune route posée — réseau réel garanti).
 *
 * @param {import('playwright').BrowserContext} context
 * @param {object} [opts]
 * @param {string} [opts.label] — préfixe des logs, pour distinguer plusieurs
 *   contextes dans un même run (ex. le nom du script appelant).
 * @param {string} [opts.cacheDir] — surcharge defaultCacheDir().
 * @param {number} [opts.ttlMs] — surcharge DEFAULT_TTL_MS.
 * @returns {Promise<{disabled: boolean, cacheDir: string, ttlMs: number}>}
 */
export async function installSupabaseCache(context, opts = {}) {
  const disabled = (process.env.TELLUX_HARNESS_CACHE || '').toLowerCase() === 'off';
  const cacheDir = opts.cacheDir || defaultCacheDir();
  const ttlMs = opts.ttlMs ?? (process.env.TELLUX_HARNESS_CACHE_TTL_MS ? Number(process.env.TELLUX_HARNESS_CACHE_TTL_MS) : DEFAULT_TTL_MS);
  const label = opts.label ? `[${opts.label}] ` : '';

  if (disabled) {
    console.log(`${label}[supabase-cache] désactivé (TELLUX_HARNESS_CACHE=off) — réseau réel pour toutes les requêtes.`);
    return { disabled: true, cacheDir, ttlMs };
  }

  await mkdir(cacheDir, { recursive: true });

  await context.route('**/rest/v1/**', async (route) => {
    // GARDE-FOU CRITIQUE (trouvé en CI, PR #1263 — pas en local) : un script
    // peut fermer sa page/son contexte AVANT que toutes les pages de
    // pagination interceptées aient fini de répondre (ex. contrast-panels.mjs
    // n'attend pas la fin du chargement BT pour conclure ses propres mesures).
    // route.fetch()/route.fulfill() lèvent alors "Request context disposed" —
    // une rejection NON INTERCEPTÉE ici plantait tout le process Node
    // (triggerUncaughtException), faisant échouer des workflows CI qui
    // n'avaient RIEN à voir avec Supabase. Tout le corps du handler est donc
    // sous try/catch : une route qui échoue parce que le contexte ferme ne
    // doit jamais faire tomber le test qui l'a fermé À DESSEIN.
    try {
      const request = route.request();
      const url = request.url();
      const u = new URL(url);
      const table = tableFromPath(u.pathname);

      // Liste blanche stricte + jamais les préflights OPTIONS (pas de corps
      // significatif, coût négligeable, complexité CORS inutile à gérer ici).
      if (!table || !CACHEABLE_TABLES.has(table) || request.method() === 'OPTIONS') {
        return await route.continue();
      }

      const headers = request.headers();
      const key = cacheKeyFor(url, headers);
      const cached = await readCacheEntry(cacheDir, table, key, ttlMs);

      if (cached) {
        // sanitizeReplayHeaders en défense — même sur une entrée écrite par une version
        // antérieure de ce fichier (avant le correctif content-encoding ci-dessus), qui
        // aurait persisté l'en-tête brut : aucun vidage de cache à exiger pour bénéficier
        // du correctif, une entrée existante s'auto-corrige dès sa prochaine lecture.
        return await route.fulfill({
          status: cached.status,
          headers: sanitizeReplayHeaders(cached.headers),
          body: Buffer.from(cached.bodyBase64, 'base64'),
        });
      }

      // Miss ou entrée expirée — toujours logué, jamais silencieux (retour Soleil).
      console.log(`${label}[supabase-cache] MISS/expiré — ${table} (${key.slice(0, 12)}…) → réseau réel.`);

      const response = await route.fetch();
      const body = await response.body();
      const rawHeaders = response.headers();
      // headers explicite (pas {response, body} seul) — ne dépend d'aucun comportement
      // implicite de Playwright pour ce couple, corrige le même défaut content-encoding
      // que la relecture cache ci-dessus, dès la toute première requête (jamais mise en
      // cache) et pas seulement sur un HIT ultérieur.
      await route.fulfill({ status: response.status(), headers: sanitizeReplayHeaders(rawHeaders), body });

      // Persiste APRÈS avoir répondu à la page — ne retarde jamais le test. En-têtes déjà
      // assainis à l'écriture : le fichier sur disque ne doit jamais prétendre décrire un
      // corps compressé qu'il ne contient plus, et n'a aucune raison de garder un cookie de
      // session Supabase sans usage pour la page locale testée.
      await writeCacheEntry(cacheDir, table, key, {
        status: response.status(),
        headers: sanitizeReplayHeaders(rawHeaders),
        bodyBase64: body.toString('base64'),
        cachedAt: new Date().toISOString(),
        url,
      }).catch((e) => {
        console.warn(`${label}[supabase-cache] échec d'écriture cache (non bloquant) : ${e.message}`);
      });
    } catch (e) {
      // Contexte/page déjà fermé(e), ou toute autre erreur réseau — le test
      // qui a déclenché cette requête a déjà cessé de s'y intéresser (sinon
      // il n'aurait pas fermé le contexte). Signalé, jamais fatal.
      console.warn(`${label}[supabase-cache] requête interrompue (contexte probablement fermé) — ${e?.message || e}`);
      await route.abort().catch(() => {}); // best-effort — peut lui-même échouer si déjà disposé
    }
  });

  return { disabled: false, cacheDir, ttlMs };
}
