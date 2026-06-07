# Rapport d'Audit Qualité — Clients_Raw_Sample

**Date :** 2024-12-01 14:30  
**Dimensions :** 31 lignes × 11 colonnes  
**Score global :** 58/100 — **INSUFFISANT**

> *Ce rapport est un exemple généré automatiquement par le Data Quality Audit Framework.*  
> *Données simulées à des fins pédagogiques — aucune donnée réelle.*

---

## 1. Synthèse exécutive

| Indicateur | Valeur |
|-----------|--------|
| Score de qualité global | **58/100** |
| Niveau | **INSUFFISANT** |
| Nombre d'anomalies détectées | **12** |
| Anomalies critiques (ÉLEVÉ) | **8** |
| Anomalies modérées (MOYEN) | **3** |
| Anomalies mineures (FAIBLE) | **1** |

---

## 2. Détail des anomalies détectées

| # | Impact | Type | Détail |
|---|--------|------|--------|
| 1 | 🔴 ÉLEVÉ | Doublons | 4 lignes entièrement dupliquées (C001 × 2, C002 × 2) |
| 2 | 🔴 ÉLEVÉ | Format / date impossible | 3 date(s) invalide(s) dans 'date_naissance' (29/02/1993, 31/04/1982, 31/02/1993) |
| 3 | 🔴 ÉLEVÉ | Valeur hors liste autorisée | 5 valeur(s) non conforme(s) dans 'statut' : ['ACTIF', 'Actif', 'active', 'Inactif', 'INACTIF'] |
| 4 | 🔴 ÉLEVÉ | Type incorrect | 1 valeur non numérique dans 'montant_contrat' : 'ABC' |
| 5 | 🔴 ÉLEVÉ | Valeur hors plage | 2 valeur(s) hors plage [0, 99999] dans 'montant_contrat' (-200, 250000) |
| 6 | 🔴 ÉLEVÉ | Date future impossible | 1 date dans le futur dans 'date_inscription' : 2026-12-31 |
| 7 | 🔴 ÉLEVÉ | Valeurs manquantes | email : 2 (6,5%), telephone : 2 (6,5%), prenom : 1 (3,2%), montant_contrat : 1 (3,2%), date_naissance : 2 (6,5%) |
| 8 | 🟡 MOYEN | Format email invalide | 2 adresse(s) email mal formée(s) : ['sophie.bernard', 'francois.boyer'] |
| 9 | 🟡 MOYEN | Format téléphone invalide | 2 numéro(s) invalide(s) : ['06123', '06 98 76 54 32'] |
| 10 | 🟡 MOYEN | Outlier statistique | 1 valeur aberrante dans 'montant_contrat' (250 000 € > borne IQR = ~6 575 €) |
| 11 | 🟢 FAIBLE | Format téléphone invalide | Espaces dans le numéro : normalisation possible |

---

## 3. Plan de correction recommandé

| Priorité | Action | Impact attendu |
|---------|--------|---------------|
| 1 — Immédiat | Supprimer les 4 lignes dupliquées | Intégrité des données |
| 2 — Court terme | Corriger les 3 dates de naissance impossibles | Fiabilité des analyses temporelles |
| 3 — Court terme | Normaliser les statuts en minuscules (actif/inactif/suspendu) | Cohérence des segments |
| 4 — Moyen terme | Corriger les 2 emails invalides (manque le @) | Qualité des campagnes email |
| 5 — Moyen terme | Vérifier le montant à 250 000 € avec le métier | Fiabilité financière |
| 6 — Long terme | Mettre en place des contrôles qualité à la source | Prévention en amont |

---

## 4. Recommandations de gouvernance

- Définir un **dictionnaire de données** avec les règles de chaque colonne
- Mettre en place des **contrôles à la saisie** dans le formulaire ou le CRM
- Automatiser cet audit qualité à chaque chargement de nouvelles données
- Documenter un **score de qualité minimal acceptable** avant publication d'un rapport
- Désigner un **Data Steward** (responsable qualité des données) par périmètre métier

---

*Rapport généré automatiquement par le Data Quality Audit Framework*  
*Auteur : Emmanuel TSAGUE — Data Scientist / Data Analyst*
