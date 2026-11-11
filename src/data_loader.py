"""Data Loader Module for Hospital Patient & Appointment Analytics.

Responsible for reading raw CSV datasets, checking schema integrity,
identifying missing/duplicate entries, and reporting dataset summaries.
"""

import logging
from pathlib import Path
from typing import Dict, Any
import pandas as pd

from src.config import RAW_DATA_FILE

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

EXPECTED_RAW_COLUMNS = [
    "PatientId",
    "AppointmentID",
    "Gender",
    "ScheduledDay",
    "AppointmentDay",
    "Age",
    "Neighbourhood",
    "Scholarship",
    "Hipertension",
    "Diabetes",
    "Alcoholism",
    "Handcap",
    "SMS_received",
    "No-show",
]


def check_raw_dataset_exists(file_path: Path = RAW_DATA_FILE) -> bool:
    """Check whether the raw dataset exists at the expected path."""
    return Path(file_path).is_file()


def load_raw_data(file_path: Path = RAW_DATA_FILE) -> pd.DataFrame:
    """Load the raw appointment dataset from disk into a Pandas DataFrame.

    Parameters
    ----------
    file_path : Path, optional
        Path to the raw CSV file. Defaults to RAW_DATA_FILE in config.

    Returns
    -------
    pd.DataFrame
        Raw dataset loaded into memory.

    Raises
    ------
    FileNotFoundError
        If the raw dataset does not exist at the specified path.
    ValueError
        If the file is empty or missing critical columns.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found at {path.resolve()}.\n"
            f"Please download 'KaggleV2-May-2016.csv' and place it in '{path.parent.resolve()}'."
        )

    logger.info(f"Loading raw dataset from {path.resolve()}...")
    df = pd.read_csv(path)
    logger.info(f"Successfully loaded {len(df):,} rows and {len(df.columns)} columns.")

    missing_cols = [col for col in EXPECTED_RAW_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Raw dataset is missing expected columns: {missing_cols}")

    return df


def validate_raw_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Inspect raw DataFrame for missing values, duplicates, and key statistics.

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame to inspect.

    Returns
    -------
    Dict[str, Any]
        Dictionary of dataset diagnostic metrics.
    """
    total_rows = len(df)
    missing_counts = df.isnull().sum().to_dict()
    total_missing = int(df.isnull().sum().sum())
    duplicate_appointment_ids = int(df["AppointmentID"].duplicated().sum())
    duplicate_rows = int(df.duplicated().sum())
    unique_patients = int(df["PatientId"].nunique())

    diagnostics = {
        "total_rows": total_rows,
        "total_columns": len(df.columns),
        "total_missing_values": total_missing,
        "missing_by_column": missing_counts,
        "duplicate_rows": duplicate_rows,
        "duplicate_appointment_ids": duplicate_appointment_ids,
        "unique_patients": unique_patients,
        "appointment_per_patient_ratio": round(total_rows / unique_patients, 2) if unique_patients else 0,
    }

    logger.info("Raw Data Validation Summary:")
    logger.info(f"  • Total Appointments: {diagnostics['total_rows']:,}")
    logger.info(f"  • Unique Patients: {diagnostics['unique_patients']:,}")
    logger.info(f"  • Missing Values: {diagnostics['total_missing_values']}")
    logger.info(f"  • Duplicate Appointments: {diagnostics['duplicate_appointment_ids']}")

    return diagnostics


if __name__ == "__main__":
    if check_raw_dataset_exists():
        raw_df = load_raw_data()
        stats = validate_raw_data(raw_df)
        print("Data loader test passed successfully.")
    else:
        print(f"Raw dataset not found at {RAW_DATA_FILE}")
