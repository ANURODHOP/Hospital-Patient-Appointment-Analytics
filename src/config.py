"""Configuration module for Hospital Patient & Appointment Analytics.

Centralizes paths, column mappings, categorical orderings, bin definitions,
and visualization settings across the entire analytical pipeline.
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLEAU_DIR = PROJECT_ROOT / "tableau"

# File Paths
RAW_DATA_FILE = RAW_DATA_DIR / "KaggleV2-May-2016.csv"
CLEANED_DATA_FILE = PROCESSED_DATA_DIR / "hospital_appointments_cleaned.csv"

# Tableau Export Targets
TABLEAU_EXEC_FILE = PROCESSED_DATA_DIR / "tableau_executive_overview.csv"
TABLEAU_DEMOG_FILE = PROCESSED_DATA_DIR / "tableau_demographics_health.csv"
TABLEAU_SCHED_FILE = PROCESSED_DATA_DIR / "tableau_scheduling_operations.csv"
TABLEAU_NEIGHBORHOOD_FILE = PROCESSED_DATA_DIR / "tableau_neighborhood_analytics.csv"

# Column Name Standardization
RENAME_COLUMNS = {
    "PatientId": "patient_id",
    "AppointmentID": "appointment_id",
    "Gender": "gender",
    "ScheduledDay": "scheduled_datetime",
    "AppointmentDay": "appointment_date",
    "Age": "age",
    "Neighbourhood": "neighbourhood",
    "Scholarship": "scholarship",
    "Hipertension": "hypertension",  # Fix original Kaggle typo
    "Diabetes": "diabetes",
    "Alcoholism": "alcoholism",
    "Handcap": "handicap",          # Fix original Kaggle typo
    "SMS_received": "sms_received",
    "No-show": "no_show_raw",
}

# Feature Engineering Bins & Labels
AGE_BINS = [-1, 12, 24, 44, 64, 125]
AGE_LABELS = ["Children (0-12)", "Youth (13-24)", "Young Adults (25-44)", "Middle-Aged (45-64)", "Seniors (65+)"]

LEAD_TIME_BINS = [-1, 0, 3, 7, 14, 30, 180]
LEAD_TIME_LABELS = [
    "Same Day (0d)",
    "Short Term (1-3d)",
    "Medium Term (4-7d)",
    "1-2 Weeks (8-14d)",
    "2-4 Weeks (15-30d)",
    "Long Term (>30d)",
]

# Color Palette for Visualizations
PALETTE_ATTENDANCE = {
    "Showed Up": "#2ecc71",     # Emerald Green
    "No Show": "#e74c3c",       # Crimson Red
}
PALETTE_PRIMARY = "#3498db"     # Classic Blue
PALETTE_SECONDARY = "#9b59b6"   # Purple
PALETTE_ACCENT = "#f39c12"      # Amber Orange
