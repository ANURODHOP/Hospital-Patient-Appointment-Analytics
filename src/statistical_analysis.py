"""Statistical Analysis Module for Hospital Patient & Appointment Analytics.

Performs hypothesis testing (Chi-Square test of independence, Cramér's V effect size,
Mann-Whitney U test, Welch's t-test), odds ratio / relative risk computations,
and generates structured statistical summaries for reporting and academic defense.
"""

import logging
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from scipy import stats

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def calculate_cramers_v(contingency_table: pd.DataFrame) -> float:
    """Calculate Cramér's V measure of association for contingency table."""
    chi2 = stats.chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    min_dim = min(kcorr - 1, rcorr - 1)
    if min_dim <= 0:
        return 0.0
    return float(np.sqrt(phi2corr / min_dim))


def perform_chi_square_tests(df: pd.DataFrame, categorical_cols: List[str]) -> List[Dict[str, Any]]:
    """Execute Chi-Square Test of Independence for each categorical feature against no-show status.

    Parameters
    ----------
    df : pd.DataFrame
        Analytical dataset.
    categorical_cols : List[str]
        List of categorical feature names to test against 'no_show_binary'.

    Returns
    -------
    List[Dict[str, Any]]
        List of test results containing chi2 statistic, p-value, degrees of freedom,
        Cramér's V, and statistical significance flag.
    """
    results = []
    logger.info("Executing Chi-Square tests of independence against 'no_show_binary'...")

    for col in categorical_cols:
        if col not in df.columns:
            continue

        contingency = pd.crosstab(df[col], df["no_show_binary"])
        chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
        cramers_v = calculate_cramers_v(contingency)

        is_significant = p_val < 0.05
        results.append({
            "feature": col,
            "chi2_stat": round(float(chi2), 3),
            "p_value": float(p_val),
            "p_value_formatted": "< 0.0001" if p_val < 0.0001 else f"{p_val:.4f}",
            "degrees_of_freedom": int(dof),
            "cramers_v": round(cramers_v, 4),
            "statistically_significant": is_significant,
            "effect_size": "Negligible" if cramers_v < 0.1 else ("Small" if cramers_v < 0.3 else "Moderate"),
        })

    return results


def perform_continuous_variable_tests(df: pd.DataFrame) -> Dict[str, Any]:
    """Execute Welch's t-test and Mann-Whitney U test on continuous variables.

    Tests difference in Age and Lead Time (days) between patients who showed up
    vs patients who did not show up.

    Parameters
    ----------
    df : pd.DataFrame
        Analytical dataset.

    Returns
    -------
    Dict[str, Any]
        Dictionary with statistical comparisons for age and lead time.
    """
    logger.info("Executing hypothesis tests on continuous variables (Age, Lead Time)...")

    show_group = df[df["no_show_binary"] == 0]
    noshow_group = df[df["no_show_binary"] == 1]

    # Age Test
    t_stat_age, t_pval_age = stats.ttest_ind(show_group["age"], noshow_group["age"], equal_var=False)
    mwu_stat_age, mwu_pval_age = stats.mannwhitneyu(show_group["age"], noshow_group["age"], alternative="two-sided")

    # Lead Time Test (highly skewed, Mann-Whitney U is primary)
    t_stat_lead, t_pval_lead = stats.ttest_ind(show_group["lead_time_days"], noshow_group["lead_time_days"], equal_var=False)
    mwu_stat_lead, mwu_pval_lead = stats.mannwhitneyu(show_group["lead_time_days"], noshow_group["lead_time_days"], alternative="two-sided")

    return {
        "age": {
            "show_mean": round(float(show_group["age"].mean()), 2),
            "show_std": round(float(show_group["age"].std()), 2),
            "show_median": round(float(show_group["age"].median()), 2),
            "noshow_mean": round(float(noshow_group["age"].mean()), 2),
            "noshow_std": round(float(noshow_group["age"].std()), 2),
            "noshow_median": round(float(noshow_group["age"].median()), 2),
            "t_stat": round(float(t_stat_age), 3),
            "t_pvalue": float(t_pval_age),
            "mwu_stat": float(mwu_stat_age),
            "mwu_pvalue": float(mwu_pval_age),
            "significant": bool(mwu_pval_age < 0.05),
        },
        "lead_time": {
            "show_mean": round(float(show_group["lead_time_days"].mean()), 2),
            "show_std": round(float(show_group["lead_time_days"].std()), 2),
            "show_median": round(float(show_group["lead_time_days"].median()), 2),
            "noshow_mean": round(float(noshow_group["lead_time_days"].mean()), 2),
            "noshow_std": round(float(noshow_group["lead_time_days"].std()), 2),
            "noshow_median": round(float(noshow_group["lead_time_days"].median()), 2),
            "t_stat": round(float(t_stat_lead), 3),
            "t_pvalue": float(t_pval_lead),
            "mwu_stat": float(mwu_stat_lead),
            "mwu_pvalue": float(mwu_pval_lead),
            "significant": bool(mwu_pval_lead < 0.05),
        },
    }


