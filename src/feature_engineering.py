"""Feature Engineering Module for Hospital Patient & Appointment Analytics.

Derives temporal, clinical, behavioral, and demographic features from cleaned
appointment records to enrich statistical models and interactive Tableau dashboards.
"""

import logging
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np

from src.config import AGE_BINS, AGE_LABELS, LEAD_TIME_BINS, LEAD_TIME_LABELS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def engineer_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Generate analytical features from cleaned appointment data.

    Features created:
    - `age_group`: Categorical age bands (Children, Youth, Young Adults, Middle-Aged, Seniors).
    - `lead_time_bracket`: Categorical waiting duration brackets.
    - `is_same_day`: 1 if booked on the day of appointment, else 0.
    - `scheduled_hour`: Hour of booking (0-23).
    - `scheduled_time_of_day`: Morning (6-11), Afternoon (12-16), Evening (17-21), Night/Early (22-5).
    - `appointment_day_of_week`: Full day name (Monday - Saturday).
    - `appointment_day_num`: Integer representation (0=Monday ... 6=Sunday).
    - `is_weekend`: 1 if Saturday or Sunday, else 0.
    - `appointment_month`: Month name of appointment.
    - `appointment_week`: Calendar week number of appointment.
    - `chronic_condition_count`: Sum of hypertension, diabetes, alcoholism, and handicap.
    - `has_chronic_condition`: 1 if patient has at least one condition, else 0.
    - `comorbidity_category`: 'No Chronic Conditions', 'Single Condition', 'Multimorbid (2+)'.
    - `patient_appointment_count`: Total appointments recorded for this patient.
    - `is_repeat_patient`: 1 if patient appears more than once, else 0.
    - `neighbourhood_no_show_rate`: Historical no-show percentage of the clinic's neighborhood.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned appointment DataFrame.

    Returns
    -------
    Tuple[pd.DataFrame, Dict[str, Any]]
        Tuple containing feature-enriched DataFrame and summary metadata.
    """
    logger.info("Starting feature engineering...")
    feat_df = df.copy()

    # 1. Demographic Features: Age Group Binning
    feat_df["age_group"] = pd.cut(
        feat_df["age"],
        bins=AGE_BINS,
        labels=AGE_LABELS,
        right=True,
        include_lowest=True,
    )

    # 2. Operational Features: Lead Time Categorization
    feat_df["lead_time_bracket"] = pd.cut(
        feat_df["lead_time_days"],
        bins=LEAD_TIME_BINS,
        labels=LEAD_TIME_LABELS,
        right=True,
        include_lowest=True,
    )
    feat_df["is_same_day"] = (feat_df["lead_time_days"] == 0).astype(int)

    # 3. Temporal Features: Scheduling Datetime Breakdown
    feat_df["scheduled_hour"] = feat_df["scheduled_datetime"].dt.hour

    def categorize_time_of_day(hour: int) -> str:
        if 6 <= hour < 12:
            return "Morning (06:00-11:59)"
        elif 12 <= hour < 17:
            return "Afternoon (12:00-16:59)"
        elif 17 <= hour < 21:
            return "Evening (17:00-20:59)"
        else:
            return "Night / Early Morning"

    feat_df["scheduled_time_of_day"] = feat_df["scheduled_hour"].apply(categorize_time_of_day)

    # 4. Temporal Features: Appointment Date Breakdown
    feat_df["appointment_day_of_week"] = feat_df["appointment_date"].dt.day_name()
    feat_df["appointment_day_num"] = feat_df["appointment_date"].dt.day_of_week
    feat_df["is_weekend"] = feat_df["appointment_day_num"].isin([5, 6]).astype(int)
    feat_df["appointment_month"] = feat_df["appointment_date"].dt.month_name()
    feat_df["appointment_week"] = feat_df["appointment_date"].dt.isocalendar().week.astype(int)

    # 5. Clinical & Comorbidity Features
    feat_df["chronic_condition_count"] = (
        feat_df["hypertension"]
        + feat_df["diabetes"]
        + feat_df["alcoholism"]
        + feat_df["has_handicap"]
    )
    feat_df["has_chronic_condition"] = (feat_df["chronic_condition_count"] > 0).astype(int)

    def categorize_comorbidity(count: int) -> str:
        if count == 0:
            return "No Chronic Conditions"
        elif count == 1:
            return "Single Condition"
        else:
            return "Multimorbid (2+ Conditions)"

    feat_df["comorbidity_category"] = feat_df["chronic_condition_count"].apply(categorize_comorbidity)

    # 6. Patient Engagement & Longitudinal Features
    patient_counts = feat_df.groupby("patient_id")["appointment_id"].transform("count")
    feat_df["patient_appointment_count"] = patient_counts
    feat_df["is_repeat_patient"] = (feat_df["patient_appointment_count"] > 1).astype(int)

    # 7. Geographic Aggregations (Neighbourhood Baselines)
    neighborhood_stats = feat_df.groupby("neighbourhood").agg(
        neighbourhood_total_appointments=("appointment_id", "count"),
        neighbourhood_no_show_count=("no_show_binary", "sum"),
    ).reset_index()
    neighborhood_stats["neighbourhood_no_show_rate"] = round(
        (neighborhood_stats["neighbourhood_no_show_count"] / neighborhood_stats["neighbourhood_total_appointments"]) * 100,
        2,
    )

    feat_df = feat_df.merge(
        neighborhood_stats[["neighbourhood", "neighbourhood_total_appointments", "neighbourhood_no_show_rate"]],
        on="neighbourhood",
        how="left",
    )

    # Summary Metadata
    feature_meta = {
        "total_records": len(feat_df),
        "total_features": len(feat_df.columns),
        "same_day_appointments": int(feat_df["is_same_day"].sum()),
        "same_day_no_show_rate": round(feat_df[feat_df["is_same_day"] == 1]["no_show_binary"].mean() * 100, 2),
        "advance_booking_no_show_rate": round(feat_df[feat_df["is_same_day"] == 0]["no_show_binary"].mean() * 100, 2),
        "repeat_patients_count": int((feat_df["is_repeat_patient"] == 1).sum()),
        "unique_neighbourhoods": int(feat_df["neighbourhood"].nunique()),
    }

    logger.info("Feature Engineering Completed:")
    logger.info(f"  • Total Columns: {feature_meta['total_features']}")
    logger.info(f"  • Same-Day Appointments: {feature_meta['same_day_appointments']:,} (No-Show Rate: {feature_meta['same_day_no_show_rate']}%)")
    logger.info(f"  • Advance Appointments No-Show Rate: {feature_meta['advance_booking_no_show_rate']}%")

    return feat_df, feature_meta
