# Dashboard 4: Geographic & Clinic Neighborhood Attendance Insights

## 1. Dashboard Objective & Summary
The **Geographic & Clinic Neighborhood Attendance Insights Dashboard** provides regional healthcare planners, community health agents, and clinic administrators with deep spatial intelligence. It analyzes attendance variation across all 81 municipal neighborhoods in Vitória, Brazil, illuminating socioeconomic disparities and targeting localized community interventions.

- **Primary Data Source**: `hospital_appointments_cleaned.csv` or `tableau_neighborhood_analytics.csv`
- **Canvas Size**: `1366 x 768` (Fixed Desktop Browser)
- **Target Audience**: Regional Health Directors, Municipal Health Secretariat, Mobile Clinic Coordinators

---

## 2. Calculated Fields Required
1. `[Neighborhood Reliable Flag]` = `IF [total_appointments] >= 100 THEN "Statistically Robust (>=100)" ELSE "Low Volume (<100)" END`
2. `[No-Show Rate %]` = `[no_show_count] / [total_appointments]` (or `[no_show_rate_pct] / 100`)
3. `[Welfare Enrollment %]` = `[scholarship_count] / [total_appointments]`

---

## 3. Worksheet Construction Steps

### Worksheet 1: Top 10 Highest Default Neighbourhoods
*Purpose: Pinpoint high-risk clinic catchment zones that require aggressive reminder strategies.*

1. Create a new worksheet named **`WS_Top10_Highest_NoShow`**.
2. Drag `[neighbourhood]` to **Rows**.
3. Drag `[no_show_rate_pct]` to **Columns** as horizontal bars.
4. Filter `[total_appointments]` >= `100` (to filter out volatile small sample sizes).
5. Sort `[neighbourhood]` by `[no_show_rate_pct]` **Descending**; limit to Top 10.
6. Color: Crimson Red (`#e74c3c`).
7. Label: No-show rate and volume (e.g. `Santos Dumont: 28.9% (N=1,276)`).

---

### Worksheet 2: Top 10 Most Reliable Neighbourhoods
*Purpose: Benchmark best-performing communities to model successful patient engagement practices.*

1. Create a new worksheet named **`WS_Top10_Lowest_NoShow`**.
2. Drag `[neighbourhood]` to **Rows**.
3. Drag `[no_show_rate_pct]` to **Columns** as horizontal bars.
4. Filter `[total_appointments]` >= `100`.
5. Sort `[neighbourhood]` by `[no_show_rate_pct]` **Ascending**; limit to Top 10 (or Bottom 10).
6. Color: Emerald Green (`#2ecc71`).
7. Label: No-show rate and volume (e.g. `Jardim da Penha: 16.3% (N=3,877)`).

---

### Worksheet 3: Volume vs Default Rate Scatter/Bubble Plot
*Purpose: Map neighborhood operational risk by contrasting clinical load against default rates.*

1. Create a new worksheet named **`WS_Neighborhood_Risk_Matrix`**.
2. Drag `[total_appointments]` to **Columns**.
3. Drag `[no_show_rate_pct]` to **Rows**.
4. Change Mark type to **Circle**.
5. Drag `[neighbourhood]` to **Detail** and **Tooltip**.
6. Drag `[scholarship_rate_pct]` to **Color** (Gradient: Blue to Red).
7. Drag `[unique_patients]` to **Size**.
8. Add Reference Lines:
   - Average appointment volume (vertical line).
   - Overall hospital no-show rate 20.2% (horizontal line).
9. Quadrant Interpretation:
   - **Top-Right (High Volume, High Default)**: Critical operational priority (e.g. Itararé, Jesus de Nazareth).

---

### Worksheet 4: Comprehensive Neighborhood Summary Table
*Purpose: Granular reference table for clinic managers.*

1. Create a new worksheet named **`WS_Neighborhood_Data_Table`**.
2. Drag `[neighbourhood]` to **Rows**.
3. Add to Measure Values:
   - `[total_appointments]`
   - `[no_show_count]`
   - `[no_show_rate_pct]`
   - `[avg_patient_age]`
   - `[avg_lead_time_days]`
   - `[scholarship_rate_pct]`
4. Format numbers cleanly with headers and shading.

---

## 4. Dashboard Assembly & Layout Guide

1. Create Dashboard: Set Size to **1366 x 768 px**.
2. **Top Header Container** (Height: `75 px`):
   - Background: Dark Teal (`#130f40`).
   - Title: "GEOGRAPHIC & CLINIC NEIGHBORHOOD ATTENDANCE ANALYTICS" (White, `18pt`, Bold).
   - Subtitle: "Spatial Disparities, Clinic Catchments & Socioeconomic Indices across Vitória, Brazil" (Yellow, `10pt`).
3. **Upper Container (Height: 340 px)**:
   - **Left Panel (50%)**: `WS_Top10_Highest_NoShow` (Red bars).
   - **Right Panel (50%)**: `WS_Top10_Lowest_NoShow` (Green bars).
4. **Lower Container (Height: 330 px)**:
   - **Left Panel (55%)**: `WS_Neighborhood_Risk_Matrix` (Bubble scatter plot).
   - **Right Panel (45%)**: `WS_Neighborhood_Data_Table` (Interactive lookup table).
5. **Interactive Actions**:
   - Filter action on `WS_Neighborhood_Risk_Matrix`: Clicking any neighborhood bubble filters the entire dashboard to display that community's specific metrics.

---

## 5. Regional Policy & Outreach Interventions
1. **Targeted Mobile Clinic Deployment**: Pockets like Santos Dumont, Santa Cecília, and Itararé exhibit no-show rates exceeding 27%. Dispatching mobile health vans directly into these neighborhoods drastically lowers transit barriers.
2. **Community Health Agent Follow-Up**: Leverage Brazilian Family Health Strategy (*Estratégia Saúde da Família*) agents to conduct in-person home visits for welfare-enrolled patients with upcoming consultations.
3. **Public Transit Partnerships**: Provide municipal transit tokens or subsidized van shuttles for patients in distant peripheral neighborhoods booked for specialized diagnostic consultations at central clinics.
