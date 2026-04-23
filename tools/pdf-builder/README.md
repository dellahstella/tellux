# Tellux — pdf-builder

Infrastructure de conversion markdown → PDF avec respect de la DA v2 gelée (palette Ardoise / Pierre / Maquis / Ocre / Porphyre / Tyrrhénien, typographie Fraunces / IBM Plex Sans / IBM Plex Mono).

Stack : WeasyPrint (HTML + CSS → PDF), markdown + pymdown-extensions, pygments pour la coloration des blocs de code.

## Statut

Infrastructure **prête à l'emploi** pour tests internes. La conversion finale des documents publics (Cadre scientifique, Position épistémique, Guide d'interprétation) reste **différée** jusqu'à la relecture par un physicien tiers et la phase de soumission institutionnelle. Cf. `ROADMAP.md` §8, Chantier 3.

Les exports générés ici relèvent du test de rendu uniquement. Ils ne sont ni publiés ni committés (cf. `.gitignore` → `build/pdf-tests/`).

## Prérequis

### Python

- Python 3.10 ou plus récent
- Dépendances : `pip install -r tools/pdf-builder/requirements.txt`

### Windows — GTK3 runtime (obligatoire)

WeasyPrint s'appuie sur Pango et GObject, qui ne sont pas inclus dans `pip install weasyprint` sur Windows. Installation standalone recommandée :

- Télécharger [gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
- Installer (emplacement par défaut : `C:\Program Files\GTK3-Runtime Win64\`)
- Le script détecte automatiquement cet emplacement via `os.add_dll_directory()`. Aucune modification du PATH système requise.

### Linux / macOS

Les DLL sont généralement fournies par le gestionnaire de paquets. Voir la [doc WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html).

## Usage

```bash
python tools/pdf-builder/build_pdf.py <source.md> --output <sortie.pdf>
```

Exemples :

```bash
# Export test (non publié, gitignoré)
python tools/pdf-builder/build_pdf.py \
  CADRE_SCIENTIFIQUE_TELLUX_v2.1.1.md \
  --output build/pdf-tests/cadre_scientifique_v2.1.1.pdf

python tools/pdf-builder/build_pdf.py \
  TELLUX_POSITION_EPISTEMIQUE.md \
  --output build/pdf-tests/position_epistemique.pdf
```

Options :

- `--title "..."` : titre du document (par défaut : premier `# h1` du markdown).
- `--css <chemin>` : CSS alternatif (par défaut : `tools/pdf-builder/da_v2.css`).

## Fichiers

| Fichier | Rôle |
|---|---|
| `build_pdf.py` | Script principal CLI |
| `da_v2.css` | Template CSS DA v2 gelée. **Ne pas modifier sans validation projet.** |
| `templates/document.html` | Template HTML minimal (title + article) |
| `requirements.txt` | Dépendances Python |

## Polices

Les `.woff2` sont référencés relativement au repo (`assets/fonts/fraunces/*.woff2`, `assets/fonts/ibm-plex-sans/*.woff2`, `assets/fonts/ibm-plex-mono/*.woff2`). Embarqués dans le repo public, pas de CDN runtime.

## Conversion finale (post-relecture physicien)

Quand la relecture sera validée :

1. S'assurer que les 3 documents sources sont finalisés (Cadre, Position, Guide d'interprétation — ce dernier à rédiger).
2. Générer les 3 PDF dans `build/pdf-publish/` (dossier à créer, également gitignoré par défaut si `build/` est couvert).
3. Publier les PDF via le canal retenu (à définir — pièces jointes soumission, dépôt repo public dans `assets/pdf/`, ou autre).
4. Remplacer les 3 placeholders « PDF bientôt disponible » dans `index.html` section `#ressources` par les liens effectifs (Chantier 4 de la roadmap).
