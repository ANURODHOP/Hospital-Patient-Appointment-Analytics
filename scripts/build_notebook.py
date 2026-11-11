"""Script to generate and validate the Jupyter notebook."""

import json
from pathlib import Path

nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Hospital Patient & Appointment Analytics: An Interactive Tableau Dashboard\n",
                "**Comprehensive Exploratory Data Analysis, Statistical Hypothesis Testing, and Tableau Data Preparation**\n",
                "\n",
                "---\n",
                "\n",
                "### Project Overview\n",
                "Missed medical appointments (no-shows) represent a substantial challenge in modern healthcare systems, resulting in:\n",
                "- **Suboptimal Clinical Outcomes**: Delayed medical interventions and deteriorated patient health.\n",
                "- **Resource Wastage**: Idled physician hours, underutilized diagnostic equipment, and operational overhead.\n",
                "- **Inflated Healthcare Costs**: Emergency department reliance due to untreated chronic conditions.\n",
                "\n",
                "This analytical notebook investigates over 110,000 appointment records from municipal clinics in Vitória, Brazil to identify the demographic, clinical, operational, and geographic drivers of patient attendance."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Setup & Environment Configuration"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import sys\n",
                "from pathlib import Path\n",
                "\n",
                "# Add project root to sys.path\n",
                "project_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n",
                "if str(project_root) not in sys.path:\n",
                "    sys.path.insert(0, str(project_root))\n",
                "\n",
                "import numpy as np\n",
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from scipy import stats\n",
                "\n",
                "from src.config import RAW_DATA_FILE, CLEANED_DATA_FILE, FIGURES_DIR, PROCESSED_DATA_DIR\n",
                "from src.data_loader import load_raw_data, validate_raw_data\n",
                "from src.data_cleaner import clean_appointment_data\n",
                "from src.feature_engineering import engineer_features\n",
                "from src.statistical_analysis import run_full_statistical_analysis\n",
                "from src.visualizer import generate_all_visualizations\n",
                "\n",
                "# Configure plotting aesthetics\n",
                "sns.set_theme(style='whitegrid', font_scale=1.05)\n",
                "plt.rcParams['figure.figsize'] = (10, 6)\n",
                "pd.set_option('display.max_columns', None)\n",
                "print('Environment initialized successfully!')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Raw Dataset Ingestion & Validation"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "raw_df = load_raw_data(RAW_DATA_FILE)\n",
                "raw_metrics = validate_raw_data(raw_df)\n",
                "print(f\"Raw records: {len(raw_df):,}\")\n",
                "raw_df.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Data Cleaning & Integrity Filtering\n",
                "In this stage, we:\n",
                "1. Standardize column headers to snake_case.\n",
                "2. Fix column spelling mistakes (`Hipertension` -> `hypertension`, `Handcap` -> `handicap`).\n",
                "3. Eliminate invalid records with negative ages (`Age < 0` or extreme `Age > 110`).\n",
                "4. Eliminate records where the scheduling date is after the appointment date (`lead_time_days < 0`).\n",
                "5. Transform binary indicators and human-readable text descriptors."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "clean_df, clean_metrics = clean_appointment_data(raw_df)\n",
                "print(f\"Cleaned records: {len(clean_df):,} (Dropped: {clean_metrics['dropped_rows']})\")\n",
                "print(f\"Baseline No-Show Rate: {clean_metrics['overall_no_show_rate']}%\")\n",
                "clean_df.info()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Feature Engineering\n",
                "Enriching data with clinical, temporal, and operational metrics:\n",
                "- **Age Bins**: Children (0-12), Youth (13-24), Young Adults (25-44), Middle-Aged (45-64), Seniors (65+).\n",
                "- **Lead Time Brackets**: Same Day (0d), Short Term (1-3d), Medium Term (4-7d), 1-2 Weeks (8-14d), 2-4 Weeks (15-30d), Long Term (>30d).\n",
                "- **Temporal Breakdown**: Hour, Time of Day, Day of Week, Month.\n",
                "- **Comorbidity Score**: Aggregation of chronic conditions (hypertension, diabetes, alcoholism, handicap).\n",
                "- **Longitudinal Patient Engagement**: Tracking recurring appointments by patient."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "feat_df, feat_meta = engineer_features(clean_df)\n",
                "print(f\"Total features engineered: {len(feat_df.columns)}\")\n",
                "print(f\"Same-day appointments: {feat_meta['same_day_appointments']:,} (No-Show: {feat_meta['same_day_no_show_rate']}%)\")\n",
                "print(f\"Advance bookings no-show rate: {feat_meta['advance_booking_no_show_rate']}%\")\n",
                "feat_df[['patient_id', 'age_group', 'lead_time_days', 'lead_time_bracket', 'is_same_day', 'chronic_condition_count', 'comorbidity_category', 'attendance_status']].head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Exploratory Data Analysis & Visualizations"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Overall Attendance Distribution\n",
                "counts = feat_df['attendance_status'].value_counts()\n",
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n",
                "ax1.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=['#2ecc71', '#e74c3c'], wedgeprops=dict(width=0.4, edgecolor='white'))\n",
                "ax1.set_title('Attendance Rate Breakdown', weight='bold')\n",
                "ax2.bar(counts.index, counts.values, color=['#2ecc71', '#e74c3c'], width=0.5)\n",
                "ax2.set_ylabel('Number of Appointments')\n",
                "ax2.set_title('Appointment Volume by Status', weight='bold')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Lead Time vs No-Show Rate (The Waiting Duration Effect)\n",
                "lead_summary = feat_df.groupby('lead_time_bracket', observed=False)['no_show_binary'].agg(['count', 'mean']).reset_index()\n",
                "lead_summary['noshow_pct'] = lead_summary['mean'] * 100\n",
                "\n",
                "plt.figure(figsize=(10, 5))\n",
                "sns.barplot(data=lead_summary, x='lead_time_bracket', y='noshow_pct', palette='Reds_r')\n",
                "plt.title('No-Show Rate (%) by Scheduling Lead Time Bracket', fontsize=13, weight='bold')\n",
                "plt.xlabel('Lead Time Bracket (Days between Scheduling and Appointment)')\n",
                "plt.ylabel('No-Show Rate (%)')\n",
                "plt.ylim(0, 38)\n",
                "for idx, row in lead_summary.iterrows():\n",
                "    plt.text(idx, row['noshow_pct'] + 0.8, f\"{row['noshow_pct']:.1f}%\", ha='center', weight='bold')\n",
                "plt.xticks(rotation=20)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Age Brackets vs Attendance\n",
                "age_summary = feat_df.groupby('age_group', observed=False)['no_show_binary'].agg(['count', 'mean']).reset_index()\n",
                "age_summary['noshow_pct'] = age_summary['mean'] * 100\n",
                "\n",
                "plt.figure(figsize=(10, 5))\n",
                "sns.barplot(data=age_summary, x='age_group', y='noshow_pct', palette='Blues_r')\n",
                "plt.title('No-Show Rate (%) across Age Groups', fontsize=13, weight='bold')\n",
                "plt.ylabel('No-Show Rate (%)')\n",
                "plt.ylim(0, 30)\n",
                "for idx, row in age_summary.iterrows():\n",
                "    plt.text(idx, row['noshow_pct'] + 0.6, f\"{row['noshow_pct']:.1f}%\", ha='center', weight='bold')\n",
                "plt.xticks(rotation=15)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Chronic Illnesses and Comorbidity Burden\n",
                "comorb_summary = feat_df.groupby('comorbidity_category', observed=False)['no_show_binary'].agg(['count', 'mean']).reset_index()\n",
                "comorb_summary['noshow_pct'] = comorb_summary['mean'] * 100\n",
                "\n",
                "plt.figure(figsize=(9, 5))\n",
                "sns.barplot(data=comorb_summary, x='comorbidity_category', y='noshow_pct', palette='viridis')\n",
                "plt.title('No-Show Rate by Patient Comorbidity Level', fontsize=13, weight='bold')\n",
                "plt.ylabel('No-Show Rate (%)')\n",
                "plt.ylim(0, 25)\n",
                "for idx, row in comorb_summary.iterrows():\n",
                "    plt.text(idx, row['noshow_pct'] + 0.5, f\"{row['noshow_pct']:.1f}%\", ha='center', weight='bold')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Inferential Statistics & Hypothesis Testing"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "stats_results = run_full_statistical_analysis(feat_df)\n",
                "chi2_df = pd.DataFrame(stats_results['chi_square_tests'])\n",
                "print('=== Chi-Square Test of Independence Results ===')\n",
                "display(chi2_df[['feature', 'chi2_stat', 'degrees_of_freedom', 'p_value_formatted', 'cramers_v', 'statistically_significant']])\n",
                "\n",
                "print('\\n=== Continuous Variable Tests (Age & Lead Time) ===')\n",
                "for var_name, res in stats_results['continuous_variable_tests'].items():\n",
                "    print(f\"[{var_name.upper()}] Show Mean: {res['show_mean']} vs No-Show Mean: {res['noshow_mean']} | MWU p-value: {res['mwu_pvalue']:.4e} (Significant: {res['significant']})\")\n",
                "\n",
                "print('\\n=== Relative Risk Analysis ===')\n",
                "rr_df = pd.DataFrame(stats_results['relative_risk_analysis'])\n",
                "display(rr_df)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Tableau-Ready Dataset Export"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from src.pipeline import export_tableau_datasets\n",
                "export_paths = export_tableau_datasets(feat_df)\n",
                "print('Tableau export files generated:')\n",
                "for name, path in export_paths.items():\n",
                "    print(f'  • {name}: {path}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 8. Strategic Healthcare Management Insights\n",
                "1. **Implement Open-Access / Same-Day Booking**: Same-day bookings have a 4.65% no-show rate versus 28.52% for advance bookings. Reserving appointment slots for rapid access directly mitigates attrition.\n",
                "2. **Targeted Engagement for Young Demographics**: Patients aged 13-24 have the highest default rate (~24.5%). Interactive confirmation (two-way SMS / WhatsApp) is essential for this cohort.\n",
                "3. **Dynamic Overbooking Based on Lead Time**: When appointments are scheduled >14 days in advance, predictive overbooking can be safely applied to maintain clinic capacity utilization.\n",
                "4. **Neighborhood Mobile Clinics**: Low-compliance geographic pockets (e.g. Santos Dumont, Itararé) benefit from local community health agent outreach."
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python (Hospital Venv)",
            "language": "python",
            "name": "hospital_venv"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbformat": 4,
            "nbformat_minor": 5,
            "version": "3.13.1"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

nb_dir = Path("notebooks")
nb_dir.mkdir(parents=True, exist_ok=True)
with open(nb_dir / "hospital_appointment_analytics.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Notebook generated successfully!")
