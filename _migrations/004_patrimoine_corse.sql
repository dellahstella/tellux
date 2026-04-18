-- 004_patrimoine_corse.sql
-- Table des sites patrimoniaux spécialisés : Tours génoises, Ponts génois,
-- Thermalisme, Châteaux médiévaux, Patrimoine & Ressources
-- Périmètre : 38 entrées migrées depuis SITES[] inline (corpus R1-R10)
-- tourNames legacy (13) et Mine de la Finosa exclus volontairement

CREATE TABLE IF NOT EXISTS patrimoine_corse (
  id          SERIAL PRIMARY KEY,
  lat         NUMERIC(9,6)  NOT NULL,
  lon         NUMERIC(9,6)  NOT NULL,
  nom         TEXT          NOT NULL,
  categorie   TEXT          NOT NULL,
  couleur     CHAR(7)       NOT NULL DEFAULT '#c8a035',
  description TEXT,
  created_at  TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_patrimoine_corse_categorie ON patrimoine_corse (categorie);

ALTER TABLE patrimoine_corse ENABLE ROW LEVEL SECURITY;
CREATE POLICY "select_all" ON patrimoine_corse FOR SELECT USING (true);

-- ════════════════════════════════════════════
-- TOURS GÉNOISES (15 entrées)
-- ════════════════════════════════════════════
INSERT INTO patrimoine_corse (lat, lon, nom, categorie, couleur, description) VALUES
(41.570, 9.290, 'Tour génoise Chiappa', 'Tour génoise', '#c8a035', 'Tour génoise XVIe · Granit rose · Réseau surveillance côtière · Vue mer'),
(42.973, 9.355, 'Tour d''Agnello (Cap Corse)', 'Tour génoise', '#c8a035', 'Tour génoise · Schiste · Réseau surveillance Cap Corse · Sommet 536m'),
(41.918, 8.623, 'Tour de la Parata (Ajaccio)', 'Tour génoise', '#c8a035', 'Tour génoise 1608 · Granit · Iles Sanguinaires · Golfe Ajaccio'),
(42.700, 9.268, 'Tour de la Mortella', 'Tour génoise', '#c8a035', 'Tour génoise 1563-1564 · Architecte Paleari Fratino · Inscrite MH 08/03/1991 PA00099279 · Modèle des 140+ Martello Towers britanniques (Angleterre, Irlande, Canada, Australie, Afrique du Sud) · Conservatoire du littoral 1980 · Saint-Florent côte ouest · GPS approx.'),
(42.888, 9.360, 'Tour de Sénèque (Pino/Luri)', 'Tour génoise', '#c8a035', 'Donjon seigneurial XVIe · Famille dei Moti · Classée MH 1840 · 564m alt. · Légende exil Sénèque 41-49 ap. J.-C. · Plus ancienne MH Corse · GPS approx.'),
(42.627, 9.497, 'Tour d''Erbalunga (Brando)', 'Tour génoise', '#c8a035', 'Tour génoise XVe · Détruite 1553, reconstruite · Brando · Vue golfe de Brando · GPS approx.'),
(42.983, 9.463, 'Tour de la Chiappella (Rogliano)', 'Tour génoise', '#c8a035', 'Tour génoise 1549 · Inscrite MH 1991 · Éventrée par Nelson 1796 · Tamarone · Associée piève Santa Maria 1176 · GPS approx.'),
(43.028, 9.405, 'Tour de Giraglia (îlot)', 'Tour génoise', '#c8a035', 'Tour génoise carrée · Îlot Giraglia extrémité nord Cap Corse · Phare actif · Conservatoire du littoral · GPS approx.'),
(42.109, 8.723, 'Tour de Sagone (Vico)', 'Tour génoise', '#c8a035', 'Tour debut XVIIe s · MH PA00099123 19/04/1974 · massacre 1566 · Rapport 8'),
(42.155, 8.554, 'Tour d''Omigna (Cargese)', 'Tour génoise', '#c8a035', 'Tour ronde 12m · 1604-1606 · MH PA00099136 08/03/1991 · restauree 2009 Conservatoire littoral · Rapport 8'),
(42.234, 8.527, 'Tour de Turghiu (Capo Rosso)', 'Tour génoise', '#c8a035', 'Sommet Capo Rosso 331m · XVIe-XVIIe s · falaises 400m · non protegee · Rapport 8'),
(42.133, 8.587, 'Tour de Cargese (ruines)', 'Tour génoise', '#c8a035', 'Tour XVIe s · base seule subsistante · Rapport 8'),
(41.908, 8.774, 'Tour de Capitello (Castelluccio)', 'Tour génoise', '#c8a035', 'Tour genoise pisane · MH PA00099137 · embouchure Gravona-Prunelli · Rapport 10'),
(41.84656, 8.76241, 'Tour d''Isolella (Sette Navi)', 'Tour génoise', '#c8a035', 'Tour circulaire 1608 · moellons granit · cordon briques · machecoulis · MH PA00099144 04/08/1992 · Rapport 10'),
(41.719, 8.664, 'Tour de Capo di Muro', 'Tour génoise', '#c8a035', 'Tour 1580-1617 juridiction Ajaccio · affectee Phares et Balises 1857 · MH · Rapport 10');

-- ════════════════════════════════════════════
-- PONTS GÉNOIS (3 entrées)
-- ════════════════════════════════════════════
INSERT INTO patrimoine_corse (lat, lon, nom, categorie, couleur, description) VALUES
(42.279, 9.189, 'Pont d''Altiani', 'Pont génois', '#475569', 'Pont génois sur le Tavignano · MH 1977 · Gorges du Tavignano · Castagniccia · Rapport 6'),
(42.268, 8.744, 'Pont de Pianella (Ota)', 'Pont génois', '#475569', 'Pont génois gorges de Spelunca · MH 1976 · Ota · Porto · GPS approx. · Rapport 6'),
(41.929, 8.994, 'Pont de Zippitoli (disparu 2023)', 'Pont génois', '#475569', 'Pont genois XVe-XVIe s · 19m arche unique · MH PA00099075 15/02/1977 · emporte Ciaran 03/11/2023 · GPS approx · Rapport 9');

-- ════════════════════════════════════════════
-- THERMALISME (6 entrées)
-- ════════════════════════════════════════════
INSERT INTO patrimoine_corse (lat, lon, nom, categorie, couleur, description) VALUES
(41.705, 8.898, 'Thermes de Baracci', 'Thermalisme', '#0ea5e9', '52°C · Eaux sulfureuses · Valinco · Faille active · Propriano · Usage thérapeutique continu XIXe-2026'),
(41.827, 9.019, 'Sources de Guitera', 'Thermalisme', '#0ea5e9', '45°C · Pliocène · Haute vallée Taravo · Granit fracturé · Source captée · GPS approx.'),
(41.902, 9.035, 'Caldane (Zévaco)', 'Thermalisme', '#0ea5e9', '40°C · Sources chaudes · Haute Corse intérieure · Granit · Faille · GPS approx.'),
(41.781, 9.069, 'Lac thermal de Tora', 'Thermalisme', '#0ea5e9', 'Lac thermal naturel · Bocognano-Taravo · Granit · Émergence géothermique · GPS approx.'),
(42.057, 9.388, 'Pietrapola (station thermale)', 'Thermalisme', '#0ea5e9', '56°C · Sulfurées sodiques hyperthermales · Unique station thermale agréée Corse (RH3 rhumatologie) · 7 sources · 200 000 L/j · Commune Isolaccio-di-Fiumorbo · 700m alt. · Propriété CdC · Rouverture post-travaux 2023'),
(42.157, 8.894, 'Guagno-les-Bains', 'Thermalisme', '#0ea5e9', 'Source Venturini 49C + Occhiu 37C · sulfurees sodiques · baignoires marbre Napoleon III · Rapport 8');

-- ════════════════════════════════════════════
-- CHÂTEAUX MÉDIÉVAUX (8 entrées)
-- ════════════════════════════════════════════
INSERT INTO patrimoine_corse (lat, lon, nom, categorie, couleur, description) VALUES
(41.860, 9.000, 'Castello della Rocca', 'Château médiéval', '#92400e', 'Ruines château comtes della Rocca · Granit biotite · Alta Rocca · XIVe s.'),
(41.844, 8.774, 'Castello di Baricci', 'Château médiéval', '#92400e', 'Château fort Cinarchesi XIIe-XIVe · Crana/Ornano · Ruines · Contrôle vallée Taravo · GPS approx.'),
(41.595, 9.015, 'Castello d''Istria', 'Château médiéval', '#92400e', 'Château médiéval · Comtes d''Istria · Sartenais · Granit · XIIe s. · Lié à Castelnovo'),
(41.587, 8.981, 'Castelnovo (Bicchisano)', 'Château médiéval', '#92400e', 'Château Cinarchesi · XIIe s. · Contrôle col · Granit · Bicchisano-Taravo · GPS approx.'),
(41.528, 8.922, 'Castellu di u Grecu', 'Château médiéval', '#92400e', 'Château génois XIIIe · Plateau de Cauria · Domaine agraire privé · Giovanni Stregia 1239 · Chessa 2000'),
(41.547, 8.952, 'Castellu d''Itali', 'Château médiéval', '#92400e', 'Château médiéval XIIIe · Même vallée que U Grecu · Plateau de Cauria · GPS approx.'),
(42.967, 9.425, 'Castellacciu San Colombano', 'Château médiéval', '#92400e', 'Château Da Mare 1246 · 32×23m · Détruit Doria 03/03/1554 · Sable construction de Macinaggio · Ermitage colombanien VIIe · Inscrit MH · Rogliano · GPS approx.'),
(41.850, 9.034, 'Castellu di Bozzi (Guitera)', 'Château médiéval', '#92400e', 'Forteresse Cinarchesi · Punta di Bozzi · XIIe-XIVe s · boucle randonnee 1h30 · GPS approx · Rapport 9');

-- ════════════════════════════════════════════
-- PATRIMOINE & RESSOURCES (6 entrées)
-- ════════════════════════════════════════════
INSERT INTO patrimoine_corse (lat, lon, nom, categorie, couleur, description) VALUES
(42.820, 9.330, 'Mine d''amiante de Canari', 'Patrimoine & Ressources', '#78350f', '1948-1965 · SA Amiante de Corse / Eternit · 300 000 t chrysotile · Serpentinites chrysotilifères · Plages galets noirs Nonza-Albo · Anomalie magnétique locale · Démolition 2025 · BRGM RR-39277-FR · IA2B000939'),
(42.880, 9.392, 'Mine de Luri (antimoine)', 'Patrimoine & Ressources', '#78350f', 'District antimonifère Cap Corse · Filons Castello + Spergane · 3400 t · Puits Terra Rossa · Stibine en schiste lustre · Conducteur EM résiduel · Mise en sécurité 2005 · POP IA2B000832'),
(42.965, 9.430, 'Mine de Meria (antimoine)', 'Patrimoine & Ressources', '#78350f', 'Plus importante mine Cap Corse · Filons Vallone, San Martino, Fossato · 5600 t · Laverie + centrale électrique 1911 · Travaux noyés · District 11 000 t total Cap Corse · GPS approx.'),
(42.990, 9.395, 'Mine d''Ersa (antimoine)', 'Patrimoine & Ressources', '#78350f', 'Filons Granaggiolo, Castagnone, Guadicello, Sainte-Marie · 2000 t · Fermée 01/01/1919 · GPS approx.'),
(42.730, 9.332, 'Mine de magnétite de Farinole', 'Patrimoine & Ressources', '#78350f', 'Gisement de fer magnétite · Versant est Cap Corse · Cible magnétique majeure · BSS BRGM InfoTerre · GPS approx.'),
(42.417, 9.290, 'Mine de Matra (Bravona)', 'Patrimoine & Ressources', '#78350f', 'Mine arsenic-antimoine 1908-1945 · Val de Bravona · GPS approx. · Rapport 6');
