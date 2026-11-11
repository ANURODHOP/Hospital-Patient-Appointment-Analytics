"""Visualization Module for Hospital Patient & Appointment Analytics.

Generates publication-quality charts and exploratory graphics saved to reports/figures/.
Configures unified aesthetic themes, palettes, and typography.
"""

import logging
from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from src.config import FIGURES_DIR, PALETTE_ATTENDANCE

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Apply clean visualization style
sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8


def ensure_figures_dir() -> Path:
    """Ensure the reports/figures directory exists."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    return FIGURES_DIR


def plot_01_overall_noshow_distribution(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> Path:
    """Generate donut chart and count summary of overall attendance."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    counts = df["attendance_status"].value_counts()
    colors = [PALETTE_ATTENDANCE.get(status, "#7f8c8d") for status in counts.index]

    # Donut Chart
    wedges, texts, autotexts = ax1.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        textprops=dict(color="#2c3e50", weight="bold", fontsize=11),
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
    )
    ax1.set_title("Overall Attendance Proportion", fontsize=13, weight="bold", pad=15)

    # Bar Chart with Counts
    bars = ax2.bar(counts.index, counts.values, color=colors, edgecolor="black", linewidth=0.5, width=0.5)
    ax2.set_ylabel("Total Number of Appointments", fontsize=11)
    ax2.set_title("Total Appointment Volume by Status", fontsize=13, weight="bold", pad=15)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    for bar in bars:
        h = bar.get_height()
        ax2.annotate(
            f"{int(h):,}\n({h/len(df)*100:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=10,
        )

    plt.suptitle("Overall Hospital Appointment Attendance Overview", fontsize=16, weight="bold", y=1.02)
    plt.tight_layout()
    out_file = output_dir / "01_overall_noshow_distribution.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved figure: {out_file.name}")
    return out_file


def plot_02_gender_and_scholarship_impact(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> Path:
    """Analyze attendance rates by Gender and Welfare Scholarship."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Gender No-Show Rate
    gender_grp = df.groupby("gender_full")["no_show_binary"].agg(["count", "mean"]).reset_index()
    gender_grp["rate_pct"] = gender_grp["mean"] * 100
    bars1 = ax1.bar(gender_grp["gender_full"], gender_grp["rate_pct"], color=["#e91e63", "#3498db"], width=0.45)
    ax1.set_ylabel("No-Show Rate (%)", fontsize=11)
    ax1.set_title("No-Show Rate by Gender", fontsize=13, weight="bold")
    ax1.set_ylim(0, 30)
    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f"{h:.2f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                     textcoords="offset points", ha="center", fontweight="bold")

    # Scholarship No-Show Rate
    schol_grp = df.groupby("scholarship_desc")["no_show_binary"].agg(["count", "mean"]).reset_index()
    schol_grp["rate_pct"] = schol_grp["mean"] * 100
    bars2 = ax2.bar(schol_grp["scholarship_desc"], schol_grp["rate_pct"], color=["#95a5a6", "#e67e22"], width=0.45)
    ax2.set_ylabel("No-Show Rate (%)", fontsize=11)
    ax2.set_title("No-Show Rate by Bolsa Família Welfare Status", fontsize=13, weight="bold")
    ax2.set_ylim(0, 30)
    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"{h:.2f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                     textcoords="offset points", ha="center", fontweight="bold")

    plt.suptitle("Socioeconomic & Demographic Attendance Predictors", fontsize=16, weight="bold", y=1.02)
    plt.tight_layout()
    out_file = output_dir / "02_gender_and_scholarship_impact.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved figure: {out_file.name}")
    return out_file


def plot_03_age_distribution_by_attendance(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> Path:
    """Plot age distribution KDE and stratified no-show rates across age groups."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # KDE Distribution
    sns.kdeplot(
        data=df,
        x="age",
        hue="attendance_status",
        palette=PALETTE_ATTENDANCE,
        common_norm=False,
        fill=True,
        alpha=0.35,
        ax=ax1,
    )
    ax1.set_title("Age Density Distribution by Attendance Status", fontsize=13, weight="bold")
    ax1.set_xlabel("Patient Age (Years)", fontsize=11)
    ax1.set_ylabel("Kernel Density", fontsize=11)

    # Age Group No-Show Rate
    age_grp = df.groupby("age_group", observed=False)["no_show_binary"].agg(["count", "mean"]).reset_index()
    age_grp["rate_pct"] = age_grp["mean"] * 100
    palette_bars = sns.color_palette("mako", len(age_grp))
    bars = ax2.bar(age_grp["age_group"], age_grp["rate_pct"], color=palette_bars, width=0.55)
    ax2.set_title("No-Show Rate across Age Brackets", fontsize=13, weight="bold")
    ax2.set_ylabel("No-Show Rate (%)", fontsize=11)
    ax2.set_xlabel("Age Bracket", fontsize=11)
    ax2.tick_params(axis="x", rotation=25)
    ax2.set_ylim(0, 30)

    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                     textcoords="offset points", ha="center", fontweight="bold")

    plt.suptitle("Age Demographics vs Appointment Attendance", fontsize=16, weight="bold", y=1.02)
    plt.tight_layout()
    out_file = output_dir / "03_age_distribution_by_attendance.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved figure: {out_file.name}")
    return out_file


