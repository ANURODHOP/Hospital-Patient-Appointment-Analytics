# Hospital Patient & Appointment Analytics: An Interactive Tableau Dashboard
## Comprehensive Data Analysis and Visualization (DAV) Project Report

---

### Executive Abstract
Missed medical appointments ("no-shows") represent an enduring operational and financial crisis in healthcare management worldwide. When patients default on scheduled consultations, clinic resources remain idle, diagnostic equipment is underutilized, waitlists lengthen, and patient health worsens due to delayed clinical intervention. 

This project presents an end-to-end analytical pipeline and business intelligence suite built upon **110,516 validated patient appointment records** from public healthcare clinics in Vitória, Espírito Santo, Brazil (Medical Appointment No Shows dataset). Combining **Python-based data engineering**, **rigorous inferential statistics** (Chi-Square tests of independence, Cramér's V effect sizes, Welch's t-tests, Mann-Whitney U tests, and Relative Risk metrics), and **four interactive Tableau Public dashboards**, this study identifies the multifaceted determinants of appointment compliance. 

Our empirical findings reveal that **scheduling lead time (waiting duration)** is the dominant operational driver of default: same-day appointments achieve a **95.35% compliance rate (4.65% no-show)**, whereas appointments booked over 30 days in advance exhibit an alarming **33.1% default rate**. Conversely, demographic factors such as patient gender exhibit no statistically significant relationship ($p = 0.1755$). Based on these insights, we formulate actionable operational policies including open-access same-day slot allocation, dynamic risk-based overbooking, targeted two-way SMS reconfirmation protocols, and localized mobile outreach.

---

## 1. Introduction & Problem Statement

### 1.1 Clinical and Financial Ramifications of Missed Appointments
Outpatient clinic operations require balancing fixed resource availability (physician time, examination rooms, specialized nursing staff, diagnostic tools) with stochastic patient demand. When a scheduled patient fails to arrive without prior cancellation:
1. **Clinical Deterioration**: Chronic conditions (e.g. hypertension, type 2 diabetes mellitus) remain unmonitored, frequently precipitating emergency room admissions and preventable complications.
2. **Economic Overhead**: Fixed clinic overhead costs continue to accrue while potential revenue or public healthcare subsidy value is forfeited.
3. **Capacity Inefficiency**: Other symptomatic patients languish on waitlists while appointments go unused.

### 1.2 Research Objectives
The primary goals of this project are:
1. To engineer a reproducible, automated Python data pipeline for dataset validation, anomaly cleansing, feature extraction, and statistical hypothesis testing.
2. To quantify the statistical associations between patient attendance and four primary dimensions:
   - **Demographic**: Age, gender.
   - **Socioeconomic**: Enrollment in the Bolsa Família welfare program.
   - **Clinical**: Hypertension, diabetes, alcoholism, motor/sensory handicap, comorbidity burden.
   - **Operational/Temporal**: Waiting lead time, day of week, hour of scheduling, and SMS reminder notifications.
3. To engineer specialized, aggregated datasets and deploy a modular suite of four interactive dashboards in **Tableau Desktop / Tableau Public**.
4. To translate empirical findings into concrete administrative policies for healthcare executives.

---

## 2. Dataset Description & Data Dictionary

The analysis evaluates the open-source Medical Appointment No Shows dataset originally published on Kaggle. It captures 110,527 medical consultations across municipal primary care clinics in Vitória, Brazil between April 2016 and June 2016.

### 2.1 Original Variable Schema

