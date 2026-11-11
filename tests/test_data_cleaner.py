"""Unit tests for the Data Cleaner module."""

import pandas as pd
from src.data_cleaner import clean_appointment_data


def test_clean_appointment_data():
    """Verify data cleaner removes negative ages, past bookings, and standardizes columns."""
    sample_raw = pd.DataFrame({
        "PatientId": [101.0, 102.0, 103.0, 104.0],
        "AppointmentID": [1, 2, 3, 4],
        "Gender": ["F", "M", "F", "M"],
        "ScheduledDay": [
            "2016-04-29T10:00:00Z",
            "2016-04-30T10:00:00Z",
            "2016-04-29T10:00:00Z",
            "2016-05-10T10:00:00Z",  # Booked in future relative to appointment
        ],
        "AppointmentDay": [
            "2016-04-29T00:00:00Z",  # Valid same day
            "2016-05-05T00:00:00Z",  # Valid lead time 5 days
            "2016-04-29T00:00:00Z",  # Invalid age row (-1)
            "2016-05-01T00:00:00Z",  # Invalid lead time (scheduled May 10, appt May 1)
        ],
        "Age": [30, 45, -1, 28],
        "Neighbourhood": ["JARDIM", "CENTRO", "CENTRO", "CENTRO"],
        "Scholarship": [0, 1, 0, 0],
        "Hipertension": [1, 0, 0, 0],
        "Diabetes": [0, 1, 0, 0],
        "Alcoholism": [0, 0, 0, 0],
        "Handcap": [0, 2, 0, 0],
        "SMS_received": [0, 1, 0, 0],
        "No-show": ["No", "Yes", "No", "No"],
    })

    clean_df, metrics = clean_appointment_data(sample_raw)

    # Must retain 2 valid rows
    assert len(clean_df) == 2
    assert metrics["dropped_rows"] == 2
    assert metrics["invalid_age_count"] == 1
    assert metrics["invalid_lead_time_count"] == 1

    # Check renamed columns
    assert "hypertension" in clean_df.columns
    assert "handicap" in clean_df.columns
    assert "lead_time_days" in clean_df.columns

    # Check binary conversions
    assert clean_df.loc[clean_df["appointment_id"] == 1, "no_show_binary"].values[0] == 0
    assert clean_df.loc[clean_df["appointment_id"] == 1, "attendance_status"].values[0] == "Showed Up"
    assert clean_df.loc[clean_df["appointment_id"] == 2, "no_show_binary"].values[0] == 1
    assert clean_df.loc[clean_df["appointment_id"] == 2, "attendance_status"].values[0] == "No Show"

    # Check handicap flag
    assert clean_df.loc[clean_df["appointment_id"] == 2, "has_handicap"].values[0] == 1
