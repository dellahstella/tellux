"""
Tellux — conversion markdown vers PDF (WeasyPrint + DA v2 gelée).

Usage :
    python tools/pdf-builder/build_pdf.py <fichier.md> --output <fichier.pdf>

Les exports test sont attendus dans build/pdf-tests/ (gitignoré).
La conversion finale des documents publics a lieu apres relecture physicien tiers
(cf. ROADMAP.md section 8, Chantier 3).
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Windows: WeasyPrint depend des DLL GTK3 (Pango, GObject). On laisse le systeme
# les trouver si elles sont dans le PATH, sinon on tente les emplacements
# canoniques d'installation GTK3-Runtime (tschoonj). Cf. README.
if sys.platform == "win32":
    for candidate in (
        r"C:\Program Files\GTK3-Runtime Win64\bin",
        r"C:\Program Files (x86)\GTK3-Runtime Win64\bin",
    ):
        if os.path.isdir(candidate):
            os.add_dll_directory(candidate)
            break

import markdown
from weasyprint import HTML, CSS

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILDER_DIR = Path(__file__).resolve().parent
TEMPLATE_HTML = BUILDER_DIR / "templates" / "document.html"
DEFAULT_CSS = BUILDER_DIR / "da_v2.css"

MARKDOWN_EXTENSIONS = [
    "extra",
    "tables",
    "fenced_code",
    "sane_lists",
    "smarty",
    "toc",
    "codehilite",
    "pymdownx.tilde",
    "pymdownx.caret",
]

MARKDOWN_EXT_CONFIGS = {
    "codehilite": {"guess_lang": False, "css_class": "codehilite"},
    "toc": {"permalink": False},
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Erreur: fichier introuvable: {path}", file=sys.stderr)
        sys.exit(2)
    except UnicodeDecodeError as exc:
        print(f"Erreur d'encodage (attendu UTF-8): {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def derive_title(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def render_html(md_text: str, title: str, css_path: Path) -> str:
    md = markdown.Markdown(
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWN_EXT_CONFIGS,
        output_format="html5",
    )
    body_html = md.convert(md_text)

    template = TEMPLATE_HTML.read_text(encoding="utf-8")
    return (
        template
        .replace("{{ title }}", title)
        .replace("{{ css_path }}", css_path.as_posix())
        .replace("{{ content|safe }}", body_html)
    )


def build_pdf(source: Path, output: Path, css_path: Path, title: str | None) -> None:
    md_text = read_text(source)
    doc_title = title or derive_title(md_text, source.stem)

    html_str = render_html(md_text, doc_title, css_path)

    output.parent.mkdir(parents=True, exist_ok=True)

    html_doc = HTML(string=html_str, base_url=str(REPO_ROOT))
    html_doc.write_pdf(str(output), stylesheets=[CSS(filename=str(css_path))])

    print(f"OK  {source} -> {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convertit un markdown Tellux en PDF (DA v2).")
    parser.add_argument("source", type=Path, help="Fichier markdown source.")
    parser.add_argument(
        "--output", "-o", type=Path, required=True, help="Chemin du PDF de sortie."
    )
    parser.add_argument(
        "--css", type=Path, default=DEFAULT_CSS, help="CSS DA v2 (par defaut: tools/pdf-builder/da_v2.css)."
    )
    parser.add_argument(
        "--title", type=str, default=None, help="Titre du document (defaut: premier h1 du markdown)."
    )
    args = parser.parse_args()

    src = args.source.resolve()
    out = args.output.resolve()
    css = args.css.resolve()

    if not src.is_file():
        print(f"Erreur: source introuvable: {src}", file=sys.stderr)
        return 2
    if not css.is_file():
        print(f"Erreur: CSS introuvable: {css}", file=sys.stderr)
        return 2

    try:
        build_pdf(src, out, css, args.title)
    except Exception as exc:
        print(f"Erreur conversion: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
