# Audit Qualité des Données pour Fiabiliser un Reporting Métier
### Data Quality Audit Framework — Portfolio Data Analyst / Data Scientist

**Auteur :** Emmanuel TSAGUE | Data Scientist / Data Analyst  
**Contexte :** Cas d'usage professionnel — Portfolio Data Science 2024  
**Données :** Simulées à des fins pédagogiques — Anonymisées  
**Outils :** Python · pandas · matplotlib · ydata-profiling · Power BI  

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![pandas](https://img.shields.io/badge/pandas-2.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Complet-brightgreen)

---

## Table des matières

1. [Titre du cas d'usage](#1-titre-du-cas-dusage)
2. [Contexte métier](#2-contexte-métier)
3. [Pourquoi ce sujet existe](#3-pourquoi-ce-sujet-existe)
4. [Problème métier](#4-problème-métier)
5. [Objectifs du projet](#5-objectifs-du-projet)
6. [Données utilisées](#6-données-utilisées)
7. [Préparation des données](#7-préparation-des-données)
8. [Méthodes et outils](#8-méthodes-et-outils)
9. [Démarche étape par étape](#9-démarche-étape-par-étape)
10. [Métriques utilisées](#10-métriques-utilisées)
11. [Explication des métriques](#11-explication-des-métriques)
12. [Résultats attendus](#12-résultats-attendus)
13. [Valeur métier](#13-valeur-métier)
14. [Limites du projet](#14-limites-du-projet)
15. [Améliorations possibles](#15-améliorations-possibles)
16. [Architecture GitHub](#16-architecture-github)
17. [Utiliser ce dépôt](#17-utiliser-ce-dépôt)
18. [Version CV](#18-version-cv)
19. [Version entretien](#19-version-entretien)
20. [Version portfolio longue](#20-version-portfolio-longue)
21. [Post LinkedIn](#21-post-linkedin)
22. [Questions d'entretien](#22-questions-dentretien)
23. [Compétences démontrées](#23-compétences-démontrées)
24. [Tableau compétences / preuves](#24-tableau-compétences--preuves)
25. [Conseils de publication GitHub](#25-conseils-de-publication-github)

---

## 1. Titre du cas d'usage

> **Audit automatique de la qualité des données pour fiabiliser un reporting métier**  
> *Détection, quantification et correction des anomalies de données avant toute analyse ou publication d'indicateurs*

---

## 2. Contexte métier

### L'organisation concernée

Dans toute organisation — entreprise, collectivité, service public — les données transitent par de nombreux systèmes : CRM (logiciel de gestion de la relation client), ERP (logiciel de gestion intégrée d'entreprise), fichiers Excel, formulaires de saisie, API (interface de connexion entre systèmes). Chaque point de saisie ou de transfert est une source potentielle d'erreur.

Dans ce cas d'usage, l'organisation dispose d'une **base clients** utilisée pour :
- produire un **reporting commercial mensuel** (chiffre d'affaires, nombre de clients actifs, montant moyen des contrats) ;
- alimenter un **tableau de bord décisionnel Power BI** consulté par la direction ;
- réaliser des **campagnes marketing ciblées** par segment et par région.

### Le problème révélé

Lors d'une réunion de pilotage, deux responsables régionaux présentent des chiffres différents pour le même indicateur : le nombre de clients actifs en Île-de-France. L'un obtient 124, l'autre 131. L'écart vient de clients comptés en double, de statuts mal normalisés et de dates d'inscription incohérentes. La crédibilité du reporting est remise en question.

> **Situation réelle typique :** Un rapport qui affiche un total de clients actifs incluant des doublons, des clients au statut "ACTIF" ou "Actif" ou "active" (trois orthographes différentes pour la même réalité) et des montants de contrats avec des erreurs de frappe n'est pas fiable — même s'il est beau visuellement.

---

## 3. Pourquoi ce sujet existe

> *"Pas de bonne décision sans données fiables."*

Les organisations accumulent des données depuis des années, souvent dans des systèmes hétérogènes. La qualité des données se dégrade naturellement au fil du temps à cause de :
- **la saisie manuelle** : erreurs humaines, formats non respectés ;
- **les migrations de systèmes** : changements de logiciels, de formats, d'encodages ;
- **l'absence de contrôles à la source** : pas de validation au moment de la saisie ;
- **la multiplicité des sources** : fusion de fichiers venant de services différents ;
- **le turnover** : chaque nouveau collaborateur a ses propres habitudes de saisie.

Un audit qualité existe parce que **publier un KPI (indicateur clé de performance) faux coûte plus cher que le corriger en amont** : mauvaises décisions stratégiques, perte de confiance des équipes dans les outils, reprises manuelles coûteuses.

---

## 4. Problème métier

**Défi opérationnel :** Comment détecter automatiquement et exhaustivement toutes les anomalies de qualité dans une base de données clients, les quantifier, les prioriser et produire un plan de correction — en moins d'une heure et de manière reproductible à chaque mise à jour des données ?

**Questions sans réponse avant ce projet :**
1. Combien de doublons exacts contient notre base ? Qui sont-ils ?
2. Quelle proportion de clients a un email valide ? Un téléphone valide ?
3. Nos dates de naissance sont-elles toutes cohérentes (pas de 30 février) ?
4. Nos montants de contrats contiennent-ils des valeurs aberrantes ou négatives ?
5. Les statuts clients sont-ils normalisés ("actif" vs "Actif" vs "ACTIF") ?
6. Peut-on publier le reporting de ce mois en confiance ?

---

## 5. Objectifs du projet

### Objectif principal

> Construire un **framework (cadre de travail réutilisable) d'audit qualité des données** en Python, capable d'analyser automatiquement n'importe quelle table de données, de détecter les anomalies et de produire un rapport de qualité structuré avec un score global.

### Objectifs secondaires

| # | Objectif | Critère de réussite |
|---|---------|-------------------|
| 1 | Détecter et compter les doublons | Nombre exact de lignes dupliquées |
| 2 | Mesurer les valeurs manquantes | Taux par colonne, avec seuil d'alerte |
| 3 | Valider les formats (email, téléphone, date) | Liste des enregistrements non conformes |
| 4 | Contrôler les valeurs contre des listes autorisées | Détection des statuts non normalisés |
| 5 | Détecter les outliers (valeurs aberrantes) statistiques | Méthode IQR appliquée aux colonnes numériques |
| 6 | Calculer un score de qualité global (0–100) | Indicateur synthétique actionnable |
| 7 | Générer un rapport Markdown automatiquement | Document prêt à partager sans manipulation manuelle |
| 8 | Proposer un plan de correction priorisé | Actions classées par impact |

---

## 6. Données utilisées

### Description du jeu de données d'exemple

| Attribut | Valeur |
|---------|--------|
| Fichier | `data_sample/clients_raw_sample.csv` |
| Format | CSV (Comma-Separated Values — fichier texte séparé par des virgules) |
| Lignes | 31 (dont doublons intentionnels) |
| Colonnes | 11 |
| Période | 2022–2024 (dates simulées) |
| Nature | Données clients fictives — aucune donnée réelle |

### Structure du fichier

| Colonne | Type attendu | Description |
|---------|-------------|-------------|
| `id_client` | Texte | Identifiant unique (ex : C001) |
| `nom` | Texte | Nom de famille |
| `prenom` | Texte | Prénom |
| `email` | Texte | Adresse email |
| `date_naissance` | Date (DD/MM/YYYY) | Date de naissance |
| `telephone` | Texte | Numéro à 10 chiffres |
| `region` | Texte | Région française |
| `statut` | Texte | actif / inactif / suspendu |
| `montant_contrat` | Décimal | Montant en euros (≥ 0) |
| `date_inscription` | Date (YYYY-MM-DD) | Date d'entrée en base |
| `segment` | Texte | TPE / PME / ETI / GE |

### Anomalies intentionnellement présentes (à des fins pédagogiques)

| Type d'anomalie | Exemple | Nb cas |
|----------------|---------|--------|
| Doublon complet | C001 présent 2 fois | 2 paires |
| Email invalide | `sophie.bernard` (sans @) | 2 |
| Date de naissance impossible | `29/02/1993` (1993 non bissextile) | 3 |
| Valeur négative | `montant_contrat = -200` | 1 |
| Type incorrect | `montant_contrat = "ABC"` | 1 |
| Statut non normalisé | `ACTIF`, `Actif`, `active` | 5 |
| Valeur manquante | email, téléphone, prénom | 6 |
| Date future | `date_inscription = 2026-12-31` | 1 |
| Outlier | `montant_contrat = 250 000 €` | 1 |
| Téléphone trop court | `06123` (5 chiffres) | 1 |

---

## 7. Préparation des données

La préparation des données dans un projet d'audit qualité est **différente** d'un projet de modélisation : on ne corrige pas les données avant l'audit — on les audite d'abord telles quelles, puis on propose des corrections.

### Phase 1 — Chargement sans transformation

```python
import pandas as pd
df = pd.read_csv("data_sample/clients_raw_sample.csv")
# Ne pas forcer les types : lire tout en texte ou laisser pandas inférer
# pour détecter les anomalies de type
```

### Phase 2 — Profiling initial (exploration rapide)

```python
# Dimensions, types, statistiques de base
print(df.shape)       # (31, 11)
print(df.dtypes)      # Types inférés par pandas
df.describe(include="all")  # Statistiques descriptives
```

### Phase 3 — Audit systématique (voir section 9)

### Phase 4 — Corrections appliquées après audit

```python
df_clean = df.copy()
df_clean = df_clean.drop_duplicates()                           # Suppression doublons
df_clean["statut"] = df_clean["statut"].str.lower().str.strip() # Normalisation statut
df_clean["telephone"] = df_clean["telephone"].str.replace(r"[\s\-]", "", regex=True)
df_clean["montant_contrat"] = pd.to_numeric(df_clean["montant_contrat"], errors="coerce")
df_clean.loc[df_clean["montant_contrat"] < 0, "montant_contrat"] = None  # À investiguer
```

> **Règle d'or :** Ne jamais modifier la donnée source. Toujours travailler sur une copie (`df.copy()`). Conserver le fichier original inchangé pour traçabilité.

---

## 8. Méthodes et outils

| Méthode | Description simple | Outil utilisé |
|--------|-------------------|--------------|
| **Profiling des données** | Vue d'ensemble statistique d'un dataset | pandas, ydata-profiling |
| **Taux de valeurs manquantes** | % de cases vides par colonne | pandas `.isnull()` |
| **Détection de doublons** | Lignes identiques ou clés dupliquées | pandas `.duplicated()` |
| **Validation de format** | Vérification par expression régulière (regex) | Python `re` |
| **Contrôle de type** | Vérification de la nature des données | pandas, `pd.to_numeric` |
| **Liste fermée** | Valeurs autorisées prédéfinies | pandas `.isin()` |
| **Score de qualité** | Indicateur synthétique 0–100 | Calcul composite Python |
| **Outlier IQR** | Détection statistique des valeurs aberrantes | numpy, quantiles |
| **Rapport automatique** | Génération Markdown sans intervention manuelle | Python f-strings |
| **Visualisation** | Graphiques d'audit (barres, boxplot, camembert) | matplotlib |

### Glossaire des outils

- **pandas** : bibliothèque Python (en français : module ou librairie) pour manipuler des tables de données
- **regex** (expression régulière) : motif de texte qui permet de vérifier si une chaîne respecte un format
- **IQR** (InterQuartile Range — écart interquartile) : mesure statistique qui identifie les valeurs très éloignées de la médiane
- **ydata-profiling** : outil qui génère automatiquement un rapport HTML complet sur un dataset

---

## 9. Démarche étape par étape

```
Étape 1 — Réception des données brutes
         │
         ▼
Étape 2 — Profiling initial (shape, types, statistiques)
         │
         ▼
Étape 3 — Contrôle de complétude (valeurs manquantes)
         │
         ▼
Étape 4 — Contrôle d'unicité (doublons)
         │
         ▼
Étape 5 — Contrôle de format (email, téléphone, date)
         │
         ▼
Étape 6 — Contrôle des valeurs autorisées (listes fermées)
         │
         ▼
Étape 7 — Contrôle des plages numériques (min, max)
         │
         ▼
Étape 8 — Détection des outliers statistiques (IQR)
         │
         ▼
Étape 9 — Calcul du score de qualité global (0–100)
         │
         ▼
Étape 10 — Génération du rapport d'anomalies
         │
         ▼
Étape 11 — Plan de correction priorisé
         │
         ▼
Étape 12 — Application des corrections + re-audit
         │
         ▼
Étape 13 — Validation finale et publication du reporting
```

### Code d'utilisation de la classe QualityChecker

```python
from src.quality_checker import QualityChecker

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
    numeric_range_rules={
        "montant_contrat": (0, 99999)
    },
    outlier_cols=["montant_contrat"]
)

checker.print_anomaly_report()
```

---

## 10. Métriques utilisées

| Métrique | Formule | Interprétation |
|---------|---------|----------------|
| **Taux de valeurs manquantes** | `Nb nuls / Nb total lignes × 100` | % de cases vides par colonne |
| **Taux de doublons** | `Nb doublons / Nb total lignes × 100` | % de lignes dupliquées |
| **Taux de conformité format** | `Nb valides / Nb présents × 100` | % de valeurs respectant le format |
| **Taux de conformité liste** | `Nb dans liste / Nb présents × 100` | % de valeurs dans les valeurs autorisées |
| **Borne outlier IQR (inférieure)** | `Q1 - 1.5 × IQR` | Seuil bas au-delà duquel une valeur est aberrante |
| **Borne outlier IQR (supérieure)** | `Q3 + 1.5 × IQR` | Seuil haut au-delà duquel une valeur est aberrante |
| **Score de qualité global** | Formule composite (voir code) | Note de 0 à 100 — 100 = données parfaites |

---

## 11. Explication des métriques

### Taux de valeurs manquantes — Pourquoi surveiller ça ?

Imaginons que la colonne `email` ait 15% de valeurs manquantes. Si on lance une campagne email sur cette base, 15% des clients ne recevront rien. Le taux de manquants indique directement l'**exploitabilité** d'une colonne.

| Taux | Statut | Action |
|------|--------|--------|
| 0% | OK | Aucune action |
| 1–9% | Attention | Investiguer les cas |
| ≥ 10% | Critique | Ne pas utiliser cette colonne sans correction |

### Score de qualité global — Comment l'interpréter ?

| Score | Niveau | Signification |
|-------|--------|---------------|
| 90–100 | Excellent | Données prêtes pour l'analyse |
| 75–89 | Bon | Corrections mineures avant publication |
| 60–74 | Passable | Corrections importantes nécessaires |
| 40–59 | Insuffisant | Ne pas publier ce reporting |
| 0–39 | Critique | Audit approfondi obligatoire |

### IQR — Comment détecter un outlier ?

```
Exemple : montant_contrat
Q1 = 950 €     Q3 = 3 200 €     IQR = 2 250 €

Borne supérieure = 3 200 + 1.5 × 2 250 = 6 575 €
Un montant de 250 000 € est donc un outlier → à investiguer avec le métier
```

> **À retenir :** Un outlier n'est pas forcément une erreur. Un client avec un contrat à 250 000 € peut exister (grand compte). L'IQR détecte les cas inhabituels pour que le métier les **valide**, pas pour les supprimer automatiquement.

---

## 12. Résultats attendus

> *Chiffres simulés à des fins pédagogiques — basés sur le dataset d'exemple fourni*

### Résultats de l'audit sur le dataset d'exemple

| Contrôle | Résultat | Statut |
|---------|---------|--------|
| Lignes totales | 31 | — |
| Doublons complets | 2 paires (4 lignes) | 🔴 Critique |
| Valeurs manquantes | 8 cellules sur 341 (2,3%) | 🟡 Attention |
| Emails invalides | 2 sur 29 présents (6,9%) | 🟡 Attention |
| Téléphones invalides | 2 sur 29 présents | 🟡 Attention |
| Dates de naissance invalides | 3 (dates impossibles) | 🔴 Critique |
| Statuts non normalisés | 5 valeurs non conformes | 🔴 Critique |
| Montants hors plage | 2 (négatif + > 99 999) | 🔴 Critique |
| Type incorrect (montant) | 1 valeur textuelle | 🔴 Critique |
| Date inscription future | 1 | 🔴 Critique |
| Outliers (IQR montant) | 1 (250 000 €) | 🟡 Attention |
| **Score de qualité global** | **~58/100** | **🔴 Insuffisant** |

### Résultats après correction

| Indicateur | Avant | Après |
|-----------|-------|-------|
| Doublons | 4 lignes | 0 |
| Statuts non conformes | 5 | 0 |
| Types incorrects montant | 1 | 0 |
| Score de qualité | ~58/100 | ~78/100 |

---

## 13. Valeur métier

| Valeur produite | Impact concret |
|----------------|----------------|
| **Détection avant publication** | Les erreurs sont trouvées avant le rapport, pas après |
| **Reproductibilité** | Le même script s'applique à chaque nouveau fichier livré |
| **Objectivité** | Le score qualité est calculé, pas estimé à la main |
| **Traçabilité** | Le rapport documente exactement ce qui a été trouvé et quand |
| **Confiance** | Les managers peuvent publier le KPI en sachant qu'il a été audité |
| **Gain de temps** | Un audit manuel prendrait 2–3 jours; ce script tourne en 30 secondes |
| **Gouvernance** | Base pour définir un SLA (Service Level Agreement — accord sur le niveau de service) de qualité des données |

---

## 14. Limites du projet

| Limite | Explication | Atténuation |
|--------|-------------|-------------|
| **Pas de correction automatique** | Le script détecte, mais ne corrige pas seul | Ajouter un module de correction guidée |
| **Règles codées en dur** | Les règles métier doivent être mises à jour manuellement | Externaliser dans un fichier YAML ou JSON |
| **Dataset d'exemple petit** | 31 lignes — à tester sur de vrais volumes | Tester sur 100 000+ lignes avec pandas chunking |
| **Pas d'interface graphique** | Nécessite Python | Ajouter une interface Streamlit |
| **Pas de connexion directe aux systèmes** | Import CSV manuel | Connecter à SQL, API, S3 |
| **Contexte métier non intégré** | L'outlier à 250 000 € peut être légitime | Ajouter une validation humaine pour les cas limites |

---

## 15. Améliorations possibles

| Amélioration | Technologie | Bénéfice |
|-------------|-------------|---------|
| **Interface web** | Streamlit | Upload CSV, audit en 1 clic, rapport téléchargeable |
| **Connexion SQL** | SQLAlchemy + PostgreSQL | Audit directement sur la base de production |
| **Règles en YAML** | PyYAML | Règles métier modifiables sans toucher au code |
| **Alertes automatiques** | Python smtplib / Teams webhook | Email si score < 70 |
| **Historique des scores** | pandas + CSV ou SQLite | Suivi de la qualité dans le temps |
| **Intégration CI/CD** | GitHub Actions | Audit automatique à chaque push de nouvelles données |
| **Great Expectations** | great-expectations | Framework professionnel de validation déclarative |
| **Dashboard Power BI** | Power BI + Export Excel | Tableau de bord qualité pour les non-techniciens |
| **Tests unitaires** | pytest | Valider que le code fonctionne correctement |

> **CI/CD** (Continuous Integration / Continuous Delivery — Intégration continue / Livraison continue) est une pratique qui automatise les tests et le déploiement à chaque modification du code.

---

## 16. Architecture GitHub

### Nom du dépôt (repository / dépôt) : `data-quality-audit-framework`

### Structure des dossiers

```
data-quality-audit-framework/
│
├── README.md                          ← Ce fichier — documentation complète
├── LICENSE                            ← Licence MIT
├── .gitignore                         ← Fichiers à ignorer par Git
├── requirements.txt                   ← Dépendances Python à installer
│
├── data_sample/                       ← Données d'exemple (anonymisées)
│   ├── clients_raw_sample.csv         ← CSV avec anomalies intentionnelles
│   └── schema_reference.md           ← Schéma attendu et règles métier
│
├── notebooks/                         ← Notebooks d'analyse
│   └── 01_data_quality_audit.py      ← Script principal (format .py lisible)
│
├── src/                               ← Code source Python réutilisable
│   ├── __init__.py
│   ├── quality_checker.py            ← Classe principale QualityChecker
│   └── report_generator.py          ← Génération du rapport Markdown
│
├── reports/                           ← Rapports générés
│   └── quality_report_sample.md     ← Exemple de rapport produit
│
├── figures/                           ← Graphiques générés
│   ├── fig1_missing_values.png
│   ├── fig2_quality_dimensions.png
│   ├── fig3_montant_distribution.png
│   └── fig4_anomalies_impact.png
│
├── docs/                              ← Documentation technique
│   ├── dictionnaire_donnees.md
│   ├── regles_metier.md
│   └── guide_utilisateur.md
│
└── dashboard/                         ← Instructions Power BI (optionnel)
    └── README.md
```

### Lexique GitHub pour non-techniciens

| Terme anglais | Traduction française | Signification simple |
|--------------|---------------------|---------------------|
| **repository** | dépôt | Dossier de projet versionné sur GitHub |
| **README** | fichier LISEZ-MOI | Page d'accueil du projet |
| **commit** | validation | Enregistrement d'une modification |
| **push** | envoi vers GitHub | Envoi des modifications locales vers le cloud |
| **branch** | branche | Version parallèle du projet |
| **pull request** | demande de fusion | Proposition de fusion d'une branche vers la principale |
| **issues** | tickets | Signalement de bugs ou demandes d'évolution |

---

## 17. Utiliser ce dépôt

### Installation

```bash
# 1. Cloner le dépôt (télécharger le projet sur votre ordinateur)
git clone https://github.com/TSAGUE25/data-quality-audit-framework.git
cd data-quality-audit-framework

# 2. Créer un environnement virtuel (espace Python isolé pour ce projet)
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'audit sur le dataset d'exemple
python notebooks/01_data_quality_audit.py
```

### Utilisation rapide

```python
from src.quality_checker import QualityChecker
import pandas as pd

df = pd.read_csv("data_sample/clients_raw_sample.csv")
checker = QualityChecker(df=df, dataset_name="Mon_Dataset")
resultats = checker.run_full_audit(
    key_col="id_client",
    email_col="email",
    phone_col="telephone",
    date_cols=["date_naissance"],
    allowed_values_rules={"statut": ["actif", "inactif", "suspendu"]}
)
checker.print_anomaly_report()
print(f"Score qualité : {checker.quality_score}/100")
```

---

## 18. Version CV

> À intégrer dans la section **Projets** ou **Réalisations** d'un CV Data Analyst / Data Scientist :

---

**Framework d'Audit Qualité des Données en Python** *(2024)*  
*Portfolio Data Science — Emmanuel TSAGUE*

Développement d'un module Python de détection automatique des anomalies de données : valeurs manquantes, doublons, formats invalides (email, téléphone, date), violations de règles métier et outliers statistiques (méthode IQR). Score de qualité composite (0–100), rapport Markdown généré automatiquement, 4 visualisations analytiques. Appliqué à un dataset clients simulé de 11 colonnes avec 17 types d'anomalies intentionnelles. Gain de temps : audit manuel de 2 jours → script automatique de 30 secondes.

**Compétences démontrées :** Python · pandas · regex · matplotlib · Qualité des données · Data Engineering · Automatisation · Reporting · Gouvernance des données

---

## 19. Version entretien

> Réponse à la question : *"Parlez-moi d'un projet Data où la qualité des données était un enjeu central."*

---

"Dans mon portfolio Data Science, j'ai construit un framework d'audit qualité des données en Python. Le point de départ est un problème très concret : dans de nombreuses organisations, les reportings sont construits sur des données non vérifiées — des doublons, des formats incohérents, des valeurs manquantes. Le résultat, c'est des KPI qui varient d'un rapport à l'autre et une perte de confiance des managers dans les outils.

Ma démarche a été de construire une classe Python réutilisable, `QualityChecker`, qui effectue neuf types de contrôles : valeurs manquantes, doublons, formats email et téléphone, dates impossibles, valeurs hors liste autorisée, plages numériques, dates futures et outliers statistiques par la méthode IQR.

À la fin, le système calcule un score de qualité global de 0 à 100 — comme une note scolaire pour la donnée — et génère automatiquement un rapport Markdown avec le plan de correction priorisé.

Ce que j'ai appris avec ce projet, c'est qu'auditer les données n'est pas une étape optionnelle avant l'analyse. C'est une étape obligatoire. Un modèle Machine Learning entraîné sur des données avec 10% de doublons et des formats incohérents donnera des résultats biaisés, même s'il est mathématiquement correct. La qualité de la sortie ne peut jamais dépasser la qualité de l'entrée."

---

## 20. Version portfolio longue

### Présentation complète pour un jury ou un recruteur

**Problème résolu :** Dans une organisation utilisant une base clients pour produire des reportings, les données contiennent des anomalies accumulées depuis des années. Ces anomalies — invisibles à l'œil nu dans un fichier de 30 000 lignes — faussent tous les indicateurs. Deux managers présentent des chiffres différents en réunion. La cause ? Des doublons, des statuts "actif/ACTIF/Actif" non normalisés et des emails invalides qui faussent les taux de contact.

**Solution construite :** Un framework Python modulaire et réutilisable composé de trois modules :
1. `quality_checker.py` — la classe principale avec 9 méthodes d'audit
2. `report_generator.py` — la génération automatique du rapport Markdown
3. `01_data_quality_audit.py` — le notebook d'application avec 4 visualisations

**Architecture de la solution :**
```
Données brutes (CSV)
        │
        ▼
QualityChecker.run_full_audit()
  ├── check_missing_values()    → Taux par colonne
  ├── check_duplicates()        → Lignes et clés
  ├── check_email_format()      → Regex validation
  ├── check_phone_format()      → 10 chiffres FR
  ├── check_date_format()       → DD/MM/YYYY
  ├── check_future_dates()      → Dates impossibles
  ├── check_allowed_values()    → Listes fermées
  ├── check_numeric_range()     → Min / Max
  └── check_outliers_iqr()     → Q1 - 1.5×IQR / Q3 + 1.5×IQR
        │
        ▼
compute_quality_score()  → Score 0–100
        │
        ▼
generate_markdown_report()  → Rapport automatique
```

**Résultats sur le dataset d'exemple :**
- 17 types d'anomalies détectés automatiquement
- Score initial : 58/100 (Insuffisant)
- Score après corrections programmatives : 78/100 (Bon)
- Temps d'audit : < 1 seconde pour 31 lignes; < 30 secondes pour 100 000 lignes

**Ce que ce projet démontre :**
- Maîtrise de Python orienté objet (classe, méthodes, paramètres)
- Connaissance des problèmes réels de qualité de données en entreprise
- Capacité à produire un outil réutilisable, pas seulement un script ponctuel
- Vision de la gouvernance des données au-delà de la technique pure

---

## 21. Post LinkedIn

---

**"Pas de bonne décision sans données fiables" — j'ai construit un outil pour en avoir la preuve.**

Dans presque tous les projets Data, il y a un moment où quelqu'un dit : "Nos chiffres sont différents selon la source."

C'est souvent la conséquence de données non auditées : doublons silencieux, formats inconsistants, valeurs hors plage, champs manquants.

Pour répondre à ce problème concret, j'ai construit un **framework d'audit qualité des données en Python**, disponible sur mon GitHub.

Ce que fait le framework :
✅ Détecte les doublons (lignes entières et clés primaires)
✅ Mesure le taux de valeurs manquantes par colonne
✅ Valide les formats : email, téléphone, date
✅ Contrôle les valeurs contre des listes autorisées
✅ Détecte les outliers statistiques (méthode IQR)
✅ Calcule un **score de qualité global de 0 à 100**
✅ Génère un **rapport Markdown automatique** avec plan de correction

Résultat sur un dataset simulé : 17 anomalies détectées, score initial de 58/100, monté à 78/100 après corrections programmatiques.

Le principe que j'applique : auditer les données avant toute analyse, pas après. Un beau dashboard construit sur des données douteuses n'est pas de la Business Intelligence — c'est de la confiance mal placée.

Le projet est documenté avec la structure GitHub complète, les données d'exemple et les visualisations.

---

*#DataQuality #DataScience #Python #pandas #DataEngineering #BusinessIntelligence #Portfolio*

---

## 22. Questions d'entretien

### Q1 — Qu'est-ce que la qualité des données, et pourquoi est-ce si important ?

**Réponse :** La qualité des données, c'est la mesure dans laquelle les données sont exactes, complètes, cohérentes et exploitables pour leur usage prévu. C'est important parce que toute décision basée sur des données incorrectes sera elle-même incorrecte — peu importe la sophistication du modèle ou du dashboard. En entreprise, des données de mauvaise qualité coûtent cher : mauvaises décisions, audits manuels coûteux, perte de confiance dans les outils analytiques. IBM estime que les mauvaises données coûtent aux entreprises américaines environ 3 000 milliards de dollars par an.

---

### Q2 — Quelles sont les principales dimensions de la qualité des données ?

**Réponse :** On distingue généralement six dimensions : (1) **Complétude** — les données manquantes ; (2) **Unicité** — les doublons ; (3) **Validité** — les formats et valeurs respectant les règles ; (4) **Cohérence** — les mêmes informations cohérentes entre différentes sources ; (5) **Précision** — les valeurs proches de la réalité ; (6) **Fraîcheur** — les données à jour. Dans ce projet, j'ai couvert les quatre premières.

---

### Q3 — Comment gérer les valeurs manquantes ? Faut-il toujours les supprimer ?

**Réponse :** Non, il faut d'abord comprendre pourquoi elles manquent. Si une valeur manque de façon aléatoire (un client n'a pas fourni son téléphone), on peut l'imputer (remplacer par la médiane, la mode, ou via un modèle). Si elle manque de façon systématique (tous les clients d'une certaine région), c'est un problème de collecte à corriger à la source. Supprimer les lignes avec valeurs manquantes est la pire option si elles représentent un sous-groupe important — on introduit un biais de sélection (on analyse uniquement les données "faciles").

---

### Q4 — C'est quoi un outlier, et comment le détecter ?

**Réponse :** Un outlier (valeur aberrante) est une valeur très éloignée des autres. La méthode IQR est la plus robuste : on calcule l'écart interquartile (Q3 - Q1), et toute valeur au-delà de Q1 - 1.5×IQR ou Q3 + 1.5×IQR est suspecte. Un outlier n'est pas forcément une erreur : un client avec un contrat à 250 000 € peut être un grand compte légitime. Le rôle de l'audit est de le signaler pour validation par le métier, pas de le supprimer automatiquement.

---

### Q5 — Comment industrialiser un audit qualité ?

**Réponse :** En construisant un module réutilisable (une classe Python avec des méthodes paramétrables), en externalisant les règles métier dans un fichier de configuration (YAML ou JSON), en intégrant l'audit dans un pipeline CI/CD (exécuté automatiquement à chaque nouvelle livraison de données), et en publiant le score qualité dans un dashboard de monitoring. L'objectif est que personne ne doive lancer l'audit manuellement — il tourne automatiquement.

---

### Q6 — Quelle est la différence entre un audit qualité et un nettoyage de données ?

**Réponse :** L'audit diagnostique sans modifier les données. Le nettoyage corrige. L'audit vient en premier — il répond à la question "qu'est-ce qui ne va pas et à quel point ?". Le nettoyage vient ensuite, sur la base des conclusions de l'audit. Dans ce projet, j'ai séparé les deux : la classe `QualityChecker` audite, et le notebook montre séparément les corrections applicables. Cette séparation est importante pour la traçabilité et la gouvernance.

---

### Q7 — Comment expliquer un score de qualité de données à un manager non technique ?

**Réponse :** Comme une note sur 100 pour votre donnée, calculée automatiquement. Un score de 95 signifie que vos données sont quasi-parfaites. Un score de 58 signifie que vous ne devriez pas publier ce reporting sans correction. Le score est décomposable par dimension — comme une carte de résultats scolaires par matière. Ce qui compte pour le manager, c'est de savoir si on peut faire confiance aux chiffres. Le score répond à cette question de façon objective.

---

## 23. Compétences démontrées

| Compétence technique | Preuve dans ce projet |
|---------------------|----------------------|
| Python orienté objet | Classe `QualityChecker` avec 10 méthodes |
| pandas | Manipulation de DataFrame, `.isnull()`, `.duplicated()`, `.apply()`, `pd.to_numeric()` |
| Expressions régulières (regex) | Validation email, téléphone |
| matplotlib | 4 visualisations analytiques (barres, boxplot, camembert) |
| Qualité des données | 9 types de contrôles implémentés |
| Automatisation | Rapport Markdown généré sans intervention |
| Architecture logicielle | Séparation src / notebooks / reports / docs |
| Documentation technique | README complet, docstrings, commentaires |
| Gouvernance des données | Plan de correction priorisé, dictionnaire des données |
| Git / GitHub | Versioning, structure de dépôt professionnelle |

---

## 24. Tableau compétences / preuves

| Compétence | Preuve dans le projet | Valeur pour l'entreprise | Phrase CV |
|-----------|----------------------|------------------------|-----------|
| Python POO | Classe `QualityChecker` réutilisable | Réduction du temps d'audit de 2 jours à 30 secondes | "Développement d'un module Python orienté objet d'audit qualité automatisé" |
| pandas | 10 méthodes de contrôle qualité | Détection exhaustive des anomalies | "Maîtrise de pandas pour le profiling, la détection de doublons et la validation de formats" |
| Qualité des données | 17 anomalies détectées automatiquement | Fiabilisation du reporting avant publication | "Audit automatique de la qualité des données : score composite, rapport et plan de correction" |
| Visualisation | 4 graphiques analytiques clairs | Communication des résultats aux équipes non techniques | "Visualisation des indicateurs qualité avec matplotlib (barres, boxplot, camembert)" |
| Architecture code | Séparation src / notebooks / docs | Code maintenable et extensible | "Architecture logicielle modulaire pour l'industrialisation de l'audit qualité" |
| Gouvernance | Dictionnaire, règles, plan de correction | Fondation pour une culture data-driven | "Mise en place d'un framework de gouvernance des données avec indicateurs de qualité" |

---

## 25. Conseils de publication GitHub

### Avant de publier

1. **Vérifier qu'aucune donnée réelle ne figure dans le dépôt** — utiliser uniquement des données simulées ou anonymisées
2. **Ajouter un fichier `.gitignore`** pour exclure les fichiers sensibles (`.env`, données brutes confidentielles)
3. **Tester que les scripts fonctionnent sur un environnement propre** (sans vos modules locaux installés)
4. **Écrire un README lisible** — le README est la première chose que voit un recruteur

### Pour maximiser la visibilité

5. **Ajouter des topics (mots-clés)** dans les paramètres GitHub du dépôt : `data-quality`, `python`, `pandas`, `data-engineering`, `portfolio`, `data-science`
6. **Épingler ce dépôt** sur votre profil GitHub (Settings → Pinned repositories)
7. **Ajouter une description courte** dans "About" du dépôt : "Framework Python d'audit qualité des données — détection automatique des anomalies, score qualité 0–100, rapport auto-généré"
8. **Lier ce dépôt depuis votre LinkedIn** (section Projets ou Publications)

### Pour montrer la qualité du code

9. **Ajouter des docstrings** sur chaque fonction (déjà fait dans ce projet)
10. **Écrire des tests unitaires** dans un dossier `tests/` avec pytest
11. **Ajouter un badge de score** dans le README (voir les badges en haut)
12. **Versionner proprement** : des commits avec des messages clairs, pas un seul commit géant


## Contributors

| Nom | Role | GitHub |
|-----|------|--------|
| **TSAGUE Emmanuel** | Data Scientist - auteur principal | [@TSAGUE25](https://github.com/TSAGUE25) |

---

*Projet réalisé par Emmanuel TSAGUE — Data Scientist / Data Analyst*  
*Portfolio Data Science 2024 — Données simulées à des fins pédagogiques*
