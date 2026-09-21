// ═══════════════════════════════════════════════════════════════════════════
// Tellux — garde clés-du-payload / colonnes-du-schéma (brief S1, 2026-09-13)
// ═══════════════════════════════════════════════════════════════════════════
//
// POURQUOI CE FICHIER EXISTE
// --------------------------
// INS-018 (registre privé) : `protocole_aveugle` a été collecté proprement
// côté client pendant 4,5 mois sans jamais avoir de colonne Supabase — visible
// nulle part depuis le site (ni le HTML, ni le payload, ni `_migrations/` qui
// ne la mentionne pas), seulement en confrontant le payload au schéma
// **vivant**. `native_capture` porte aujourd'hui le même défaut, encore
// ouvert. Ce script automatise cette confrontation.
//
// RAPPORT SEULEMENT — PAS REQUIS
// -------------------------------
// `native_capture` est un défaut connu et encore ouvert : ce check serait
// rouge dès le premier run s'il tournait aujourd'hui, et un check REQUIS rouge
// dès sa pose bloquerait `main` sur un défaut préexistant, pas sur une
// régression. Il devient requis APRÈS la migration qui ajoute la colonne
// (Cran C, arbitrage Soleil), pas avant. D'ici là : visible, non bloquant.
//
// CE QU'IL ÉNUMÈRE, ET POURQUOI L'ÉNUMÉRATION EST LE POINT FAIBLE
// -------------------------------------------------------------------
// La liste SITES ci-dessous nomme chaque site d'écriture connu vers une table
// publique. Un nouveau site d'écriture qui n'y est pas ajouté échappe
// entièrement au contrôle, en silence — c'est un défaut de la même famille que
// celui que ce script existe pour attraper ailleurs (une chose employée hors
// du domaine que son auteur croyait couvrir). Non résolu ici : SITES doit être
// tenue à jour à la main. Un commentaire est posé à chaque site d'écriture
// (`app.html`, `radon.html`) pointant vers ce fichier, pour qu'un futur ajout
// de champ — ou de site — ait une chance d'être remarqué.
//
// EXTRACTION DES CLÉS — STATIQUE, PAS UNE EXÉCUTION DE app.html
// -------------------------------------------------------------
// Chaque site est repéré par une ancre stable (ex. `const row={`) puis les
// clés de premier niveau de l'objet sont lues par comptage d'accolades depuis
// le texte source — jamais en import/exécution de app.html (aucun DOM, aucun
// navigateur). Une clé imbriquée (ex. `csv_stats:{min:...}`) n'est jamais
// remontée comme si elle visait une colonne : seul le premier niveau compte,
// c'est ce que `topLevelKeys()` fait explicitement.
//
// ACCÈS AU SCHÉMA — NON CONFIGURÉ PAR DÉFAUT, ET C'EST VOULU
// -------------------------------------------------------------
// Lire `information_schema.columns` depuis la CI suppose un secret capable
// d'exécuter du SQL en lecture sur le projet Supabase — PostgREST n'expose pas
// `information_schema` par défaut, donc la clé anon déjà publique dans
// `app.html` ne suffit pas. Ce script lit `SUPABASE_MGMT_PAT` (nom proposé,
// portée décrite dans le corps de la PR — pas ici, jamais dans un commentaire
// de code) ; **si la variable est absente, le script sort en 0 avec un
// message explicite** — un secret manquant n'est pas une régression du code,
// et ne doit jamais se lire comme telle. Rien n'a été demandé, posé ni généré
// pour cette session : la variable est un nom proposé, pas un accès qui
// existe. Arbitrage Soleil.
//
// TAMPON DU POINT DE VALIDATION (brief §4/§5) — testé, pas affirmé
// ---------------------------------------------------------------------
// « La garde aurait-elle attrapé native_capture le jour de son ajout ? »
// Vérifié par `selfTestHistorical()`, exécuté avant toute lecture réseau :
// rejoue la comparaison sur le schéma du 2026-04-22 (fixture, 33 colonnes —
// les 35 actuelles moins `protocole_aveugle`/`native_capture`, jamais
// ajoutées) contre le payload introduit par le commit `7be75f4` (34 clés,
// les deux comprises). Si ce test ne détecte pas les deux clés comme
// orphelines, le script sort en 2 avant même de tenter le réseau — un
// détecteur dont le témoin échoue ne mesure rien (même règle qu'INS-016).
// ═══════════════════════════════════════════════════════════════════════════