| Column Name | Raw Type | Description |
| :--- | :--- | :--- |
| `PatientId` | Float64 | Unique numerical identifier for individual patients. |
| `AppointmentID` | Int64 | Unique identifier for each specific booking. |
| `Gender` | String | Patient sex ('F' = Female, 'M' = Male). |
| `ScheduledDay` | Datetime ISO | Exact timestamp when the appointment was registered. |
| `AppointmentDay` | Datetime ISO | Calendar date designated for the consultation (time truncated to midnight). |
| `Age` | Int64 | Patient age in completed years. |
| `Neighbourhood` | String | Geographical district of the clinic / healthcare facility. |
| `Scholarship` | Int64 (Binary) | 1 if patient is enrolled in Bolsa Família welfare program; 0 otherwise. |
| `Hipertension` | Int64 (Binary) | Original typo for Hypertension (1 = Diagnosed, 0 = Normal). |
| `Diabetes` | Int64 (Binary) | Diabetes mellitus status (1 = Diagnosed, 0 = Absent). |
| `Alcoholism` | Int64 (Binary) | Alcohol use disorder status (1 = Diagnosed, 0 = Absent). |
| `Handcap` | Int64 (Discrete)| Number of physical/sensory disabilities (0 to 4). |
| `SMS_received` | Int64 (Binary) | 1 if an SMS reminder was dispatched to the patient; 0 otherwise. |
| `No-show` | String | Target indicator: **'No' = Showed Up**, **'Yes' = Did NOT Show Up**. |

---

## 3. Data Cleansing & Quality Assurance

Rigorous automated data quality validation identified several domain and structural anomalies that required remediation:

1. **Typographic Header Correction**: Standardized `Hipertension` to `hypertension`, `Handcap` to `handicap`, and converted all headers to consistent `snake_case`.
2. **Identification Type Casting**: Converted `PatientId` from scientific-notation float to 64-bit integer (`int64`) to preserve patient identity without precision loss.
3. **Biological Age Anomalies**: Found 1 record with `Age = -1` (data entry error) and 5 records with `Age > 110`. Applied filter `(age >= 0) & (age <= 110)`, eliminating 6 records.
4. **Physical Lead Time Contradictions**: Derived preliminary lead time:
   $$\text{Lead Time Days} = \text{Date}(\text{AppointmentDay}) - \text{Date}(\text{ScheduledDay})$$
   Identified 5 records where `lead_time_days < 0` (e.g. appointment registered days *after* the consultation date). These chronological anomalies were purged.
5. **Target Variable Disambiguation**: The original Kaggle target `No-show` where 'No' signifies patient compliance is notoriously prone to misinterpretation. Created unambiguous fields:
   - `no_show_binary`: $1$ for default, $0$ for attendance.
   - `showed_up_binary`: $1$ for attendance, $0$ for default.
   - `attendance_status`: Categorical labels `'Showed Up'` and `'No Show'`.
6. **Handicap Standardization**: Preserved `handicap_count` (0–4) while deriving a boolean `has_handicap` flag (1 if handicap $\ge 1$, else 0).

**Validation Outcome**: Retained **110,516 valid records** (99.99% retention rate), eliminating exactly 11 anomalous rows. Baseline global no-show rate settled at **20.19%** (88,208 completed shows vs 22,308 defaults).

---

## 4. Feature Engineering

To facilitate multidimensional exploration and statistical modeling, the dataset was enriched with domain-specific features:

1. **Age Stratification (`age_group`)**: Categorized continuous age into five epidemiological life stages:
   - *Children*: 0–12 years (N = 21,057)
   - *Youth*: 13–24 years (N = 14,524)
   - *Young Adults*: 25–44 years (N = 30,068)
   - *Middle-Aged*: 45–64 years (N = 30,473)
   - *Seniors*: 65+ years (N = 14,394)
2. **Lead Time Categorization (`lead_time_bracket`)**: Segmented waiting duration into 6 operational tiers:
   - *Same Day (0d)*: Booked on the consultation date.
   - *Short Term (1-3d)*
   - *Medium Term (4-7d)*
   - *1-2 Weeks (8-14d)*
   - *2-4 Weeks (15-30d)*
   - *Long Term (>30d)*
3. **Same-Day Indicator (`is_same_day`)**: Discrete binary flag (1 if `lead_time_days == 0`).
4. **Clinical Comorbidity Burden (`chronic_condition_count` & `comorbidity_category`)**:
   $$\text{Comorbidity Count} = \text{hypertension} + \text{diabetes} + \text{alcoholism} + \text{has\_handicap}$$
   Categorized into *No Chronic Conditions* (0), *Single Condition* (1), and *Multimorbid (2+)*.
5. **Temporal Breakdown**: Extracted `scheduled_hour`, `scheduled_time_of_day` (Morning, Afternoon, Evening, Night), `appointment_day_of_week`, and `is_weekend`.
6. **Longitudinal Engagement (`is_repeat_patient`)**: Identified patients with multiple appointments across the study window.
7. **Spatial Clinic Baselines**: Aggregated neighborhood volume and historical default rates.

