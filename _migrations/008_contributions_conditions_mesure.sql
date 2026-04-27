-- Migration 008 : conditions de mesure smartphone
-- NON APPLIQUÉE — décision Soleil requise avant exécution en production
-- Règle : ADD COLUMN IF NOT EXISTS uniquement (non destructif)

ALTER TABLE contributions ADD COLUMN IF NOT EXISTS airplane_mode_on boolean DEFAULT NULL;
ALTER TABLE contributions ADD COLUMN IF NOT EXISTS usb_charging_off boolean DEFAULT NULL;
ALTER TABLE contributions ADD COLUMN IF NOT EXISTS no_metal_proximity boolean DEFAULT NULL;
ALTER TABLE contributions ADD COLUMN IF NOT EXISTS measurement_duration_s integer DEFAULT NULL;