import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..');

// ─────────────────────────────────────────────────────────────────────────
// Sites d'écriture connus. À tenir à jour à la main (cf. commentaire de tête).
// anchor : texte littéral qui ouvre l'objet payload (recherché tel quel).
// ─────────────────────────────────────────────────────────────────────────
const SITES = [
  {
    table: 'contributions',
    file: 'app.html',
    fn: 'saveContrib()',
    anchor: 'const row={',
  },
  {
    table: 'contributions',
    file: 'app.html',
    fn: 'capSubmitMeasurement()',
    anchor: 'const row={',
    // Deux sites distincts partagent le même texte d'ancre littéral dans
    // app.html : `occurrence` sélectionne laquelle (0-indexé, ordre
    // d'apparition dans le fichier). Fragile par construction — cf. limite
    // ci-dessus. Si un troisième site apparaît un jour avec la même ancre,
    // ce champ devra être révisé.
    occurrence: 1,
  },
  {
    table: 'orientations_contributions',
    file: 'app.html',
    fn: '(aucun — aucun appelant trouvé, cf. FAIT registre privé)',
    anchor: null, // Table acceptant l'INSERT public (RLS) mais sans appelant
                   // client connu au 2026-09-13 (INS-018, amendement du
                   // 2026-09-13). Rien à extraire : présente ici pour que sa
                   // réapparition future comme site actif soit remarquée par
                   // quiconque relit cette liste, pas pour être vérifiée.
  },
  {
    table: 'radon_depots_erp',
    file: 'radon.html',
    fn: 'submit handler (dr-submit-btn)',
    anchor: 'var payload = {',
  },
];

/** Coupe `text` depuis `anchorIndex` (positionné juste après `{`) jusqu'à
 *  l'accolade fermante correspondante, en comptant la profondeur — gère les
 *  objets imbriqués (ex. `csv_stats:{...}`) sans s'y arrêter. */
function sliceBalancedObject(text, openBraceIndex) {
  let depth = 1;
  let i = openBraceIndex + 1;
  for (; i < text.length && depth > 0; i++) {
    if (text[i] === '{') depth++;
    else if (text[i] === '}') depth--;
  }
  if (depth !== 0) throw new Error('accolade non refermée — ancre ou fichier a changé de forme');
  return text.slice(openBraceIndex + 1, i - 1);
}

/** Retire les commentaires de ligne et les commentaires de bloc d'un texte
 *  JS. Ne comprend pas les littéraux de chaîne (un commentaire de ligne DANS
 *  une chaîne serait à tort traité comme un vrai commentaire) — sans effet
 *  ici : aucune valeur de ces payloads n'en contient (vérifié à l'écriture ;
 *  à revoir si un site futur en ajoute). Un vrai parseur (acorn ou
 *  équivalent) réglerait ce point plus proprement, au prix d'une dépendance
 *  nouvelle — écarté pour un projet qui n'en a aucune à ce jour au-delà de
 *  Playwright. */
