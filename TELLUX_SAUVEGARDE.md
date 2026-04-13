# TELLUX — Stratégie de sauvegarde

**Date :** 9 avril 2026
**Principe directeur :** Règle 3-2-1 — 3 copies, 2 supports différents, 1 hors site.

---

## B1. Sauvegarde du code source

### État actuel (présumé)

- **Copie 1 :** GitHub (origin) — dépôt probablement public ou privé, branche `main`.
- **Copie 2 :** Clone local sur l'ordinateur de Soleil — probable mais à vérifier.
- **Copie 3 :** Aucune (pas de mirror, pas de sauvegarde hors site).

### Stratégie cible

| Copie | Support | Localisation | Synchronisation | Coût |
|---|---|---|---|---|
| 1 | GitHub | Cloud (Microsoft/Azure) | Automatique à chaque push | 0 € |
| 2 | GitLab mirror | Cloud (Google Cloud) | Automatique, toutes les 5-60 min | 0 € |
| 3 | Clone local + copie disque dur externe ou cloud personnel | Chez Soleil | Hebdomadaire (manuelle) | 0 € |

### Mise en œuvre

**Copie 2 — Mirror GitLab (voir Action 2 de l'audit infrastructure).** Une fois configuré, la synchronisation est automatique et invisible. Pas de maintenance.

**Copie 3 — Sauvegarde locale hebdomadaire.** Chaque vendredi (ou au rythme qui convient) :

```bash
# Depuis le dossier du projet
git pull origin main
# Copier le dossier complet sur un disque externe ou un cloud personnel
cp -r ~/Tellux /Volumes/DisqueExterne/Tellux_backup_$(date +%Y%m%d)
```

Alternative : `git bundle create tellux_backup.bundle --all` crée un fichier unique contenant tout l'historique Git, copiable sur n'importe quel support.

**Cloud personnel recommandé :** Proton Drive (chiffré, européen, gratuit jusqu'à 1 Go) ou pCloud (suisse, 10 Go gratuit). Éviter Google Drive et Dropbox si la souveraineté des données est un critère.

---

## B2. Sauvegarde de la base Supabase

### Risque

Si la base Supabase est perdue (panne, corruption, suppression accidentelle, migration ratée), toutes les contributions citoyennes (mesures terrain, données crowdsourcées) disparaissent. Les données institutionnelles (ANFR, églises) sont reconstituables depuis les sources, mais les contributions terrain sont irremplaçables.

### Option 1 — Export automatique quotidien (recommandée à terme)

Un script déclenché par un cron (GitHub Action ou tâche planifiée locale) qui exporte les tables critiques en JSON ou CSV chaque jour.

**Script prêt à l'emploi :**

```bash
#!/bin/bash
# tellux_backup_supabase.sh
# Exporte les tables critiques de Supabase en JSON
# Prérequis : curl, jq installés
# Variables : SUPABASE_URL et SUPABASE_ANON_KEY à renseigner

SUPABASE_URL="https://<project-ref>.supabase.co"
SUPABASE_ANON_KEY="<votre-anon-key>"
BACKUP_DIR="./supabase_backups/$(date +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"

# Liste des tables à sauvegarder
TABLES=("contributions" "mesures" "churches")

for TABLE in "${TABLES[@]}"; do
  echo "Export de $TABLE..."
  curl -s \
    -H "apikey: $SUPABASE_ANON_KEY" \
    -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
    "$SUPABASE_URL/rest/v1/$TABLE?select=*" \
    -o "$BACKUP_DIR/${TABLE}.json"
  
  ROWS=$(jq length "$BACKUP_DIR/${TABLE}.json" 2>/dev/null || echo "erreur")
  echo "  → $ROWS lignes exportées"
done

echo "Sauvegarde terminée dans $BACKUP_DIR"
```

**Note :** Les noms de tables (`contributions`, `mesures`, `churches`) sont des suppositions basées sur le contexte du projet. Soleil doit adapter la liste `TABLES` aux noms réels dans sa base Supabase (visibles dans le dashboard → Table Editor).

**Automatisation via GitHub Actions :**

```yaml
# .github/workflows/backup-supabase.yml
name: Backup Supabase
on:
  schedule:
    - cron: '0 3 * * *'  # Chaque jour à 3h du matin UTC
  workflow_dispatch:       # Permet aussi le déclenchement manuel

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Export tables
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
        run: |
          chmod +x scripts/tellux_backup_supabase.sh
          ./scripts/tellux_backup_supabase.sh
      - name: Commit et push
        run: |
          git config user.name "Tellux Backup Bot"
          git config user.email "noreply@tellux.fr"
          git add supabase_backups/
          git commit -m "Backup Supabase $(date +%Y-%m-%d)" || echo "Pas de changement"
          git push
```

**Configuration requise :** Dans GitHub → Settings → Secrets and variables → Actions, ajouter `SUPABASE_URL` et `SUPABASE_ANON_KEY`.

**Limite :** L'API REST Supabase retourne par défaut 1 000 lignes par requête. Si une table dépasse 1 000 lignes, ajouter `&limit=10000` à l'URL (ou paginer). Pour Tellux en phase tests, c'est largement suffisant.

### Option 2 — Export manuel hebdomadaire (en attendant l'automatisation)

1. Dashboard Supabase → Table Editor.
2. Sélectionner chaque table critique.
3. « Export to CSV ».
4. Sauvegarder dans `_data_backups/` dans le dépôt Git.
5. Committer.

**Fréquence recommandée :** Hebdomadaire pendant la phase tests (peu de contributions attendues). Passer au quotidien automatisé dès que les contributions augmentent.

### Recommandation

Commencer par l'Option 2 (manuelle) dès cette semaine. Mettre en place l'Option 1 (automatique) quand Soleil sera à l'aise avec GitHub Actions — possiblement lors d'une session Claude Code dédiée.

---

## B3. Sauvegarde des fichiers documentaires

### État actuel

Les fichiers `.md` et `.docx` du projet sont dans le dossier Tellux monté dans Cowork. **Sont-ils dans le dépôt Git ?** C'est la question clé.

### Vérification requise

Soleil doit vérifier que les fichiers suivants sont bien dans le dépôt Git et commités :

| Fichier | Critique ? | Dans Git ? |
|---|---|---|
| `tellux_v6_design.html` | Oui — source de vérité code | À vérifier |
| `CANDIDATURE_TELLUX_v7.docx` | Oui — dossier CTC | À vérifier |
| `DIRECTION_ARTISTIQUE_v2.md` | Oui — DA gelée | À vérifier |
| `TELLUX_LOGO_V7.html` | Oui — logo source | À vérifier |
| `TELLUX_BRIEFING.md` | Oui — briefing consolidé | À vérifier |
| `TELLUX_ROADMAP.md` | Oui — feuille de route | À vérifier |
| `TELLUX_MONTEE_EN_GAMME.md` | Moyen — plan stratégique | À vérifier |
| `TELLUX_AUDIT_MODELE.md` | Moyen — audit interne | À vérifier |
| `TELLUX_DOSSIER_SCIENTIFIQUES.md` | Moyen — dossier contacts | À vérifier |
| `TELLUX_KIT_ENVOI_EM.md` | Moyen — kit associations | À vérifier |
| `TELLUX_AUDIT_INFRASTRUCTURE.md` | Moyen — cet audit | À vérifier |
| `favicons/tellux-v7.svg` | Oui — favicon | À vérifier |

### Recommandation

Si certains fichiers ne sont pas dans Git : les ajouter. Un simple `git add` suivi d'un commit suffit. Le `.docx` est un fichier binaire qui prend de la place dans l'historique Git, mais pour un seul fichier de quelques centaines de Ko, c'est acceptable.

Pour le `.docx` spécifiquement : Git ne fait pas de diff lisible sur les binaires. Si des modifications fréquentes sont prévues, envisager d'exporter une version `.md` du contenu à chaque mise à jour pour garder un diff lisible dans l'historique.

---

## B4. Sauvegarde des données institutionnelles

### Contexte

Tellux utilise des données téléchargées depuis des sources institutionnelles : BRGM (failles), ANFR (antennes), IGRF-14 (champ magnétique), EMAG2v3 (anomalies crustales), ASNR (radon). Ces données sont intégrées dans le code HTML ou chargées depuis Supabase.

### Risque

Faible — ces sources sont institutionnelles et pérennes. Mais les URL changent (ex : passage de Géoportail à data.geopf.fr), les formats évoluent, et les versions utilisées dans Tellux doivent être traçables pour la reproductibilité scientifique.

### Recommandation

Créer un sous-dossier `_data_sources/` dans le dépôt Git contenant :

```
_data_sources/
├── README.md               ← pour chaque source : nom, URL, date de récupération, version, format
├── ANFR_antennes_corse.csv  ← snapshot des 974 antennes utilisées
├── BRGM_failles_corse.json  ← snapshot des failles utilisées
├── IGRF14_coefficients.txt  ← coefficients IGRF-14 (si utilisés localement)
└── EMAG2v3_corse.geojson    ← grille EMAG2v3 extraite pour la Corse
```

Le `README.md` devrait documenter pour chaque fichier :
- Source officielle (URL)
- Date de téléchargement
- Version utilisée
- Transformations appliquées (filtrage géographique, conversion de format)
- Licence d'utilisation

**Taille estimée :** Quelques Mo. Acceptable dans Git.

**Bénéfice :** Reproductibilité scientifique (un chercheur peut vérifier exactement quelles données Tellux utilise), et protection contre la disparition ou le changement de format des sources.

---

## Synthèse

| Donnée | Copie 1 | Copie 2 | Copie 3 | État |
|---|---|---|---|---|
| Code source | GitHub | GitLab mirror | Local + disque externe | À mettre en place (mirror + backup local) |
| Base Supabase | Supabase (unique) | Export JSON/CSV dans Git | — | À mettre en place (export manuel puis auto) |
| Fichiers documentaires | Git | Mirror GitLab | Local | À vérifier (tous dans Git ?) |
| Données institutionnelles | Dans le HTML / Supabase | — | — | À externaliser dans `_data_sources/` |

---

*Plan rédigé le 9 avril 2026. L'automatisation des exports Supabase est un chantier technique léger (~1h avec GitHub Actions) à réaliser lors d'une prochaine session Claude Code.*
