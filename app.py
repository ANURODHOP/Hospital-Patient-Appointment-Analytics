"""Hospital Patient & Appointment Analytics - Clinical Intelligence Portal.

An enterprise-grade executive dashboard suite for healthcare operations,
patient attendance analytics, and empirical hypothesis testing.
Designed for clinical directors, operations leads, and health data analysts.
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Centralized project imports
from src.config import (
    CLEANED_DATA_FILE,
    TABLEAU_NEIGHBORHOOD_FILE,
)
from src.statistical_analysis import run_full_statistical_analysis

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hospital Outpatient Intelligence & Attendance Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Bespoke Clinical Enterprise Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0f172a;
    }

    /* Main background & container padding */
    .stApp {
        background-color: #f8fafc;
    }

    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        padding-left: 2.2rem;
        padding-right: 2.2rem;
        max-width: 1400px;
    }

    /* Top Executive Header Banner */
    .top-header-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 22px 28px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.02);
    }
    .header-kicker {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #0284c7;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .header-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 6px 0;
        line-height: 1.25;
        letter-spacing: -0.02em;
    }
    .header-subtitle {
        font-size: 0.95rem;
        color: #475569;
        margin: 0;
        line-height: 1.5;
    }
    .header-metadata {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 14px;
        padding-top: 12px;
        border-top: 1px solid #f1f5f9;
    }
    .meta-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        background: #f1f5f9;
        color: #334155;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .meta-pill-live {
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
    }
    .live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10b981;
    }

    /* Bespoke Executive KPI Card Grid */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.02);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(15, 23, 42, 0.06);
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 8px;
    }
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748b;
    }
    .kpi-value {
        font-family: 'JetBrains Mono', 'Plus Jakarta Sans', monospace;
        font-size: 1.85rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin-bottom: 6px;
    }
    .kpi-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    .badge-success {
        background-color: #ecfdf5;
        color: #047857;
        border: 1px solid #d1fae5;
    }
    .badge-danger {
        background-color: #fff1f2;
        color: #be123c;
        border: 1px solid #ffe4e6;
    }
    .badge-neutral {
        background-color: #f1f5f9;
        color: #475569;
        border: 1px solid #e2e8f0;
    }
    .badge-amber {
        background-color: #fffbeb;
        color: #b45309;
        border: 1px solid #fef3c7;
    }
    .kpi-subtext {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 4px;
    }

    /* Chart & Section Framing Cards */
    .section-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 22px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.02);
    }
    .section-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 4px 0;
    }
    .section-card-subtitle {
        font-size: 0.82rem;
        color: #64748b;
        margin: 0 0 16px 0;
    }

    /* Clinical Insight Banner */
    .clinical-insight {
        background-color: #f0fdfa;
        border-left: 4px solid #0d9488;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin: 18px 0 24px 0;
    }
    .insight-title {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #0f766e;
        margin-bottom: 4px;
    }
    .insight-body {
        font-size: 0.88rem;
        color: #134e4a;
        line-height: 1.5;
        margin: 0;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        color: #f8fafc;
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }
    .sidebar-brand-box {
        padding: 8px 0 20px 0;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 20px;
    }
    .brand-title {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin: 8px 0 2px 0;
    }
    .brand-subtitle {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #38bdf8;
    }
    .sidebar-filter-summary {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px 14px;
        margin-top: 14px;
    }
    .filter-count-label {
        font-size: 0.72rem;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.04em;
    }
    .filter-count-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        color: #38bdf8;
    }

    /* Clean Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.88rem;
        font-weight: 600;
        color: #64748b;
        padding: 10px 16px;
        border-radius: 6px 6px 0 0;
    }
    .stTabs [aria-selected="true"] {
        color: #0284c7 !important;
        border-bottom: 2px solid #0284c7 !important;
        background-color: transparent !important;
    }

    /* Clean Dataframe Styling */
    div[data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Plotly Unified Clinical Theme Helper
# ---------------------------------------------------------
def apply_clinical_theme(fig, height=350, title=None):
    """Apply a standardized, high-end clinical aesthetic to any Plotly figure."""
    fig.update_layout(
        font=dict(
            family="Plus Jakarta Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
            color="#334155",
            size=11,
        ),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        height=height,
        margin=dict(t=35 if title else 20, b=25, l=35, r=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text="",
            font=dict(size=11, color="#475569"),
        ),
        hoverlabel=dict(
            bgcolor="#0f172a",
            font_size=12,
            font_family="Plus Jakarta Sans, sans-serif",
            font_color="#ffffff",
            bordercolor="#0f172a",
        ),
    )
    if title:
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=13, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
                x=0,
                y=0.98,
            )
        )
    fig.update_xaxes(
        gridcolor="#f1f5f9",
        zerolinecolor="#e2e8f0",
        linecolor="#cbd5e1",
        tickfont=dict(color="#64748b", size=10),
        title_font=dict(color="#475569", size=11),
    )
    fig.update_yaxes(
        gridcolor="#f1f5f9",
        zerolinecolor="#e2e8f0",
        linecolor="#cbd5e1",
        tickfont=dict(color="#64748b", size=10),
        title_font=dict(color="#475569", size=11),
    )
    return fig


# ---------------------------------------------------------
# Data Ingestion & Caching
# ---------------------------------------------------------
@st.cache_data
def load_data():
    """Load and cache the validated clinical dataset."""
    df = pd.read_csv(CLEANED_DATA_FILE)
    df["scheduled_datetime"] = pd.to_datetime(df["scheduled_datetime"])
    df["appointment_date"] = pd.to_datetime(df["appointment_date"])
    return df


@st.cache_data
def load_neighborhood_summary():
    """Load neighborhood aggregate catchment statistics."""
    return pd.read_csv(TABLEAU_NEIGHBORHOOD_FILE)


df_raw = load_data()
df_neigh = load_neighborhood_summary()

# ---------------------------------------------------------
# Sidebar Navigation & Filter Controls
# ---------------------------------------------------------
with st.sidebar:
    # Organization Emblem & Branding
    st.markdown("""
    <div class="sidebar-brand-box">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="24" height="24" rx="6" fill="#0284c7"/>
            <path d="M12 5V19M5 12H19" stroke="white" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div class="brand-title">Vitória Health BI</div>
        <div class="brand-subtitle">Clinical Appointment Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    # Primary View Selector
    page = st.radio(
        "Navigation",
        [
            "Executive Attendance Overview",
            "Demographics & Chronic Profile",
            "Scheduling Lead-Time & Capacity",
            "Geographic Catchment Disparities",
            "Statistical Inference & Hypotheses",
            "Tableau BI Architecture & Viva Prep",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border: 0; border-top: 1px solid #1e293b; margin: 18px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 12px;'>Patient Population Filters</p>", unsafe_allow_html=True)

    # Gender Filter
    gender_filter = st.multiselect(
        "Patient Gender",
        options=["Female", "Male"],
        default=["Female", "Male"],
    )

    # Age Bracket Filter
    available_ages = list(df_raw["age_group"].dropna().unique())
    age_filter = st.multiselect(
        "Life Stage Age Cohort",
        options=available_ages,
        default=available_ages,
    )

    # Welfare Filter
    available_welfare = list(df_raw["scholarship_desc"].dropna().unique())
    welfare_filter = st.multiselect(
        "Bolsa Família Welfare Program",
        options=available_welfare,
        default=available_welfare,
    )

    # Apply Active Filters
    filtered_df = df_raw[
        (df_raw["gender_full"].isin(gender_filter))
        & (df_raw["age_group"].isin(age_filter))
        & (df_raw["scholarship_desc"].isin(welfare_filter))
    ]

    coverage_pct = (len(filtered_df) / len(df_raw) * 100) if len(df_raw) > 0 else 0

    st.markdown(f"""
    <div class="sidebar-filter-summary">
        <div class="filter-count-label">Active Sample Cohort</div>
        <div class="filter-count-val">{len(filtered_df):,} <span style="font-size: 0.75rem; color: #94a3b8; font-weight: normal;">/ {len(df_raw):,}</span></div>
        <div style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">{coverage_pct:.1f}% of total appointments retained</div>
    </div>
    """, unsafe_allow_html=True)

    if len(filtered_df) < len(df_raw):
        if st.button("Reset Global Filters", use_container_width=True):
            st.rerun()


# ---------------------------------------------------------
# Reusable Executive Top Header
# ---------------------------------------------------------
def render_header(kicker, title, subtitle):
    st.markdown(f"""
    <div class="top-header-container">
        <div class="header-kicker">
            <span>{kicker}</span>
        </div>
        <h1 class="header-title">{title}</h1>
        <p class="header-subtitle">{subtitle}</p>
        <div class="header-metadata">
            <span class="meta-pill meta-pill-live">
                <span class="live-dot"></span> Verified Cohort Active
            </span>
            <span class="meta-pill">
                📍 Municipal Health Network • Vitória (ES), Brazil
            </span>
            <span class="meta-pill">
                🏥 81 Catchment Clinics • N = {len(filtered_df):,} Appointments
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# VIEW 1: EXECUTIVE ATTENDANCE OVERVIEW
# ---------------------------------------------------------
if page == "Executive Attendance Overview":
    render_header(
        "Executive BI • Strategic Attendance Overview",
        "Clinical Appointment Volume & Attendance Intelligence",
        "High-level operational performance indicators, daily consultation trends, and communication intervention efficacy.",
    )

    # Calculate Top KPIs
    total_appts = len(filtered_df)
    total_shows = int(filtered_df["showed_up_binary"].sum())
    total_noshows = int(filtered_df["no_show_binary"].sum())
    noshow_rate = (total_noshows / total_appts * 100) if total_appts > 0 else 0
    show_rate = 100 - noshow_rate
    avg_lead = filtered_df["lead_time_days"].mean() if total_appts > 0 else 0
    adv_df = filtered_df[filtered_df["lead_time_days"] >= 3]
    adv_noshow_rate = (adv_df["no_show_binary"].mean() * 100) if len(adv_df) > 0 else 0

    # Executive KPI Cards Grid
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-label">Total Appointments</span>
                <span class="kpi-badge badge-neutral">Scheduled</span>
            </div>
            <div class="kpi-value">{total_appts:,}</div>
            <div class="kpi-subtext">Filtered outpatient cohort</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-label">Completed Visits</span>
                <span class="kpi-badge badge-success">Attended</span>
            </div>
            <div class="kpi-value">{total_shows:,}</div>
            <div class="kpi-subtext"><b style="color: #047857;">{show_rate:.1f}%</b> overall completion rate</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-label">No-Shows (Defaults)</span>
                <span class="kpi-badge badge-danger">Missed Slot</span>
            </div>
            <div class="kpi-value">{total_noshows:,}</div>
            <div class="kpi-subtext"><b style="color: #be123c;">{noshow_rate:.1f}%</b> default rate</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-label">Avg Scheduling Lead Time</span>
                <span class="kpi-badge badge-neutral">Operational</span>
            </div>
            <div class="kpi-value">{avg_lead:.1f} <span style="font-size: 1rem; color: #64748b;">Days</span></div>
            <div class="kpi-subtext">Lead booking buffer</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-label">Advance Default Rate</span>
                <span class="kpi-badge badge-amber">≥3 Days Lead</span>
            </div>
            <div class="kpi-value">{adv_noshow_rate:.1f}%</div>
            <div class="kpi-subtext">Elevated default exposure</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: Donut Breakdown + Longitudinal Daily Volume
    r1_col1, r1_col2 = st.columns([1, 2])

    with r1_col1:
        st.markdown("""
        <div class="section-card-title">Overall Attendance Distribution</div>
        <div class="section-card-subtitle">Ratio of completed patient visits to missed clinical slots</div>
        """, unsafe_allow_html=True)

        status_counts = filtered_df["attendance_status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]

        fig_donut = px.pie(
            status_counts,
            values="Count",
            names="Status",
            hole=0.62,
            color="Status",
            color_discrete_map={"Showed Up": "#059669", "No Show": "#e11d48"},
        )
        fig_donut.update_traces(
            textinfo="percent+label",
            textfont=dict(family="Plus Jakarta Sans", size=12, color="#ffffff"),
            marker=dict(line=dict(color="#ffffff", width=2)),
        )
        fig_donut.update_layout(
            showlegend=False,
            height=320,
            margin=dict(t=10, b=10, l=10, r=10),
            annotations=[
                dict(
                    text=f"<b>{noshow_rate:.1f}%</b><br><span style='font-size:10px; color:#64748b;'>No-Show</span>",
                    x=0.5,
                    y=0.5,
                    font_size=18,
                    showarrow=False,
                    font_color="#0f172a",
                )
            ],
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with r1_col2:
        st.markdown("""
        <div class="section-card-title">Daily Appointment Volume & Trend</div>
        <div class="section-card-subtitle">Daily consultation cadence stratified by attendance status</div>
        """, unsafe_allow_html=True)

        daily_trend = (
            filtered_df.groupby(["appointment_date", "attendance_status"])
            .size()
            .reset_index(name="Volume")
        )
        fig_trend = px.line(
            daily_trend,
            x="appointment_date",
            y="Volume",
            color="attendance_status",
            color_discrete_map={"Showed Up": "#059669", "No Show": "#e11d48"},
            labels={"appointment_date": "Date", "Volume": "Daily Consultations"},
        )
        fig_trend.update_traces(line=dict(width=2.2))
        apply_clinical_theme(fig_trend, height=320)
        st.plotly_chart(fig_trend, use_container_width=True)

    # Operational Insight Callout
    st.markdown("""
    <div class="clinical-insight">
        <div class="insight-title">Executive Operational Takeaway</div>
        <p class="insight-body">
            Municipal clinics exhibit an aggregate no-show rate of <b>20.2%</b>. However, default rates drop to <b>4.6%</b> for same-day bookings and surge to <b>33.1%</b> for appointments booked over 30 days in advance. Clinical capacity buffers should prioritize same-week and walk-in backfill allocations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Row 2: Weekday Load + SMS Communication Intervention
    r2_col1, r2_col2 = st.columns(2)

    with r2_col1:
        st.markdown("""
        <div class="section-card-title">Attendance Rate Across Days of the Week</div>
        <div class="section-card-subtitle">Evaluating weekly clinical workflow patterns and day-of-week risk</div>
        """, unsafe_allow_html=True)

        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        dow_df = (
            filtered_df.groupby("appointment_day_of_week")["no_show_binary"]
            .agg(["count", "mean"])
            .reindex(weekday_order)
            .dropna()
            .reset_index()
        )
        dow_df["noshow_pct"] = dow_df["mean"] * 100

        fig_dow = px.bar(
            dow_df,
            x="appointment_day_of_week",
            y="noshow_pct",
            text=dow_df["noshow_pct"].apply(lambda x: f"{x:.1f}%"),
            labels={"appointment_day_of_week": "Weekday", "noshow_pct": "Default Rate (%)"},
            color="noshow_pct",
            color_continuous_scale=[[0, "#cbd5e1"], [0.5, "#94a3b8"], [1, "#e11d48"]],
        )
        fig_dow.update_traces(
            textposition="outside",
            marker=dict(line=dict(color="#ffffff", width=1.5)),
        )
        fig_dow.add_hline(
            y=20.2,
            line_dash="dot",
            line_color="#64748b",
            annotation_text="System Baseline (20.2%)",
            annotation_position="bottom right",
        )
        apply_clinical_theme(fig_dow, height=310)
        fig_dow.update_layout(coloraxis_showscale=False, yaxis_range=[0, 32])
        st.plotly_chart(fig_dow, use_container_width=True)

    with r2_col2:
        st.markdown("""
        <div class="section-card-title">SMS Reminder Efficacy (Advance Bookings ≥ 3 Days)</div>
        <div class="section-card-subtitle">Evaluating SMS reminder outcomes isolated from same-day booking bias</div>
        """, unsafe_allow_html=True)

        if len(adv_df) > 0:
            sms_df = adv_df.groupby("sms_desc")["no_show_binary"].agg(["count", "mean"]).reset_index()
            sms_df["noshow_pct"] = sms_df["mean"] * 100

            fig_sms = px.bar(
                sms_df,
                x="sms_desc",
                y="noshow_pct",
                text=sms_df["noshow_pct"].apply(lambda x: f"{x:.1f}%"),
                labels={"sms_desc": "SMS Notification Status", "noshow_pct": "Default Rate (%)"},
                color="sms_desc",
                color_discrete_sequence=["#0284c7", "#059669"],
            )
            fig_sms.update_traces(
                textposition="outside",
                marker=dict(line=dict(color="#ffffff", width=1.5)),
            )
            apply_clinical_theme(fig_sms, height=310)
            fig_sms.update_layout(showlegend=False, yaxis_range=[0, 42])
            st.plotly_chart(fig_sms, use_container_width=True)
        else:
            st.info("No advance appointments meet current filter criteria.")


# ---------------------------------------------------------
# VIEW 2: DEMOGRAPHICS & CLINICAL PROFILE
# ---------------------------------------------------------
elif page == "Demographics & Chronic Profile":
    render_header(
        "Population Health • Epidemiological Profile",
        "Patient Demographics & Chronic Disease Burden",
        "Evaluating attendance compliance across life-stage age cohorts, gender equity, and chronic disease comorbidities.",
    )

    d_col1, d_col2 = st.columns(2)

    with d_col1:
        st.markdown("""
        <div class="section-card-title">Default Rate Across Life-Stage Cohorts</div>
        <div class="section-card-subtitle">Age gradient showing youthful vulnerability vs senior compliance</div>
        """, unsafe_allow_html=True)

        age_summary = (
            filtered_df.groupby("age_group", observed=False)["no_show_binary"]
            .agg(["count", "mean"])
            .reset_index()
        )
        age_summary["noshow_pct"] = age_summary["mean"] * 100

        fig_age = px.bar(
            age_summary,
            x="age_group",
            y="noshow_pct",
            text=age_summary["noshow_pct"].apply(lambda x: f"{x:.1f}%"),
            labels={"age_group": "Age Cohort", "noshow_pct": "Default Rate (%)"},
            color="noshow_pct",
            color_continuous_scale=[[0, "#059669"], [0.5, "#0284c7"], [1, "#e11d48"]],
        )
        fig_age.update_traces(
            textposition="outside",
            marker=dict(line=dict(color="#ffffff", width=1.5)),
        )
        apply_clinical_theme(fig_age, height=330)
        fig_age.update_layout(coloraxis_showscale=False, yaxis_range=[0, 32])
        st.plotly_chart(fig_age, use_container_width=True)

    with d_col2:
        st.markdown("""
        <div class="section-card-title">Gender Attendance Parity</div>
        <div class="section-card-subtitle">Empirical validation: Attendance behavior is gender-invariant (p = 0.176)</div>
        """, unsafe_allow_html=True)

        gender_summary = (
            filtered_df.groupby("gender_full")["no_show_binary"]
            .agg(["count", "mean"])
            .reset_index()
        )
        gender_summary["noshow_pct"] = gender_summary["mean"] * 100

        fig_gen = px.bar(
            gender_summary,
            x="gender_full",
            y="noshow_pct",
            text=gender_summary["noshow_pct"].apply(lambda x: f"{x:.2f}%"),
            labels={"gender_full": "Gender", "noshow_pct": "Default Rate (%)"},
            color="gender_full",
            color_discrete_map={"Female": "#0284c7", "Male": "#0d9488"},
        )
        fig_gen.update_traces(
            textposition="outside",
            marker=dict(line=dict(color="#ffffff", width=1.5)),
        )
        apply_clinical_theme(fig_gen, height=330)
        fig_gen.update_layout(showlegend=False, yaxis_range=[0, 30])
        st.plotly_chart(fig_gen, use_container_width=True)

    st.markdown("""
    <div class="clinical-insight">
        <div class="insight-title">Epidemiological Finding: The Chronic Engagement Effect</div>
        <p class="insight-body">
            Patients diagnosed with chronic diseases (hypertension and diabetes) consistently adhere to appointments at significantly higher rates (<b>17.3% – 18.0% default</b>) than non-chronic patients (<b>20.9% default</b>). Chronic illness prompts consistent engagement with primary care physicians.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_col1, c_col2 = st.columns(2)

    with c_col1:
        st.markdown("""
        <div class="section-card-title">Chronic Disease Comorbidity Gradient</div>
        <div class="section-card-subtitle">Stratified attendance across cumulative disease burdens</div>
        """, unsafe_allow_html=True)

        comorb_order = ["No Chronic Conditions", "Single Condition", "Multimorbid (2+ Conditions)"]
        comorb_summary = (
            filtered_df.groupby("comorbidity_category", observed=False)["no_show_binary"]
            .agg(["count", "mean"])
            .reindex(comorb_order)
            .dropna()
            .reset_index()
        )
        comorb_summary["noshow_pct"] = comorb_summary["mean"] * 100

        fig_comorb = px.bar(
            comorb_summary,
            x="comorbidity_category",
            y="noshow_pct",
            text=comorb_summary["noshow_pct"].apply(lambda x: f"{x:.1f}%"),
            labels={"comorbidity_category": "Comorbidity Level", "noshow_pct": "Default Rate (%)"},
            color="comorbidity_category",
            color_discrete_sequence=["#e11d48", "#0284c7", "#059669"],
        )
        fig_comorb.update_traces(textposition="outside", marker=dict(line=dict(color="#ffffff", width=1.5)))
        apply_clinical_theme(fig_comorb, height=320)
        fig_comorb.update_layout(showlegend=False, yaxis_range=[0, 28])
        st.plotly_chart(fig_comorb, use_container_width=True)

    with c_col2:
        st.markdown("""
        <div class="section-card-title">Condition-Specific Default Rates</div>
        <div class="section-card-subtitle">Diagnosed vs Absent comparison across target clinical diagnoses</div>
        """, unsafe_allow_html=True)

        conds = []
        for c, name in [
            ("hypertension", "Hypertension"),
            ("diabetes", "Diabetes"),
            ("alcoholism", "Alcoholism"),
            ("has_handicap", "Handicap"),
        ]:
            conds.append({
                "Condition": name,
                "Status": "Diagnosed",
                "No-Show Rate (%)": filtered_df[filtered_df[c] == 1]["no_show_binary"].mean() * 100,
            })
            conds.append({
                "Condition": name,
                "Status": "Normal / Absent",
                "No-Show Rate (%)": filtered_df[filtered_df[c] == 0]["no_show_binary"].mean() * 100,
            })
        cond_df = pd.DataFrame(conds)

        fig_cond = px.bar(
            cond_df,
            x="Condition",
            y="No-Show Rate (%)",
            color="Status",
            barmode="group",
            color_discrete_map={"Diagnosed": "#059669", "Normal / Absent": "#94a3b8"},
        )
        fig_cond.update_traces(marker=dict(line=dict(color="#ffffff", width=1.2)))
        apply_clinical_theme(fig_cond, height=320)
        fig_cond.update_layout(yaxis_range=[0, 32])
        st.plotly_chart(fig_cond, use_container_width=True)


# ---------------------------------------------------------
# VIEW 3: SCHEDULING & OPERATIONAL CAPACITY
# ---------------------------------------------------------
elif page == "Scheduling Lead-Time & Capacity":
    render_header(
        "Operations Research • Capacity & Waiting-Time Dynamics",
        "Scheduling Lead Time & Operational Bottlenecks",
        "Quantifying the primary operational determinant of patient attendance: The Waiting-Time Curve.",
    )

    # Lead Time Dual-Axis Curve
    lead_summary = (
        filtered_df.groupby("lead_time_bracket", observed=False)
        .agg(
            Volume=("appointment_id", "count"),
            NoShowRate=("no_show_binary", "mean"),
        )
        .reset_index()
    )
    lead_summary["NoShowPct"] = lead_summary["NoShowRate"] * 100

    fig_dual = go.Figure()
    fig_dual.add_trace(
        go.Bar(
            x=lead_summary["lead_time_bracket"],
            y=lead_summary["Volume"],
            name="Appointment Volume",
            marker=dict(color="#cbd5e1", line=dict(color="#ffffff", width=1.5)),
            yaxis="y",
        )
    )
    fig_dual.add_trace(
        go.Scatter(
            x=lead_summary["lead_time_bracket"],
            y=lead_summary["NoShowPct"],
            name="Default Rate (%)",
            line=dict(color="#e11d48", width=3),
            marker=dict(size=8, color="#e11d48", line=dict(color="#ffffff", width=2)),
            mode="lines+markers+text",
            text=lead_summary["NoShowPct"].apply(lambda x: f"{x:.1f}%"),
            textposition="top center",
            yaxis="y2",
        )
    )
    fig_dual.update_layout(
        title=dict(
            text="The Waiting-Time Curve: Scheduled Volume vs Clinical Default Risk",
            font=dict(size=14, color="#0f172a", family="Plus Jakarta Sans"),
        ),
        xaxis=dict(title="Advance Scheduling Lead Time (Days)"),
        yaxis=dict(title="Total Consultations", side="left", gridcolor="#f1f5f9"),
        yaxis2=dict(
            title="Default Rate (%)",
            overlaying="y",
            side="right",
            range=[0, 45],
            showgrid=False,
        ),
        height=390,
        legend=dict(x=0.01, y=0.98, bgcolor="rgba(255,255,255,0.8)"),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(t=50, b=30, l=45, r=45),
        font=dict(family="Plus Jakarta Sans", color="#334155"),
    )
    st.plotly_chart(fig_dual, use_container_width=True)

    st.markdown("""
    <div class="clinical-insight">
        <div class="insight-title">Strategic Operations Metric: 6.14x Relative Risk</div>
        <p class="insight-body">
            Same-day appointments (0-day lead time) carry an exceptional compliance rate (<b>95.35%</b> attendance). For every week of added waiting duration, no-show rates steadily escalate, plateauing beyond 30 days at <b>33.1%</b> (RR = 6.14x). Hospital schedulers should cap elective booking windows at 14 days.
        </p>
    </div>
    """, unsafe_allow_html=True)

    op_col1, op_col2 = st.columns(2)

    with op_col1:
        st.markdown("""
        <div class="section-card-title">Same-Day vs Advance Booking Contrast</div>
        <div class="section-card-subtitle">Zero-day walk-ins vs multi-day scheduled appointments</div>
        """, unsafe_allow_html=True)

        same_day_summary = (
            filtered_df.groupby("is_same_day")["no_show_binary"]
            .agg(["count", "mean"])
            .reset_index()
        )
        same_day_summary["Type"] = same_day_summary["is_same_day"].map({
            1: "Same-Day Booking (0d)",
            0: "Advance Booking (>0d)",
        })
        same_day_summary["noshow_pct"] = same_day_summary["mean"] * 100

        fig_sameday = px.bar(
            same_day_summary,
            x="Type",
            y="noshow_pct",
            text=same_day_summary["noshow_pct"].apply(lambda x: f"{x:.1f}%"),
            color="Type",
            color_discrete_map={
                "Same-Day Booking (0d)": "#059669",
                "Advance Booking (>0d)": "#e11d48",
            },
            labels={"noshow_pct": "Default Rate (%)"},
        )
        fig_sameday.update_traces(textposition="outside", marker=dict(line=dict(color="#ffffff", width=1.5)))
        apply_clinical_theme(fig_sameday, height=320)
        fig_sameday.update_layout(showlegend=False, yaxis_range=[0, 36])
        st.plotly_chart(fig_sameday, use_container_width=True)

    with op_col2:
        st.markdown("""
        <div class="section-card-title">Age Cohort × Lead Time Cross-Tabulation</div>
        <div class="section-card-subtitle">Default percentage heatmap across age brackets and booking horizons</div>
        """, unsafe_allow_html=True)

        pivot = (
            filtered_df.pivot_table(
                index="age_group",
                columns="lead_time_bracket",
                values="no_show_binary",
                aggfunc="mean",
                observed=False,
            )
            * 100
        )
        fig_pivot = px.imshow(
            pivot,
            text_auto=".1f",
            color_continuous_scale=[[0, "#ecfdf5"], [0.4, "#fed7aa"], [1, "#e11d48"]],
            labels=dict(x="Waiting Duration", y="Age Cohort", color="Default %"),
        )
        apply_clinical_theme(fig_pivot, height=320)
        st.plotly_chart(fig_pivot, use_container_width=True)


# ---------------------------------------------------------
# VIEW 4: GEOGRAPHIC CATCHMENT DISPARITIES
# ---------------------------------------------------------
elif page == "Geographic Catchment Disparities":
    render_header(
        "Geospatial BI • Clinic Catchment Analysis",
        "Geographic Disparities & Clinic Catchment Zones",
        "Spatial variability across 81 municipal healthcare zones in Vitória, Brazil.",
    )

    g_col1, g_col2 = st.columns(2)
    stable_neigh = df_neigh[df_neigh["total_appointments"] >= 100].copy()

    with g_col1:
        st.markdown("""
        <div class="section-card-title">Top 10 High-Risk Catchment Zones</div>
        <div class="section-card-subtitle">Neighborhoods requiring mobile community health worker outreach</div>
        """, unsafe_allow_html=True)

        top10_high = stable_neigh.sort_values(by="no_show_rate_pct", ascending=False).head(10)
        fig_high = px.bar(
            top10_high,
            x="no_show_rate_pct",
            y="neighbourhood",
            orientation="h",
            text=top10_high["no_show_rate_pct"].apply(lambda x: f"{x:.1f}%"),
            color_discrete_sequence=["#e11d48"],
            labels={"no_show_rate_pct": "Default Rate (%)", "neighbourhood": "Neighborhood"},
        )
        fig_high.update_traces(textposition="outside", marker=dict(line=dict(color="#ffffff", width=1)))
        apply_clinical_theme(fig_high, height=360)
        fig_high.update_layout(yaxis=dict(autorange="reversed"), xaxis_range=[0, 38])
        st.plotly_chart(fig_high, use_container_width=True)

    with g_col2:
        st.markdown("""
        <div class="section-card-title">Top 10 High-Compliance Catchment Zones</div>
        <div class="section-card-subtitle">Clinics achieving benchmark attendance reliability</div>
        """, unsafe_allow_html=True)

        top10_low = stable_neigh.sort_values(by="no_show_rate_pct", ascending=True).head(10)
        fig_low = px.bar(
            top10_low,
            x="no_show_rate_pct",
            y="neighbourhood",
            orientation="h",
            text=top10_low["no_show_rate_pct"].apply(lambda x: f"{x:.1f}%"),
            color_discrete_sequence=["#059669"],
            labels={"no_show_rate_pct": "Default Rate (%)", "neighbourhood": "Neighborhood"},
        )
        fig_low.update_traces(textposition="outside", marker=dict(line=dict(color="#ffffff", width=1)))
        apply_clinical_theme(fig_low, height=360)
        fig_low.update_layout(yaxis=dict(autorange="reversed"), xaxis_range=[0, 38])
        st.plotly_chart(fig_low, use_container_width=True)

    st.markdown("""
    <div class="clinical-insight">
        <div class="insight-title">Catchment Risk Matrix Quadrant Analysis</div>
        <p class="insight-body">
            Catchments in the upper-right quadrant combine high consultation volume with elevated no-show rates and high welfare dependency (e.g., <i>Itararé</i>, <i>Jesus de Nazareth</i>). These clinics should be prioritized for dedicated SMS reminder dispatch and municipal transport subsidies.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card-title">Catchment Risk Matrix (Volume vs Default Rate vs Welfare %)</div>
    <div class="section-card-subtitle">Bubble size represents unique patients; color indicates welfare coverage</div>
    """, unsafe_allow_html=True)

    fig_bubble = px.scatter(
        stable_neigh,
        x="total_appointments",
        y="no_show_rate_pct",
        size="unique_patients",
        color="scholarship_rate_pct",
        hover_name="neighbourhood",
        color_continuous_scale="Viridis",
        labels={
            "total_appointments": "Total Consultations",
            "no_show_rate_pct": "Default Rate (%)",
            "scholarship_rate_pct": "Welfare Coverage (%)",
        },
    )
    fig_bubble.add_hline(
        y=20.2,
        line_dash="dash",
        line_color="#e11d48",
        annotation_text="System Baseline (20.2%)",
        annotation_position="bottom right",
    )
    apply_clinical_theme(fig_bubble, height=420)
    st.plotly_chart(fig_bubble, use_container_width=True)

    with st.expander("Searchable Catchment Registry (81 Municipal Neighborhoods)"):
        search_query = st.text_input("Filter by Neighborhood Name:", "")
        display_neigh = df_neigh.copy()
        if search_query:
            display_neigh = display_neigh[
                display_neigh["neighbourhood"].str.contains(search_query, case=False, na=False)
            ]
        st.dataframe(
            display_neigh.rename(
                columns={
                    "neighbourhood": "Neighborhood",
                    "total_appointments": "Total Consultations",
                    "showed_up_count": "Attended",
                    "no_show_count": "No-Shows",
                    "no_show_rate_pct": "Default Rate (%)",
                    "unique_patients": "Unique Patients",
                    "scholarship_rate_pct": "Welfare %",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


# ---------------------------------------------------------
# VIEW 5: STATISTICAL HYPOTHESIS TESTING & INFERENCE
# ---------------------------------------------------------
elif page == "Statistical Inference & Hypotheses":
    render_header(
        "Clinical Biostatistics • Formal Inferential Evidence",
        "Empirical Hypothesis Testing & Statistical Significance",
        "Rigorous verification using Chi-Square (χ²), Cramér's V effect sizes, Welch's t-test, Mann-Whitney U, and Relative Risk.",
    )

    stats_summary = run_full_statistical_analysis(df_raw)

    st.markdown("""
    <div class="section-card-title">1. Categorical Tests: Pearson's Chi-Square (χ²) of Independence</div>
    <div class="section-card-subtitle">Evaluating categorical features against the target binary outcome: Appointment Default (No-Show)</div>
    """, unsafe_allow_html=True)

    chi_df = pd.DataFrame(stats_summary["chi_square_tests"])
    st.dataframe(
        chi_df[
            [
                "feature",
                "chi2_stat",
                "degrees_of_freedom",
                "p_value_formatted",
                "cramers_v",
                "effect_size",
                "statistically_significant",
            ]
        ].rename(
            columns={
                "feature": "Tested Feature",
                "chi2_stat": "Chi-Square (χ²)",
                "degrees_of_freedom": "df",
                "p_value_formatted": "p-value",
                "cramers_v": "Cramér's V",
                "effect_size": "Effect Size Magnitude",
                "statistically_significant": "Significant (α=0.05)",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("<hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 24px 0;'>", unsafe_allow_html=True)

    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.markdown("""
        <div class="section-card-title">2. Continuous Predictor Hypothesis Testing</div>
        <div class="section-card-subtitle">Parametric Welch's t-test and non-parametric Mann-Whitney U test</div>
        """, unsafe_allow_html=True)

        age_t = stats_summary["continuous_variable_tests"]["age"]
        lead_t = stats_summary["continuous_variable_tests"]["lead_time"]

        st.markdown(f"""
        <div class="section-card" style="margin-bottom: 14px;">
            <div style="font-weight: 700; color: #0284c7; font-size: 0.88rem; text-transform: uppercase;">Variable: Patient Age</div>
            <div style="font-size: 0.82rem; color: #475569; margin: 8px 0 12px 0;">
                Attended Mean: <b>{age_t['show_mean']} yrs</b> (±{age_t['show_std']}) | No-Show Mean: <b>{age_t['noshow_mean']} yrs</b> (±{age_t['noshow_std']})
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; background: #f8fafc; padding: 8px 12px; border-radius: 6px; border: 1px solid #e2e8f0;">
                Welch's t = {age_t['t_stat']} (p &lt; 0.0001)<br>
                Mann-Whitney U = {age_t['mwu_stat']:.2e} (p &lt; 0.0001)
            </div>
            <div style="margin-top: 8px; font-size: 0.78rem; color: #047857; font-weight: 600;">
                ✓ Statistically significant: Older patients demonstrate greater compliance.
            </div>
        </div>

        <div class="section-card">
            <div style="font-weight: 700; color: #0284c7; font-size: 0.88rem; text-transform: uppercase;">Variable: Scheduling Lead Time</div>
            <div style="font-size: 0.82rem; color: #475569; margin: 8px 0 12px 0;">
                Attended Mean: <b>{lead_t['show_mean']} days</b> (Median: {lead_t['show_median']}d) | No-Show Mean: <b>{lead_t['noshow_mean']} days</b> (Median: {lead_t['noshow_median']}d)
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; background: #f8fafc; padding: 8px 12px; border-radius: 6px; border: 1px solid #e2e8f0;">
                Welch's t = {lead_t['t_stat']} (p &lt; 0.0001)<br>
                Mann-Whitney U = {lead_t['mwu_stat']:.2e} (p &lt; 0.0001)
            </div>
            <div style="margin-top: 8px; font-size: 0.78rem; color: #047857; font-weight: 600;">
                ✓ Statistically significant: Skewed lead time is the dominant attendance determinant.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with s_col2:
        st.markdown("""
        <div class="section-card-title">3. Relative Risk (RR) & Odds Ratios (OR)</div>
        <div class="section-card-subtitle">Quantifying clinical effect sizes and exposure likelihoods</div>
        """, unsafe_allow_html=True)

        rr_df = pd.DataFrame(stats_summary["relative_risk_analysis"])
        st.dataframe(
            rr_df.rename(
                columns={
                    "risk_factor": "Risk Factor / Exposure",
                    "exposed_rate_pct": "Exposed (%)",
                    "unexposed_rate_pct": "Unexposed (%)",
                    "relative_risk": "Relative Risk (RR)",
                    "odds_ratio": "Odds Ratio (OR)",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


# ---------------------------------------------------------
# VIEW 6: TABLEAU BI ARCHITECTURE & VIVA PREP
# ---------------------------------------------------------
elif page == "Tableau BI Architecture & Viva Prep":
    render_header(
        "Academic & Enterprise BI Architecture",
        "Tableau BI Architecture & Viva Examination Preparation",
        "Technical workbook schematics, copy-paste calculated fields, and academic viva voce briefing.",
    )

    t_tab1, t_tab2, t_tab3 = st.tabs([
        "Tableau Workbooks Architecture",
        "Calculated Fields Reference",
        "Viva Voce Examination Q&A",
    ])

    with t_tab1:
        st.markdown("""
        ### The 4 Interactive Tableau BI Dashboards
        
        The repository provides full technical specifications for 4 production Tableau dashboards:
        
        1. **Dashboard 1: Executive KPI & Attendance Overview**
           - **Target Audience**: Hospital Chief Medical Officer (CMO) & Operations Lead
           - **Core Visuals**: KPI Banner, Donut Distribution, Daily Trend Curve, SMS Interventions
           - **File Guide**: `tableau/dashboard_1_executive_overview.md`
        
        2. **Dashboard 2: Patient Demographics & Clinical Profile**
           - **Target Audience**: Population Health Analysts & Epidemiologists
           - **Core Visuals**: Age Cohort Compliance, Gender Parity Split, Chronic Comorbidity Gradient
           - **File Guide**: `tableau/dashboard_2_demographics_health.md`
        
        3. **Dashboard 3: Operational Lead-Time & Scheduling Analysis**
           - **Target Audience**: Clinic Capacity Planners & Scheduling Coordinators
           - **Core Visuals**: The Waiting-Time Curve (Dual Axis), Same-Day vs Advance, Age × Lead Heatmap
           - **File Guide**: `tableau/dashboard_3_operational_scheduling.md`
        
        4. **Dashboard 4: Geographic & Catchment Attendance Disparities**
           - **Target Audience**: Regional Health Secretariat & Mobile Clinic Fleet Coordinators
           - **Core Visuals**: Top 10 High/Low Risk Rankings, Catchment Risk Matrix (Bubble Scatter)
           - **File Guide**: `tableau/dashboard_4_neighborhood_attendance.md`
        """)

    with t_tab2:
        st.markdown("""
        ### Core Tableau Calculated Field Formulas
        
        Standardized copy-paste formulas ready for direct implementation in Tableau Desktop / Public:
        
        ```tableau
        // 1. Total Consultations
        COUNT([appointment_id])
        
        // 2. No-Show Rate %
        SUM([no_show_binary]) / COUNT([appointment_id])
        
        // 3. Attendance Rate %
        SUM([showed_up_binary]) / COUNT([appointment_id])
        
        // 4. Booking Classification
        IF [lead_time_days] = 0 THEN "Same-Day Booking" 
        ELSE "Advance Booking (>0d)" END
        
        // 5. Chronic Comorbidity Stratification
        IF [chronic_condition_count] = 0 THEN "0. No Chronic Conditions"
        ELSEIF [chronic_condition_count] = 1 THEN "1. Single Disease"
        ELSE "2. Multimorbid (2+)" END
        ```
        """)

    with t_tab3:
        st.markdown("""
        ### Academic Viva Voce Examination Briefing
        """)

        with st.expander("Q1: What is the primary operational determinant of appointment no-shows?"):
            st.markdown(r"""
            **Answer**: Scheduling lead time (waiting days between appointment booking and actual consultation date). Same-day appointments default at **4.65%**, whereas bookings made $>30$ days in advance experience a default rate of **33.1%** ($RR = 6.14$, $\chi^2 = 9623.1, p < 0.0001$).
            """)

        with st.expander("Q2: Does patient gender influence attendance compliance?"):
            st.markdown(r"""
            **Answer**: No. Gender is statistically invariant with respect to attendance compliance. Females default at **20.31%** while males default at **19.97%**. Pearson's Chi-Square test yields $\chi^2 = 1.836, p = 0.1755$, confirming no statistically significant association.
            """)

        with st.expander("Q3: Why do SMS reminders show an apparent paradox (higher default rate for recipients)?"):
            st.markdown(r"""
            **Answer**: **Confounding by indication (lead time)**. The Vitória municipal clinic protocol only dispatched SMS reminders for appointments scheduled at least 3 days in advance. Same-day appointments never received an SMS and had a 4.6% default rate. When isolating advance bookings ($\ge 3$ days), SMS reminders systematically reduce default rates.
            """)

        with st.expander("Q4: Why apply both Welch's t-test and the Mann-Whitney U test on lead time?"):
            st.markdown(r"""
            **Answer**: Scheduling lead time is severely right-skewed with a heavy tail (skewness $> 2.0$, with a spike at 0 days). While Welch's t-test assesses differences in means under unequal variances, the non-parametric **Mann-Whitney U test** compares distribution medians/ranks without assuming normality, making it the mathematical gold standard.
            """)
