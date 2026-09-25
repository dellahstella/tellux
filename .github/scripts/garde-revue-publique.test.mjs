#!/usr/bin/env node
// Tests de non-régression pour garde-revue-publique.mjs — node:test (natif, aucune
// dépendance). Lancer : node --test .github/scripts/garde-revue-publique.test.mjs
//
// Portée : niveau unité (fonctions exportées), pas le pipeline git complet — le
// pipeline complet (6 rejeux contre des diffs réels + variantes) est rejoué
// manuellement à chaque revue et consigné dans la description de la PR #1522, pas
// encodé ici (dépend de SHA réels du dépôt, pas reproductible en isolation).
//
// Origine des 4 paires de ce fichier : revue Soleil du 2026-09-18 (PR #1522, point 1)
// — « le mot seul qui compte, c'est celui qui bascule un sens réglementaire ou
// scientifique », pas un état d'UI. Ce sont les cas qui justifient le garde-fou.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  jsStringTextFlags,
  htmlTextNodeFlag,
  visibleAttrFlag,
  domTextSinkFlags,
  lexiconTermFlags,
} from './garde-revue-publique.mjs';

const LOCKED_PAIRS = [
  ['potentiel', 'niveau'],
  ['seuil', 'niveau de référence'],
  ['majorant', 'estimation'],
  ['plafond', 'estimation'],
  ['nGy/h', 'nSv/h'],
];

function combinedJsFlags(line) {
  return [...jsStringTextFlags(line), ...lexiconTermFlags(line)];
}

test('termes verrouillés — sink JS structurel (.textContent=) : détecté sans le lexique déjà', () => {
  for (const [a, b] of LOCKED_PAIRS) {
    const before = jsStringTextFlags(`el.textContent='${a}';`);
    const after = jsStringTextFlags(`el.textContent='${b}';`);
    assert.notDeepEqual(before, after, `${a} -> ${b} via .textContent= aurait dû différer`);
  }
});

test('termes verrouillés — littéral JS nu hors sink : MANQUÉ par la détection heuristique seule (gap Q1 documenté)', () => {
  for (const [a, b] of LOCKED_PAIRS) {
    const before = jsStringTextFlags(`var LABEL = '${a}';`);
    const after = jsStringTextFlags(`var LABEL = '${b}';`);
    if (a === 'seuil') {
      // Seul cas où le remplacement (≥2 mots) est détecté par l'heuristique générale
      // elle-même, sans avoir besoin du lexique — asymétrie déjà relevée en revue.
      assert.notDeepEqual(before, after, `${a} -> ${b} : attendu détecté même sans lexique`);
    } else {
      assert.deepEqual(before, after, `${a} -> ${b} : attendu MANQUÉ par l'heuristique seule (before=${before}, after=${after})`);
    }
  }
});

test('termes verrouillés — littéral JS nu hors sink, AVEC le lexique : détecté dans les 5 cas', () => {
  for (const [a, b] of LOCKED_PAIRS) {
    const before = combinedJsFlags(`var LABEL = '${a}';`);
    const after = combinedJsFlags(`var LABEL = '${b}';`);
    assert.notDeepEqual(before, after, `${a} -> ${b} : le lexique aurait dû combler le manque`);
  }
});

test('termes verrouillés — balisage HTML statique (texte nu) : détecté, jamais de seuil de mots', () => {
  for (const [a, b] of LOCKED_PAIRS) {
    const before = htmlTextNodeFlag(`<div>${a}</div>`);
    const after = htmlTextNodeFlag(`<div>${b}</div>`);
    assert.notEqual(before, after, `${a} -> ${b} en texte HTML statique aurait dû différer`);
  }
});

test('termes verrouillés — attribut visible statique (title=) : détecté', () => {
  for (const [a, b] of LOCKED_PAIRS) {
    const before = visibleAttrFlag(`<span title="${a}">x</span>`);
    const after = visibleAttrFlag(`<span title="${b}">x</span>`);
    assert.notEqual(before, after, `${a} -> ${b} en attribut title= aurait dû différer`);
  }
});

test('lexique — faux positif identifiant connu (.seuil_legal_vm, app.html:14524) : exclu', () => {
  assert.deepEqual(lexiconTermFlags("var x = '.seuil_legal_vm';"), []);
});

test('lexique — terme isolé réel toujours détecté malgré le correctif ci-dessus', () => {
  assert.deepEqual(lexiconTermFlags('le seuil est dépassé'), ['seuil']);
});

test('domTextSinkFlags — setAttribute sur un attribut visible, un seul mot', () => {
  assert.deepEqual(domTextSinkFlags("el.setAttribute('title', 'indisponible');"), ['indisponible']);
});

test('domTextSinkFlags — setAttribute sur un attribut NON visible (href) : ignoré', () => {
  assert.deepEqual(domTextSinkFlags("el.setAttribute('href', 'indisponible');"), []);
});
