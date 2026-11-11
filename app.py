"""Hospital Patient & Appointment Analytics - Interactive Web Application.

Provides a live, interactive browser-based dashboard suite implementing:
1. Executive KPI & Attendance Overview
2. Patient Demographics & Clinical Profile
3. Operational & Scheduling Lead-Time Analysis
4. Geographic & Clinic Neighborhood Attendance
5. Statistical Hypothesis Testing Explorer
6. Tableau Blueprints & Viva Preparation
"""

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Centralized imports
from src.config import (
    CLEANED_DATA_FILE,
    TABLEAU_NEIGHBORHOOD_FILE,
    PALETTE_ATTENDANCE,
)
from src.statistical_analysis import run_full_statistical_analysis

# Page configuration
st.set_page_config(
    page_title="Hospital Patient & Appointment Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for executive look
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3799;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #636e72;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 4px solid #3498db;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and cache the master cleaned dataset."""
    df = pd.read_csv(CLEANED_DATA_FILE)
    df["scheduled_datetime"] = pd.to_datetime(df["scheduled_datetime"])
    df["appointment_date"] = pd.to_datetime(df["appointment_date"])
    return df


@st.cache_data
def load_neighborhood_summary():
    """Load neighborhood aggregate table."""
    return pd.read_csv(TABLEAU_NEIGHBORHOOD_FILE)


# Load dataset
df_raw = load_data()
df_neigh = load_neighborhood_summary()

# ----------------- SIDEBAR -----------------
st.sidebar.image("https://img.icons8.com/fluency/96/hospital.png", width=70)
st.sidebar.title("Hospital Analytics BI")
st.sidebar.markdown("**Interactive Dashboard Suite**")

# Navigation Selector
page = st.sidebar.radio(
    "Select View / Dashboard:",
    [
        "📊 Dashboard 1: Executive KPI Overview",
        "👥 Dashboard 2: Demographics & Clinical Profile",
        "⏱️ Dashboard 3: Scheduling & Lead-Time Analysis",
        "🗺️ Dashboard 4: Geographic Neighborhoods",
        "🔬 Statistical Hypothesis Testing",
        "📘 Tableau Architecture & Viva Q&A",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters")

# Gender Filter
gender_filter = st.sidebar.multiselect(
    "Patient Gender:",
    options=["Female", "Male"],
    default=["Female", "Male"],
)

# Age Bracket Filter
age_filter = st.sidebar.multiselect(
    "Age Group:",
    options=list(df_raw["age_group"].dropna().unique()),
    default=list(df_raw["age_group"].dropna().unique()),
)

# Welfare Filter
welfare_filter = st.sidebar.multiselect(
    "Bolsa Família Welfare:",
    options=list(df_raw["scholarship_desc"].dropna().unique()),
    default=list(df_raw["scholarship_desc"].dropna().unique()),
)

# Apply Filters
filtered_df = df_raw[
    (df_raw["gender_full"].isin(gender_filter))
    & (df_raw["age_group"].isin(age_filter))
    & (df_raw["scholarship_desc"].isin(welfare_filter))
]

st.sidebar.info(f"Displaying **{len(filtered_df):,}** of **{len(df_raw):,}** total appointments.")

# ----------------- DASHBOARD 1: EXECUTIVE OVERVIEW -----------------
if page == "📊 Dashboard 1: Executive KPI Overview":
    st.markdown("<p class='main-header'>🏥 Executive KPI & Attendance Overview</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>High-level attendance KPIs, daily volume trends, and communication interventions</p>", unsafe_allow_html=True)

    # Top KPI Metrics
    total_appts = len(filtered_df)
    total_shows = int(filtered_df["showed_up_binary"].sum())
    total_noshows = int(filtered_df["no_show_binary"].sum())
    noshow_rate = (total_noshows / total_appts * 100) if total_appts > 0 else 0
    avg_lead = filtered_df["lead_time_days"].mean() if total_appts > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Appointments", f"{total_appts:,}")
    col2.metric("Completed Shows", f"{total_shows:,}", f"{100 - noshow_rate:.1f}%")
    col3.metric("No-Shows (Defaults)", f"{total_noshows:,}", f"-{noshow_rate:.1f}%", delta_color="inverse")
    col4.metric("No-Show Rate (%)", f"{noshow_rate:.1f}%")
    col5.metric("Avg Lead Time", f"{avg_lead:.1f} Days")

    st.markdown("---")

    # Row 1: Donut + Daily Trend
    row1_c1, row1_c2 = st.columns([1, 2])

    with row1_c1:
        st.subheader("Attendance Status Breakdown")
        status_counts = filtered_df["attendance_status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_donut = px.pie(
            status_counts,
            values="Count",
            names="Status",
            hole=0.45,
            color="Status",
            color_discrete_map={"Showed Up": "#2ecc71", "No Show": "#e74c3c"},
        )
        fig_donut.update_traces(textinfo="percent+label", textfont_size=13)
        fig_donut.update_layout(showlegend=False, margin=dict(t=20, b=20, l=10, r=10), height=350)
        st.plotly_chart(fig_donut, use_container_width=True)

    with row1_c2:
        st.subheader("Daily Appointment Volume & Trend")
        daily_trend = filtered_df.groupby(["appointment_date", "attendance_status"]).size().reset_index(name="Volume")
        fig_trend = px.line(
            daily_trend,
            x="appointment_date",
            y="Volume",
            color="attendance_status",
            color_discrete_map={"Showed Up": "#2ecc71", "No Show": "#e74c3c"},
            labels={"appointment_date": "Appointment Date", "Volume": "Number of Appointments"},
        )
        fig_trend.update_layout(height=350, margin=dict(t=20, b=20, l=10, r=10), legend_title_text="Status")
        st.plotly_chart(fig_trend, use_container_width=True)

    # Row 2: Weekday Load + SMS Reminder Impact
    row2_c1, row2_c2 = st.columns(2)

    with row2_c1:
        st.subheader("Attendance by Day of the Week")
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        dow_df = filtered_df.groupby("appointment_day_of_week")["no_show_binary"].agg(["count", "mean"]).reindex(weekday_order).reset_index()
        dow_df["noshow_pct"] = dow_df["mean"] * 100
        fig_dow = px.bar(
            dow_df,
            x="appointment_day_of_week",
            y="noshow_pct",
            text=dow_df["noshow_pct"].apply(lambda x: f"{x:.1f}%"),
            labels={"appointment_day_of_week": "Weekday", "noshow_pct": "No-Show Rate (%)"},
            color="noshow_pct",
            color_continuous_scale="Reds",
        )
        fig_dow.update_layout(height=320, coloraxis_showscale=False, yaxis_range=[0, 30])
        st.plotly_chart(fig_dow, use_container_width=True)

    with row2_c2:
        st.subheader("SMS Reminder Impact (Advance Bookings ≥ 3 Days)")
        adv_df = filtered_df[filtered_df["lead_time_days"] >= 3]
        if len(adv_df) > 0:
            sms_df = adv_df.groupby("sms_desc")["no_show_binary"].agg(["count", "mean"]).reset_index()
            sms_df["noshow_pct"] = sms_df["mean"] * 100
            fig_sms = px.bar(
                sms_df,
                x="sms_desc",
                y="noshow_pct",
                text=sms_df["noshow_pct"].apply(lambda x: f"{x:.1f}%"),
                labels={"sms_desc": "SMS Notification", "noshow_pct": "No-Show Rate (%)"},
                color="sms_desc",
                color_discrete_sequence=["#e67e22", "#27ae60"],
            )
            fig_sms.update_layout(height=320, showlegend=False, yaxis_range=[0, 40])
            st.plotly_chart(fig_sms, use_container_width=True)
        else:
            st.warning("No advance bookings match current filters.")

# ----------------- DASHBOARD 2: DEMOGRAPHICS & CLINICAL -----------------
elif page == "👥 Dashboard 2: Demographics & Clinical Profile":
    st.markdown("<p class='main-header'>👥 Patient Demographics & Clinical Health Profile</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Stratified compliance across age brackets, gender parity, and chronic disease burdens</p>", unsafe_allow_html=True)

    d_col1, d_col2 = st.columns(2)

    with d_col1:
        st.subheader("No-Show Rate across Life Stage Age Groups")
        age_summary = filtered_df.groupby("age_group", observed=False)["no_show_binary"].agg(["count", "mean"]).reset_index()
        age_summary["noshow_pct"] = age_summary["mean"] * 100
        fig_age = px.bar(
            age_summary,
            x="age_group",
            y="noshow_pct",
            text=age_summary["noshow_pct"].apply(lambda x: f"{x:.1f}%"),
            labels={"age_group": "Age Bracket", "noshow_pct": "No-Show Rate (%)"},
            color="noshow_pct",
            color_continuous_scale="Blues_r",
        )
        fig_age.update_layout(height=340, coloraxis_showscale=False, yaxis_range=[0, 32])
        st.plotly_chart(fig_age, use_container_width=True)

    with d_col2:
        st.subheader("Gender Attendance Comparison")
        gender_summary = filtered_df.groupby("gender_full")["no_show_binary"].agg(["count", "mean"]).reset_index()
        gender_summary["noshow_pct"] = gender_summary["mean"] * 100
        fig_gen = px.bar(
            gender_summary,
            x="gender_full",
            y="noshow_pct",
            text=gender_summary["noshow_pct"].apply(lambda x: f"{x:.2f}%"),
            labels={"gender_full": "Gender", "noshow_pct": "No-Show Rate (%)"},
            color="gender_full",
            color_discrete_map={"Female": "#e91e63", "Male": "#3498db"},
        )
        fig_gen.update_layout(height=340, showlegend=False, yaxis_range=[0, 30])
        st.plotly_chart(fig_gen, use_container_width=True)

    st.markdown("---")
    c_col1, c_col2 = st.columns(2)

    with c_col1:
        st.subheader("Chronic Disease Comorbidity Gradient")
        comorb_order = ["No Chronic Conditions", "Single Condition", "Multimorbid (2+ Conditions)"]
        comorb_summary = filtered_df.groupby("comorbidity_category", observed=False)["no_show_binary"].agg(["count", "mean"]).reindex(comorb_order).reset_index()
        comorb_summary["noshow_pct"] = comorb_summary["mean"] * 100
        fig_comorb = px.bar(
            comorb_summary,
            x="comorbidity_category",
            y="noshow_pct",
            text=comorb_summary["noshow_pct"].apply(lambda x: f"{x:.1f}%"),
            labels={"comorbidity_category": "Comorbidity Level", "noshow_pct": "No-Show Rate (%)"},
            color="comorbidity_category",
            color_discrete_sequence=["#1abc9c", "#f39c12", "#8e44ad"],
        )
        fig_comorb.update_layout(height=340, showlegend=False, yaxis_range=[0, 28])
        st.plotly_chart(fig_comorb, use_container_width=True)

    with c_col2:
        st.subheader("Individual Chronic Conditions Breakdown")
        conds = []
        for c, name in [("hypertension", "Hypertension"), ("diabetes", "Diabetes"), ("alcoholism", "Alcoholism"), ("has_handicap", "Handicap")]:
            conds.append({"Condition": name, "Status": "Diagnosed", "No-Show Rate (%)": filtered_df[filtered_df[c] == 1]["no_show_binary"].mean() * 100})
            conds.append({"Condition": name, "Status": "Normal/Absent", "No-Show Rate (%)": filtered_df[filtered_df[c] == 0]["no_show_binary"].mean() * 100})
        cond_df = pd.DataFrame(conds)
        fig_cond = px.bar(
            cond_df,
            x="Condition",
            y="No-Show Rate (%)",
            color="Status",
            barmode="group",
            color_discrete_map={"Diagnosed": "#e74c3c", "Normal/Absent": "#3498db"},
        )
        fig_cond.update_layout(height=340, yaxis_range=[0, 28])
        st.plotly_chart(fig_cond, use_container_width=True)

# ----------------- DASHBOARD 3: SCHEDULING & LEAD-TIME -----------------
elif page == "⏱️ Dashboard 3: Scheduling & Lead-Time Analysis":
    st.markdown("<p class='main-header'>⏱️ Operational & Scheduling Lead-Time Analysis</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>The Waiting-Time Curve: Quantifying the primary operational driver of patient default</p>", unsafe_allow_html=True)

    # Lead Time Dual-Axis Curve
    lead_summary = filtered_df.groupby("lead_time_bracket", observed=False).agg(
        Volume=("appointment_id", "count"),
        NoShowRate=("no_show_binary", "mean"),
    ).reset_index()
    lead_summary["NoShowPct"] = lead_summary["NoShowRate"] * 100

    fig_dual = go.Figure()
    fig_dual.add_trace(go.Bar(
        x=lead_summary["lead_time_bracket"],
        y=lead_summary["Volume"],
        name="Appointment Volume",
        marker_color="#bdc3c7",
        yaxis="y",
    ))
    fig_dual.add_trace(go.Scatter(
        x=lead_summary["lead_time_bracket"],
        y=lead_summary["NoShowPct"],
        name="No-Show Rate (%)",
        line=dict(color="#c0392b", width=3),
        mode="lines+markers+text",
        text=lead_summary["NoShowPct"].apply(lambda x: f"{x:.1f}%"),
        textposition="top center",
        yaxis="y2",
    ))
    fig_dual.update_layout(
        title="The Waiting-Time Curve: Volume vs Default Rate",
        xaxis=dict(title="Scheduling Lead Time (Waiting Days)"),
        yaxis=dict(title="Appointment Volume", side="left"),
        yaxis2=dict(title="No-Show Rate (%)", overlaying="y", side="right", range=[0, 45]),
        height=400,
        legend=dict(x=0.01, y=0.99),
        margin=dict(t=50, b=30, l=40, r=40),
    )
    st.plotly_chart(fig_dual, use_container_width=True)

    st.markdown("---")
    op_col1, op_col2 = st.columns(2)

    with op_col1:
        st.subheader("Same-Day vs Advance Booking Contrast")
        same_day_summary = filtered_df.groupby("is_same_day")["no_show_binary"].agg(["count", "mean"]).reset_index()
        same_day_summary["Type"] = same_day_summary["is_same_day"].map({1: "Same-Day Booking (0d)", 0: "Advance Booking (>0d)"})
        same_day_summary["noshow_pct"] = same_day_summary["mean"] * 100
        fig_sameday = px.bar(
            same_day_summary,
            x="Type",
            y="noshow_pct",
            text=same_day_summary["noshow_pct"].apply(lambda x: f"{x:.1f}%"),
            color="Type",
            color_discrete_map={"Same-Day Booking (0d)": "#2ecc71", "Advance Booking (>0d)": "#e74c3c"},
            labels={"noshow_pct": "No-Show Rate (%)"},
        )
        fig_sameday.update_layout(height=340, showlegend=False, yaxis_range=[0, 35])
        st.plotly_chart(fig_sameday, use_container_width=True)

    with op_col2:
        st.subheader("Age Bracket × Lead Time Cross-Tabulation")
        pivot = filtered_df.pivot_table(
            index="age_group",
            columns="lead_time_bracket",
            values="no_show_binary",
            aggfunc="mean",
            observed=False,
        ) * 100
        fig_pivot = px.imshow(
            pivot,
            text_auto=".1f",
            color_continuous_scale="YlOrRd",
            labels=dict(x="Waiting Duration", y="Age Bracket", color="No-Show %"),
        )
        fig_pivot.update_layout(height=340)
        st.plotly_chart(fig_pivot, use_container_width=True)

# ----------------- DASHBOARD 4: GEOGRAPHIC NEIGHBORHOODS -----------------
elif page == "🗺️ Dashboard 4: Geographic Neighborhoods":
    st.markdown("<p class='main-header'>🗺️ Geographic & Clinic Neighborhood Attendance Insights</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Spatial Disparities across 81 Municipal Catchment Zones in Vitória, Brazil</p>", unsafe_allow_html=True)

    g_col1, g_col2 = st.columns(2)

    # Filter neighborhoods with >= 100 appointments for stability
    stable_neigh = df_neigh[df_neigh["total_appointments"] >= 100].copy()

    with g_col1:
        st.subheader("Top 10 Highest Default Neighbourhoods")
        top10_high = stable_neigh.sort_values(by="no_show_rate_pct", ascending=False).head(10)
        fig_high = px.bar(
            top10_high,
            x="no_show_rate_pct",
            y="neighbourhood",
            orientation="h",
            text=top10_high["no_show_rate_pct"].apply(lambda x: f"{x:.1f}%"),
            color_discrete_sequence=["#e74c3c"],
            labels={"no_show_rate_pct": "No-Show Rate (%)", "neighbourhood": "Neighbourhood"},
        )
        fig_high.update_layout(yaxis=dict(autorange="reversed"), height=360, xaxis_range=[0, 35])
        st.plotly_chart(fig_high, use_container_width=True)

    with g_col2:
        st.subheader("Top 10 Most Reliable Neighbourhoods")
        top10_low = stable_neigh.sort_values(by="no_show_rate_pct", ascending=True).head(10)
        fig_low = px.bar(
            top10_low,
            x="no_show_rate_pct",
            y="neighbourhood",
            orientation="h",
            text=top10_low["no_show_rate_pct"].apply(lambda x: f"{x:.1f}%"),
            color_discrete_sequence=["#2ecc71"],
            labels={"no_show_rate_pct": "No-Show Rate (%)", "neighbourhood": "Neighbourhood"},
        )
        fig_low.update_layout(yaxis=dict(autorange="reversed"), height=360, xaxis_range=[0, 35])
        st.plotly_chart(fig_low, use_container_width=True)

    st.markdown("---")
    st.subheader("Clinic Catchment Risk Matrix (Volume vs Default Rate vs Welfare)")
    fig_bubble = px.scatter(
        stable_neigh,
        x="total_appointments",
        y="no_show_rate_pct",
        size="unique_patients",
        color="scholarship_rate_pct",
        hover_name="neighbourhood",
        color_continuous_scale="Plasma",
        labels={
            "total_appointments": "Total Consultations",
            "no_show_rate_pct": "No-Show Rate (%)",
            "scholarship_rate_pct": "Welfare (Bolsa Família) %",
        },
    )
    fig_bubble.add_hline(y=20.2, line_dash="dash", line_color="red", annotation_text="Baseline (20.2%)")
    fig_bubble.update_layout(height=420)
    st.plotly_chart(fig_bubble, use_container_width=True)

    with st.expander("🔍 View Complete Neighborhood Data Table"):
        st.dataframe(df_neigh, use_container_width=True)

# ----------------- STATISTICAL HYPOTHESIS TESTING -----------------
elif page == "🔬 Statistical Hypothesis Testing":
    st.markdown("<p class='main-header'>🔬 Statistical Hypothesis Testing & Rigorous Inference</p>", unsafe_allow_html=True)
    st.markdown(r"<p class='sub-header'>Formal empirical tests: Chi-Square ($\chi^2$), Cramér's V, Mann-Whitney U, and Relative Risk</p>", unsafe_allow_html=True)

    stats_summary = run_full_statistical_analysis(df_raw)

    st.subheader(r"1. Chi-Square ($\chi^2$) Tests of Independence (Target: No-Show Status)")
    chi_df = pd.DataFrame(stats_summary["chi_square_tests"])
    st.dataframe(
        chi_df[["feature", "chi2_stat", "degrees_of_freedom", "p_value_formatted", "cramers_v", "effect_size", "statistically_significant"]].rename(
            columns={
                "feature": "Feature Tested",
                "chi2_stat": "Chi-Square (χ²)",
                "degrees_of_freedom": "df",
                "p_value_formatted": "p-value",
                "cramers_v": "Cramér's V",
                "effect_size": "Effect Size",
                "statistically_significant": "Significant?",
            }
        ),
        use_container_width=True,
    )

    st.markdown("---")
    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.subheader("2. Continuous Variable Tests")
        age_t = stats_summary["continuous_variable_tests"]["age"]
        lead_t = stats_summary["continuous_variable_tests"]["lead_time"]

        st.markdown(f"""
        **Patient Age**:
        - Showed Up Mean: **{age_t['show_mean']} years** (±{age_t['show_std']})
        - No-Show Mean: **{age_t['noshow_mean']} years** (±{age_t['noshow_std']})
        - Welch's $t = {age_t['t_stat']}$, $p < 0.0001$
        - Mann-Whitney $U = {age_t['mwu_stat']:.1e}$, $p < 0.0001$
        
        **Scheduling Lead Time (Waiting Days)**:
        - Showed Up Mean: **{lead_t['show_mean']} days** (Median: {lead_t['show_median']}d)
        - No-Show Mean: **{lead_t['noshow_mean']} days** (Median: {lead_t['noshow_median']}d)
        - Welch's $t = {lead_t['t_stat']}$, $p < 0.0001$
        - Mann-Whitney $U = {lead_t['mwu_stat']:.1e}$, $p < 0.0001$
        """)

    with s_col2:
        st.subheader("3. Relative Risk (RR) and Odds Ratio (OR)")
        rr_df = pd.DataFrame(stats_summary["relative_risk_analysis"])
        st.dataframe(
            rr_df.rename(
                columns={
                    "risk_factor": "Risk Factor",
                    "exposed_rate_pct": "Exposed (%)",
                    "unexposed_rate_pct": "Unexposed (%)",
                    "relative_risk": "Relative Risk (RR)",
                    "odds_ratio": "Odds Ratio (OR)",
                }
            ),
            use_container_width=True,
        )

# ----------------- TABLEAU ARCHITECTURE & VIVA -----------------
elif page == "📘 Tableau Architecture & Viva Q&A":
    st.markdown("<p class='main-header'>📘 Tableau BI Architecture & Examination Preparation</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Documentation references, calculated fields, and academic viva questions</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Tableau Workbooks", "🧮 Calculated Fields Reference", "🎓 Viva Examination Q&A"])

    with tab1:
        st.markdown("""
        ### The 4 Interactive Tableau Dashboards
        1. **Executive KPI & Attendance Overview** ([Guide Link](tableau/dashboard_1_executive_overview.md))
           - Primary Target: Hospital CMO & Operations Lead
           - Key Metrics: Total Volume, Shows, Defaults, Daily Trend, SMS Impact
        2. **Patient Demographics & Clinical Profile** ([Guide Link](tableau/dashboard_2_demographics_health.md))
           - Primary Target: Population Health Analysts & Epidemiologists
           - Key Metrics: Age pyramid, Gender breakdown, Chronic Comorbidities
        3. **Operational & Scheduling Lead-Time** ([Guide Link](tableau/dashboard_3_operational_scheduling.md))
           - Primary Target: Clinic Capacity Planners & Scheduling Coordinators
           - Key Metrics: The Waiting-Time Curve, Same-Day contrast, Booking hours
        4. **Geographic & Clinic Neighborhood Attendance** ([Guide Link](tableau/dashboard_4_neighborhood_attendance.md))
           - Primary Target: Regional Health Secretariat & Mobile Clinic Outreach
           - Key Metrics: Top 10 High/Low default catchments, Risk Matrix
        """)

    with tab2:
        st.markdown("""
        ### Core Tableau Calculated Field Formulas
        ```tableau
        // 1. Total Appointments
        COUNT([appointment_id])

        // 2. No-Show Rate %
        SUM([no_show_binary]) / COUNT([appointment_id])

        // 3. Attendance Rate %
        SUM([showed_up_binary]) / COUNT([appointment_id])

        // 4. Booking Type
        IF [lead_time_days] = 0 THEN "Same-Day Booking" ELSE "Advance Booking (>0d)" END

        // 5. Comorbidity Category
        IF [chronic_condition_count] = 0 THEN "0. No Chronic Conditions"
        ELSEIF [chronic_condition_count] = 1 THEN "1. Single Disease"
        ELSE "2. Multimorbid (2+)" END
        ```
        """)

    with tab3:
        st.markdown(r"""
        ### Top Viva Examination Questions & Answers
        - **Q: What is the primary operational determinant of appointment default?**
          - *A*: Scheduling lead time (waiting days). Same-day appointments default at 4.65%, whereas appointments booked >30 days in advance default at 33.1% ($RR = 6.14$).
        - **Q: Does gender influence no-shows?**
          - *A*: No. Chi-square test yields $\chi^2 = 1.836, p = 0.1755$ (not statistically significant).
        - **Q: What explains the SMS counter-intuitive trend?**
          - *A*: Confounding by indication. SMS was only sent for advance appointments ($\ge 3$ days), which already carry an elevated default baseline ($>28\%$).
        - **Q: Why use both t-test and Mann-Whitney U?**
          - *A*: Lead time is severely right-skewed; the non-parametric Mann-Whitney U test is the statistical gold standard for skewed continuous data.
        """)
