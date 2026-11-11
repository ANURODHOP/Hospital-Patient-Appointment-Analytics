# Hospital Patient & Appointment Analytics: An Interactive Tableau Dashboard

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2+-green.svg)](https://pandas.pydata.org/)
[![Tableau](https://img.shields.io/badge/Tableau-Public%20%7C%20Desktop-orange.svg)](https://public.tableau.com/)
[![Tests](https://img.shields.io/badge/Pytest-Passing-brightgreen.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-Academic%20%2F%20CC%20BY--NC--SA-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

An end-to-end healthcare data analytics, statistical hypothesis testing, and interactive business intelligence dashboard suite designed to investigate and mitigate patient no-shows across **110,516 validated clinical appointments** in municipal clinics of Vitória, Brazil.

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Key Empirical Discoveries](#key-empirical-discoveries)
3. [Project Directory Architecture](#project-directory-architecture)
4. [Dataset Information](#dataset-information)
5. [Quickstart & Installation (Beginner-Friendly)](#quickstart--installation-beginner-friendly)
6. [Automated Pipeline Execution](#automated-pipeline-execution)
7. [Automated Test Suite](#automated-test-suite)
8. [Jupyter Notebook Walkthrough](#jupyter-notebook-walkthrough)
9. [Tableau Dashboards Implementation Guide](#tableau-dashboards-implementation-guide)
10. [Academic Reports & Viva Preparation](#academic-reports--viva-preparation)

---

## 1. Project Overview

Missed medical appointments ("no-shows") cost healthcare systems billions annually, underutilize expensive physician and diagnostic capacity, and delay clinical care for patients suffering from chronic diseases. 

This repository provides:
- **Modular Data Engineering**: Clean, typed Python pipeline (`src/`) for schema validation, anomaly removal, feature engineering, and statistical tests.
- **Publication-Quality Figures**: 9 high-resolution analytical charts (`reports/figures/`).
- **Statistical Rigor**: Chi-Square tests of independence, Cramér's V effect sizes, Mann-Whitney U tests, Welch's t-tests, and Relative Risk / Odds Ratio calculations.
- **Tableau Public BI Suite**: 4 fully specified interactive dashboards with calculated field formulas and layout specifications.
- **Academic Project Deliverables**: Complete DAV Project Report and Viva Q&A guide.

---

## 2. Key Empirical Discoveries

- **The Lead-Time Dominance**: Scheduling lead time (waiting days) is the single strongest operational driver of attendance. Same-day bookings have a **4.65% no-show rate**, whereas bookings made $>30$ days in advance experience a **33.1% no-show rate** ($\chi^2 = 9623.1, p < 0.0001, \text{Cramér's } V = 0.295$).
- **Demographic Parity**: Patient gender does not influence attendance ($p = 0.1755$).
- **Age Inversion**: Youth (13–24) have the highest default rate (**24.53%**), while Seniors (65+) are the most compliant (**15.23%**).
- **The Chronic Care Effect**: Patients managing hypertension (17.3% no-show) and diabetes (18.0% no-show) attend significantly more reliably than patients without chronic diagnoses (20.9% no-show).
- **The SMS Confounder**: SMS reminders are only dispatched for advance appointments ($\ge 3$ days), which inherently have a high default baseline ($>28\%$).

---

## 3. Project Directory Architecture

```
Hospital Patient & Appointment Analytic/
├── .gitignore                                  # Git exclusion definitions
├── README.md                                   # Master project guide
├── requirements.txt                            # Pinned Python package dependencies
├── data/
│   ├── raw/
│   │   └── KaggleV2-May-2016.csv              # Original Kaggle dataset (110,527 rows)
│   └── processed/
│       ├── hospital_appointments_cleaned.csv  # Cleaned master dataset (110,516 rows)
│       ├── tableau_executive_overview.csv     # Aggregated for Dashboard 1
│       ├── tableau_demographics_health.csv    # Aggregated for Dashboard 2
│       ├── tableau_scheduling_operations.csv  # Aggregated for Dashboard 3
│       └── tableau_neighborhood_analytics.csv # Aggregated for Dashboard 4
├── src/
│   ├── __init__.py
│   ├── config.py                              # Centralized paths, bins, and palettes
│   ├── data_loader.py                         # Loading, schema validation & null audits
│   ├── data_cleaner.py                        # Anomaly removal & standardizations
│   ├── feature_engineering.py                 # Clinical, temporal, & demographic features
│   ├── statistical_analysis.py                # Chi-Square, MWU, Welch t-test, RR & OR
│   ├── visualizer.py                          # 9 publication-grade Matplotlib/Seaborn plots
│   └── pipeline.py                            # End-to-end pipeline orchestrator
├── notebooks/
│   └── hospital_appointment_analytics.ipynb   # Executed Jupyter Notebook with outputs
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py                    # Unit tests for ingestion
│   ├── test_data_cleaner.py                   # Unit tests for cleansing rules
│   ├── test_feature_engineering.py            # Unit tests for derived variables
│   ├── test_statistical_analysis.py           # Unit tests for inferential functions
│   └── test_pipeline.py                       # Full integration test
├── reports/
│   ├── statistical_summary_report.md          # Automated statistical output tables
│   ├── dav_project_report.md                  # Comprehensive academic/technical report
│   ├── viva_questions_and_answers.md          # 15 detailed examination Q&A
│   └── figures/                               # 9 high-resolution generated figures
└── tableau/
    ├── README.md                              # Tableau connection guide & architecture
    ├── calculated_fields_reference.md         # Copy-paste calculated field formulas
    ├── dashboard_1_executive_overview.md      # Click-by-click guide for Dashboard 1
    ├── dashboard_2_demographics_health.md     # Click-by-click guide for Dashboard 2
    ├── dashboard_3_operational_scheduling.md  # Click-by-click guide for Dashboard 3
    └── dashboard_4_neighborhood_attendance.md # Click-by-click guide for Dashboard 4
```

---

## 4. Dataset Information

- **Dataset**: *Medical Appointment No Shows* from Kaggle
- **URL**: [https://www.kaggle.com/datasets/joniarroba/noshowappointments](https://www.kaggle.com/datasets/joniarroba/noshowappointments)
- **Primary Raw File**: `data/raw/KaggleV2-May-2016.csv`
- **Location**: The dataset is already downloaded and validated in `data/raw/`.
- *(Manual Download Fallback)*: If you ever need to download it manually:
  1. Visit the Kaggle link above.
  2. Download the `.zip` archive.
  3. Extract `KaggleV2-May-2016.csv` directly into the `data/raw/` directory.

---

## 5. Quickstart & Installation (Beginner-Friendly)

Follow these step-by-step instructions in PowerShell or Terminal:

### Step 5.1: Clone or Navigate to the Workspace
```powershell
cd "c:\IMP\Big potato project\Hospital Patient & Appointment Analytic"
```

### Step 5.2: Create and Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1
```

### Step 5.3: Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 6. Automated Pipeline Execution

To run the complete data engineering, statistical modeling, chart generation, and Tableau export pipeline in one command:

```powershell
.\venv\Scripts\python -m src.pipeline
```

**Expected Console Output**:
- Validates 110,527 raw rows.
- Cleans and drops 11 anomalous records (retaining 110,516 rows).
- Computes inferential statistics ($\chi^2$, Mann-Whitney U, Welch t-test, Relative Risk).
- Saves statistical summary to `reports/statistical_summary_report.md`.
- Generates 9 PNG figures in `reports/figures/`.
- Exports 5 Tableau-ready CSV files in `data/processed/`.

---

## 7. Automated Test Suite

We use `pytest` for unit and integration testing:

```powershell
.\venv\Scripts\pytest -v
```

All 9 test suites verify data loading, negative age filtering, lead time calculation, comorbidity derivation, statistical mathematics, and file generation.

---

## 8. Jupyter Notebook Walkthrough

An interactive, fully executed Jupyter Notebook is provided at `notebooks/hospital_appointment_analytics.ipynb`.

To open it in your browser:
```powershell
.\venv\Scripts\jupyter notebook notebooks/hospital_appointment_analytics.ipynb
```
Select the **Python (Hospital Venv)** kernel. All plots, dataframes, and statistical summaries are embedded directly inside.

---

## 9. Tableau Dashboards Implementation Guide

The project includes step-by-step construction guides for 4 interactive Tableau dashboards:

| Dashboard | File Guide | Target Focus |
| :--- | :--- | :--- |
| **Dashboard 1** | [`tableau/dashboard_1_executive_overview.md`](file:///c:/IMP/Big%20potato%20project/Hospital%20Patient%20&%20Appointment%20Analytic/tableau/dashboard_1_executive_overview.md) | High-level KPIs, daily volume trends, SMS impact |
| **Dashboard 2** | [`tableau/dashboard_2_demographics_health.md`](file:///c:/IMP/Big%20potato%20project/Hospital%20Patient%20&%20Appointment%20Analytic/tableau/dashboard_2_demographics_health.md) | Age cohorts, gender parity, chronic comorbidities |
| **Dashboard 3** | [`tableau/dashboard_3_operational_scheduling.md`](file:///c:/IMP/Big%20potato%20project/Hospital%20Patient%20&%20Appointment%20Analytic/tableau/dashboard_3_operational_scheduling.md) | The waiting-time curve, booking hour heatmap |
| **Dashboard 4** | [`tableau/dashboard_4_neighborhood_attendance.md`](file:///c:/IMP/Big%20potato%20project/Hospital%20Patient%20&%20Appointment%20Analytic/tableau/dashboard_4_neighborhood_attendance.md) | Clinic neighborhood rankings, regional disparity |

All copy-paste formulas for Tableau calculated fields are cataloged in [`tableau/calculated_fields_reference.md`](file:///c:/IMP/Big%20potato%20project/Hospital%20Patient%20&%20Appointment%20Analytic/tableau/calculated_fields_reference.md).

---

## 10. Academic Reports & Viva Preparation

- **Full DAV Project Report**: [`reports/dav_project_report.md`](file:///c:/IMP/Big%20potato project/Hospital%20Patient%20&%20Appointment%20Analytic/reports/dav_project_report.md)
- **Viva Questions & Answers**: [`reports/viva_questions_and_answers.md`](file:///c:/IMP/Big%20potato%20project/Hospital%20Patient%20&%20Appointment%20Analytic/reports/viva_questions_and_answers.md)
- **Statistical Tables**: [`reports/statistical_summary_report.md`](file:///c:/IMP/Big%20potato%20project/Hospital%20Patient%20&%20Appointment%20Analytic/reports/statistical_summary_report.md)