---

## 5. Exploratory Data Analysis & Empirical Visualizations

Nine publication-quality visualizations were programmatically generated to elucidate core relationships.

### 5.1 Overall Attendance Distribution
![Overall Attendance Distribution](figures/01_overall_noshow_distribution.png)
- **Finding**: Of 110,516 total appointments, **79.8% (88,208)** were successfully attended, while **20.2% (22,308)** defaulted. This establishes an approximately 4:1 baseline attendance-to-default ratio.

---

### 5.2 Socioeconomic & Demographic Predictors
![Gender and Scholarship Impact](figures/02_gender_and_scholarship_impact.png)
- **Gender**: Female default rate is 20.31% vs Male default rate of 19.97%. The absolute difference is a negligible 0.34%.
- **Bolsa Família Welfare**: Patients receiving welfare exhibit a **23.74%** default rate compared to **19.80%** among non-welfare patients ($\chi^2 = 93.87, p < 0.0001$), highlighting socioeconomic transit barriers.

---

### 5.3 Age Demographics & Default Curve
![Age Distribution by Attendance](figures/03_age_distribution_by_attendance.png)
- **Age Inversion**: Default risk is highest among **Youth (13–24)** at **24.53%** and **Young Adults (25–44)** at **22.05%**.
- **Senior Reliability**: As patients age into retirement, attendance increases markedly; seniors aged 65+ record the lowest default rate at **15.23%**.

---

### 5.4 Chronic Illnesses & Clinical Comorbidity
![Chronic Conditions and Comorbidity](figures/04_chronic_conditions_comorbidity.png)
- **Individual Conditions**: Hypertensive patients default at 17.30% (vs 20.90% for normal blood pressure); diabetic patients default at 18.00% (vs 20.36% for non-diabetic).
- **Multimorbidity Effect**: Patients with 0 chronic conditions default at 20.92%, single-condition patients default at 17.95%, and multimorbid patients (2+ conditions) default at only **17.65%**. Regular prescription management and frequent doctor contact foster compliance.

---

### 5.5 The Waiting-Time Curve: Lead Time vs Default Rate
![Lead Time vs No Show Rate](figures/05_lead_time_vs_noshow_rate.png)
- **The Core Operational Phenomenon**: Same-day bookings (38,561 appointments, ~35% of total volume) have a microscopic no-show rate of **4.65%**.
- In stark contrast, appointments booked 1–3 days in advance surge to **23.8%** no-shows, and appointments booked >30 days out default at **33.1%**. As waiting time increases, motivation wanes, symptoms resolve, or scheduling conflicts arise.

---

### 5.6 Scheduling Time of Day & SMS Reminder Impact
![Day of Week and SMS Impact](figures/06_day_of_week_and_sms_impact.png)
- **Weekday Consistency**: Default rates across Monday (20.6%), Tuesday (20.1%), Wednesday (19.7%), Thursday (19.3%), and Friday (21.2%) remain relatively uniform.
- **The SMS Counter-Intuitive Trend**: SMS recipients display a 27.58% default rate vs 16.69% for non-recipients. Crucially, SMS messages are **only dispatched for appointments scheduled 3 or more days in advance**. Because advance appointments have an elevated baseline default rate (>28%), SMS notifications partially mitigate, but cannot completely offset, long lead-time inertia.

---

### 5.7 Geographic Disparities Across Neighborhoods
![Top and Bottom Neighbourhoods](figures/07_top_bottom_neighbourhoods.png)
- **High Default Pockets**: Santos Dumont (28.9%), Santa Cecília (27.5%), and Itararé (26.3%) exhibit severe default rates.
- **High Compliance Pockets**: Jardim da Penha (16.3%), Mata da Praia (12.1%), and Bento Ferreira (17.5%) demonstrate exemplary compliance.

---

### 5.8 Correlation Matrix Heatmap
![Correlation Heatmap](figures/08_correlation_heatmap.png)
- Confirms strong collinearity between age and chronic conditions (hypertension Pearson $r = 0.50$, diabetes $r = 0.29$).
- Confirms strong positive association between `lead_time_days` and `no_show_binary` ($r = 0.19$, $p < 0.0001$), with all other factors exhibiting correlation coefficients $< 0.10$.

