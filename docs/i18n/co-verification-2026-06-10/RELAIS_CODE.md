# Relais Code — câblage repo de la passe vérification i18n CO

> Cowork ne commet pas (doctrine FUSE). Ce brief liste ce que Code doit faire pour
> livrer la passe : **branche dédiée + PR vers `dev`, PAS d'auto-merge.**
> Cowork n'a PAS édité `app.html` directement (fichier volumineux + bug de troncature
> Cowork constaté cette session) : le seul changement applicatif — le bandeau bêta —
> est fourni ci-dessous comme patch exact à appliquer côté Code.

## 0. État

- Branche de travail Cowork : aucune (working tree `main`, lecture/écriture fichiers docs + scripts).
- **Aucune correction de valeur CO** appliquée dans `app.html` : la vérification a trouvé le
  corse largement attesté ; les items flaggés sont des néologismes/termes techniques ou faux-sens
  **sans remplacement attesté en base** → conservés tels quels et flaggés (doctrine : ne pas inventer).
- **FR intact** : contrôle automatique OK (clés + colonne FR identiques à `HEAD:app.html`).

## 1. Fichiers produits par Cowork (à committer)

```
docs/i18n/REVUE_FR_CO_app.md                      (régénéré : table 6 colonnes + STATUT/SOURCE)
docs/i18n/verification_co.tokens.json             (données de vérif : formes -> id INFCOR + flags)
docs/i18n/verification_co.tsv                      (sidecar par chaîne)
docs/i18n/FLAGGED_CO_NATIF.md                      (liste flaggée pour le natif)
docs/i18n/NOTE_METHODE_CO.md                       (note méthode dossier)
docs/i18n/co-verification-2026-06-10/contrat.md    (contrat d'itération — pour l'évaluateur)
docs/i18n/co-verification-2026-06-10/RELAIS_CODE.md (ce fichier)
docs/i18n/co-verification-2026-06-10/infcor_cache.md (journal brut des requêtes INFCOR — traçabilité)
scripts/verify_i18n_co.mjs                          (nouveau : calcule le sidecar TSV)
scripts/export_i18n_co_table.mjs                    (étendu : fusionne STATUT/SOURCE dans la table)
```

Régénération (idempotente, à relancer après le patch bandeau) :

```bash
node scripts/verify_i18n_co.mjs        # recalcule docs/i18n/verification_co.tsv
node scripts/export_i18n_co_table.mjs  # réinjecte la table 6 colonnes dans REVUE_FR_CO_app.md
```

## 2. Patch bandeau bêta (seul changement `app.html`)

Insérer le bloc suivant **dans l'IIFE i18n**, juste **avant** la ligne de fermeture `})();`
(actuellement à la fin du `<script>` i18n, après le `console.log/console.warn` — repère :
ligne `})();` qui suit `window.__telluxI18n = …`). Étant dans l'IIFE, le bandeau ne s'affiche
que sous `?lang=co` (retour anticipé si `lang !== 'co'` en tête d'IIFE). Texte en **français**
(doctrine : pas de texte CO non vérifié contre source). Aucune dépendance externe. Aucun
guillemet courbe.

```js
  // --- Bandeau bêta CO (passe vérification 2026-06-10) — texte FR (non vérifié en CO) ---
  try {
    var coBanner = document.createElement('div');
    coBanner.id = 'co-beta-banner';
    coBanner.setAttribute('role', 'note');
    coBanner.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:9999;' +
      'background:var(--tx-ardoise,#22262B);color:var(--tx-pierre,#F4EFE6);' +
      'font:500 12px/1.45 system-ui,sans-serif;padding:8px 38px 8px 14px;text-align:center;' +
      'box-shadow:0 -1px 6px rgba(0,0,0,.25)';
    coBanner.appendChild(document.createTextNode(
      'Version corse (beta) — traduction automatique en cours de verification, '
      + 'non validee par un locuteur natif. La version francaise fait foi.'));
    var coBannerX = document.createElement('button');
    coBannerX.type = 'button';
    coBannerX.setAttribute('aria-label', 'Fermer');
    coBannerX.textContent = '✕';
    coBannerX.style.cssText = 'position:absolute;right:8px;top:50%;transform:translateY(-50%);' +
      'background:none;border:none;color:inherit;font-size:14px;line-height:1;cursor:pointer';
    coBannerX.onclick = function () { coBanner.remove(); };
    coBanner.appendChild(coBannerX);
    (document.body || document.documentElement).appendChild(coBanner);
  } catch (_eBanner) {}
```

> NB texte : volontairement écrit en clair FR sans accents dans les littéraux JS par prudence
> d'encodage (le reste du fichier accepte les accents ; Code peut réintroduire les accents
> « bêta / vérification / validée / française » s'il préfère — au choix, FR uniquement, jamais
> de guillemets courbes ' ').

## 3. i18n-co-check à repasser côté Code (le brief l'exige)

1. **FR intact** : `git diff HEAD -- app.html` ne doit montrer QUE l'ajout du bandeau (aucune
   modification d'une 4e valeur de tuple `I18N_ENTRIES`, aucune modif FR).
2. **307/307 appliquées** : ouvrir `app.html?lang=co`, vérifier en console
   `window.__telluxI18n.applied === 307` et `window.__telluxI18n.skipped.length === 0`.
3. **0 erreur console** : zéro rouge au boot et après interaction ; le bandeau s'affiche sous
   `?lang=co` et se ferme via la croix ; il **n'apparaît pas** sans `?lang=co`.
4. **Pas de régression** : `?lang=co` absent → app strictement identique à aujourd'hui.

## 4. Livraison

- Branche : `feat/i18n-co-verification` (depuis `dev`).
- PR vers `dev`, **pas d'auto-merge** — arbitrage Soleil.
- Message suggéré : `i18n(co): passe de vérification lexicale INFCOR (256 formes attestées-direct + 111 flexions ; 141 chaînes vérifiées + 76 vérifiées-flexion, 89 flaggées, 1 à confirmer) + bandeau bêta FR + outillage rejouable`.
