"""Unit tests for the Feature Engineering module."""

import pandas as pd
from src.data_cleaner import clean_appointment_data
from src.feature_engineering import engineer_features


def test_feature_engineering():
    """Verify categorical binning, comorbidity calculation, and temporal features."""
    sample_raw = pd.DataFrame({
        "PatientId": [101.0, 101.0, 102.0],
        "AppointmentID": [1, 2, 3],
        "Gender": ["F", "F", "M"],
        "ScheduledDay": [
            "2016-04-29T08:30:00Z",
            "2016-05-01T14:15:00Z",
            "2016-05-01T19:45:00Z",
        ],
        "AppointmentDay": [
            "2016-04-29T00:00:00Z",  # Same day lead time = 0
            "2016-05-15T00:00:00Z",  # Lead time = 14 days
            "2016-06-15T00:00:00Z",  # Lead time = 45 days
        ],
        "Age": [8, 48, 72],
        "Neighbourhood": ["CENTRO", "CENTRO", "JARDIM"],
        "Scholarship": [0, 0, 1],
        "Hipertension": [0, 1, 1],
        "Diabetes": [0, 1, 0],
        "Alcoholism": [0, 0, 1],
        "Handcap": [0, 0, 0],
        "SMS_received": [0, 1, 1],
        "No-show": ["No", "Yes", "No"],
    })

    clean_df, _ = clean_appointment_data(sample_raw)
    feat_df, meta = engineer_features(clean_df)

    # Check Age Groups
    assert str(feat_df.loc[feat_df["appointment_id"] == 1, "age_group"].values[0]) == "Children (0-12)"
    assert str(feat_df.loc[feat_df["appointment_id"] == 2, "age_group"].values[0]) == "Middle-Aged (45-64)"
    assert str(feat_df.loc[feat_df["appointment_id"] == 3, "age_group"].values[0]) == "Seniors (65+)"

    # Check Lead Time Brackets
    assert feat_df.loc[feat_df["appointment_id"] == 1, "is_same_day"].values[0] == 1
    assert str(feat_df.loc[feat_df["appointment_id"] == 1, "lead_time_bracket"].values[0]) == "Same Day (0d)"
    assert str(feat_df.loc[feat_df["appointment_id"] == 3, "lead_time_bracket"].values[0]) == "Long Term (>30d)"

    # Check Scheduled Time of Day
    assert "Morning" in feat_df.loc[feat_df["appointment_id"] == 1, "scheduled_time_of_day"].values[0]
    assert "Afternoon" in feat_df.loc[feat_df["appointment_id"] == 2, "scheduled_time_of_day"].values[0]
    assert "Evening" in feat_df.loc[feat_df["appointment_id"] == 3, "scheduled_time_of_day"].values[0]

    # Check Comorbidity calculation
    # Appt 1: 0 conditions
    assert feat_df.loc[feat_df["appointment_id"] == 1, "chronic_condition_count"].values[0] == 0
    assert feat_df.loc[feat_df["appointment_id"] == 1, "comorbidity_category"].values[0] == "No Chronic Conditions"
    # Appt 2: Hypertension + Diabetes = 2 conditions
    assert feat_df.loc[feat_df["appointment_id"] == 2, "chronic_condition_count"].values[0] == 2
    assert feat_df.loc[feat_df["appointment_id"] == 2, "comorbidity_category"].values[0] == "Multimorbid (2+ Conditions)"

    # Check Repeat Patient flag
    # Patient 101 has 2 appointments
    assert feat_df.loc[feat_df["patient_id"] == 101, "is_repeat_patient"].values[0] == 1
    # Patient 102 has 1 appointment
    assert feat_df.loc[feat_df["patient_id"] == 102, "is_repeat_patient"].values[0] == 0
