# Data Quality Audit Framework

> Framework Python d'audit automatique de la qualité des données : détection des anomalies, score de qualité composite (0–100) et rapport Markdown auto-généré — pour fiabiliser un reporting métier avant publication.
> **Stack :** Python · pandas · matplotlib · regex

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![pandas](https://img.shields.io/badge/pandas-2.0%2B-green)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Portfolio](https://img.shields.io/badge/Portfolio-TSAGUE%20Emmanuel-purple)](https://github.com/TSAGUE25)

---

## Table des matières

1. [Contexte métier](#1-contexte-métier)
2. [Problème résolu](#2-problème-résolu)
3. [Données utilisées](#3-données-utilisées)
4. [Méthodes et outils](#4-méthodes-et-outils)
5. [Démarche analytique](#5-démarche-analytique)
6. [Métriques clés](#6-métriques-clés)
7. [Résultats obtenus](#7-résultats-obtenus)
8. [Valeur métier](#8-valeur-métier)
9. [Architecture du projet](#9-architecture-du-projet)
10. [Installation et usage](#10-installation-et-usage)
11. [Compétences démontrées](#11-compétences-démontrées)
12. [Limites et améliorations](#12-limites-et-améliorations)
13. [Contributors](#13-contributors)

---

## 1. Contexte métier

Dans toute organisation, les données transitent par de nombreux systèmes : CRM, ERP, fichiers Excel, formulaires, API. Chaque point de saisie ou de transfert est une source potentielle d'erreur.

**Symptôme typique :** lors d'une réunion de pilotage, deux responsables régionaux présentent des chiffres différents pour le même indicateur. L'écart vient de clients comptés en double, de statuts mal normalisés et de dates incohérentes. La crédibilité du reporting est remise en question.

Ce projet construit un **framework réutilisable d'audit qualité** qui détecte automatiquement et exhaustivement toutes les anomalies d'une base de données clients avant tout reporting ou analyse.

---

## 2. Problème résolu

> *"Comment détecter automatiquement toutes les anomalies de qualité dans notre base clients, les quantifier, les prioriser et produire un plan de correction — de façon reproductible à chaque mise à jour ?"*

Ce framework répond à 6 questions concrètes :
1. Combien de doublons contient notre base ?
2. Quelle proportion de clients a un email / téléphone valide ?
3. Nos dates contiennent-elles des valeurs impossibles ?
4. Nos montants ont-ils des valeurs aberrantes ou négatives ?
5. Les statuts sont-ils normalisés ("actif" vs "Actif" vs "ACTIF") ?
6. Peut-on publier ce reporting en confiance ?

| Objectif | Critère de réussite |
|---------|-------------------|
| Détecter et compter les doublons | Nombre exact de lignes dupliquées |
| Mesurer les valeurs manquantes | Taux par colonne, avec seuil d'alerte |
| Valider les formats (email, téléphone, date) | Liste des enregistrements non conformes |
| Contrôler les valeurs autorisées | Détection des statuts non normalisés |
| Détecter les outliers statistiques | Méthode IQR sur colonnes numériques |
| Calculer un score de qualité global (0–100) | Indicateur synthétique actionnable |

---

## 3. Données utilisées

> **Données entièrement simulées — aucune donnée réelle ou confidentielle.**

### `clients_raw_sample.csv` — 31 clients fictifs avec anomalies intentionnelles

| Colonne | Type attendu | Description |
|---------|-------------|-------------|
| `id_client` | Texte | Identifiant unique (ex : C001) |
| `email` | Texte | Adresse email |
| `date_naissance` | Date (DD/MM/YYYY) | Date de naissance |
| `telephone` | Texte | Numéro à 10 chiffres |
| `statut` | Texte | actif / inactif / suspendu |
| `montant_contrat` | Décimal | Montant en euros (≥ 0) |
| `date_inscription` | Date (YYYY-MM-DD) | Date d'entrée en base |
| `segment` | Texte | TPE / PME / ETI / GE |

### Anomalies présentes dans le dataset (à des fins de démonstration)

| Type d'anomalie | Nb cas |
|----------------|--------|
| Doublon complet | 2 paires |
| Email invalide | 2 |
| Date de naissance impossible | 3 |
| Valeur négative (montant) | 1 |
| Type incorrect (texte dans numérique) | 1 |
| Statut non normalisé (ACTIF / Actif / active) | 5 |
| Valeur manquante | 6 |
| Date future (inscription 2026) | 1 |
| Outlier statistique (250 000 €) | 1 |

---

## 4. Méthodes et outils

| Méthode | Description | Outil |
|--------|-------------|-------|
| **Taux de valeurs manquantes** | % de cases vides par colonne | pandas `.isnull()` |
| **Détection de doublons** | Lignes identiques ou clés dupliquées | pandas `.duplicated()` |
| **Validation de format** | Vérification par expression régulière (regex) | Python `re` |
| **Contrôle de type** | Vérification de la nature des données | `pd.to_numeric` |
| **Liste fermée** | Valeurs autorisées prédéfinies | pandas `.isin()` |
| **Outlier IQR** | Bornes Q1-1.5×IQR / Q3+1.5×IQR | numpy, quantiles |
| **Score de qualité** | Indicateur synthétique 0–100 | Calcul composite Python |
| **Rapport automatique** | Génération Markdown sans intervention | Python f-strings |

**Règle clé :** ne jamais modifier la donnée source. Toujours travailler sur une copie (`df.copy()`) — le fichier original reste intact pour traçabilité.

---

## 5. Démarche analytique

```
Données brutes (CSV)
        │
        ▼
Chargement sans transformation (lire les anomalies de type)
        │
        ▼
Profiling initial (shape, types, statistiques)
        │
        ▼
QualityChecker.run_full_audit()
  ├── check_missing_values()    → Taux par colonne
  ├── check_duplicates()        → Lignes et clés primaires
  ├── check_email_format()      → Regex validation
  ├── check_phone_format()      → 10 chiffres FR
  ├── check_date_format()       → DD/MM/YYYY
  ├── check_future_dates()      → Dates impossibles
  ├── check_allowed_values()    → Listes fermées
  ├── check_numeric_range()     → Min / Max
  └── check_outliers_iqr()      → Q1-1.5×IQR / Q3+1.5×IQR
        │
        ▼
compute_quality_score()  → Score 0–100
        │
        ▼
generate_markdown_report()  → Rapport + plan de correction
```

---

## 6. Métriques clés

| Métrique | Formule |
|---------|---------|
| Taux de valeurs manquantes | `Nb nuls / Nb total × 100` |
| Taux de doublons | `Nb doublons / Nb total × 100` |
| Taux de conformité format | `Nb valides / Nb présents × 100` |
| Borne outlier IQR sup. | `Q3 + 1.5 × (Q3 - Q1)` |
| **Score de qualité global** | Formule composite pondérée — 0=critique, 100=parfait |

**Grille d'interprétation du score :**

| Score | Statut | Décision |
|-------|--------|----------|
| 90–100 | Excellent | Données prêtes pour l'analyse |
| 75–89 | Bon | Corrections mineures avant publication |
| 60–74 | Passable | Corrections importantes nécessaires |
| 40–59 | Insuffisant | Ne pas publier ce reporting |
| 0–39 | Critique | Audit approfondi obligatoire |

---

## 7. Résultats obtenus

### Audit sur le dataset d'exemple

| Contrôle | Résultat | Statut |
|---------|---------|--------|
| Lignes totales | 31 | — |
| Doublons complets | 4 lignes (2 paires) | Critique |
| Valeurs manquantes | 8 cellules (2.3%) | Attention |
| Emails invalides | 2 / 29 présents | Attention |
| Dates de naissance invalides | 3 | Critique |
| Statuts non normalisés | 5 valeurs | Critique |
| Montants hors plage | 2 (négatif + >99 999) | Critique |
| Date inscription future | 1 | Critique |
| **Score de qualité initial** | **~58/100** | **Insuffisant** |

### Après corrections programmatiques

| Indicateur | Avant | Après |
|-----------|-------|-------|
| Doublons | 4 lignes | 0 |
| Statuts non conformes | 5 | 0 |
| **Score de qualité** | **58/100** | **~78/100** |

---

## 8. Valeur métier

| Valeur produite | Impact concret |
|----------------|----------------|
| **Détection avant publication** | Les erreurs sont trouvées avant le rapport, pas après |
| **Reproductibilité** | Le même script s'applique à chaque nouveau fichier livré |
| **Objectivité** | Le score est calculé, pas estimé à la main |
| **Traçabilité** | Le rapport documente exactement ce qui a été trouvé et quand |
| **Gain de temps** | Audit manuel : 2–3 jours → script automatique : 30 secondes |
| **Gouvernance** | Base pour définir un SLA de qualité des données |

---

## 9. Architecture du projet

```
data-quality-audit-framework/
│
├── data_sample/
│   ├── clients_raw_sample.csv        # CSV avec anomalies intentionnelles
│   └── schema_reference.md          # Schéma attendu et règles métier
│
├── notebooks/
│   └── 01_data_quality_audit.py     # Script principal — audit complet
│
├── src/
│   ├── __init__.py
│   ├── quality_checker.py           # Classe QualityChecker (9 méthodes)
│   └── report_generator.py         # Génération rapport Markdown
│
├── reports/
│   └── quality_report_sample.md    # Exemple de rapport produit
│
├── figures/
│   ├── fig1_missing_values.png
│   ├── fig2_quality_dimensions.png
│   ├── fig3_montant_distribution.png
│   └── fig4_anomalies_impact.png
│
├── docs/
│   ├── dictionnaire_donnees.md
│   ├── regles_metier.md
│   └── guide_utilisateur.md
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 10. Installation et usage

```bash
git clone https://github.com/TSAGUE25/data-quality-audit-framework
cd data-quality-audit-framework
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python notebooks/01_data_quality_audit.py
```

**Utilisation directe :**

```python
from src.quality_checker import QualityChecker
import pandas as pd

df      = pd.read_csv("data_sample/clients_raw_sample.csv")
checker = QualityChecker(df=df, dataset_name="Clients_2024")

resultats = checker.run_full_audit(
    key_col="id_client",
    email_col="email",
    phone_col="telephone",
    date_cols=["date_naissance"],
    date_inscription_col="date_inscription",
    allowed_values_rules={
        "statut": ["actif", "inactif", "suspendu"],
        "segment": ["TPE", "PME", "ETI", "GE"]
    },
    numeric_range_rules={"montant_contrat": (0, 99999)},
    outlier_cols=["montant_contrat"]
)

checker.print_anomaly_report()
print(f"Score qualité : {checker.quality_score}/100")
```

**Sorties produites :**
- `reports/quality_report_sample.md` — rapport Markdown avec toutes les anomalies listées
- `figures/` — 4 visualisations analytiques (valeurs manquantes, dimensions qualité, outliers...)

---

## 11. Compétences démontrées

| Compétence | Mise en œuvre | Fichier |
|-----------|--------------|---------|
| **Python OOP** | Classe `QualityChecker` avec 9 méthodes paramétrables | `src/quality_checker.py` |
| **pandas** | `.isnull()`, `.duplicated()`, `.apply()`, `pd.to_numeric()` | `src/quality_checker.py` |
| **Regex** | Validation email (RFC), téléphone (10 chiffres FR), dates | `src/quality_checker.py` |
| **Outlier IQR** | Bornes dynamiques calculées par colonne | `src/quality_checker.py` |
| **Score composite** | Pondération de 9 dimensions qualité → note 0–100 | `src/quality_checker.py` |
| **Rapport automatisé** | Markdown généré sans intervention manuelle | `src/report_generator.py` |
| **Visualisation** | 4 figures analytiques (barres, boxplot, camembert) | `notebooks/` |
| **Gouvernance** | Plan de correction priorisé, dictionnaire, règles métier | `docs/` |

**Stack technique :** `pandas` · `numpy` · `matplotlib` · `re` (expressions régulières)

---

## 12. Limites et améliorations

**Limites actuelles :**

| Limite | Impact |
|--------|--------|
| Pas de correction automatique | Le script détecte, mais ne corrige pas seul |
| Règles codées en dur | Doivent être mises à jour manuellement |
| Dataset d'exemple petit (31 lignes) | À tester sur de vrais volumes |
| Pas d'interface graphique | Nécessite Python |

**Pistes d'amélioration :**
- **Interface Streamlit** : upload CSV, audit en 1 clic, rapport téléchargeable
- **Connexion SQL** : audit directement sur une base PostgreSQL / BigQuery
- **Règles en YAML** : règles métier modifiables sans toucher au code
- **GitHub Actions** : audit automatique à chaque push de nouvelles données
- **Great Expectations** : framework professionnel de validation déclarative

---

## 13. Contributors

| Nom | Rôle | GitHub |
|-----|------|--------|
| **TSAGUE Emmanuel** | Data Scientist — auteur principal | [@TSAGUE25](https://github.com/TSAGUE25) |

---

*Auteur : Emmanuel TSAGUE — Data Scientist / Data Analyst*
*Formation : DataScientest | Domaines : DataOps · Finance · Commerce · Énergie*
*Contact : emmatsague@yahoo.fr*
*Données : entièrement simulées — aucune donnée réelle ou confidentielle*