def plot_04_chronic_conditions_comorbidity(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> Path:
    """Plot no-show rates across chronic clinical conditions and comorbidity levels."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Individual Conditions
    cond_data = []
    for cond, name in [
        ("hypertension", "Hypertension"),
        ("diabetes", "Diabetes"),
        ("alcoholism", "Alcoholism"),
        ("has_handicap", "Handicap"),
    ]:
        rate_present = df[df[cond] == 1]["no_show_binary"].mean() * 100
        rate_absent = df[df[cond] == 0]["no_show_binary"].mean() * 100
        cond_data.append({"Condition": name, "Status": "Present", "Rate": rate_present})
        cond_data.append({"Condition": name, "Status": "Absent", "Rate": rate_absent})

    cond_df = pd.DataFrame(cond_data)
    sns.barplot(data=cond_df, x="Condition", y="Rate", hue="Status", palette=["#e74c3c", "#3498db"], ax=ax1)
    ax1.set_title("No-Show Rate by Individual Chronic Condition", fontsize=13, weight="bold")
    ax1.set_ylabel("No-Show Rate (%)", fontsize=11)
    ax1.set_ylim(0, 25)

    # Comorbidity Level
    comorb_grp = df.groupby("comorbidity_category", observed=False)["no_show_binary"].agg(["count", "mean"]).reset_index()
    comorb_grp["rate_pct"] = comorb_grp["mean"] * 100
    order = ["No Chronic Conditions", "Single Condition", "Multimorbid (2+ Conditions)"]
    comorb_grp = comorb_grp.set_index("comorbidity_category").reindex(order).reset_index()

    bars = ax2.bar(comorb_grp["comorbidity_category"], comorb_grp["rate_pct"], color=["#1abc9c", "#f39c12", "#8e44ad"], width=0.5)
    ax2.set_title("No-Show Rate by Patient Comorbidity Burden", fontsize=13, weight="bold")
    ax2.set_ylabel("No-Show Rate (%)", fontsize=11)
    ax2.tick_params(axis="x", rotation=15)
    ax2.set_ylim(0, 25)

    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"{h:.2f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                     textcoords="offset points", ha="center", fontweight="bold")

    plt.suptitle("Clinical Health Profiles & Chronic Disease Comorbidity", fontsize=16, weight="bold", y=1.02)
    plt.tight_layout()
    out_file = output_dir / "04_chronic_conditions_comorbidity.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved figure: {out_file.name}")
    return out_file


def plot_05_lead_time_vs_noshow_rate(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> Path:
    """Analyze the impact of scheduling lead time (waiting days) on no-show rates."""
    fig, ax1 = plt.subplots(figsize=(12, 6))

    lead_grp = df.groupby("lead_time_bracket", observed=False).agg(
        volume=("appointment_id", "count"),
        noshow_rate=("no_show_binary", "mean"),
    ).reset_index()
    lead_grp["noshow_rate_pct"] = lead_grp["noshow_rate"] * 100

    # Primary Axis: Volume of Appointments
    bars = ax1.bar(
        lead_grp["lead_time_bracket"],
        lead_grp["volume"],
        color="#bdc3c7",
        alpha=0.6,
        width=0.6,
        label="Appointment Volume",
    )
    ax1.set_ylabel("Appointment Booking Volume", fontsize=12, color="#2c3e50")
    ax1.set_xlabel("Scheduling Lead Time (Waiting Duration)", fontsize=12)
    ax1.tick_params(axis="x", rotation=20)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    # Secondary Axis: No-Show Rate Line
    ax2 = ax1.twinx()
    line = ax2.plot(
        lead_grp["lead_time_bracket"],
        lead_grp["noshow_rate_pct"],
        color="#c0392b",
        linewidth=3,
        marker="o",
        markersize=8,
        label="No-Show Rate (%)",
    )
    ax2.set_ylabel("No-Show Rate (%)", fontsize=12, color="#c0392b")
    ax2.grid(False)  # Avoid conflicting grids
    ax2.set_ylim(0, 40)

    for i, val in enumerate(lead_grp["noshow_rate_pct"]):
        ax2.annotate(
            f"{val:.1f}%",
            xy=(i, val),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            weight="bold",
            color="#962d22",
        )

    plt.title("Scheduling Lead Time vs No-Show Probability: The Waiting Time Curve", fontsize=15, weight="bold", pad=15)
    plt.tight_layout()
    out_file = output_dir / "05_lead_time_vs_noshow_rate.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved figure: {out_file.name}")
    return out_file


def plot_06_day_of_week_and_sms_impact(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> Path:
    """Analyze Day of Week distribution and SMS notification interaction."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Day of Week
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    day_grp = df.groupby("appointment_day_of_week", observed=False)["no_show_binary"].agg(["count", "mean"]).reindex(day_order).reset_index()
    day_grp["rate_pct"] = day_grp["mean"] * 100

    bars = ax1.bar(day_grp["appointment_day_of_week"], day_grp["rate_pct"], color="#34495e", width=0.5)
    ax1.set_title("No-Show Rate by Day of the Week", fontsize=13, weight="bold")
    ax1.set_ylabel("No-Show Rate (%)", fontsize=11)
    ax1.tick_params(axis="x", rotation=25)
    ax1.set_ylim(0, 30)

    for bar in bars:
        h = bar.get_height()
        if not np.isnan(h):
            ax1.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                         textcoords="offset points", ha="center", fontweight="bold")

    # SMS Reminder Interaction across lead time
    # SMS is typically only sent for advance bookings (>2 days)
    adv_df = df[df["lead_time_days"] >= 3]
    sms_adv = adv_df.groupby(["sms_desc"])["no_show_binary"].agg(["count", "mean"]).reset_index()
    sms_adv["rate_pct"] = sms_adv["mean"] * 100

    bars2 = ax2.bar(sms_adv["sms_desc"], sms_adv["rate_pct"], color=["#e67e22", "#27ae60"], width=0.45)
    ax2.set_title("SMS Impact on Advance Appointments (Lead Time ≥ 3 Days)", fontsize=13, weight="bold")
    ax2.set_ylabel("No-Show Rate (%)", fontsize=11)
    ax2.set_ylim(0, 40)

    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                     textcoords="offset points", ha="center", fontweight="bold")

    plt.suptitle("Operational Timing & Patient Communication Interventions", fontsize=16, weight="bold", y=1.02)
    plt.tight_layout()
    out_file = output_dir / "06_day_of_week_and_sms_impact.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved figure: {out_file.name}")
    return out_file


