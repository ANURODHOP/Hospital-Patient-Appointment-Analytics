# Tableau Calculated Fields Reference Guide

This reference document provides copy-paste ready calculated field formulas for **Tableau Desktop** and **Tableau Public** when working with `hospital_appointments_cleaned.csv` or the aggregated datasets.

---

## 1. Core Attendance & KPI Metrics

### 1.1 Total Appointments
- **Field Name**: `[Total Appointments]`
- **Data Type**: Integer (Measure)
- **Tableau Formula**:
  ```tableau
  COUNT([appointment_id])
  ```
- **Description**: Computes total appointment volume across all selected filters.

---

### 1.2 Total No-Shows
- **Field Name**: `[Total No Shows]`
- **Data Type**: Integer (Measure)
- **Tableau Formula**:
  ```tableau
  SUM([no_show_binary])
  ```
- **Description**: Aggregates the total number of missed appointments (where patient defaulted).

---

### 1.3 Total Completed Shows
- **Field Name**: `[Total Completed Shows]`
- **Data Type**: Integer (Measure)
- **Tableau Formula**:
  ```tableau
  SUM([showed_up_binary])
  ```
- **Description**: Aggregates the total number of attended appointments.

---

### 1.4 No-Show Rate (%)
- **Field Name**: `[No-Show Rate %]`
- **Data Type**: Decimal / Percentage (Measure)
- **Tableau Formula**:
  ```tableau
  SUM([no_show_binary]) / COUNT([appointment_id])
  ```
- **Default Number Formatting**: Percentage with `1` decimal place (e.g. `20.2%`).
- **Description**: Primary hospital performance KPI metric.

---

### 1.5 Attendance Compliance Rate (%)
- **Field Name**: `[Attendance Rate %]`
- **Data Type**: Decimal / Percentage (Measure)
- **Tableau Formula**:
  ```tableau
  SUM([showed_up_binary]) / COUNT([appointment_id])
  ```
- **Default Number Formatting**: Percentage with `1` decimal place (e.g. `79.8%`).

---

## 2. Thresholds & Dynamic Alert Formatting

### 2.1 KPI Performance Alert
- **Field Name**: `[KPI Status Alert]`
- **Data Type**: String (Dimension / Color)
- **Tableau Formula**:
  ```tableau
  IF [No-Show Rate %] <= 0.15 THEN "Optimal (< 15%)"
  ELSEIF [No-Show Rate %] <= 0.22 THEN "Moderate (15-22%)"
  ELSE "Critical (> 22%)"
  END
  ```
- **Recommended Palette**:
  - `Optimal`: Green (`#2ecc71`)
  - `Moderate`: Amber / Yellow (`#f39c12`)
  - `Critical`: Red (`#e74c3c`)

---

### 2.2 Booking Type Classification
- **Field Name**: `[Booking Type]`
- **Data Type**: String (Dimension)
- **Tableau Formula**:
  ```tableau
  IF [lead_time_days] = 0 THEN "Same-Day Booking"
  ELSE "Advance Booking (> 0 Days)"
  END
  ```

---

## 3. Clinical & Comorbidity Segmentation

### 3.1 Comorbidity Level (Clinical Score)
- **Field Name**: `[Comorbidity Level]`
- **Data Type**: String (Dimension)
- **Tableau Formula**:
  ```tableau
  IF [chronic_condition_count] = 0 THEN "0. No Chronic Conditions"
  ELSEIF [chronic_condition_count] = 1 THEN "1. Single Chronic Disease"
  ELSE "2. Multimorbid (2+ Chronic Diseases)"
  END
  ```

---

### 3.2 High-Risk Vulnerability Flag
- **Field Name**: `[High Risk Patient Flag]`
- **Data Type**: String (Dimension)
- **Tableau Formula**:
  ```tableau
  IF [lead_time_days] > 14 AND [age] < 30 AND [scholarship] = 1 THEN "High Risk Patient"
  ELSE "Standard Risk"
  END
  ```
- **Description**: Identifies young patients receiving welfare scheduled far in advance, who exhibit statistical default rates exceeding 35%.

---

## 4. Date & Temporal Calculations

### 4.1 Day of Week Sorter
- **Field Name**: `[Day of Week Sort]`
- **Data Type**: Integer (Dimension)
- **Tableau Formula**:
  ```tableau
  CASE [appointment_day_of_week]
      WHEN "Monday" THEN 1
      WHEN "Tuesday" THEN 2
      WHEN "Wednesday" THEN 3
      WHEN "Thursday" THEN 4
      WHEN "Friday" THEN 5
      WHEN "Saturday" THEN 6
      ELSE 7
  END
  ```

---

### 4.2 Lead Time Order Sorter
- **Field Name**: `[Lead Time Sort]`
- **Data Type**: Integer (Dimension)
- **Tableau Formula**:
  ```tableau
  CASE [lead_time_bracket]
      WHEN "Same Day (0d)" THEN 1
      WHEN "Short Term (1-3d)" THEN 2
      WHEN "Medium Term (4-7d)" THEN 3
      WHEN "1-2 Weeks (8-14d)" THEN 4
      WHEN "2-4 Weeks (15-30d)" THEN 5
      WHEN "Long Term (>30d)" THEN 6
      ELSE 7
  END
  ```

---

## 5. Tooltip Strings

### 5.1 Dynamic Tooltip Summary
- **Field Name**: `[Attendance Tooltip Text]`
- **Data Type**: String (Measure)
- **Tableau Formula**:
  ```tableau
  "Appointments: " + STR(COUNT([appointment_id])) + 
  " | No-Shows: " + STR(SUM([no_show_binary])) + 
  " (" + STR(ROUND([No-Show Rate %] * 100, 1)) + "%)"
  ```
