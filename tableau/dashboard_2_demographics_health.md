# Dashboard 2: Patient Demographics & Clinical Profile

## 1. Dashboard Objective & Summary
The **Patient Demographics & Clinical Profile Dashboard** allows population health researchers, epidemiologists, and clinical directors to evaluate how patient age, gender, socioeconomic welfare status, and chronic disease burdens correlate with appointment attendance.

- **Primary Data Source**: `hospital_appointments_cleaned.csv` (or `tableau_demographics_health.csv`)
- **Canvas Size**: `1366 x 768` (Fixed Desktop Browser)
- **Target Audience**: Chief Medical Officer, Population Health Analysts, Community Health Coordinators

---

## 2. Calculated Fields Required
1. `[Comorbidity Level]` = `IF [chronic_condition_count] = 0 THEN "0. No Chronic Conditions" ELSEIF [chronic_condition_count] = 1 THEN "1. Single Disease" ELSE "2. Multimorbid (2+)" END`
2. `[No-Show Rate %]` = `SUM([no_show_binary]) / COUNT([appointment_id])`
3. `[Attendance Rate %]` = `SUM([showed_up_binary]) / COUNT([appointment_id])`

---

## 3. Worksheet Construction Steps

### Worksheet 1: Age Bracket Attendance Pyramid / Bar
*Purpose: Reveal age cohorts most prone to missing appointments.*

1. Create a new worksheet named **`WS_Age_Group_Attendance`**.
2. Drag `[age_group]` to **Columns** (sorted: Children, Youth, Young Adults, Middle-Aged, Seniors).
3. Drag `[Total Appointments]` to **Rows** as primary bar height.
4. Drag `[attendance_status]` to **Color** (Emerald Green for Showed Up, Crimson Red for No Show).
5. Drag `[No-Show Rate %]` to **Tooltip** and **Label**.
6. Format bar labels: Bold, percentage format.

---

### Worksheet 2: Gender Distribution & Compliance
*Purpose: Dissect appointment volume and default propensity between Female and Male cohorts.*

1. Create a new worksheet named **`WS_Gender_Comparison`**.
2. Drag `[gender_full]` to **Columns**.
3. Drag `[Total Appointments]` to **Rows**.
4. Drag `[No-Show Rate %]` to **Label** and **Color**.
5. Key Observation: Females represent ~65% of all bookings, but their default rate (~20.3%) is virtually identical to males (~19.96%), confirming gender is not a statistically significant attendance driver ($p = 0.1755$).

---

### Worksheet 3: Chronic Condition Comparison Matrix
*Purpose: Benchmark attendance across four diagnosed clinical conditions.*

1. Create a new worksheet named **`WS_Chronic_Condition_Matrix`**.
2. Create a clustered bar chart or side-by-side table:
   - Conditions to compare: Hypertension, Diabetes, Alcoholism, Handicap.
   - For each condition, show Attendance Rate for Diagnosed (`1`) vs Non-diagnosed (`0`).
3. Add `[No-Show Rate %]` to **Rows** and **Label**.
4. Color by Condition Presence (Blue for Diagnosed, Slate Gray for Non-diagnosed).

---

### Worksheet 4: Comorbidity Burden Analysis
*Purpose: Analyze whether multiple chronic illnesses increase appointment compliance.*

1. Create a new worksheet named **`WS_Comorbidity_Burden`**.
2. Drag `[comorbidity_category]` to **Columns** (ordered: No Chronic Conditions, Single Condition, Multimorbid).
3. Drag `[No-Show Rate %]` to **Rows**.
4. Change Mark type to **Bar** with gradient palette (from Yellow-Orange to Deep Purple).
5. Add `[Total Appointments]` to **Tooltip**.
6. Label each bar with the exact no-show rate.

---

### Worksheet 5: Bolsa Família Welfare (Scholarship) Impact
*Purpose: Measure attendance disparity between low-income welfare recipients and standard patients.*

1. Create a new worksheet named **`WS_Welfare_Impact`**.
2. Drag `[scholarship_desc]` to **Columns**.
3. Drag `[No-Show Rate %]` to **Rows**.
4. Color by `[scholarship_desc]` (e.g. Amber `#e67e22` for Welfare, Gray `#95a5a6` for Standard).
5. Format labels with no-show rate percentage.

---

## 4. Dashboard Assembly & Layout Guide

1. Create Dashboard: Set Size to **1366 x 768 px**.
2. **Top Header** (Height: `75 px`):
   - Background: Slate Indigo (`#2c3e50`).
   - Title: "PATIENT DEMOGRAPHICS & CLINICAL HEALTH PROFILES" (White, `18pt`, Bold).
   - Subtitle: "Stratified Compliance by Age, Gender, Chronic Illnesses & Socioeconomic Welfare" (Light Blue, `10pt`).
3. **Filter Bar Container** (Height: `50 px`):
   - Horizontal container holding quick filters: `[gender_full]`, `[age_group]`, `[scholarship_desc]`, `[hypertension_desc]`.
   - Set filters to "Apply to All Using This Data Source".
4. **Main Grid (2 x 2 Arrangement)**:
   - **Top-Left**: `WS_Age_Group_Attendance` (Age curve).
   - **Top-Right**: `WS_Comorbidity_Burden` (Multimorbidity gradient).
   - **Bottom-Left**: `WS_Chronic_Condition_Matrix` (Hypertension & Diabetes adherence).
   - **Bottom-Right**: `WS_Welfare_Impact` & `WS_Gender_Comparison`.
5. **Interactive Actions**:
   - Filter action on `WS_Age_Group_Attendance`: Clicking an age bracket filters chronic conditions and comorbidity profiles for that specific age cohort.

---

## 5. Clinical & Epidemiological Insights
- **Youth Vulnerability**: Adolescents and young adults (13–24) experience the highest default rate (~24.5%), driven by active school/work schedules and lack of direct parental supervision.
- **Senior Compliance**: Seniors (65+) display the highest compliance (~15.2% default rate).
- **The Chronic Care Effect**: Patients managing hypertension (17.3% no-show) or diabetes (18.0% no-show) demonstrate higher attendance than patients without chronic diagnoses (~20.9% no-show), reflecting continuous prescription renewal needs.
