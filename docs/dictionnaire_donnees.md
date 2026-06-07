# Dictionnaire des Données — Table Clients

**Auteur :** Emmanuel TSAGUE | Version 1.0

> Un dictionnaire des données (data dictionary) est le document de référence
> qui décrit chaque colonne d'une table : son nom, son type, sa signification,
> ses valeurs possibles et ses règles de validation.

---

| Colonne | Type SQL | Type Python | Obligatoire | Description | Valeurs / Format | Exemple valide | Exemple invalide |
|---------|---------|------------|------------|-------------|-----------------|---------------|-----------------|
| `id_client` | VARCHAR(10) | str | Oui | Identifiant unique du client | `C` + 3 chiffres | `C001` | `001`, `CLIENT1` |
| `nom` | VARCHAR(100) | str | Oui | Nom de famille | Texte libre | `DUPONT` | *(vide)* |
| `prenom` | VARCHAR(100) | str | Oui | Prénom | Texte libre | `Marie` | *(vide)* |
| `email` | VARCHAR(200) | str | Non | Adresse email de contact | format@domaine.ext | `marie.dupont@email.com` | `marie.dupont` |
| `date_naissance` | DATE | str (converti) | Oui | Date de naissance | DD/MM/YYYY | `15/03/1985` | `29/02/1993`, `1985/03/15` |
| `telephone` | VARCHAR(20) | str | Non | Numéro de téléphone français | 10 chiffres | `0612345678` | `06123`, `06 12 34 56 78` |
| `region` | VARCHAR(100) | str | Oui | Région administrative française | Liste fermée (13 régions) | `Ile-de-France` | `Paris`, `IDF` |
| `statut` | VARCHAR(20) | str | Oui | Statut du client | actif / inactif / suspendu | `actif` | `ACTIF`, `active`, `1` |
| `montant_contrat` | DECIMAL(10,2) | float | Oui | Montant du contrat en euros | 0.00 à 99 999.99 | `1250.00` | `-200`, `ABC`, `250000` |
| `date_inscription` | DATE | str (converti) | Oui | Date d'entrée en base de données | YYYY-MM-DD · ≤ aujourd'hui | `2022-01-15` | `2026-12-31` |
| `segment` | VARCHAR(10) | str | Oui | Segment de l'entreprise cliente | TPE / PME / ETI / GE | `PME` | `pme`, `Grande entreprise` |

---

## Notes de version

| Version | Date | Modification |
|---------|------|-------------|
| 1.0 | 2024 | Création initiale |

*Emmanuel TSAGUE — Data Scientist / Data Analyst — 2024*
