#!/usr/bin/env node
// ─── generer_agregat_bt.mjs — agrégat statique de bt_lines, variante (i) ────────────────────
//
// Usage :  node scripts/generer_agregat_bt.mjs
// Écrit  :  public/data/bt_lines_agregat.json          (lignes, forme {pts,type} — sans id,
//                                                        inutile hors pagination live)
//           public/data/bt_lines_agregat_marqueur.json ({genere_le, derniere_ligne_id, nb_lignes})
// Sort 1 si la génération échoue ou produit un jeu incohérent avec sa propre déclaration de
// total (`Content-Range`) — CE script-ci n'est pas un instrument de mesure au sens de
// perimetre-reprise.mjs, c'est un générateur d'artefact committé : une sortie fausse doit
// empêcher le commit, pas seulement l'annoncer.
//
// ─── POURQUOI CETTE FORME, PAS UNE AUTRE ────────────────────────────────────────────────────
// Brief "agrégat BT variante (i)", 2026-09-14 : géométrie inchangée, mêmes 156 130 lignes,
// simplement empaquetées en un seul fichier au lieu de 157 requêtes Supabase. `id` est retiré
// du fichier de lignes lui-même (mesuré : ~1 Mo gzip de moins, 2026-09-14, cf. rapport de
// session) — il ne sert qu'à la pagination live, pas au calcul (buildBTSegmentGrid ne lit que
// pts/type) ; il reste nécessaire au MARQUEUR (identifie précisément QUELLES lignes ont été
// captées), donc conservé là, séparément.
//
// ─── LE POINT DUR DU LOT, PAS UN DÉTAIL ─────────────────────────────────────────────────────
// Un agrégat qui dérive de sa source sert une donnée fausse en silence — pire que les 157
// requêtes qu'il remplace. Ce script ne suffit PAS à s'en protéger seul : il produit le
// fichier et son marqueur, mais c'est app.html (loadBTAgregatOuRepli, chargement) et le check
// planifié (verifie_fraicheur_agregat_bt.mjs) qui portent la garde réelle, à deux moments
// distincts — l'un à chaque chargement client, l'autre en continu côté dépôt. Ce script ne
// fait que déclarer honnêtement, dans le marqueur, ce qu'il a réellement capté.
import https from 'node:https';
import { writeFileSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..');

// SB_URL/SB_KEY extraits d'app.html plutôt que dupliqués ici — une seule source, jamais deux
// valeurs qui peuvent diverger si la clé anon est un jour recréée.
const appHtml = readFileSync(join(RACINE, 'app.html'), 'utf8');
const mUrl = appHtml.match(/const SB_URL\s*=\s*'([^']+)'/);
const mKey = appHtml.match(/const SB_KEY\s*=\s*'([^']+)'/);
if (!mUrl || !mKey) { console.error('SB_URL/SB_KEY introuvables dans app.html — extraction cassée, ne pas générer sur une hypothèse.'); process.exit(1); }
const SB_HOST = new URL(mUrl[1]).host;
const SB_KEY = mKey[1];

const PAGE = 1000;
function fetchPage(idGt) {
  return new Promise((resolve, reject) => {
    const path = `/rest/v1/bt_lines?select=pts,type,id&clat=gte.41.3&clat=lte.43.1&clon=gte.8.5&clon=lte.9.7&order=id&id=gt.${idGt}&limit=${PAGE}`;
    const req = https.request({ hostname: SB_HOST, path, method: 'GET',
      headers: { apikey: SB_KEY, Authorization: 'Bearer ' + SB_KEY, ...(idGt === 0 ? { Prefer: 'count=exact' } : {}) } },
      (res) => { const chunks = []; res.on('data', c => chunks.push(c));
        res.on('end', () => resolve({ status: res.statusCode, body: Buffer.concat(chunks).toString('utf8'), headers: res.headers })); });
    req.on('error', reject); req.end();
  });
}
async function fetchPageAvecRetry(idGt, tentative = 0) {
  const r = await fetchPage(idGt);
  // 200 (sans Prefer:count=exact) ou 206 Partial Content (PostgREST, quand count=exact déclenche
  // une réponse de type Range) — les deux sont des succès. Bug trouvé en relançant ce script
  // (200 seul rejetait systématiquement la 1ère page, id>0, seule à porter count=exact).
  if (r.status !== 200 && r.status !== 206) {
    if (tentative >= 5) throw new Error(`HTTP ${r.status} persistant après 5 tentatives (id>${idGt})`);
    await new Promise(res => setTimeout(res, 1000 * (tentative + 1)));
    return fetchPageAvecRetry(idGt, tentative + 1);
  }
  return r;
}

console.error('[agrégat bt] pagination par curseur (même patron que loadBTLinesAsync, PR #1456)…');
let all = [], lastId = 0, totalDeclare = null;
while (true) {
  const r = await fetchPageAvecRetry(lastId);
  if (totalDeclare === null) {
    const cr = r.headers['content-range']; // https natif : objet brut, pas l'API Headers de fetch()
    const m = cr && cr.match(/\/(\d+)\s*$/);
    if (m) totalDeclare = parseInt(m[1], 10);
  }
  const page = JSON.parse(r.body);
  if (!Array.isArray(page) || page.length === 0) break;
  all = all.concat(page);
  process.stderr.write(`  id>${lastId} +${page.length} (total=${all.length})\n`);
  if (page.length < PAGE) break;
  lastId = page[page.length - 1].id;
}

if (all.length === 0) { console.error('[agrégat bt] 0 ligne reçue — refus d\'écrire un agrégat vide.'); process.exit(1); }
if (totalDeclare !== null && all.length !== totalDeclare) {
  console.error(`[agrégat bt] incohérent : ${all.length} lignes reçues, ${totalDeclare} déclarées par Content-Range. Refus d'écrire.`);
  process.exit(1);
}

const derniereLigneId = all[all.length - 1].id;
const lignes = all.map(r => ({ pts: r.pts, type: r.type }));
const marqueur = {
  genere_le: new Date().toISOString(),
  derniere_ligne_id: derniereLigneId,
  nb_lignes: all.length,
};

writeFileSync(join(RACINE, 'public/data/bt_lines_agregat.json'), JSON.stringify(lignes));
writeFileSync(join(RACINE, 'public/data/bt_lines_agregat_marqueur.json'), JSON.stringify(marqueur, null, 2) + '\n');

console.error(`[agrégat bt] écrit : ${all.length} lignes, dernier id=${derniereLigneId}, ${marqueur.genere_le}`);
