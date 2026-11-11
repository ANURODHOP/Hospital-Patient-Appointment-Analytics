"""Unit tests for the Statistical Analysis module."""

import pandas as pd
import numpy as np

from src.statistical_analysis import (
    calculate_cramers_v,
    perform_chi_square_tests,
    perform_continuous_variable_tests,
    compute_relative_risks,
    run_full_statistical_analysis,
)


def test_calculate_cramers_v():
    """Verify Cramér's V returns values between 0.0 and 1.0."""
    table = pd.DataFrame([[100, 20], [30, 80]])
    v = calculate_cramers_v(table)
    assert 0.0 <= v <= 1.0


def test_statistical_suite():
    """Verify statistical testing functions execute properly on sample data."""
    # Synthetic dataset with known patterns
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        "gender": np.random.choice(["Male", "Female"], n),
        "scholarship_desc": np.random.choice(["Bolsa Família Enrolled", "No Welfare"], n),
        "hypertension_desc": np.random.choice(["Hypertensive", "Normal BP"], n),
        "diabetes_desc": np.random.choice(["Diabetic", "Non-Diabetic"], n),
        "alcoholism_desc": ["No Alcohol Disorder"] * n,
        "sms_desc": np.random.choice(["SMS Reminder Received", "No SMS Sent"], n),
        "has_handicap": np.random.choice([0, 1], n),
        "age_group": np.random.choice(["Youth (13-24)", "Seniors (65+)"], n),
        "lead_time_bracket": np.random.choice(["Same Day (0d)", "Long Term (>30d)"], n),
        "scheduled_time_of_day": ["Morning (06:00-11:59)"] * n,
        "appointment_day_of_week": ["Monday"] * n,
        "comorbidity_category": ["No Chronic Conditions"] * n,
        "is_same_day": np.random.choice([0, 1], n),
        "age": np.random.randint(18, 80, n),
        "lead_time_days": np.random.randint(0, 30, n),
        "no_show_binary": np.random.choice([0, 1], n, p=[0.8, 0.2]),
    })

    summary = run_full_statistical_analysis(df)
    assert summary["total_sample_size"] == n
    assert "chi_square_tests" in summary
    assert "continuous_variable_tests" in summary
    assert "relative_risk_analysis" in summary

    # Verify Continuous Tests structure
    age_test = summary["continuous_variable_tests"]["age"]
    assert "show_mean" in age_test
    assert "noshow_mean" in age_test
    assert "mwu_stat" in age_test

    lead_test = summary["continuous_variable_tests"]["lead_time"]
    assert "show_mean" in lead_test
    assert "noshow_mean" in lead_test
    assert "mwu_stat" in lead_test
