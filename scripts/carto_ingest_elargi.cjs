// Brief "Ingestion Cartoradio élargie" (2026-09-02) — ingère les 206 fiches Cartoradio
// absentes de public/data/cartoradio_certified_corse.json, données seules.
//
// GARDE-FOU CENTRAL : chaque fiche ingérée porte calib_eligible:false. calibrateRF()
// (app.html) doit vérifier ce marqueur AVANT tout autre traitement et exclure toute fiche
// où il vaut explicitement false. Les 30 fiches d'origine n'ont pas le champ — son absence
// reste équivalente à "éligible", donc AUCUNE des 30 n'est retouchée par ce script : ni leurs
// valeurs, ni leur ordre, ni leur présence. Le contrôle de non-régression (n_used=21,
// k=0,3606093719868869) se vérifie en rechargeant app.html après écriture, pas en le supposant.
//
// N'écrit QUE dans public/data/cartoradio_certified_corse.json (mesures[] étendu +
// statistiques_ingestion_elargie{} ajouté à la racine). Le bloc `statistiques` d'origine
// n'est PAS touché : il continue de décrire exactement les 30 fiches actives en calibration,
// tel qu'avant ce script.
//
// Lit : scripts/carto_corse_nouvelles_fiches_2026-09-02.json (instantané brut des 206 fiches,
// endpoint /api/v1/mesures/{id}, extrait le 2026-09-02 — mêmes bbox/flags que
// carto_regenerate.cjs, sans fenêtre anciennete). Committé pour traçabilité/reproductibilité,
// même convention que carto_corse_geojson_snapshot_2026-04-27.json.
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const JSON_PATH = path.join(ROOT, 'public', 'data', 'cartoradio_certified_corse.json');
const SNAPSHOT_PATH = path.join(__dirname, 'carto_corse_nouvelles_fiches_2026-09-02.json');

const local = JSON.parse(fs.readFileSync(JSON_PATH, 'utf8'));
const snap = JSON.parse(fs.readFileSync(SNAPSHOT_PATH, 'utf8'));

const localIds = new Set(local.mesures.map(m => String(m.id)));

// Règle de classement vérifiée SANS EXCEPTION sur les 30/30 fiches déjà intégrées
// (cf. brief d'inventaire du 2026-09-02) : le champ "environnement" de l'API, pas "milieu",
// porte la distinction résidentiel / extérieur public que calibrateRF() utilise déjà.
function classify(environnement) {
  return environnement === "Lieu d'habitation" ? 'residentiel' : 'exterieur_public';
}

function toIso(dateFr) {
  // "28/05/2024" -> "2024-05-28"
  const [d, m, y] = dateFr.split('/');
  return `${y}-${m}-${d}`;
}

function titleCase(commune) {
  // L'API rend les communes en MAJUSCULES ("AJACCIO") ; les 30 fiches d'origine utilisent une
  // casse titre ("Ajaccio"). Alignement cosmétique pur, aucune donnée métier modifiée.
  return commune.toLowerCase().replace(/(^|[\s'-])\p{L}/gu, c => c.toUpperCase());
}

const nouveaux = [];
const ignores = [];
for (const f of snap.fiches) {
  const id = String(f.numero);
  if (localIds.has(id)) { ignores.push(id); continue; } // défensif : ne double aucune fiche déjà présente
  const commune = titleCase(f.adresse.commune);
  nouveaux.push({
    id,
    commune,
    lat: f._coord.lat,
    lon: f._coord.lon,
    precision_coord: 'exacte',
    valeur_max_vm: parseFloat(f.mesureglobale),
    unite: 'V/m', // convention uniforme des 30 fiches d'origine, y compris les 2 "objet communicant"
    valeurs_par_bande: null,
    date_mesure: toIso(f.date),
    laboratoire: f.laboratoire,
    protocole: f.protocole,
    seuil_legal_vm: 28, // constante réglementaire ANFR/DR 15-4, identique aux 30 fiches d'origine
    conforme: f.conformite === 'true' || f.conformite === true,
    adresse_complete: `${f.adresse.voie} ${f.adresse.commune}`.trim(),
    type_environnement: classify(f.environnement),
    milieu: f.milieu, // champ absent du schéma d'origine, demandé par le brief d'ingestion
    environnement: f.environnement, // idem — texte brut API, sous-jacent à type_environnement
    hauteur_mesure_m: null,
    source_pdf: f.rapport || null,
    note: null,
    calib_eligible: false, // ═══ GARDE-FOU CENTRAL — cf. calibrateRF() dans app.html ═══
    _provenance_ingestion_elargie: {
      date_extraction: snap.date_extraction,
      methode: "Endpoint par fiche /api/v1/mesures/{id} (JSON structuré, sans OCR)",
      url_liste: snap.source_liste,
      url_fiche: snap.source_fiche,
      note: "Éligibilité calibration non évaluée pour ce lot — calib_eligible:false par construction. Cf. dette privée CARTORADIO-REFRESH-001.",
    },
  });
}

if (ignores.length) {
  console.log(`Ignorées (déjà présentes dans le fichier intégré) : ${ignores.length} — ${ignores.join(', ')}`);
}

local.mesures = local.mesures.concat(nouveaux);

// Bloc séparé, à la racine — ne touche PAS `local.statistiques` (qui continue de décrire les
// 30 fiches actives en calibration, comme avant ce script).
local.statistiques_ingestion_elargie = {
  date_ingestion: '2026-09-02',
  fiches_ajoutees: nouveaux.length,
  calib_eligible: false,
  note: "Fiches ajoutées par l'ingestion élargie du 2026-09-02 (206 fiches Cartoradio absentes du "
    + "corpus d'origine, même bbox/flags que la régénération d'avril, sans fenêtre temporelle). "
    + "Toutes marquées calib_eligible:false — n'entrent pas dans le pool de calibrateRF(). "
    + "Éligibilité et intégration au pool de calibration : cf. dette privée CARTORADIO-REFRESH-001, "
    + "arbitrage Soleil requis (GELÉ-001b).",
};

fs.writeFileSync(JSON_PATH, JSON.stringify(local, null, 2) + '\n');

console.log('=== Ingestion terminée ===');
console.log('Fiches ajoutées :', nouveaux.length);
console.log('Total mesures dans le fichier :', local.mesures.length);
console.log('Toutes calib_eligible:false :', nouveaux.every(m => m.calib_eligible === false));
