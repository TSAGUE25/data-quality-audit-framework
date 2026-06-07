# Règles Métier — Data Quality Audit Framework

**Auteur :** Emmanuel TSAGUE  
**Version :** 1.0

> Ce fichier définit les règles métier utilisées dans l'audit qualité.
> Dans un projet réel, ce fichier serait validé et maintenu par le Data Steward
> (responsable qualité des données) en collaboration avec les équipes métier.

---

## Table clients

| Colonne | Règle | Type de contrôle | Gravité si violation |
|---------|-------|-----------------|---------------------|
| `id_client` | Format `C` + 3 chiffres · Unique | Format + Unicité | CRITIQUE |
| `nom` | Non vide · Texte uniquement | Complétude + Type | ÉLEVÉ |
| `prenom` | Non vide | Complétude | ÉLEVÉ |
| `email` | Format RFC 5322 simplifié (`x@y.z`) | Format | MOYEN |
| `date_naissance` | Format DD/MM/YYYY · Date valide · Âge 18–120 ans | Format + Plage | ÉLEVÉ |
| `telephone` | 10 chiffres · Commence par 0[1-9] | Format | FAIBLE |
| `region` | Liste fermée : 13 régions françaises officielles | Liste fermée | ÉLEVÉ |
| `statut` | Liste fermée : actif / inactif / suspendu (minuscules) | Liste fermée + Format | ÉLEVÉ |
| `montant_contrat` | Numérique · 0 ≤ valeur ≤ 99 999 | Type + Plage | CRITIQUE |
| `date_inscription` | Format YYYY-MM-DD · Date ≤ aujourd'hui | Format + Cohérence | ÉLEVÉ |
| `segment` | Liste fermée : TPE / PME / ETI / GE (majuscules) | Liste fermée + Format | MOYEN |

---

## Régions françaises valides (13 régions métropolitaines)

```python
REGIONS_VALIDES = [
    "Auvergne-Rhône-Alpes",
    "Bourgogne-Franche-Comté",
    "Bretagne",
    "Centre-Val de Loire",
    "Corse",
    "Grand Est",
    "Hauts-de-France",
    "Ile-de-France",
    "Normandie",
    "Nouvelle-Aquitaine",
    "Occitanie",
    "PACA",
    "Pays de la Loire"
]
```

---

## Statuts clients valides

```python
STATUTS_VALIDES = ["actif", "inactif", "suspendu"]
# Note : toujours comparer en minuscules après normalisation
```

## Segments valides

```python
SEGMENTS_VALIDES = ["TPE", "PME", "ETI", "GE"]
# TPE = Très Petite Entreprise (< 10 salariés)
# PME = Petite et Moyenne Entreprise (10–249 salariés)
# ETI = Entreprise de Taille Intermédiaire (250–4999 salariés)
# GE  = Grande Entreprise (5000+ salariés)
```

---

## Seuils d'alerte du score qualité

| Score | Action requise |
|-------|---------------|
| ≥ 90 | Publication autorisée |
| 75–89 | Publication avec réserves documentées |
| 60–74 | Corrections obligatoires avant publication |
| < 60 | Publication bloquée — audit approfondi |

---

*Emmanuel TSAGUE — Data Scientist / Data Analyst — 2024*
