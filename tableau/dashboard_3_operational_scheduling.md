# Dashboard 3: Operational & Scheduling Lead-Time Analysis

## 1. Dashboard Objective & Summary
The **Operational & Scheduling Lead-Time Dashboard** empowers clinic managers, patient access coordinators, and scheduling optimization teams to pinpoint scheduling bottlenecks. It centers on the single most influential operational metric in healthcare attendance: **the lead time (waiting duration between booking and consultation)**.

- **Primary Data Source**: `hospital_appointments_cleaned.csv` (or `tableau_scheduling_operations.csv`)
- **Canvas Size**: `1366 x 768` (Fixed Desktop Browser)
- **Target Audience**: Outpatient Clinic Operations Managers, Capacity Planners, Scheduling Supervisors

---

## 2. Calculated Fields Required
1. `[Booking Type]` = `IF [lead_time_days] = 0 THEN "Same-Day Booking" ELSE "Advance Booking (> 0 Days)" END`
2. `[Lead Time Sort]` = `CASE [lead_time_bracket] WHEN "Same Day (0d)" THEN 1 WHEN "Short Term (1-3d)" THEN 2 WHEN "Medium Term (4-7d)" THEN 3 WHEN "1-2 Weeks (8-14d)" THEN 4 WHEN "2-4 Weeks (15-30d)" THEN 5 ELSE 6 END`
3. `[No-Show Rate %]` = `SUM([no_show_binary]) / COUNT([appointment_id])`

---

## 3. Worksheet Construction Steps

### Worksheet 1: The Waiting Time Dual-Axis Curve
*Purpose: Illustrate the exponential escalation of default probability as waiting duration lengthens.*

1. Create a new worksheet named **`WS_Lead_Time_Curve`**.
2. Drag `[lead_time_bracket]` to **Columns** (Sort manually or via `[Lead Time Sort]`).
3. Drag `[Total Appointments]` to **Rows** (Mark type: **Bar**, Light Slate `#bdc3c7`).
4. Drag `[No-Show Rate %]` to **Rows** next to `[Total Appointments]`.
5. Right-click the second measure on Rows and select **Dual Axis**.
6. Change the second mark type to **Line** with Markers:
   - Line Color: Crimson Red (`#c0392b`), Size: Thick (`3pt`).
   - Add `[No-Show Rate %]` to **Label** on the line mark.
7. Title: "The Waiting-Time Curve: Appointment Volume vs Default Rate".

---

### Worksheet 2: Same-Day vs Advance Booking Contrast
*Purpose: Stark benchmark between instantaneous demand and advance reservations.*

1. Create a new worksheet named **`WS_SameDay_vs_Advance`**.
2. Drag `[Booking Type]` to **Columns**.
3. Drag `[No-Show Rate %]` to **Rows** as a bar chart.
4. Color by `[Booking Type]`:
   - `Same-Day Booking`: Emerald Green (`#2ecc71`) (Only **4.6%** no-show).
   - `Advance Booking`: Sunset Coral (`#e74c3c`) (**28.5%** no-show).
5. Add `[Total Appointments]` and `[No-Show Rate %]` to **Label**.
6. Notice: Same-day bookings comprise 38,561 appointments (~35% of total volume) with exceptional adherence.

---

### Worksheet 3: Scheduling Time of Day & Hour Heatmap
*Purpose: Identify peak booking hours and time-of-day default variations.*

1. Create a new worksheet named **`WS_Scheduling_Hour_Heatmap`**.
2. Drag `[scheduled_hour]` to **Columns** (Values 6 through 21).
3. Drag `[appointment_day_of_week]` to **Rows** (Monday through Saturday).
4. Drag `[No-Show Rate %]` to **Color** (Heatmap palette: Yellow-Orange-Red).
5. Drag `[Total Appointments]` to **Size** (or use Square mark for a uniform grid).
6. Title: "Booking Hour of Day vs Appointment Day Heatmap".

---

### Worksheet 4: Age Cohort × Lead Time Cross-Tabulation
*Purpose: Uncover whether certain age groups are more sensitive to long waiting delays.*

1. Create a new worksheet named **`WS_Age_LeadTime_Matrix`**.
2. Drag `[lead_time_bracket]` to **Columns**.
3. Drag `[age_group]` to **Rows**.
4. Change Mark type to **Square** (Heatmap).
5. Drag `[No-Show Rate %]` to **Color** and **Label**.
6. Insight: Young adults waiting >30 days suffer default rates approaching **36%**, whereas seniors waiting >30 days have a ~26% default rate.

---

## 4. Dashboard Assembly & Layout Guide

1. Create Dashboard: Set Size to **1366 x 768 px**.
2. **Top Header** (Height: `75 px`):
   - Background: Dark Charcoal (`#1e272e`).
   - Title: "OPERATIONAL & SCHEDULING LEAD-TIME ANALYTICS" (White, `18pt`, Bold).
   - Subtitle: "Evaluating Patient Default Probabilities Across Waiting Durations & Booking Windows" (`#00d2d3`, `10pt`).
3. **Top Split Containers (Height: 330 px)**:
   - **Left (60%)**: `WS_Lead_Time_Curve` (The core dual-axis waiting curve).
   - **Right (40%)**: `WS_SameDay_vs_Advance` (The same-day operational comparison).
4. **Bottom Split Containers (Height: 330 px)**:
   - **Left (55%)**: `WS_Age_LeadTime_Matrix` (Cross-tabulation matrix).
   - **Right (45%)**: `WS_Scheduling_Hour_Heatmap` (Hourly booking patterns).
5. **Interactive Actions**:
   - Filter action on `WS_Lead_Time_Curve`: Clicking a lead time bracket (e.g. `Long Term (>30d)`) filters the demographic matrix and hour heatmap to inspect long-wait patients.

---

## 5. Actionable Capacity Planning Strategies
1. **Expand Same-Day Open Access Slots**: Because same-day bookings boast a 95.35% attendance rate, reserving 20–30% of daily clinic capacity for same-day walk-ins or same-day digital booking radically curbs vacant slots.
2. **Implement Dynamic Overbooking for >14-Day Bookings**: For appointments scheduled beyond two weeks, hospitals can safely overbook by 20–25% to offset the predictable ~30–33% attrition.
3. **Mandatory 48-Hour Reconfirmation**: Implement automated two-way SMS or telephone confirmation 48 hours prior to consultation for any appointment with a lead time greater than 7 days.