function stripComments(text) {
  return text.replace(/\/\/[^\n]*/g, '').replace(/\/\*[\s\S]*?\*\//g, '');
}

/** Extrait les clés de PREMIER NIVEAU d'un corps d'objet (entre les accolades
 *  extérieures, déjà retirées par sliceBalancedObject). Ignore tout ce qui
 *  est à une profondeur > 0 (objets/tableaux imbriqués, appels de fonction,
 *  parenthèses). Une clé est un identifiant JS simple suivi de `:`, **et
 *  seulement si ce `:` est le premier token depuis le début de l'objet ou
 *  depuis la dernière virgule de profondeur 0** — condition qui exclut par
 *  construction le `:` d'un ternaire (`cond ? a : b`, jamais précédé d'une
 *  virgule) sans avoir besoin de comprendre la grammaire des expressions.
 *  Reproduit par le témoin de non-régression `selfTestTernaryAndComments()`
 *  ci-dessous, sur un extrait réel du fichier (kp/bz avec `Number.isFinite`
 *  en ternaire) qui a fait échouer une première version regex naïve. */
function topLevelKeys(objectBodyRaw) {
  const objectBody = stripComments(objectBodyRaw);
  const keys = [];
  let depth = 0;
  let i = 0;
  let atKeyPosition = true; // vrai juste après '{' ou une ',' de profondeur 0
  const re = /[A-Za-z_$][A-Za-z0-9_$]*\s*:/y;
  while (i < objectBody.length) {
    const ch = objectBody[i];
    if (/\s/.test(ch)) { i++; continue; } // l'espace ne change pas atKeyPosition
    if (ch === '{' || ch === '[' || ch === '(') { depth++; atKeyPosition = false; i++; continue; }
    if (ch === '}' || ch === ']' || ch === ')') { depth--; atKeyPosition = false; i++; continue; }
    if (depth === 0 && ch === ',') { atKeyPosition = true; i++; continue; }
    if (depth === 0 && atKeyPosition) {
      re.lastIndex = i;
      const m = re.exec(objectBody);
      if (m && m.index === i) {
        keys.push(m[0].slice(0, -1).trim());
        i = re.lastIndex;
        atKeyPosition = false;
        continue;
      }
    }
    atKeyPosition = false;
    i++;
  }
  return keys;
}

/** Témoin de non-régression — un extrait réel (pas inventé) d'app.html qui a
 *  fait échouer une première version de topLevelKeys() : le ternaire
 *  `Number.isFinite(kpNum)?kpNum:null` ressortait `kpNum` comme fausse clé,
 *  et le commentaire multi-lignes entre `attenuation_prevue_db` et
 *  `native_capture` ressortait des fragments de mots comme `BT`/`crite`.
 *  Lancé par selfTestHistorical() avant tout accès réseau, même règle. */
function selfTestTernaryAndComments() {
  const sample = `
    lat:ll.lat,lon:ll.lng,
    kp:Number.isFinite(kpNum)?kpNum:null,bz:Number.isFinite(bzNum)?bzNum:null,
    // bt_terme_inclus (2026-09-09, migration 011) — un commentaire long avec
    // des mots qui ressemblent à des clés : BT, critique, etat.
    bt_terme_inclus:btTermeInclus(),
    native_capture: window._nativeCaptureUsed === true ? true : null,
  `;
  const got = topLevelKeys(sample);
  const expected = ['lat', 'lon', 'kp', 'bz', 'bt_terme_inclus', 'native_capture'];
  const gotStr = got.join(',');
  const expStr = expected.join(',');
  if (gotStr !== expStr) {
    console.error('::error title=Garde clés/colonnes — témoin d\'extraction en échec::' +
      `attendu [${expStr}], obtenu [${gotStr}]. L'extraction regex ne mesure pas ce qu'elle prétend.`);
    process.exit(2);
  }
  console.log('✓ Témoin d\'extraction : ternaire et commentaire ne produisent plus de fausses clés.');
}

function nthIndexOf(haystack, needle, n) {
  let idx = -1;
  for (let k = 0; k <= n; k++) {
    idx = haystack.indexOf(needle, idx + 1);
    if (idx === -1) return -1;
  }
  return idx;
}

async function extractSiteKeys(site) {
  if (!site.anchor) return null; // site documenté mais non vérifiable (cf. SITES)
  const filePath = path.join(REPO_ROOT, site.file);
  const src = await readFile(filePath, 'utf8');
  const occurrence = site.occurrence ?? 0;
  const anchorPos = nthIndexOf(src, site.anchor, occurrence);
  if (anchorPos === -1) {
    throw new Error(`ancre "${site.anchor}" (occurrence ${occurrence}) introuvable dans ${site.file} — le site a bougé, mettre SITES à jour`);
  }
  const openBrace = anchorPos + site.anchor.length - 1; // l'ancre se termine sur '{'
  const body = sliceBalancedObject(src, openBrace);
  return topLevelKeys(body);
}

/** Compare un ensemble de clés envoyées à un ensemble de colonnes réelles.
 *  Retourne les clés orphelines (envoyées, sans colonne). Pure — aucune E/S,
 *  c'est ce qui la rend testable sur fixture sans réseau. */
function orphanKeys(sentKeys, realColumns) {
  const cols = new Set(realColumns);
  return sentKeys.filter((k) => !cols.has(k));
}

// ─────────────────────────────────────────────────────────────────────────
// Auto-test historique — exécuté AVANT tout accès réseau, à chaque run.
// ─────────────────────────────────────────────────────────────────────────
function selfTestHistorical() {
  // Schéma `contributions` au 2026-04-22, veille de 7be75f4 — reconstruit en
  // retirant des 35 colonnes vivantes (lues le 2026-09-12/13, session S2,
  // INS-018) les 6 ajoutées PAR DES MIGRATIONS POSTÉRIEURES au 2026-04-23 :
  // `excluded_from_public` (migration « 007_excluded_from_public »,
  // 2026-04-26) ; `airplane_mode_on`/`usb_charging_off`/`no_metal_proximity`/
  // `measurement_duration_s` (migration « contributions_conditions_mesure »,
  // alias du fichier 008, 2026-04-27, cf. FAIT-007) ; `bt_terme_inclus`
  // (migration 011, 2026-09-09, cf. commentaire du site d'appel). Reste :
  // 29 colonnes. `protocole_aveugle`/`native_capture` n'apparaissent nulle
  // part ici parce qu'elles n'ont jamais été des colonnes, à aucune date.
  const schemaBefore = [
    'id','created_at','lat','lon','type','valeur','unite','note','kp','bz',
    'densite_protons','flux_protons','igrf_nt','perturbation_humaine_nt',
    'facteur_eau_nt','reseaux_actifs','score_anomalie','delta_nt','session_id',
    'version_app','contexte','etage','geo_nets','geo_netval','materiaux_murs',
    'appareils_actifs','attenuation_prevue_db','csv_stats','unite_saisie',
  ];
  // Clés introduites par 7be75f4 (2026-04-23T13:26:09Z) dans `saveContrib()`,
  // lues dans le commit lui-même — pas le fichier d'aujourd'hui, qui a bougé.
  const payloadAtIntroduction = [
    'lat','lon','type','valeur','unite','unite_saisie','csv_stats','note',
    'kp','bz','densite_protons','flux_protons','igrf_nt',
    'perturbation_humaine_nt','facteur_eau_nt','score_anomalie','delta_nt',
    'session_id','version_app','contexte','etage','materiaux_murs',
    'appareils_actifs','attenuation_prevue_db',
    'protocole_aveugle','native_capture',
    // airplane_mode_on/usb_charging_off/no_metal_proximity/measurement_duration_s
    // sont arrivés plus tard (migration 008, 2026-04-27) — absents ici à
    // dessein, sans effet sur ce test.
  ];
  const found = new Set(orphanKeys(payloadAtIntroduction, schemaBefore));
  const expected = ['protocole_aveugle', 'native_capture'];
  const missing = expected.filter((k) => !found.has(k));
  const extra = [...found].filter((k) => !expected.includes(k));
  if (missing.length || extra.length) {
    console.error('::error title=Garde clés/colonnes — témoin historique en échec::' +
      `attendu {${expected.join(', ')}} orphelines le 2026-04-23 ; manquantes: {${missing.join(', ') || 'aucune'}}, ` +
      `en trop: {${extra.join(', ') || 'aucune'}}. La logique de comparaison ne mesure pas ce qu'elle prétend — ` +
      `corrigée avant d'être crue, pas après (cf. INS-016).`);
    process.exit(2);
  }
  console.log(`✓ Témoin historique : protocole_aveugle et native_capture auraient été détectées le 2026-04-23 (${schemaBefore.length} colonnes vs ${payloadAtIntroduction.length} clés envoyées).`);
}

// ─────────────────────────────────────────────────────────────────────────
// Lecture du schéma vivant — Management API Supabase. Forme non éprouvée par
// un vrai jeton dans cette session (aucun jeton détenu ni demandé) : à
// vérifier contre la documentation Supabase courante avant activation.
// ─────────────────────────────────────────────────────────────────────────
async function fetchLiveColumns(table, projectRef, pat) {
  const res = await fetch(`https://api.supabase.com/v1/projects/${projectRef}/database/query`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${pat}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: `select column_name from information_schema.columns where table_schema='public' and table_name='${table}'`,
    }),
  });
  if (!res.ok) {
    throw new Error(`Management API ${res.status} pour ${table} : ${await res.text()}`);
  }
  const rows = await res.json();
  return rows.map((r) => r.column_name);
}

