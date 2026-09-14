#!/usr/bin/env node
// ─── verifie_fraicheur_agregat_bt.mjs — LE SECOND GARDE, indépendant du premier ────────────
//
// Usage :  node scripts/verifie_fraicheur_agregat_bt.mjs
// Sort 1 (échec bruyant) si public/data/bt_lines_agregat_marqueur.json a plus de
// SEUIL_AGE_MS. Sort 0 sinon. C'est TOUT ce que ce script fait — il ne régénère rien, ne
// corrige rien, ne contacte pas Supabase.
//
// ─── POURQUOI CE SCRIPT EXISTE, SÉPARÉMENT DU PREMIER GARDE ─────────────────────────────────
// loadBTAgregatOuRepli() (app.html) protège la JUSTESSE de chaque chargement : un marqueur
// périmé y fait tomber sur loadBTLinesAsync(), jamais de donnée fausse servie. Mais ce repli
// est SILENCIEUX pour qui ne regarde pas la console — un cron de régénération cassé pourrait
// laisser TOUS les visiteurs sur le chemin lent indéfiniment, sans qu'aucun humain ne le
// remarque : le gain de la variante (i) aurait disparu en silence, alors que rien n'est faux.
// Brief "agrégat BT, mise en oeuvre" (2026-09-14), Soleil : « Sans lui, tu ne merges pas ».
//
// ─── LE SEUIL EST UN LITTÉRAL, PAS UNE VARIABLE ──────────────────────────────────────────────
// Délibéré (consigne explicite du brief) : un seuil lu depuis un secret/une variable
// d'environnement/un fichier de config peut être changé sans que ce changement soit visible
// dans une revue de code normale — exactement le genre d'écart silencieux que ce script existe
// pour empêcher ailleurs. 14 jours : le double de la cadence de régénération visée (7 jours,
// cf. .github/workflows/regenere-agregat-bt.yml) — une marge, pas la cadence elle-même, pour
// ne pas alarmer sur un simple retard normal du planificateur GitHub Actions (`schedule` est
// documenté best-effort, cf. intermagnet-cron.yml, constat 2026-09-08).
const SEUIL_AGE_MS = 14 * 24 * 60 * 60 * 1000; // 14 jours — LITTÉRAL, ne pas paramétrer.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const CHEMIN_MARQUEUR = join(ICI, '..', 'public', 'data', 'bt_lines_agregat_marqueur.json');

let marqueur;
try {
  marqueur = JSON.parse(readFileSync(CHEMIN_MARQUEUR, 'utf8'));
} catch (e) {
  console.error(`[fraîcheur agrégat BT] ÉCHEC — marqueur illisible (${CHEMIN_MARQUEUR}) : ${e.message}`);
  process.exit(1);
}

if (!marqueur || typeof marqueur.genere_le !== 'string') {
  console.error('[fraîcheur agrégat BT] ÉCHEC — marqueur sans champ genere_le exploitable.');
  process.exit(1);
}

const genereLeMs = Date.parse(marqueur.genere_le);
if (Number.isNaN(genereLeMs)) {
  console.error(`[fraîcheur agrégat BT] ÉCHEC — genere_le illisible comme date : "${marqueur.genere_le}".`);
  process.exit(1);
}

const ageMs = Date.now() - genereLeMs;
const ageJours = (ageMs / (24 * 60 * 60 * 1000)).toFixed(1);
const seuilJours = (SEUIL_AGE_MS / (24 * 60 * 60 * 1000)).toFixed(0);

if (ageMs > SEUIL_AGE_MS) {
  console.error(`[fraîcheur agrégat BT] ÉCHEC — marqueur vieux de ${ageJours} j (> ${seuilJours} j). `
    + `genere_le=${marqueur.genere_le}, derniere_ligne_id=${marqueur.derniere_ligne_id}, nb_lignes=${marqueur.nb_lignes}. `
    + `Le repli client (loadBTAgregatOuRepli) protège la justesse de chaque visite, mais ce workflow `
    + `de régénération semble arrêté — la piste n'a de sens que si ce cas est visible. `
    + `Vérifier .github/workflows/regenere-agregat-bt.yml (dernières exécutions).`);
  process.exit(1);
}

console.log(`[fraîcheur agrégat BT] OK — marqueur vieux de ${ageJours} j (seuil ${seuilJours} j). `
  + `genere_le=${marqueur.genere_le}, nb_lignes=${marqueur.nb_lignes}.`);
