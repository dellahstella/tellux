#!/usr/bin/env node
// Extract inline <script> blocks from HTML files and validate their syntax via `node --check`.
// Handlers inline (onclick, onload, etc.) are intentionally NOT validated in this v1.
// External scripts (<script src="...">) are skipped — they are CDN-hosted and not part of the repo.
//
// v2 (2026-07-03, post-incident geomagnetisme.html tronqué) :
//   - TARGETS dynamique via `git ls-files '*.html'` — toute page trackée est couverte,
//     une page nouvelle ne peut plus échapper au check par oubli de liste.
//   - Contrôle de fin de fichier : chaque page doit se terminer par </html>
//     (attrape les troncatures de fichier).
//   - Détection de bloc <script> inline non refermé (troncature en plein script :
//     la regex d'extraction l'ignorait silencieusement).

import { readFileSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';

const TARGETS = execFileSync('git', ['ls-files', '*.html'], { encoding: 'utf8' })
  .split('\n')
  .map(f => f.trim())
  .filter(Boolean);

// Capture inline <script> blocks (exclude those with src= attribute)
const INLINE_SCRIPT_RE = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;

const tmpRoot = mkdtempSync(join(tmpdir(), 'tellux-js-check-'));
let totalBlocks = 0;
let failures = 0;

for (const file of TARGETS) {
  let html;
  try {
    html = readFileSync(file, 'utf8');
  } catch (err) {
    console.error(`[SKIP] ${file} — not readable: ${err.message}`);
    continue;
  }

  // Contrôle troncature 1 : le fichier doit se terminer par </html>
  if (!html.trimEnd().toLowerCase().endsWith('</html>')) {
    failures += 1;
    console.error(`[FAIL] ${file} — ne se termine pas par </html> (fichier tronqué ?)`);
  }

  const matches = [...html.matchAll(INLINE_SCRIPT_RE)];

  // Contrôle troncature 2 : une ouverture <script> sans </script> (coupure en plein
  // script) échappe à la regex d'extraction. On retire les blocs complets capturés,
  // puis on cherche une ouverture résiduelle dans ce qui reste (hors corps de blocs,
  // pour ne pas faux-positiver sur la chaîne "<script" dans du JS).
  let residue = '';
  let cursor = 0;
  for (const m of matches) {
    residue += html.slice(cursor, m.index);
    cursor = m.index + m[0].length;
  }
  residue += html.slice(cursor);
  const orphan = residue.match(/<script(?![^>]*\bsrc=)[^>]*>/i);
  if (orphan) {
    failures += 1;
    const lineNum = residue.slice(0, orphan.index).split('\n').length;
    console.error(`[FAIL] ${file} — ouverture <script> sans </script> (résidu ~L${lineNum}) : bloc non refermé (fichier tronqué ?)`);
  }

  if (matches.length === 0) {
    console.log(`[OK]   ${file} — no inline <script> block`);
    continue;
  }

  matches.forEach((match, index) => {
    totalBlocks += 1;
    const body = match[1];
    // Count 1-based line where the <script> tag starts, for human-readable reporting
    const charOffset = match.index;
    const lineNum = html.slice(0, charOffset).split('\n').length;

    const tmpFile = join(tmpRoot, `${file.replace(/\W/g, '_')}__block${index + 1}.js`);
    writeFileSync(tmpFile, body, 'utf8');

    try {
      execFileSync('node', ['--check', tmpFile], { stdio: 'pipe' });
      console.log(`[OK]   ${file}:L${lineNum} — block ${index + 1}/${matches.length} syntax valid`);
    } catch (err) {
      failures += 1;
      const stderr = (err.stderr || '').toString().trim();
      console.error(`[FAIL] ${file}:L${lineNum} — block ${index + 1}/${matches.length} syntax error`);
      console.error(stderr.split('\n').map(l => `         ${l}`).join('\n'));
    }
  });
}

rmSync(tmpRoot, { recursive: true, force: true });

console.log(`\nSummary: ${totalBlocks} inline <script> block(s) checked, ${failures} failure(s).`);
process.exit(failures === 0 ? 0 : 1);
