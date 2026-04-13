-- 001_contributions_contexte_batiment.sql
-- Ajoute les colonnes contexte bâtiment à la table contributions
-- Résout l'erreur PGRST204 dans saveContrib() (colonnes manquantes)
--
-- Colonnes ajoutées :
--   contexte        : 'exterieur' ou 'interieur'
--   etage           : sous_sol, rdc, 1, 2
--   geo_nets        : noms des réseaux géobiologiques détectés
--   geo_netval      : score réseau géobiologique
--   materiaux_murs  : matériaux cochés dans le formulaire
--   appareils_actifs: appareils actifs au moment de la mesure
--   attenuation_prevue_db : atténuation RF calculée depuis les matériaux
--
-- Application : SQL Editor du dashboard Supabase
-- Prérequis : sauvegarder la base avant (voir TELLUX_SAUVEGARDE.md)

ALTER TABLE public.contributions
  ADD COLUMN IF NOT EXISTS contexte TEXT;

ALTER TABLE public.contributions
  ADD COLUMN IF NOT EXISTS etage TEXT;

ALTER TABLE public.contributions
  ADD COLUMN IF NOT EXISTS geo_nets TEXT[];

ALTER TABLE public.contributions
  ADD COLUMN IF NOT EXISTS geo_netval DOUBLE PRECISION;

ALTER TABLE public.contributions
  ADD COLUMN IF NOT EXISTS materiaux_murs TEXT[];

ALTER TABLE public.contributions
  ADD COLUMN IF NOT EXISTS appareils_actifs TEXT[];

ALTER TABLE public.contributions
  ADD COLUMN IF NOT EXISTS attenuation_prevue_db DOUBLE PRECISION;

-- Commentaires pour documentation
COMMENT ON COLUMN public.contributions.contexte IS 'Contexte du lieu : exterieur ou interieur';
COMMENT ON COLUMN public.contributions.etage IS 'Étage si intérieur : sous_sol, rdc, 1, 2';
COMMENT ON COLUMN public.contributions.geo_nets IS 'Réseaux géobiologiques détectés (Hartmann, Curry, Peyré)';
COMMENT ON COLUMN public.contributions.geo_netval IS 'Score numérique réseau géobiologique';
COMMENT ON COLUMN public.contributions.materiaux_murs IS 'Matériaux des murs cochés par le contributeur';
COMMENT ON COLUMN public.contributions.appareils_actifs IS 'Appareils actifs pendant la mesure (wifi, linky, induction…)';
COMMENT ON COLUMN public.contributions.attenuation_prevue_db IS 'Atténuation RF prévue en dB calculée depuis les matériaux';
