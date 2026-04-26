-- ===========================================================================
-- MIGRATION 007 — Colonne excluded_from_public + tag des contributions polluees
-- ===========================================================================
-- Date d application : 2026-04-27
-- Contexte : audit en navigateur direct sur la prod le 27 avril 2026 a revele
-- 6 contributions enregistrees avec une valeur en degres DeviceOrientation
-- au lieu d un champ magnetique en uT/nT, suite a un fallback silencieux du
-- flux B (Capteurs appareil) quand l API Magnetometer n etait pas disponible.
-- Cette migration :
--   1. Ajoute une colonne `excluded_from_public` pour permettre d exclure
--      certaines contributions de l affichage public sans les supprimer
--      (preservation pour tracabilite et audit ulterieur).
--   2. Tag les 6 contributions polluees identifiees (unite = 'deg' ou '°',
--      sur la fenetre 2026-04-21 a 2026-04-25).
--
-- La cause racine du fallback DeviceOrientation est corrigee dans le meme
-- ticket cote `app.html` (durcissement de capCheckSupport, retrait du push
-- des angles dans capSamples, garde-fous capStartRecording/capComputeStats/
-- capSubmitMeasurement). Ref dette CONTRIB-SCHEMA-001.
-- ===========================================================================

-- 1. Ajouter la colonne (idempotent)
ALTER TABLE public.contributions
  ADD COLUMN IF NOT EXISTS excluded_from_public BOOLEAN NOT NULL DEFAULT FALSE;

COMMENT ON COLUMN public.contributions.excluded_from_public IS
  'Contribution exclue de l affichage public (donnees polluees, tests, doublons). Conservee pour tracabilite.';

-- 2. Tag des 6 contributions polluees
UPDATE public.contributions
SET excluded_from_public = TRUE,
    note = COALESCE(note, '') || ' | Exclu : valeur en degres DeviceOrientation, pas un champ magnetique. Audit 2026-04-27.'
WHERE created_at >= '2026-04-21'
  AND created_at <= '2026-04-25'
  AND (unite = 'deg' OR unite = '°')
  AND excluded_from_public = FALSE;
