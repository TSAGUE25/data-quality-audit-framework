# Schéma de référence — Table Clients

## Règles métier attendues

| Colonne | Type attendu | Format | Obligatoire | Règle métier |
|---------|-------------|--------|-------------|--------------|
| `id_client` | Texte | `C` + 3 chiffres (ex: C001) | Oui | Unique, pas de doublon |
| `nom` | Texte | Majuscules | Oui | Non vide |
| `prenom` | Texte | Première lettre majuscule | Oui | Non vide |
| `email` | Texte | format@domaine.ext | Non | Regex email valide si présent |
| `date_naissance` | Date | DD/MM/YYYY | Oui | Entre 1920 et aujourd'hui - 18 ans |
| `telephone` | Texte | 10 chiffres consécutifs | Non | 10 digits si présent |
| `region` | Texte | Région française officielle | Oui | Liste fermée de 13 régions |
| `statut` | Texte | Minuscules | Oui | Valeurs: actif, inactif, suspendu |
| `montant_contrat` | Décimal | Nombre positif | Oui | Entre 0 et 99 999 € |
| `date_inscription` | Date | YYYY-MM-DD | Oui | Passée (≤ aujourd'hui) |
| `segment` | Texte | Majuscules | Oui | Valeurs: TPE, PME, ETI, GE |

## Régions françaises valides

Auvergne-Rhône-Alpes, Bourgogne-Franche-Comté, Bretagne, Centre-Val de Loire,
Corse, Grand Est, Hauts-de-France, Ile-de-France, Normandie, Nouvelle-Aquitaine,
Occitanie, PACA, Pays de la Loire

## Problèmes de qualité intentionnellement présents dans clients_raw_sample.csv

| # | Type | Description | Lignes concernées |
|---|------|-------------|------------------|
| 1 | Doublon | C001 et C002 présents deux fois | 6 et 23 |
| 2 | Email invalide | Absence de @ | C003, C018 |
| 3 | Date format incorrect | YYYY/MM/DD au lieu de DD/MM/YYYY | C002 |
| 4 | Date impossible | 29/02/1993 (1993 non bissextile) | C006 |
| 5 | Date impossible | 31/04/1982 (avril = 30 jours) | C008 |
| 6 | Date impossible | 31/02/1993 | C023 |
| 7 | Valeur négative | montant_contrat = -200 | C004 |
| 8 | Type incorrect | montant_contrat = "ABC" | C009 |
| 9 | Valeur nulle email | email vide | C006, C016 |
| 10 | Valeur nulle téléphone | telephone vide | C007, C016 |
| 11 | Valeur nulle prénom | prenom vide | C008 |
| 12 | Valeur nulle montant | montant_contrat vide | C019 |
| 13 | Valeur nulle date_naissance | date_naissance vide | C010, C026 |
| 14 | Statut non conforme | "active", "ACTIF", "Actif", "Inactif", "INACTIF" | Multiples |
| 15 | Téléphone format court | 06123 (5 chiffres) | C012 |
| 16 | Date future inscription | 2026-12-31 (dans le futur) | C011 |
| 17 | Outlier montant | 250 000 € (hors plage normale) | C028 |

*Ce fichier est un exemple pédagogique — données fictives*
