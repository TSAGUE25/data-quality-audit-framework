# Dashboard Power BI — Qualité des Données

## Objectif

Compléter l'audit Python avec un tableau de bord Power BI permettant aux équipes
non techniques (managers, responsables métier) de suivre l'évolution de la qualité
des données dans le temps.

## Données d'entrée pour Power BI

Le script Python génère dans `reports/` un fichier `quality_report_sample.md`.
Pour Power BI, exporter un CSV de synthèse depuis le notebook :

```python
# Ajouter à la fin du notebook :
synthese = pd.DataFrame([{
    "date_audit": checker.audit_date,
    "dataset": checker.dataset_name,
    "n_lignes": checker.n_rows,
    "score_qualite": checker.quality_score,
    "n_anomalies": len(checker.anomalies),
    "n_anomalies_elevees": sum(1 for a in checker.anomalies if a["impact"] == "ÉLEVÉ"),
    "n_doublons": checker.results.get("duplicates", {}).get("n_doublons_complets", 0),
    "taux_manquants_global": checker.results["missing_values"]["nb_manquants"].sum() /
                             (checker.n_rows * checker.n_cols) * 100
}])
synthese.to_csv("reports/quality_summary.csv", index=False)
```

## Pages du tableau de bord recommandées

| Page | Contenu |
|------|---------|
| 1 — Synthèse | Score global · Nb anomalies · Doublons · Manquants |
| 2 — Évolution | Courbe du score qualité dans le temps |
| 3 — Détail | Tableau des anomalies par type et impact |
| 4 — Colonnes | Heatmap des taux de manquants par colonne |

---

*Emmanuel TSAGUE — Data Scientist / Data Analyst — 2024*