---

### 5.9 Cross-Sectional Matrix: Age Group × Lead Time Bracket
![Age Group vs Waiting Bracket](figures/09_age_group_vs_waiting_bracket.png)
- Reveals intersectional risk: Youth (13–24) scheduled >30 days in advance exhibit an astonishing **38.8% default rate**, while Seniors (65+) booked on the same day exhibit only **3.2% default rate**.

---

## 6. Inferential Statistical Analysis & Hypothesis Testing

To validate these visual patterns, we executed formal hypothesis tests at significance level $\alpha = 0.05$.

### 6.1 Chi-Square ($\chi^2$) Tests of Independence
The null hypothesis ($H_0$) states that appointment attendance is independent of the tested categorical factor.

| Feature Tested | Chi-Square ($\chi^2$) | df | p-value | Cramér's V | Effect Size | Reject $H_0$? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `gender` | 1.836 | 1 | 0.1755 | 0.0027 | Negligible | Fail to Reject |
| `scholarship_desc` | 93.873 | 1 | < 0.0001 | 0.0290 | Negligible | **Reject $H_0$** |
| `hypertension_desc` | 140.088 | 1 | < 0.0001 | 0.0355 | Negligible | **Reject $H_0$** |
| `diabetes_desc` | 25.207 | 1 | < 0.0001 | 0.0148 | Negligible | **Reject $H_0$** |
| `alcoholism_desc` | 0.001 | 1 | 0.9715 | 0.0000 | Negligible | Fail to Reject |
| `sms_desc` | 1769.295 | 1 | < 0.0001 | 0.1265 | Small | **Reject $H_0$** |
| `has_handicap` | 6.723 | 1 | 0.0095 | 0.0072 | Negligible | **Reject $H_0$** |
| `age_group` | 747.595 | 4 | < 0.0001 | 0.0820 | Negligible | **Reject $H_0$** |
| **`lead_time_bracket`** | **9623.121** | **5** | **< 0.0001** | **0.2950** | **Moderate** | **Reject $H_0$** |
| **`is_same_day`** | **8876.205** | **1** | **< 0.0001** | **0.2834** | **Moderate** | **Reject $H_0$** |
| `comorbidity_category` | 118.735 | 2 | < 0.0001 | 0.0325 | Negligible | **Reject $H_0$** |

*Statistical Takeaway*: Lead time bracket and same-day booking generate the largest test statistics ($\chi^2 > 9,000$) and highest Cramér's V measures of association (~0.295), proving that operational timing overwhelmingly dominates demographic or clinical variables.

---

### 6.2 Continuous Variable Tests (Welch's t-test and Mann-Whitney U)

1. **Patient Age**:
   - Showed Up: $\bar{x} = 37.79 \pm 23.34$ years (Median: 38.0)
   - No Show: $\bar{x} = 34.31 \pm 21.95$ years (Median: 33.0)
   - Welch's $t = 20.896, p = 2.15 \times 10^{-96}$; Mann-Whitney $U = 1.07 \times 10^9, p = 2.42 \times 10^{-92}$.
   - *Result*: Patients who attend are significantly older than those who default.

2. **Scheduling Lead Time (Days)**:
   - Showed Up: $\bar{x} = 8.75 \pm 14.55$ days (Median: 2.0 days)
   - No Show: $\bar{x} = 15.84 \pm 16.61$ days (Median: 11.0 days)
   - Welch's $t = -58.284, p \approx 0.00$; Mann-Whitney $U = 5.94 \times 10^8, p \approx 0.00$.
   - *Result*: No-show patients experience nearly double the mean lead time and **over 5 times the median waiting duration** (11 days vs 2 days).

---

### 6.3 Relative Risk (RR) and Odds Ratio (OR) Metrics

