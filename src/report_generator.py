"""
report_generator.py — Génère un rapport Markdown à partir des résultats d'audit.
Auteur : Emmanuel TSAGUE
"""

from datetime import datetime


def generate_markdown_report(audit_results: dict, dataset_name: str,
                              n_rows: int, n_cols: int) -> str:
    """
    Génère un rapport Markdown complet à partir du dictionnaire retourné par run_full_audit().

    Paramètres
    ----------
    audit_results : dict retourné par QualityChecker.run_full_audit()
    dataset_name : nom du jeu de données
    n_rows, n_cols : dimensions du dataset

    Retourne
    --------
    str : contenu du rapport au format Markdown
    """
    score = audit_results["score"]
    grade = audit_results["grade"]
    anomalies = audit_results["anomalies"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Couleur du score
    score_badge = (
        "![score](https://img.shields.io/badge/Score_qualité-"
        + str(score) + "%25-"
        + ("brightgreen" if score >= 90 else "yellow" if score >= 75 else "orange" if score >= 60 else "red")
        + ")"
    )

    lines = [
        f"# Rapport d'Audit Qualité — {dataset_name}",
        f"",
        f"**Date :** {now}  ",
        f"**Dimensions :** {n_rows} lignes × {n_cols} colonnes  ",
        f"**Score global :** {score}/100 — **{grade}**  ",
        f"{score_badge}",
        f"",
        "---",
        "",
        "## 1. Synthèse exécutive",
        "",
        f"| Indicateur | Valeur |",
        f"|-----------|--------|",
        f"| Score de qualité global | **{score}/100** |",
        f"| Niveau | **{grade}** |",
        f"| Nombre d'anomalies détectées | **{len(anomalies)}** |",
        f"| Anomalies critiques (ÉLEVÉ) | **{sum(1 for a in anomalies if a['impact'] == 'ÉLEVÉ')}** |",
        f"| Anomalies modérées (MOYEN) | **{sum(1 for a in anomalies if a['impact'] == 'MOYEN')}** |",
        f"| Anomalies mineures (FAIBLE) | **{sum(1 for a in anomalies if a['impact'] == 'FAIBLE')}** |",
        "",
        "---",
        "",
        "## 2. Détail des anomalies détectées",
        "",
        "| # | Impact | Type | Détail |",
        "|---|--------|------|--------|",
    ]

    impact_icons = {"ÉLEVÉ": "🔴", "MOYEN": "🟡", "FAIBLE": "🟢"}
    for i, a in enumerate(anomalies, 1):
        icon = impact_icons.get(a["impact"], "⚪")
        lines.append(f"| {i} | {icon} {a['impact']} | {a['type']} | {a['detail']} |")

    lines += [
        "",
        "---",
        "",
        "## 3. Plan de correction recommandé",
        "",
        "| Priorité | Action | Impact attendu |",
        "|---------|--------|---------------|",
        "| 1 — Immédiat | Supprimer les lignes dupliquées | Intégrité des données |",
        "| 2 — Court terme | Corriger les formats de date invalides | Fiabilité des analyses temporelles |",
        "| 3 — Court terme | Valider et normaliser les valeurs de statut | Cohérence des segments |",
        "| 4 — Moyen terme | Compléter les valeurs manquantes ou les isoler | Qualité des agrégats |",
        "| 5 — Moyen terme | Vérifier les montants aberrants avec le métier | Fiabilité financière |",
        "| 6 — Long terme | Mettre en place des contrôles qualité à la source | Prévention en amont |",
        "",
        "---",
        "",
        "## 4. Recommandations de gouvernance",
        "",
        "- Définir un **dictionnaire de données** (data dictionary) avec les règles de chaque colonne",
        "- Mettre en place des **contrôles à la saisie** (validation formulaire, CRM, ERP)",
        "- Automatiser cet audit qualité à chaque chargement de nouvelles données",
        "- Documenter un **score de qualité minimal acceptable** avant publication d'un rapport",
        "- Désigner un **Data Steward** (responsable qualité des données) par périmètre métier",
        "",
        "---",
        "",
        f"*Rapport généré automatiquement par le Data Quality Audit Framework*  ",
        f"*Auteur : Emmanuel TSAGUE — Data Scientist / Data Analyst*",
    ]

    return "\n".join(lines)


def save_report(content: str, filepath: str):
    """Sauvegarde le rapport Markdown dans un fichier."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Rapport sauvegardé : {filepath}")