def compute_relative_risks(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Compute Relative Risk (Risk Ratio) and Odds Ratio for key clinical and operational risk factors."""
    logger.info("Computing Relative Risk and Odds Ratios for key risk factors...")
    factors = [
        ("SMS Received", "sms_received", 1, 0),
        ("Bolsa Família Scholarship", "scholarship", 1, 0),
        ("Same Day Booking", "is_same_day", 0, 1),  # Advance booking vs Same Day
        ("Has Chronic Condition", "has_chronic_condition", 1, 0),
        ("Hypertension", "hypertension", 1, 0),
        ("Diabetes", "diabetes", 1, 0),
        ("Alcoholism", "alcoholism", 1, 0),
    ]

    rr_results = []
    for label, col, exposed_val, unexposed_val in factors:
        if col not in df.columns:
            continue

        exposed = df[df[col] == exposed_val]["no_show_binary"]
        unexposed = df[df[col] == unexposed_val]["no_show_binary"]

        risk_exposed = exposed.mean()
        risk_unexposed = unexposed.mean()

        rr = risk_exposed / risk_unexposed if risk_unexposed > 0 else np.nan

        # Odds
        odds_exposed = risk_exposed / (1 - risk_exposed) if risk_exposed < 1 else np.nan
        odds_unexposed = risk_unexposed / (1 - risk_unexposed) if risk_unexposed < 1 else np.nan
        odds_ratio = odds_exposed / odds_unexposed if (odds_unexposed and odds_unexposed > 0) else np.nan

        rr_results.append({
            "risk_factor": label,
            "exposed_rate_pct": round(risk_exposed * 100, 2),
            "unexposed_rate_pct": round(risk_unexposed * 100, 2),
            "relative_risk": round(float(rr), 3) if not np.isnan(rr) else None,
            "odds_ratio": round(float(odds_ratio), 3) if not np.isnan(odds_ratio) else None,
        })

    return rr_results


def run_full_statistical_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """Execute all statistical analyses and return a structured report dictionary."""
    cat_cols = [
        "gender",
        "scholarship_desc",
        "hypertension_desc",
        "diabetes_desc",
        "alcoholism_desc",
        "sms_desc",
        "has_handicap",
        "age_group",
        "lead_time_bracket",
        "scheduled_time_of_day",
        "appointment_day_of_week",
        "comorbidity_category",
        "is_same_day",
    ]

    chi2_results = perform_chi_square_tests(df, cat_cols)
    continuous_results = perform_continuous_variable_tests(df)
    rr_results = compute_relative_risks(df)

    summary = {
        "total_sample_size": len(df),
        "overall_no_show_rate_pct": round(df["no_show_binary"].mean() * 100, 2),
        "chi_square_tests": chi2_results,
        "continuous_variable_tests": continuous_results,
        "relative_risk_analysis": rr_results,
    }

    return summary