| Clinical / Operational Factor | Default Rate (Exposed) | Default Rate (Unexposed) | Relative Risk (RR) | Odds Ratio (OR) |
| :--- | :--- | :--- | :--- | :--- |
| **Advance Booking vs Same-Day** | **28.52%** | **4.65%** | **6.136** | **8.185** |
| **Bolsa Família Welfare** | 23.74% | 19.80% | 1.199 | 1.261 |
| **SMS Received** | 27.58% | 16.69% | 1.652 | 1.900 |
| **Chronic Condition (Any)** | 17.84% | 20.92% | 0.853 | 0.821 |
| **Hypertension** | 17.30% | 20.90% | 0.828 | 0.792 |
| **Diabetes** | 18.00% | 20.36% | 0.884 | 0.859 |

*Interpretation*: Patients booked in advance are **6.14 times more likely to default** (Odds Ratio = 8.19) compared to patients booked on the same day. Patients with chronic hypertension have a **17.2% reduction in default risk** ($RR = 0.828$).

---

## 7. Interactive Tableau Dashboard Architecture

Four dedicated interactive dashboards were architected to translate these insights into executive decision tools:

```
Tableau BI Suite
├── Dashboard 1: Executive KPI & Attendance Overview
│   ├── KPI Scorecards (Total Volume, Shows, No-Shows, Lead Time)
│   ├── Attendance Donut Chart
│   ├── Daily Volume & Attendance Longitudinal Trend
│   ├── Day of Week Compliance Bars
│   └── SMS Impact Visualizer
│
├── Dashboard 2: Patient Demographics & Clinical Profile
│   ├── Age Cohort Attendance Pyramid
│   ├── Gender Comparison Matrix
│   ├── Chronic Illness Adherence Benchmarks
│   ├── Comorbidity Burden Gradient
│   └── Bolsa Família Welfare Disparity
│
├── Dashboard 3: Operational & Scheduling Lead-Time
│   ├── The Waiting-Time Dual-Axis Curve (Volume vs Default Rate)
│   ├── Same-Day vs Advance Booking Contrast
│   ├── Booking Hour & Time-of-Day Heatmap
│   └── Age Bracket × Waiting Duration Matrix
│
└── Dashboard 4: Geographic & Clinic Neighborhood Attendance
    ├── Top 10 High-Default Catchment Zones
    ├── Top 10 High-Compliance Communities
    ├── Volume vs Risk Quadrant Bubble Plot
    └── Granular Clinic Directory & Lookup Table
```

All dashboards utilize standardized typography, color palettes (Emerald Green `#2ecc71` for compliance, Crimson Red `#e74c3c` for default), synchronized cross-sheet filtering actions, and responsive containers sized at `1366 x 768 px`.

---

## 8. Strategic Healthcare Management Interventions

Based on our empirical analysis, we recommend four concrete administrative policies:

1. **Adopt Open-Access (Same-Day) Scheduling Capacity**:
   - *Rationale*: Same-day bookings have a stellar 95.35% attendance rate.
   - *Action*: Reserve 25% of clinic daily capacity for same-day walk-in or phone appointments. This immediately compresses waiting times and guarantees high room utilization.
2. **Implement Lead-Time Risk-Based Overbooking**:
   - *Rationale*: Appointments scheduled $>14$ days in advance carry a predictable 30–33% default rate.
   - *Action*: Apply a 20% overbooking algorithm exclusively to slots booked $>14$ days out, while strictly avoiding overbooking for same-day slots.
3. **Transition to Two-Way Interactive SMS/WhatsApp Protocols**:
   - *Rationale*: Static one-way SMS reminders fail to capture cancellations.
   - *Action*: Dispatch interactive messages 48 hours prior requiring patients to reply `1` to confirm or `2` to reschedule, releasing cancelled slots to waitlisted patients.
4. **Deploy Local Mobile Clinics in High-Default Catchments**:
   - *Rationale*: Neighborhoods like Santos Dumont, Santa Cecília, and Itararé suffer from severe default rates linked to poverty and transit friction.
   - *Action*: Partner with municipal transit agencies or dispatch community mobile vans into these sectors for routine primary screenings.

---

## 9. Conclusion
This project successfully integrates reproducible Python data engineering, inferential statistics, publication-grade figures, and executive Tableau dashboards. By isolating scheduling lead time as the preeminent lever of appointment default, the study provides healthcare leaders with clear, actionable strategies to reduce idle clinic capacity, curb operational waste, and improve clinical outcomes across the healthcare continuum.
