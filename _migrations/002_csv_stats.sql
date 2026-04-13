-- Migration 002 — Import CSV Phyphox + tracabilite unite de saisie
-- Executee manuellement dans le SQL Editor Supabase avant deploiement
-- Date : 2026-04-13

ALTER TABLE contributions
  ADD COLUMN IF NOT EXISTS csv_stats jsonb,
  ADD COLUMN IF NOT EXISTS unite_saisie text;

COMMENT ON COLUMN contributions.csv_stats IS 'Statistiques agregees session Phyphox : moyenne, ecart-type, min, max, n_points, duree_s';
COMMENT ON COLUMN contributions.unite_saisie IS 'Unite choisie par utilisateur (ex: µT). La valeur dans .valeur est toujours en nT pour instruments magnetiques.';
