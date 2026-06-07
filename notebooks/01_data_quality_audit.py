# %% [markdown]
# # Audit Qualité des Données — Notebook d'analyse
# **Auteur :** Emmanuel TSAGUE — Data Scientist / Data Analyst
# **Contexte :** Audit automatique de la qualité d'un fichier clients avant reporting
#
# Ce notebook illustre l'utilisation de la classe `QualityChecker` sur un jeu de données
# clients simulé contenant des problèmes de qualité intentionnels.
#
# **Structure du notebook :**
# 1. Chargement des données
# 2. Exploration rapide (profiling)
# 3. Audit qualité complet avec QualityChecker
# 4. Visualisations
# 5. Rapport final
# 6. Plan de correction

# %% [markdown]
# ## 1. Imports et chargement

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
import os

# Ajouter le dossier src au path Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from quality_checker import QualityChecker
from report_generator import generate_markdown_report, save_report

# Paramètres d'affichage
pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 120)
plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["font.family"] = "sans-serif"

# %% [markdown]
# ## 2. Chargement des données brutes

# %%
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data_sample", "clients_raw_sample.csv")
df = pd.read_csv(DATA_PATH)

print(f"Dimensions : {df.shape[0]} lignes × {df.shape[1]} colonnes")
print(f"\nColonnes : {df.columns.tolist()}")
df.head(10)

# %% [markdown]
# ## 3. Profiling rapide — vue d'ensemble

# %%
print("=== TYPES DE DONNÉES ===")
print(df.dtypes)
print("\n=== STATISTIQUES DESCRIPTIVES ===")
df.describe(include="all")

# %%
# Aperçu des valeurs uniques par colonne catégorielle
for col in df.select_dtypes(include="object").columns:
    vals = df[col].value_counts(dropna=False).head(8)
    print(f"\n[{col}] — {df[col].nunique(dropna=False)} valeurs distinctes")
    print(vals.to_string())

# %% [markdown]
# ## 4. Audit qualité complet

# %%
# Initialisation du QualityChecker
checker = QualityChecker(
    df=df,
    dataset_name="Clients_Raw_Sample"
)

# Lancement de l'audit complet
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

# Affichage du rapport d'anomalies
checker.print_anomaly_report()

# %% [markdown]
# ## 5. Visualisations

# %%
# --- Graphique 1 : Valeurs manquantes par colonne ---
missing_df = checker.results["missing_values"]
missing_df_sorted = missing_df.sort_values("nb_manquants", ascending=False)

colors = missing_df_sorted["statut"].map(
    {"OK": "#2ecc71", "ATTENTION": "#f39c12", "CRITIQUE": "#e74c3c"}
)

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.barh(missing_df_sorted["colonne"], missing_df_sorted["taux_manquants_pct"],
               color=colors, edgecolor="white", linewidth=0.5)
ax.set_xlabel("Taux de valeurs manquantes (%)")
ax.set_title("Valeurs manquantes par colonne", fontsize=14, fontweight="bold", pad=15)
ax.axvline(x=10, color="#e74c3c", linestyle="--", alpha=0.7, label="Seuil critique (10%)")
ax.axvline(x=5, color="#f39c12", linestyle=":", alpha=0.7, label="Seuil attention (5%)")

legend_patches = [
    mpatches.Patch(color="#2ecc71", label="OK (0%)"),
    mpatches.Patch(color="#f39c12", label="Attention (< 10%)"),
    mpatches.Patch(color="#e74c3c", label="Critique (≥ 10%)"),
]
ax.legend(handles=legend_patches, loc="lower right")
ax.set_xlim(0, max(missing_df_sorted["taux_manquants_pct"].max() * 1.2, 5))
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "..", "figures", "fig1_missing_values.png"),
            dpi=150, bbox_inches="tight")
plt.show()
print("Figure 1 sauvegardée.")

# %%
# --- Graphique 2 : Distribution du score qualité par dimension ---
dimensions = ["Complétude\n(manquants)", "Unicité\n(doublons)", "Formats\n(email/tel/date)",
              "Règles métier\n(valeurs/plages)", "Outliers\n(aberrants)"]

# Calcul des scores partiels (simulation basée sur l'audit)
dup_res = checker.results.get("duplicates", {})
taux_dup = dup_res.get("taux_doublons_pct", 0)
missing_res = checker.results.get("missing_values", pd.DataFrame())
taux_missing = (missing_res["nb_manquants"].sum() / (checker.n_rows * checker.n_cols) * 100
                if not missing_res.empty else 0)

scores_partiels = [
    max(0, 100 - taux_missing * 5),
    max(0, 100 - taux_dup * 10),
    max(0, 100 - sum(4 for a in checker.anomalies
                     if "format" in a["type"].lower() or "date" in a["type"].lower())),
    max(0, 100 - sum(5 for a in checker.anomalies
                     if a["type"] in ("Valeur hors liste autorisée", "Valeur hors plage", "Type incorrect"))),
    max(0, 100 - sum(10 for a in checker.anomalies if "outlier" in a["type"].lower()))
]

