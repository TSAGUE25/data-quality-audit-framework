"""
Data Quality Audit Framework — quality_checker.py
Auteur : Emmanuel TSAGUE — Data Scientist / Data Analyst
Contexte : Audit automatique de la qualité des données avant analyse ou reporting

Ce module fournit la classe principale QualityChecker qui analyse une DataFrame
pandas et produit un rapport de qualité structuré.
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings("ignore")


class QualityChecker:
    """
    Classe principale d'audit qualité.

    Effectue les contrôles suivants :
    - Valeurs manquantes (null / NaN / vide)
    - Doublons (lignes entières et colonnes clés)
    - Types de données incorrects
    - Formats invalides (email, téléphone, date)
    - Règles métier (plages de valeurs, listes fermées)
    - Détection d'outliers statistiques
    - Calcul du score de qualité global (0 à 100)
    """

    def __init__(self, df: pd.DataFrame, schema: Dict = None, dataset_name: str = "dataset"):
        """
        Initialise l'auditeur qualité.

        Paramètres
        ----------
        df : pd.DataFrame
            Le jeu de données à auditer.
        schema : dict, optionnel
            Dictionnaire décrivant les règles attendues par colonne.
        dataset_name : str
            Nom du jeu de données (pour le rapport).
        """
        self.df = df.copy()
        self.schema = schema or {}
        self.dataset_name = dataset_name
        self.n_rows = len(df)
        self.n_cols = len(df.columns)
        self.results = {}   # Stocke tous les résultats d'audit
        self.anomalies = [] # Liste détaillée des anomalies détectées
        self.audit_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # -------------------------------------------------------------------------
    # 1. VALEURS MANQUANTES
    # -------------------------------------------------------------------------
    def check_missing_values(self) -> pd.DataFrame:
        """
        Calcule le taux de valeurs manquantes par colonne.

        Returns
        -------
        pd.DataFrame avec colonnes : colonne, nb_manquants, taux_manquants_pct, statut
        """
        missing = self.df.isnull().sum()
        # Compter aussi les chaînes vides comme manquantes
        for col in self.df.select_dtypes(include="object").columns:
            missing[col] += (self.df[col].astype(str).str.strip() == "").sum()

        missing_df = pd.DataFrame({
            "colonne": missing.index,
            "nb_manquants": missing.values,
            "taux_manquants_pct": (missing.values / self.n_rows * 100).round(2)
        })
        missing_df["statut"] = missing_df["taux_manquants_pct"].apply(
            lambda x: "OK" if x == 0 else ("ATTENTION" if x < 10 else "CRITIQUE")
        )

        self.results["missing_values"] = missing_df
        n_colonnes_avec_manquants = (missing_df["nb_manquants"] > 0).sum()
        if n_colonnes_avec_manquants > 0:
            self.anomalies.append({
                "type": "Valeurs manquantes",
                "detail": f"{n_colonnes_avec_manquants} colonne(s) avec valeurs manquantes",
                "impact": "MOYEN" if missing_df["taux_manquants_pct"].max() < 20 else "ÉLEVÉ"
            })
        return missing_df

    # -------------------------------------------------------------------------
    # 2. DOUBLONS
    # -------------------------------------------------------------------------
    def check_duplicates(self, key_columns: List[str] = None) -> Dict:
        """
        Détecte les doublons sur l'ensemble des colonnes et sur les colonnes clés.

        Paramètres
        ----------
        key_columns : liste de colonnes servant d'identifiant unique (ex: ['id_client'])
        """
        # Doublons complets (toutes colonnes)
        n_doublons_complets = self.df.duplicated().sum()

        result = {
            "n_doublons_complets": int(n_doublons_complets),
            "taux_doublons_pct": round(n_doublons_complets / self.n_rows * 100, 2),
            "lignes_dupliquées": self.df[self.df.duplicated(keep=False)].index.tolist()
        }

        # Doublons sur clé primaire
        if key_columns:
            valid_keys = [c for c in key_columns if c in self.df.columns]
            if valid_keys:
                n_doublons_cle = self.df.duplicated(subset=valid_keys).sum()
                result["n_doublons_cle"] = int(n_doublons_cle)
                result["cle_utilisee"] = valid_keys
                result["lignes_cle_dupliquée"] = (
                    self.df[self.df.duplicated(subset=valid_keys, keep=False)][valid_keys]
                    .drop_duplicates()
                    .values.tolist()
                )

        self.results["duplicates"] = result
        if n_doublons_complets > 0:
            self.anomalies.append({
                "type": "Doublons",
                "detail": f"{n_doublons_complets} ligne(s) entièrement dupliquée(s)",
                "impact": "ÉLEVÉ"
            })
        return result

    # -------------------------------------------------------------------------
    # 3. TYPES DE DONNÉES
    # -------------------------------------------------------------------------
    def check_data_types(self, expected_types: Dict[str, str] = None) -> pd.DataFrame:
        """
        Vérifie les types détectés vs. les types attendus.

        Paramètres
        ----------
        expected_types : dict {colonne: type_attendu}
        Exemple : {"montant_contrat": "float", "date_naissance": "date"}
        """
        actual_types = self.df.dtypes.reset_index()
        actual_types.columns = ["colonne", "type_detecte"]
        actual_types["type_detecte"] = actual_types["type_detecte"].astype(str)

        if expected_types:
            actual_types["type_attendu"] = actual_types["colonne"].map(expected_types).fillna("non spécifié")
            actual_types["conforme"] = actual_types.apply(
                lambda r: "OK" if r["type_attendu"] == "non spécifié"
                else ("OK" if r["type_attendu"] in r["type_detecte"] else "ERREUR"),
                axis=1
            )
        else:
            actual_types["type_attendu"] = "non spécifié"
            actual_types["conforme"] = "non vérifié"

        self.results["data_types"] = actual_types
        return actual_types

    # -------------------------------------------------------------------------
    # 4. FORMATS — EMAIL, TÉLÉPHONE, DATE
    # -------------------------------------------------------------------------
    def check_email_format(self, col: str) -> pd.Series:
        """Valide le format email dans une colonne."""
        if col not in self.df.columns:
            return pd.Series(dtype=bool)
        pattern = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
        mask_non_null = self.df[col].notna() & (self.df[col].astype(str).str.strip() != "")
        valid = self.df.loc[mask_non_null, col].astype(str).str.match(pattern)
        invalids = self.df[mask_non_null].loc[~valid, col]
        n_invalid = len(invalids)
        result = {
            "colonne": col,
            "n_presents": int(mask_non_null.sum()),
            "n_invalides": n_invalid,
            "taux_invalides_pct": round(n_invalid / self.n_rows * 100, 2),
            "exemples_invalides": invalids.head(5).tolist()
        }
        self.results["email_format"] = result
        if n_invalid > 0:
            self.anomalies.append({
                "type": "Format email invalide",
                "detail": f"{n_invalid} adresse(s) email mal formée(s) dans '{col}'",
                "impact": "MOYEN"
            })
        return result

    def check_phone_format(self, col: str) -> Dict:
        """Valide le format téléphone français (10 chiffres)."""
        if col not in self.df.columns:
            return {}
        mask_non_null = self.df[col].notna() & (self.df[col].astype(str).str.strip() != "")
        # Nettoyer : supprimer espaces, points, tirets
        cleaned = self.df.loc[mask_non_null, col].astype(str).str.replace(r"[\s\.\-]", "", regex=True)
        valid = cleaned.str.match(r"^0[1-9]\d{8}$")
        invalids = self.df[mask_non_null].loc[~valid, col]
        n_invalid = len(invalids)
        result = {
            "colonne": col,
            "n_presents": int(mask_non_null.sum()),
            "n_invalides": n_invalid,
            "exemples_invalides": invalids.head(5).tolist()
        }
        self.results["phone_format"] = result
        if n_invalid > 0:
            self.anomalies.append({
                "type": "Format téléphone invalide",
                "detail": f"{n_invalid} numéro(s) de téléphone invalide(s) dans '{col}'",
                "impact": "FAIBLE"
            })
        return result

    def check_date_format(self, col: str, fmt: str = "%d/%m/%Y") -> Dict:
        """
        Valide le format de date et détecte les dates impossibles (31 avril, etc.).
        """
        if col not in self.df.columns:
            return {}
        mask_non_null = self.df[col].notna() & (self.df[col].astype(str).str.strip() != "")
        values = self.df.loc[mask_non_null, col].astype(str)

        invalids = []
        for idx, val in values.items():
            try:
                datetime.strptime(val.strip(), fmt)
            except ValueError:
                invalids.append((idx, val))

        result = {
            "colonne": col,
            "format_attendu": fmt,
            "n_presents": int(mask_non_null.sum()),
            "n_invalides": len(invalids),
            "exemples_invalides": invalids[:5]
        }
        self.results[f"date_format_{col}"] = result
        if invalids:
            self.anomalies.append({
                "type": "Format / date impossible",
                "detail": f"{len(invalids)} date(s) invalide(s) dans '{col}'",
                "impact": "ÉLEVÉ"
            })
        return result

    # -------------------------------------------------------------------------
    # 5. RÈGLES MÉTIER
    # -------------------------------------------------------------------------
    def check_allowed_values(self, col: str, allowed: List[str], case_sensitive: bool = False) -> Dict:
        """Vérifie que les valeurs d'une colonne appartiennent à une liste fermée."""
        if col not in self.df.columns:
            return {}
        mask_non_null = self.df[col].notna()
        values = self.df.loc[mask_non_null, col].astype(str)
        if not case_sensitive:
            values = values.str.lower()
            allowed = [v.lower() for v in allowed]
        non_conformes = values[~values.isin(allowed)]
        result = {
            "colonne": col,
            "valeurs_autorisées": allowed,
            "n_non_conformes": len(non_conformes),
            "valeurs_trouvées": non_conformes.value_counts().to_dict()
        }
        self.results[f"allowed_values_{col}"] = result
        if len(non_conformes) > 0:
            self.anomalies.append({
                "type": "Valeur hors liste autorisée",
                "detail": f"{len(non_conformes)} valeur(s) non conforme(s) dans '{col}': {non_conformes.unique().tolist()}",
                "impact": "ÉLEVÉ"
            })
        return result

    def check_numeric_range(self, col: str, min_val: float = None, max_val: float = None) -> Dict:
        """Vérifie qu'une colonne numérique est dans une plage de valeurs acceptables."""
        if col not in self.df.columns:
            return {}
        # Tenter la conversion en numérique
        numeric = pd.to_numeric(self.df[col], errors="coerce")
        n_non_convertibles = numeric.isna().sum() - self.df[col].isna().sum()

        out_of_range = pd.Series(dtype=bool, index=numeric.index)
        if min_val is not None:
            out_of_range = out_of_range | (numeric < min_val)
        if max_val is not None:
            out_of_range = out_of_range | (numeric > max_val)
        out_of_range = out_of_range.fillna(False)

        result = {
            "colonne": col,
            "min_attendu": min_val,
            "max_attendu": max_val,
            "min_observé": float(numeric.min()) if not numeric.dropna().empty else None,
            "max_observé": float(numeric.max()) if not numeric.dropna().empty else None,
            "n_non_convertibles": int(n_non_convertibles),
            "n_hors_plage": int(out_of_range.sum()),
            "exemples_hors_plage": self.df.loc[out_of_range, col].head(5).tolist()
        }
        self.results[f"range_{col}"] = result
        if n_non_convertibles > 0:
            self.anomalies.append({
                "type": "Type incorrect",
                "detail": f"{n_non_convertibles} valeur(s) non numérique(s) dans '{col}'",
                "impact": "ÉLEVÉ"
            })
        if out_of_range.sum() > 0:
            self.anomalies.append({
                "type": "Valeur hors plage",
                "detail": f"{out_of_range.sum()} valeur(s) hors plage [{min_val}, {max_val}] dans '{col}'",
                "impact": "ÉLEVÉ"
            })
        return result

    def check_future_dates(self, col: str, fmt: str = "%Y-%m-%d") -> Dict:
        """Détecte les dates dans le futur (anomalie pour dates d'inscription passées)."""
        if col not in self.df.columns:
            return {}
        today = date.today()
        future_rows = []
        mask_non_null = self.df[col].notna()
        for idx, val in self.df.loc[mask_non_null, col].astype(str).items():
            try:
                d = datetime.strptime(val.strip(), fmt).date()
                if d > today:
                    future_rows.append((idx, val))
            except ValueError:
                pass
        result = {
            "colonne": col,
            "n_dates_futures": len(future_rows),
            "exemples": future_rows[:5]
        }
        self.results[f"future_dates_{col}"] = result
        if future_rows:
            self.anomalies.append({
                "type": "Date future impossible",
                "detail": f"{len(future_rows)} date(s) dans le futur dans '{col}'",
                "impact": "ÉLEVÉ"
            })
        return result

    # -------------------------------------------------------------------------
    # 6. OUTLIERS STATISTIQUES
    # -------------------------------------------------------------------------
    def check_outliers_iqr(self, col: str) -> Dict:
        """
        Détecte les outliers (valeurs aberrantes) via la méthode IQR (interquartile range).

        Un outlier est une valeur inférieure à Q1 - 1.5*IQR ou supérieure à Q3 + 1.5*IQR.
        IQR = Q3 - Q1 (l'écart entre le 75e et le 25e percentile).
        """
        if col not in self.df.columns:
            return {}
        numeric = pd.to_numeric(self.df[col], errors="coerce").dropna()
        if numeric.empty:
            return {"colonne": col, "statut": "non numérique"}

        q1 = numeric.quantile(0.25)
        q3 = numeric.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = numeric[(numeric < lower) | (numeric > upper)]
        result = {
            "colonne": col,
            "Q1": round(q1, 2),
            "Q3": round(q3, 2),
            "IQR": round(iqr, 2),
            "borne_inférieure": round(lower, 2),
            "borne_supérieure": round(upper, 2),
            "n_outliers": len(outliers),
            "valeurs_outliers": outliers.tolist()
        }
        self.results[f"outliers_{col}"] = result
        if len(outliers) > 0:
            self.anomalies.append({
                "type": "Outlier statistique",
                "detail": f"{len(outliers)} valeur(s) aberrante(s) dans '{col}' (IQR method)",
                "impact": "MOYEN"
            })
        return result

    # -------------------------------------------------------------------------
    # 7. SCORE DE QUALITÉ GLOBAL
    # -------------------------------------------------------------------------
    def compute_quality_score(self) -> float:
        """
        Calcule un score de qualité global de 0 à 100.

        Formule :
        - Pénalité valeurs manquantes : jusqu'à -30 points
        - Pénalité doublons : jusqu'à -20 points
        - Pénalité formats invalides : jusqu'à -20 points
        - Pénalité règles métier : jusqu'à -20 points
        - Pénalité outliers : jusqu'à -10 points
        """
        score = 100.0

        # Pénalité manquants
        missing = self.results.get("missing_values")
        if missing is not None:
            taux_global_manquants = missing["nb_manquants"].sum() / (self.n_rows * self.n_cols) * 100
            score -= min(30, taux_global_manquants * 3)

        # Pénalité doublons
        dup = self.results.get("duplicates", {})
        taux_dup = dup.get("taux_doublons_pct", 0)
        score -= min(20, taux_dup * 5)

        # Pénalité formats
        n_anomalies_format = sum(
            1 for a in self.anomalies
            if a["type"] in ("Format email invalide", "Format téléphone invalide",
                             "Format / date impossible", "Date future impossible")
        )
        score -= min(20, n_anomalies_format * 4)

        # Pénalité règles métier
        n_anomalies_regles = sum(
            1 for a in self.anomalies
            if a["type"] in ("Valeur hors liste autorisée", "Valeur hors plage", "Type incorrect")
        )
        score -= min(20, n_anomalies_regles * 5)

        # Pénalité outliers
        n_outliers_anomalies = sum(1 for a in self.anomalies if a["type"] == "Outlier statistique")
        score -= min(10, n_outliers_anomalies * 3)

        self.quality_score = max(0, round(score, 1))
        return self.quality_score

    # -------------------------------------------------------------------------
    # 8. RAPPORT COMPLET
    # -------------------------------------------------------------------------
    def run_full_audit(self,
                       key_col: str = None,
                       email_col: str = None,
                       phone_col: str = None,
                       date_cols: List[str] = None,
                       date_inscription_col: str = None,
                       allowed_values_rules: Dict = None,
                       numeric_range_rules: Dict = None,
                       outlier_cols: List[str] = None) -> Dict:
        """
        Lance l'audit complet et retourne un dictionnaire de résultats.

        Paramètres
        ----------
        key_col : colonne identifiant unique (ex: 'id_client')
        email_col : colonne email à valider
        phone_col : colonne téléphone à valider
        date_cols : liste de colonnes date à valider (format DD/MM/YYYY)
        date_inscription_col : colonne date d'inscription (format YYYY-MM-DD) à tester futur
        allowed_values_rules : dict {col: [valeurs_autorisées]}
        numeric_range_rules : dict {col: (min, max)}
        outlier_cols : liste de colonnes pour détection outliers
        """
        print(f"\n{'='*60}")
        print(f"  AUDIT QUALITÉ — {self.dataset_name}")
        print(f"  Date : {self.audit_date}")
        print(f"  Dimensions : {self.n_rows} lignes × {self.n_cols} colonnes")
        print(f"{'='*60}\n")

        print("▶ Contrôle 1 : Valeurs manquantes")
        self.check_missing_values()

        print("▶ Contrôle 2 : Doublons")
        self.check_duplicates(key_columns=[key_col] if key_col else None)

        if email_col:
            print(f"▶ Contrôle 3 : Format email ({email_col})")
            self.check_email_format(email_col)

        if phone_col:
            print(f"▶ Contrôle 4 : Format téléphone ({phone_col})")
            self.check_phone_format(phone_col)

        if date_cols:
            for col in date_cols:
                print(f"▶ Contrôle 5 : Format date ({col})")
                self.check_date_format(col, fmt="%d/%m/%Y")

        if date_inscription_col:
            print(f"▶ Contrôle 6 : Date future ({date_inscription_col})")
            self.check_future_dates(date_inscription_col, fmt="%Y-%m-%d")

        if allowed_values_rules:
            for col, vals in allowed_values_rules.items():
                print(f"▶ Contrôle 7 : Valeurs autorisées ({col})")
                self.check_allowed_values(col, vals)

        if numeric_range_rules:
            for col, (mn, mx) in numeric_range_rules.items():
                print(f"▶ Contrôle 8 : Plage numérique ({col})")
                self.check_numeric_range(col, mn, mx)

        if outlier_cols:
            for col in outlier_cols:
                print(f"▶ Contrôle 9 : Outliers ({col})")
                self.check_outliers_iqr(col)

        score = self.compute_quality_score()

        print(f"\n{'='*60}")
        print(f"  SCORE DE QUALITÉ GLOBAL : {score}/100")
        grade = ("EXCELLENT" if score >= 90 else
                 "BON" if score >= 75 else
                 "PASSABLE" if score >= 60 else
                 "INSUFFISANT" if score >= 40 else "CRITIQUE")
        print(f"  NIVEAU : {grade}")
        print(f"  Anomalies détectées : {len(self.anomalies)}")
        print(f"{'='*60}\n")

        return {
            "score": score,
            "grade": grade,
            "n_anomalies": len(self.anomalies),
            "anomalies": self.anomalies,
            "details": self.results
        }

    def print_anomaly_report(self):
        """Affiche le rapport d'anomalies dans la console."""
        print(f"\n{'─'*60}")
        print(f"  RAPPORT D'ANOMALIES — {len(self.anomalies)} problème(s) détecté(s)")
        print(f"{'─'*60}")
        for i, a in enumerate(self.anomalies, 1):
            impact_symbol = {"ÉLEVÉ": "🔴", "MOYEN": "🟡", "FAIBLE": "🟢"}.get(a["impact"], "⚪")
            print(f"  {i:02d}. [{impact_symbol} {a['impact']}] {a['type']}")
            print(f"      → {a['detail']}")
        print()