async function main() {
  selfTestTernaryAndComments();
  selfTestHistorical();

  const pat = process.env.SUPABASE_MGMT_PAT;
  const projectRef = process.env.SUPABASE_PROJECT_REF || 'knckulwghgfrxmbweada';

  if (!pat) {
    const msg = 'SUPABASE_MGMT_PAT absent — garde non exécutée (accès non provisionné, arbitrage Soleil en attente). Ce silence n\'est pas un vert : c\'est un secret manquant, pas une conformité mesurée.';
    console.log(msg);
    if (process.env.GITHUB_STEP_SUMMARY) {
      await import('node:fs/promises').then(({ appendFile }) =>
        appendFile(process.env.GITHUB_STEP_SUMMARY, `## Garde clés/colonnes\n\n⏭️ **Non exécutée** — ${msg}\n`));
    }
    process.exit(0); // rapport seulement : un accès non fourni n'est pas un échec de PR
  }

  const findings = [];
  for (const site of SITES) {
    if (!site.anchor) {
      findings.push({ site, skipped: true });
      continue;
    }
    let sentKeys;
    try {
      sentKeys = await extractSiteKeys(site);
    } catch (e) {
      findings.push({ site, error: `extraction : ${e.message}` });
      continue;
    }
    let liveColumns;
    try {
      liveColumns = await fetchLiveColumns(site.table, projectRef, pat);
    } catch (e) {
      findings.push({ site, error: `schéma vivant : ${e.message}` });
      continue;
    }
    const orphans = orphanKeys(sentKeys, liveColumns);
    findings.push({ site, sentKeys, liveColumns, orphans });
  }

  let anyOrphan = false;
  const lines = ['## Garde clés/colonnes — requis (bloquant depuis le 2026-09-14, ADR-068)\n'];
  for (const f of findings) {
    const label = `${f.site.table} — ${f.site.fn}`;
    if (f.skipped) { lines.push(`- ⚪ ${label} : non vérifiable (pas d'appelant client connu)`); continue; }
    if (f.error) { lines.push(`- ⚠️ ${label} : ${f.error}`); continue; }
    if (f.orphans.length === 0) {
      lines.push(`- ✅ ${label} : ${f.sentKeys.length} clé(s) envoyée(s), toutes ont une colonne`);
    } else {
      anyOrphan = true;
      lines.push(`- ❌ ${label} : clé(s) sans colonne — **${f.orphans.join(', ')}**`);
      console.error(`::error title=Garde clés/colonnes::${label} — clé(s) sans colonne : ${f.orphans.join(', ')}`);
    }
  }
  const summary = lines.join('\n');
  console.log(summary);
  if (process.env.GITHUB_STEP_SUMMARY) {
    const { appendFile } = await import('node:fs/promises');
    await appendFile(process.env.GITHUB_STEP_SUMMARY, summary + '\n');
  }
  // Requis depuis le 2026-09-14 (ADR-068, plancher CI 3 → 4) : ce workflow
  // EST dans la liste des required status checks — un rouge ici bloque le
  // merge. Sort non-zéro pour que le check s'affiche rouge et visible (cf.
  // test de sortie, brief §2 — un rapport que personne ne lit n'est pas une
  // garde). Statut à revérifier en direct (gh api .../protection/
  // required_status_checks) avant de modifier ce commentaire — cf. LOT A,
  // BRIEF_CODE_CLOTURE_BASCULE_EMAG2_2026-09-19, corrigé le 2026-09-19 après
  // que cette ligne et le titre du rapport ci-dessus aient affirmé le
  // contraire pendant 5 jours.
  process.exit(anyOrphan ? 1 : 0);
}

main().catch((e) => {
  console.error('::error title=Garde clés/colonnes — échec du script::' + (e?.stack || e));
  process.exit(1);
});
