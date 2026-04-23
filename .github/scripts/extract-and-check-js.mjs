#!/usr/bin/env node
// Extract inline <script> blocks from HTML files and validate their syntax via `node --check`.
// Handlers inline (onclick, onload, etc.) are intentionally NOT validated in this v1.
// External scripts (<script src="...">) are skipped — they are CDN-hosted and not part of the repo.

import { readFileSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';

const TARGETS = ['app.html', 'index.html', 'corpus.html', 'patrimoine.html', 'agronomie.html'];

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

  const matches = [...html.matchAll(INLINE_SCRIPT_RE)];
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
