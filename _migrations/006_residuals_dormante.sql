-- ===========================================================================
-- MIGRATION DORMANTE — NE PAS APPLIQUER À SUPABASE EN L'ÉTAT
-- ===========================================================================
-- Cette migration définit la table `residuals` destinée au chantier
-- auto-affinage du modèle Tellux. Elle est posée dans le repo pour fixer
-- le schéma cible, mais ne sera appliquée à la base qu'au moment de
-- l'amorçage de la phase 1 du chantier, après décision explicite.
--
-- Référence : docs/auto-affinage-conception-v1.md
-- Date de conception : 26 avril 2026
-- Statut : DORMANTE (non appliquée)
-- ===========================================================================

CREATE TABLE IF NOT EXISTS public.residuals (
  id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contribution_id      UUID NOT NULL REFERENCES public.contributions(id) ON DELETE CASCADE,
  domain               TEXT NOT NULL CHECK (domain IN ('M_static', 'M_elf', 'RF', 'I_gamma')),
  measured_value       NUMERIC NOT NULL,
  measured_unit        TEXT NOT NULL,
  predicted_value      NUMERIC NOT NULL,
  predicted_unit       TEXT NOT NULL,
  residual             NUMERIC GENERATED ALWAYS AS (measured_value - predicted_value) STORED,
  confidence_level     SMALLINT NOT NULL CHECK (confidence_level IN (1, 2)),
  model_version        TEXT NOT NULL,
  prediction_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  notes                TEXT,
  created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexation
CREATE INDEX IF NOT EXISTS idx_residuals_domain_confidence
  ON public.residuals(domain, confidence_level);
CREATE INDEX IF NOT EXISTS idx_residuals_prediction_timestamp
  ON public.residuals(prediction_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_residuals_contribution
  ON public.residuals(contribution_id);

-- Row Level Security (verrou complet)
-- Aucune policy n'est créée pour `anon` ni pour `authenticated` :
-- avec RLS activé et aucune policy, l'accès est entièrement bloqué pour
-- ces rôles. Seul `service_role` (clé privée serveur) peut lire et écrire.
ALTER TABLE public.residuals ENABLE ROW LEVEL SECURITY;

-- Trigger updated_at
CREATE OR REPLACE FUNCTION public.trigger_residuals_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER residuals_updated_at
  BEFORE UPDATE ON public.residuals
  FOR EACH ROW
  EXECUTE FUNCTION public.trigger_residuals_updated_at();

-- Documentation des colonnes
COMMENT ON TABLE public.residuals IS
  'Auto-affinage du modele Tellux : ecart mesure - prediction par contribution. Migration dormante au moment de la creation, voir docs/auto-affinage-conception-v1.md.';
COMMENT ON COLUMN public.residuals.domain IS
  'Domaine physique : M_static (magnetique statique), M_elf (basse frequence), RF (radiofrequence), I_gamma (rayonnement ionisant).';
COMMENT ON COLUMN public.residuals.confidence_level IS
  'Niveau de fiabilite de la contribution : 1 (protocole strict, eligible calibration), 2 (capteur Android brut, couverture territoriale uniquement).';
COMMENT ON COLUMN public.residuals.model_version IS
  'Version du moteur Tellux ayant produit la prediction. Permet le recalcul historique lors d evolution du modele.';
COMMENT ON COLUMN public.residuals.measured_unit IS
  'Unite de la valeur mesuree (ex. nT, uT, V/m, uSv/h). Doit correspondre a unite_saisie de la contribution.';
COMMENT ON COLUMN public.residuals.predicted_unit IS
  'Unite de la valeur predite par le moteur Tellux. Doit etre comparable a measured_unit (apres conversion eventuelle dans le moteur).';
