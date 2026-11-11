# Interactive Tableau Dashboard Architecture & Implementation Suite

This directory contains complete, click-by-click construction guides for four interactive dashboards in **Tableau Desktop** or **Tableau Public** (free version).

---

## 1. Dashboard Architecture Overview

| Dashboard # | Title | Target Audience | Primary Focus | Key Data Source |
| :--- | :--- | :--- | :--- | :--- |
| **Dashboard 1** | **Executive KPI & Attendance Overview** | Hospital CMO, Clinic Directors, Operations Lead | High-level attendance KPIs, daily appointment trends, SMS reminder impact | `hospital_appointments_cleaned.csv` or `tableau_executive_overview.csv` |
| **Dashboard 2** | **Patient Demographics & Clinical Profile** | Population Health Analysts, Chief Medical Officer | Age brackets, gender distribution, chronic comorbidities (hypertension, diabetes) | `hospital_appointments_cleaned.csv` or `tableau_demographics_health.csv` |
| **Dashboard 3** | **Operational & Scheduling Lead-Time** | Outpatient Clinic Managers, Scheduling Coordinators | The waiting-time curve, booking hours, day-of-week load, same-day booking | `hospital_appointments_cleaned.csv` or `tableau_scheduling_operations.csv` |
| **Dashboard 4** | **Geographic & Clinic Neighborhood Insights** | Regional Health Authorities, Community Outreach Teams | Clinic neighbourhood rankings, geographic disparities, welfare (Bolsa Família) | `hospital_appointments_cleaned.csv` or `tableau_neighborhood_analytics.csv` |

---

## 2. Directory Structure

```
tableau/
├── README.md                               # Architecture, data dictionary, workflow
├── calculated_fields_reference.md          # Copy-paste formulas for Tableau calculations
├── dashboard_1_executive_overview.md       # Step-by-step guide for Dashboard 1
├── dashboard_2_demographics_health.md      # Step-by-step guide for Dashboard 2
├── dashboard_3_operational_scheduling.md   # Step-by-step guide for Dashboard 3
└── dashboard_4_neighborhood_attendance.md  # Step-by-step guide for Dashboard 4
```

---

## 3. How to Connect Data in Tableau Public / Desktop

1. **Launch Tableau**: Open Tableau Desktop or Tableau Public.
2. **Connect to Data**: Under the left sidebar **Connect -> To a File**, click **Text file**.
3. **Select File**: Navigate to your project folder:
   ```
   c:\IMP\Big potato project\Hospital Patient & Appointment Analytic\data\processed\
   ```
   Choose `hospital_appointments_cleaned.csv` (or the specific aggregated file).
4. **Data Verification**:
   - Ensure `scheduled_datetime` is recognized as Date & Time.
   - Ensure `appointment_date` is recognized as Date.
   - Ensure `no_show_binary` and `showed_up_binary` are recognized as Numbers.
5. **Add Calculated Fields**:
   Open [calculated_fields_reference.md](file:///c:/IMP/Big%20potato%20project/Hospital%20Patient%20&%20Appointment%20Analytic/tableau/calculated_fields_reference.md) and copy the formulas for `[No-Show Rate %]`, `[Total Appointments]`, and `[KPI Status Alert]`.
