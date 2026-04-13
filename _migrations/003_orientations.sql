-- Migration 003 : Table des contributions d'orientation des sites
-- Date : 13 avril 2026 — Session Cowork Sonnet Patrimoine
-- Usage : Permettre aux mairies et associations de contribuer l'orientation
--         astrale des sites mégalithiques et des églises romanes

CREATE TABLE IF NOT EXISTS orientations_contributions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz DEFAULT now(),
  site_id text NOT NULL,
  azimut numeric NOT NULL CHECK (azimut >= 0 AND azimut <= 360),
  precision text CHECK (precision IN ('precise', 'bonne', 'approx')),
  source text,
  commentaire text,
  session_id text,
  validated boolean DEFAULT false
);

-- Index pour les requêtes fréquentes
CREATE INDEX IF NOT EXISTS idx_orient_site ON orientations_contributions(site_id);
CREATE INDEX IF NOT EXISTS idx_orient_validated ON orientations_contributions(validated);

-- RLS : lecture publique, écriture anonyme
ALTER TABLE orientations_contributions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "read orientations" ON orientations_contributions
  FOR SELECT TO anon USING (true);

CREATE POLICY "insert orientations" ON orientations_contributions
  FOR INSERT TO anon WITH CHECK (true);

-- Commentaire table
COMMENT ON TABLE orientations_contributions IS 'Contributions citoyennes d''orientation astrale des sites mégalithiques et églises. Validées manuellement avant intégration.';
