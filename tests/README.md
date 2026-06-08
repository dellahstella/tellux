# tests/

Fixtures et tests de non-régression pour le moteur de calcul Tellux.

Le sous-dossier `fixtures/` contient les jeux de valeurs de référence capturés sur l'application en production avant un changement structurant (extraction du moteur, refactoring, etc.). Chaque fixture est un instantané immuable d'un comportement attendu, à comparer avec la sortie post-changement pour détecter toute régression.

La méthodologie de capture et la stratégie de test post-extraction sont documentées en interne.