def plot_07_top_bottom_neighbourhoods(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> Path:
    """Analyze clinic neighbourhood attendance for clinics with >= 100 appointments."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    neigh_grp = df.groupby("neighbourhood").agg(
        volume=("appointment_id", "count"),
        noshow_rate=("no_show_binary", "mean"),
    ).reset_index()
    neigh_grp = neigh_grp[neigh_grp["volume"] >= 100]  # Minimum sample threshold
    neigh_grp["noshow_rate_pct"] = neigh_grp["noshow_rate"] * 100

    # Top 10 highest no-show
    top10 = neigh_grp.sort_values(by="noshow_rate_pct", ascending=False).head(10)
    ax1.barh(top10["neighbourhood"], top10["noshow_rate_pct"], color="#e74c3c", height=0.6)
    ax1.set_xlabel("No-Show Rate (%)", fontsize=11)
    ax1.set_title("Top 10 Highest No-Show Neighbourhoods (Min. 100 Appts)", fontsize=13, weight="bold")
    ax1.invert_yaxis()
    ax1.set_xlim(0, 35)
    for i, row in top10.reset_index().iterrows():
        ax1.annotate(f"{row['noshow_rate_pct']:.1f}% (N={row['volume']})",
                     xy=(row["noshow_rate_pct"], i), xytext=(4, 0), textcoords="offset points",
                     va="center", fontsize=9, weight="bold")

    # Bottom 10 lowest no-show
    bottom10 = neigh_grp.sort_values(by="noshow_rate_pct", ascending=True).head(10)
    ax2.barh(bottom10["neighbourhood"], bottom10["noshow_rate_pct"], color="#2ecc71", height=0.6)
    ax2.set_xlabel("No-Show Rate (%)", fontsize=11)
    ax2.set_title("Top 10 Most Reliable Neighbourhoods (Min. 100 Appts)", fontsize=13, weight="bold")
    ax2.invert_yaxis()
    ax2.set_xlim(0, 35)
    for i, row in bottom10.reset_index().iterrows():
        ax2.annotate(f"{row['noshow_rate_pct']:.1f}% (N={row['volume']})",
                     xy=(row["noshow_rate_pct"], i), xytext=(4, 0), textcoords="offset points",
                     va="center", fontsize=9, weight="bold")

    plt.suptitle("Geographical Disparities in Appointment Compliance across Vitória, Brazil", fontsize=16, weight="bold", y=1.02)
    plt.tight_layout()
    out_file = output_dir / "07_top_bottom_neighbourhoods.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved figure: {out_file.name}")
    return out_file


def plot_08_correlation_heatmap(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> Path:
    """Plot correlation matrix across key numerical and binary attributes."""
    corr_cols = [
        "age",
        "lead_time_days",
        "scholarship",
        "hypertension",
        "diabetes",
        "alcoholism",
        "has_handicap",
        "sms_received",
        "chronic_condition_count",
        "is_same_day",
        "no_show_binary",
    ]
    corr_matrix = df[corr_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
        ax=ax,
    )
    plt.title("Correlation Matrix of Clinical, Operational, and Demographic Factors", fontsize=14, weight="bold", pad=15)
    plt.tight_layout()
    out_file = output_dir / "08_correlation_heatmap.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved figure: {out_file.name}")
    return out_file


def plot_09_age_group_vs_waiting_bracket(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> Path:
    """Plot 2D cross-tabulation heatmap of No-Show Rate across Age Groups and Lead Time Brackets."""
    pivot = df.pivot_table(
        index="age_group",
        columns="lead_time_bracket",
        values="no_show_binary",
        aggfunc="mean",
        observed=False,
    ) * 100

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".1f",
        cmap="YlOrRd",
        linewidths=0.8,
        cbar_kws={"label": "No-Show Rate (%)"},
        ax=ax,
    )
    plt.title("No-Show Rate Heatmap: Age Bracket × Scheduling Lead Time", fontsize=14, weight="bold", pad=15)
    plt.xlabel("Scheduling Lead Time (Waiting Duration)", fontsize=11)
    plt.ylabel("Patient Age Bracket", fontsize=11)
    plt.tight_layout()
    out_file = output_dir / "09_age_group_vs_waiting_bracket.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved figure: {out_file.name}")
    return out_file


def generate_all_visualizations(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> List[Path]:
    """Execute and save the complete suite of analytical visualizations."""
    ensure_figures_dir()
    logger.info(f"Generating full visualization suite to {output_dir.resolve()}...")

    generated_paths = [
        plot_01_overall_noshow_distribution(df, output_dir),
        plot_02_gender_and_scholarship_impact(df, output_dir),
        plot_03_age_distribution_by_attendance(df, output_dir),
        plot_04_chronic_conditions_comorbidity(df, output_dir),
        plot_05_lead_time_vs_noshow_rate(df, output_dir),
        plot_06_day_of_week_and_sms_impact(df, output_dir),
        plot_07_top_bottom_neighbourhoods(df, output_dir),
        plot_08_correlation_heatmap(df, output_dir),
        plot_09_age_group_vs_waiting_bracket(df, output_dir),
    ]

    logger.info(f"Successfully generated and saved {len(generated_paths)} analytical charts.")
    return generated_paths
