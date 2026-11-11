"""Data Cleaner Module for Hospital Patient & Appointment Analytics.

Performs data cleansing, column renaming, type casting, domain rule validation,
and anomaly filtering on raw appointment data.
"""

import logging
from typing import Tuple, Dict, Any
import pandas as pd

from src.config import RENAME_COLUMNS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def clean_appointment_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Clean the raw medical appointments DataFrame.

    Operations performed:
    1. Standardize column names to snake_case.
    2. Convert IDs to integers.
    3. Convert timestamp strings to pandas datetime objects.
    4. Normalize scheduled and appointment dates.
    5. Filter invalid age entries (age < 0 or age > 110).
    6. Filter impossible negative lead time anomalies (appointment booked in past).
    7. Standardize binary indicators and create clear status labels.
    8. Map gender abbreviations to full names.

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame as loaded from CSV.

    Returns
    -------
    Tuple[pd.DataFrame, Dict[str, Any]]
        A tuple of (cleaned_df, cleaning_metrics_dict).
    """
    initial_rows = len(df)
    logger.info(f"Starting data cleaning on {initial_rows:,} records...")

    # 1. Standardize column names
    clean_df = df.rename(columns=RENAME_COLUMNS).copy()

    # 2. Type casting for IDs
    clean_df["patient_id"] = clean_df["patient_id"].astype("int64")
    clean_df["appointment_id"] = clean_df["appointment_id"].astype("int64")

    # 3. Parse Datetimes
    clean_df["scheduled_datetime"] = pd.to_datetime(clean_df["scheduled_datetime"])
    clean_df["appointment_date"] = pd.to_datetime(clean_df["appointment_date"]).dt.tz_localize(None).dt.normalize()
    clean_df["scheduled_date"] = clean_df["scheduled_datetime"].dt.tz_localize(None).dt.normalize()

    # Calculate preliminary lead time to identify anomalous negative values
    lead_time_days = (clean_df["appointment_date"] - clean_df["scheduled_date"]).dt.days

    # 4. Filter invalid rows
    # Invalid ages: < 0 or > 110
    invalid_age_mask = (clean_df["age"] < 0) | (clean_df["age"] > 110)
    invalid_age_count = int(invalid_age_mask.sum())

    # Invalid lead time: < 0 days (scheduled after appointment date)
    invalid_lead_mask = lead_time_days < 0
    invalid_lead_count = int(invalid_lead_mask.sum())

    # Filter valid records
    valid_mask = (~invalid_age_mask) & (~invalid_lead_mask)
    clean_df = clean_df[valid_mask].copy()
    clean_df["lead_time_days"] = (clean_df["appointment_date"] - clean_df["scheduled_date"]).dt.days

    # 5. Target variable standardization
    clean_df["no_show_raw"] = clean_df["no_show_raw"].str.strip()
    clean_df["no_show_binary"] = (clean_df["no_show_raw"] == "Yes").astype(int)
    clean_df["showed_up_binary"] = (clean_df["no_show_raw"] == "No").astype(int)
    clean_df["attendance_status"] = clean_df["no_show_binary"].map({1: "No Show", 0: "Showed Up"})

    # 6. Handicap standardization
    clean_df["handicap_count"] = clean_df["handicap"].astype(int)
    clean_df["has_handicap"] = (clean_df["handicap_count"] > 0).astype(int)

    # 7. Descriptive text mappings for clear dashboards and reports
    clean_df["gender_full"] = clean_df["gender"].map({"F": "Female", "M": "Male"})
    clean_df["scholarship_desc"] = clean_df["scholarship"].map({1: "Bolsa Família Enrolled", 0: "No Welfare"})
    clean_df["hypertension_desc"] = clean_df["hypertension"].map({1: "Hypertensive", 0: "Normal BP"})
    clean_df["diabetes_desc"] = clean_df["diabetes"].map({1: "Diabetic", 0: "Non-Diabetic"})
    clean_df["alcoholism_desc"] = clean_df["alcoholism"].map({1: "Alcohol Use Disorder", 0: "No Alcohol Disorder"})
    clean_df["sms_desc"] = clean_df["sms_received"].map({1: "SMS Reminder Received", 0: "No SMS Sent"})

    # Reset index
    clean_df = clean_df.reset_index(drop=True)
    final_rows = len(clean_df)
    dropped_rows = initial_rows - final_rows

    cleaning_metrics = {
        "initial_rows": initial_rows,
        "final_rows": final_rows,
        "dropped_rows": dropped_rows,
        "dropped_percentage": round((dropped_rows / initial_rows) * 100, 4),
        "invalid_age_count": invalid_age_count,
        "invalid_lead_time_count": invalid_lead_count,
        "overall_no_show_rate": round(clean_df["no_show_binary"].mean() * 100, 2),
    }

    logger.info("Data Cleaning Completed:")
    logger.info(f"  • Rows Retained: {final_rows:,} / {initial_rows:,} (dropped {dropped_rows})")
    logger.info(f"  • Invalid Ages Dropped: {invalid_age_count}")
    logger.info(f"  • Negative Lead Times Dropped: {invalid_lead_count}")
    logger.info(f"  • Overall Baseline No-Show Rate: {cleaning_metrics['overall_no_show_rate']}%")

    return clean_df, cleaning_metrics