fig, ax = plt.subplots(figsize=(10, 5))
colors_scores = ["#2ecc71" if s >= 80 else "#f39c12" if s >= 60 else "#e74c3c"
                 for s in scores_partiels]
bars = ax.bar(dimensions, scores_partiels, color=colors_scores, edgecolor="white", linewidth=0.5)
ax.axhline(y=80, color="green", linestyle="--", alpha=0.5, label="Seuil bon (80)")
ax.axhline(y=60, color="orange", linestyle=":", alpha=0.5, label="Seuil acceptable (60)")
ax.set_ylim(0, 110)
ax.set_ylabel("Score (0 à 100)")
ax.set_title(f"Score Qualité par Dimension — Score global : {checker.quality_score}/100",
             fontsize=13, fontweight="bold", pad=15)
for bar, score in zip(bars, scores_partiels):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
            f"{score:.0f}", ha="center", va="bottom", fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "..", "figures", "fig2_quality_dimensions.png"),
            dpi=150, bbox_inches="tight")
plt.show()
print("Figure 2 sauvegardée.")

# %%
# --- Graphique 3 : Distribution du montant_contrat (avec outliers) ---
montant_num = pd.to_numeric(df["montant_contrat"], errors="coerce").dropna()

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(montant_num, bins=20, color="#3498db", edgecolor="white", alpha=0.8)
axes[0].set_title("Distribution du montant contrat (€)", fontweight="bold")
axes[0].set_xlabel("Montant (€)")
axes[0].set_ylabel("Fréquence")

axes[1].boxplot(montant_num, vert=True, patch_artist=True,
                boxprops=dict(facecolor="#3498db", alpha=0.7))
axes[1].set_title("Boxplot — Détection des outliers (IQR)", fontweight="bold")
axes[1].set_ylabel("Montant (€)")

plt.suptitle("Analyse du montant_contrat", fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "..", "figures", "fig3_montant_distribution.png"),
            dpi=150, bbox_inches="tight")
plt.show()
print("Figure 3 sauvegardée.")

# %%
# --- Graphique 4 : Répartition des anomalies par impact ---
from collections import Counter
impact_counts = Counter(a["impact"] for a in checker.anomalies)
labels = list(impact_counts.keys())
sizes = list(impact_counts.values())
colors_pie = ["#e74c3c" if l == "ÉLEVÉ" else "#f39c12" if l == "MOYEN" else "#2ecc71"
              for l in labels]

fig, ax = plt.subplots(figsize=(7, 5))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors_pie,
                                   autopct="%1.0f%%", startangle=90,
                                   textprops={"fontsize": 12})
ax.set_title("Répartition des anomalies par niveau d'impact", fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "..", "figures", "fig4_anomalies_impact.png"),
            dpi=150, bbox_inches="tight")
plt.show()
print("Figure 4 sauvegardée.")

# %% [markdown]
# ## 6. Génération du rapport Markdown

# %%
rapport_md = generate_markdown_report(
    audit_results=resultats,
    dataset_name="Clients_Raw_Sample",
    n_rows=checker.n_rows,
    n_cols=checker.n_cols
)

report_path = os.path.join(os.path.dirname(__file__), "..", "reports", "quality_report_sample.md")
save_report(rapport_md, report_path)
print("\nRapport généré avec succès !")

# %% [markdown]
# ## 7. Plan de correction — DataFrame nettoyée
#
# Démonstration des principales corrections applicables programmatiquement.

# %%
df_clean = df.copy()

# Correction 1 : Supprimer les doublons complets
df_clean = df_clean.drop_duplicates()
print(f"Après suppression doublons : {len(df_clean)} lignes (était {len(df)})")

# Correction 2 : Normaliser le statut en minuscules
df_clean["statut"] = df_clean["statut"].str.lower().str.strip()

# Correction 3 : Nettoyer le téléphone (supprimer espaces)
df_clean["telephone"] = df_clean["telephone"].str.replace(r"[\s\.\-]", "", regex=True)

# Correction 4 : Convertir montant en numérique (les non-convertibles → NaN)
df_clean["montant_contrat"] = pd.to_numeric(df_clean["montant_contrat"], errors="coerce")

# Correction 5 : Mettre les valeurs négatives à NaN (à investiguer avec le métier)
df_clean.loc[df_clean["montant_contrat"] < 0, "montant_contrat"] = np.nan

print(f"\nDataFrame nettoyée — aperçu :")
print(df_clean.head(5).to_string())

# %%
# Re-audit sur les données nettoyées pour mesurer le gain
print("\n=== AUDIT POST-NETTOYAGE ===")
checker2 = QualityChecker(df_clean, dataset_name="Clients_Clean")
checker2.run_full_audit(
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
print(f"\nScore avant nettoyage : {checker.quality_score}/100")
print(f"Score après nettoyage : {checker2.quality_score}/100")
print(f"Gain : +{checker2.quality_score - checker.quality_score:.1f} points")
