# Dashboard 1: Executive KPI & Attendance Overview

## 1. Dashboard Objective & Summary
The **Executive KPI & Attendance Overview** provides hospital leadership, clinic directors, and operations executives with real-time visibility into overall patient compliance, appointment volumes, daily attendance fluctuations, and the efficacy of patient communication interventions.

- **Primary Data Source**: `hospital_appointments_cleaned.csv` (or `tableau_executive_overview.csv`)
- **Canvas Size**: `1366 x 768` (Fixed Desktop Browser)
- **Target Audience**: Chief Medical Officer (CMO), Clinic Operations Director, Hospital Administrators

---

## 2. Calculated Fields Required
Ensure the following calculated fields are created in Tableau (refer to `tableau/calculated_fields_reference.md`):
1. `[Total Appointments]` = `COUNT([appointment_id])`
2. `[Total No Shows]` = `SUM([no_show_binary])`
3. `[Total Completed Shows]` = `SUM([showed_up_binary])`
4. `[No-Show Rate %]` = `SUM([no_show_binary]) / COUNT([appointment_id])` (Format: `0.0%`)
5. `[Attendance Rate %]` = `SUM([showed_up_binary]) / COUNT([appointment_id])` (Format: `0.0%`)
6. `[KPI Status Alert]` = `IF [No-Show Rate %] <= 0.15 THEN "Optimal" ELSEIF [No-Show Rate %] <= 0.22 THEN "Moderate" ELSE "Critical" END`

---

## 3. Worksheet Construction Steps

### Worksheet 1: KPI Summary Scorecards
*Purpose: At-a-glance display of the 4 primary operational indicators.*

1. Create a new worksheet named **`WS_KPI_Cards`**.
2. Drag `Measure Values` to the **Text** card on the Marks shelf.
3. In the `Measure Values` shelf, keep only:
   - `[Total Appointments]`
   - `[Attendance Rate %]`
   - `[No-Show Rate %]`
   - `AVG([lead_time_days])`
4. Drag `Measure Names` to **Columns**.
5. Change Mark type to **Text** (or **Square** for colored KPI tiles).
6. Format fonts: Size `18pt`, Bold, Dark Slate Gray (`#2c3e50`).
7. Edit title to hide it (we will use dashboard banner containers).

---

### Worksheet 2: Attendance Status Donut Chart
*Purpose: Clean proportional breakdown of Show vs No-Show volume.*

1. Create a new worksheet named **`WS_Attendance_Donut`**.
2. Change Mark type to **Pie**.
3. Drag `[attendance_status]` to **Color**:
   - `Showed Up`: Emerald Green (`#2ecc71`)
   - `No Show`: Crimson Red (`#e74c3c`)
4. Drag `[Total Appointments]` to **Angle**.
5. Drag `[attendance_status]` and `[No-Show Rate %]` to **Label**.
6. Format label: Bold, `10pt`.
7. **Create Donut Hole**:
   - In Rows shelf, type `MIN(0)` and duplicate it (`MIN(0)` twice).
   - Right-click the second `MIN(0)` and select **Dual Axis**.
   - Synchronize axes and hide headers.
   - On the second mark card, change color to **White**, remove labels, and reduce size slightly to form the donut hole.

---

### Worksheet 3: Daily Appointment Volume & Attendance Trend
*Purpose: Longitudinal view of appointment load and daily attendance patterns over time.*

1. Create a new worksheet named **`WS_Daily_Trend`**.
2. Drag `[appointment_date]` to **Columns** as **Continuous Day** (`DAY(appointment_date)`).
3. Drag `[Total Appointments]` to **Rows**.
4. Drag `[attendance_status]` to **Color** (using the unified Green / Red palette).
5. Change Mark type to **Line** or **Area (stacked)**.
6. Add an average reference line for daily volume.
7. Format axis: Title "Appointment Date", clean tick marks.

---

### Worksheet 4: Day of the Week Attendance Load
*Purpose: Identify which weekdays suffer the highest default rates.*

1. Create a new worksheet named **`WS_DayOfWeek_Breakdown`**.
2. Drag `[appointment_day_of_week]` to **Columns**.
   - Sort by Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.
3. Drag `[Total Appointments]` to **Rows** as a bar chart.
4. Drag `[No-Show Rate %]` to **Color** (diverging red-to-green palette) and **Label**.
5. Format labels as percentage `0.0%`.
6. Add Title: "Appointment Volume & No-Show Rate by Day of Week".

---

### Worksheet 5: SMS Notification Impact
*Purpose: Compare default rates between patients who received SMS reminders versus those who did not.*

1. Create a new worksheet named **`WS_SMS_Impact`**.
2. Drag `[sms_desc]` to **Columns**.
3. Drag `[No-Show Rate %]` to **Rows**.
4. Change Mark type to **Bar**.
5. Drag `[sms_desc]` to **Color** (e.g. Teal `#1abc9c` vs Slate `#95a5a6`).
6. Add `[No-Show Rate %]` to **Label**.
7. In Filters, you can optionally filter `[lead_time_bracket]` to exclude same-day appointments (since SMS is only applicable for advance bookings).

---

## 4. Dashboard Assembly & Layout Guide

1. Create a new Dashboard: Set Size to **Fixed Size: 1366 x 768 px**.
2. **Top Header Container** (Height: `80 px`):
   - Background: Dark Navy (`#1a252f`).
   - Text Object: "HOSPITAL PATIENT & APPOINTMENT ANALYTICS | EXECUTIVE OVERVIEW" (White, `18pt`, Bold).
   - Subtitle: "City of Vitória Municipal Clinics • 110,516 Validated Appointment Records" (Light gray, `10pt`).
3. **KPI Scorecard Container** (Height: `90 px`):
   - Insert `WS_KPI_Cards`. Fit to Entire View.
4. **Main Content Container (Horizontal Split)**:
   - **Left Panel (Width: 35%)**:
     - `WS_Attendance_Donut`
     - `WS_SMS_Impact`
   - **Right Panel (Width: 65%)**:
     - `WS_Daily_Trend`
     - `WS_DayOfWeek_Breakdown`
5. **Interactive Dashboard Actions**:
   - Click **Dashboard -> Actions -> Add Action -> Filter**.
   - **Action Name**: `Filter by Day of Week`.
   - **Source Sheet**: `WS_DayOfWeek_Breakdown`.
   - **Target Sheets**: `WS_Daily_Trend`, `WS_Attendance_Donut`, `WS_KPI_Cards`.
   - **Run Action On**: Select (Click).
   - **Clearing Selection**: Show all values.

---

## 5. Executive Insights to Highlight
- **Global No-Show Rate**: ~20.2% baseline attrition across 110,516 appointments.
- **Mid-Week Peak**: Tuesdays and Wednesdays record the highest total consultation volumes (~33,000 appointments combined).
- **Saturday Outlier**: Saturday features very low volume (<50 appointments), predominantly urgent or specialized clinics.
