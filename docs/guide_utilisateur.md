# Guide Utilisateur — Data Quality Audit Framework

**Pour :** Data Analysts, Data Engineers, Responsables reporting  
**Prérequis :** Python 3.10+, pandas

---

## Démarrage rapide (5 minutes)

```bash
git clone https://github.com/TSAGUE25/data-quality-audit-framework.git
cd data-quality-audit-framework
pip install pandas matplotlib
python notebooks/01_data_quality_audit.py
```

## Adapter à vos propres données

1. Remplacez `data_sample/clients_raw_sample.csv` par votre fichier
2. Ajustez les paramètres de `run_full_audit()` selon vos colonnes
3. Mettez à jour les règles dans `docs/regles_metier.md`
4. Relancez le script

## Interpréter le rapport

- **Score ≥ 75** → données exploitables (avec réserves documentées)
- **Score < 60** → stop, ne pas publier le reporting
- **Anomalies 🔴 ÉLEVÉ** → corriger avant toute analyse
- **Anomalies 🟡 MOYEN** → signaler au métier pour validation
- **Anomalies 🟢 FAIBLE** → documenter, corriger si possible

## FAQ

**Q : Peut-on l'utiliser sur un fichier Excel ?**  
R : Oui — `pd.read_excel("fichier.xlsx")` puis passer le DataFrame à QualityChecker.

**Q : Comment ajouter une nouvelle règle ?**  
R : Ajouter une méthode `check_xxxx()` dans `quality_checker.py` et l'appeler dans `run_full_audit()`.

**Q : Le script modifie-t-il mes données ?**  
R : Non. Il travaille sur une copie interne (`df.copy()`). Vos fichiers source restent intacts.

---

*Emmanuel TSAGUE — Data Scientist / Data Analyst — 2024*
