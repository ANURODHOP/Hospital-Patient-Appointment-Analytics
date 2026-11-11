"""Unit tests for the Data Loader module."""

import pytest
from pathlib import Path
import pandas as pd

from src.data_loader import check_raw_dataset_exists, load_raw_data, validate_raw_data, EXPECTED_RAW_COLUMNS
from src.config import RAW_DATA_FILE


def test_check_raw_dataset_exists():
    """Verify that the raw dataset existence checker behaves accurately."""
    assert check_raw_dataset_exists(RAW_DATA_FILE) is True
    assert check_raw_dataset_exists(Path("non_existent_path.csv")) is False


def test_load_raw_data_success():
    """Verify loading raw dataset returns a valid non-empty DataFrame."""
    df = load_raw_data(RAW_DATA_FILE)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 100000
    for col in EXPECTED_RAW_COLUMNS:
        assert col in df.columns


def test_load_raw_data_missing_file():
    """Verify that attempting to load a missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_raw_data(Path("invalid/path/missing.csv"))


def test_validate_raw_data_structure():
    """Verify diagnostic metrics structure returned by validate_raw_data."""
    sample_df = pd.DataFrame({
        "PatientId": [101, 102, 101],
        "AppointmentID": [1, 2, 3],
        "Gender": ["F", "M", "F"],
        "ScheduledDay": ["2016-04-29T18:00:00Z"] * 3,
        "AppointmentDay": ["2016-04-29T00:00:00Z"] * 3,
        "Age": [25, 45, 25],
        "Neighbourhood": ["CENTRO"] * 3,
        "Scholarship": [0, 1, 0],
        "Hipertension": [0, 0, 0],
        "Diabetes": [0, 0, 0],
        "Alcoholism": [0, 0, 0],
        "Handcap": [0, 0, 0],
        "SMS_received": [0, 1, 0],
        "No-show": ["No", "Yes", "No"],
    })
    diagnostics = validate_raw_data(sample_df)
    assert diagnostics["total_rows"] == 3
    assert diagnostics["unique_patients"] == 2
    assert diagnostics["total_missing_values"] == 0
    assert diagnostics["duplicate_appointment_ids"] == 0
