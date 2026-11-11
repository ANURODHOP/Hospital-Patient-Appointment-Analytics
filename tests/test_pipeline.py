"""Integration tests for the complete analytical pipeline."""

from pathlib import Path
from src.config import (
    CLEANED_DATA_FILE,
    TABLEAU_EXEC_FILE,
    TABLEAU_DEMOG_FILE,
    TABLEAU_SCHED_FILE,
    TABLEAU_NEIGHBORHOOD_FILE,
    FIGURES_DIR,
    REPORTS_DIR,
)
from src.pipeline import run_pipeline


def test_full_pipeline_execution():
    """Verify that running the pipeline produces all required CSVs, figures, and reports."""
    results = run_pipeline()

    assert results["raw_validation"]["total_rows"] > 100000
    assert results["cleaning_metrics"]["final_rows"] > 100000

    # Verify CSV files exist and are populated
    for key, path_str in results["tableau_exports"].items():
        csv_path = Path(path_str)
        assert csv_path.exists(), f"Missing CSV export: {csv_path}"
        assert csv_path.stat().st_size > 0, f"Empty CSV export: {csv_path}"

    # Verify figures generated
    expected_figures = [
        "01_overall_noshow_distribution.png",
        "02_gender_and_scholarship_impact.png",
        "03_age_distribution_by_attendance.png",
        "04_chronic_conditions_comorbidity.png",
        "05_lead_time_vs_noshow_rate.png",
        "06_day_of_week_and_sms_impact.png",
        "07_top_bottom_neighbourhoods.png",
        "08_correlation_heatmap.png",
        "09_age_group_vs_waiting_bracket.png",
    ]
    for fig_name in expected_figures:
        fig_path = FIGURES_DIR / fig_name
        assert fig_path.exists(), f"Missing figure: {fig_name}"
        assert fig_path.stat().st_size > 1000, f"Figure appears corrupted or empty: {fig_name}"

    # Verify Markdown Report
    report_path = REPORTS_DIR / "statistical_summary_report.md"
    assert report_path.exists()
    assert report_path.stat().st_size > 500
