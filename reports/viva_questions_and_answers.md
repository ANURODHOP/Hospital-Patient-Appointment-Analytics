# Hospital Patient & Appointment Analytics: Viva Questions and Comprehensive Answers

This document serves as an exhaustive examination and defense preparation guide for academic evaluations, course vivas, and technical interviews.

---

## Section 1: Project Motivation & Core Concepts

### Q1: What is the primary objective of this project, and why is appointment attendance critical in healthcare?
**Answer**:
The primary objective is to analyze demographic, clinical, temporal, and geographic drivers of missed medical appointments ("no-shows") across 110,516 outpatient records and translate these findings into interactive Tableau dashboards and actionable clinic policies.

Attendance is critical for three reasons:
1. **Clinical Health Outcomes**: Patients who miss appointments delay diagnoses, fail to manage chronic conditions (hypertension, diabetes), and often suffer avoidable acute complications requiring emergency hospitalization.
2. **Operational Efficiency**: Fixed overhead costs (physician hours, clinic suites, support staff) remain constant whether patients show up or not; unused appointment slots represent deadweight operational loss.
3. **Queue Health & Equity**: Missed appointments waste slots that could have been allocated to patients waiting on lengthy public health queues.

---

### Q2: What is the baseline no-show rate in this dataset, and what does it indicate?
**Answer**:
The baseline no-show rate is **20.19%** (88,208 completed consultations vs 22,308 no-shows). This indicates that approximately 1 in every 5 scheduled consultations ends in a default, matching the global outpatient average reported in healthcare literature (typically 18% to 25%).

---

## Section 2: Data Cleansing, Preprocessing & Integrity

### Q3: What anomalies were identified in the raw Kaggle dataset, and how did you resolve them?
**Answer**:
1. **Negative Patient Age**: Found one record with `Age = -1`. We filtered this out using the domain rule `Age >= 0 and Age <= 110`.
2. **Extreme Upper Age Outliers**: Five records had ages $> 110$ (unverifiable data entry errors). We capped valid ages at 110.
3. **Negative Lead Times**: Found 5 records where `ScheduledDay` occurred *after* `AppointmentDay` (e.g. lead time of $-1$ or $-6$ days). In reality, an appointment cannot be booked in the future for a past appointment. These chronological contradictions were dropped.
4. **Header Spelling Typos**: `Hipertension` and `Handcap` were corrected to `hypertension` and `handicap`.
5. **Precision in Patient Identification**: `PatientId` was imported as a scientific-notation float (`2.98725e+13`); we cast it to 64-bit integer (`int64`) to prevent ID collisions during aggregation.
6. **Ambiguous Target Variable**: In the raw dataset, `No-show = "No"` means the patient *showed up*, and `"Yes"` means the patient *did not show up*. This confusing double-negative was transformed into `no_show_binary` (1 = Default, 0 = Show) and `attendance_status` ('No Show' vs 'Showed Up').

---

### Q4: How many records were dropped during cleaning, and what is the data retention rate?
**Answer**:
Out of 110,527 raw rows, exactly **11 rows** were eliminated (6 age anomalies + 5 negative lead time anomalies). We retained **110,516 rows**, representing a **99.99% data retention rate**.

---

## Section 3: Feature Engineering & Domain Logic

### Q5: What features did you engineer, and what clinical or operational rationale justified each?
**Answer**:
1. **`lead_time_days` and `lead_time_bracket`**: Computed as `AppointmentDay - ScheduledDay`. Segmented into *Same Day (0d)*, *Short Term (1-3d)*, *Medium Term (4-7d)*, *1-2 Weeks (8-14d)*, *2-4 Weeks (15-30d)*, and *Long Term (>30d)*. Rationale: Waiting time is known to decay patient motivation.
2. **`is_same_day`**: Discrete flag for appointments booked and attended on the same calendar day. Rationale: Captures immediate demand vs advance planning.
3. **`age_group`**: Segmented age into Children (0-12), Youth (13-24), Young Adults (25-44), Middle-Aged (45-64), and Seniors (65+). Rationale: Life stages correspond to distinct lifestyle factors (parental care, school, work, retirement).
4. **`chronic_condition_count` and `comorbidity_category`**: Sum of hypertension, diabetes, alcoholism, and handicap. Categorized into *No Conditions*, *Single Condition*, and *Multimorbid (2+)*. Rationale: Evaluates whether chronic illness severity increases medical compliance.
5. **`scheduled_time_of_day` & `appointment_day_of_week`**: Extracted temporal markers to test morning vs evening booking patterns and weekday demand.
6. **`is_repeat_patient`**: Flagged patients with multiple bookings to identify recurring users.

---

## Section 4: Inferential Statistics & Mathematical Rigor

### Q6: Why did you use the Chi-Square ($\chi^2$) Test of Independence, and what were the primary results?
**Answer**:
The Chi-Square test of independence assesses whether a statistically significant relationship exists between two categorical variables by comparing observed frequencies ($O$) to expected frequencies under the null hypothesis of independence ($E$):
$$\chi^2 = \sum \frac{(O - E)^2}{E}$$

Key findings:
- **`gender`**: $\chi^2 = 1.836, p = 0.1755$. Since $p > 0.05$, we fail to reject $H_0$. Patient sex does **not** influence attendance.
- **`lead_time_bracket`**: $\chi^2 = 9623.12, p < 0.0001$. Enormous association with attendance.
- **`is_same_day`**: $\chi^2 = 8876.21, p < 0.0001$. Overwhelming evidence of association.
- **`scholarship`**: $\chi^2 = 93.87, p < 0.0001$. Statistically significant; welfare recipients face higher default risk.
- **`hypertension`**: $\chi^2 = 140.09, p < 0.0001$. Hypertensive patients have significantly lower default rates.

---

### Q7: What is Cramér's V, and why is reporting p-values alone insufficient for large datasets?
**Answer**:
In large sample sizes ($N = 110,516$), even tiny, negligible differences achieve statistical significance ($p < 0.0001$) because standard error shrinks asymptotically to near-zero. 

**Cramér's V** measures the practical *magnitude* or effect size of association for contingency tables, bounded between $0$ (no relationship) and $1$ (perfect relationship):
$$V = \sqrt{\frac{\phi^2}{\min(r-1, k-1)}} = \sqrt{\frac{\chi^2 / N}{\min(r-1, k-1)}}$$

In our results:
- `lead_time_bracket` achieves $V = 0.2950$ (a strong, practically meaningful effect size).
- `scholarship` achieves $V = 0.0290$ (statistically significant, but negligible practical effect size).
Reporting Cramér's V prevents over-interpreting trivial differences that are merely artifacts of high statistical power.

---

### Q8: Why did you use both Welch's t-test and the Mann-Whitney U test for continuous variables?
**Answer**:
- **Welch's t-test**: Compares mean differences between two independent groups without assuming equal variances.
- **Mann-Whitney U Test**: A non-parametric rank-sum test that evaluates whether the distribution of one group stochastically dominates another. It does not assume a normal distribution.
- **Why Both?**: While `age` is relatively normally distributed, `lead_time_days` is severely right-skewed (median = 2 days, standard deviation = 15 days, maximum = 179 days). For highly skewed distributions, parametric t-tests can be biased by long tails, making the **Mann-Whitney U test** the rigorous gold standard. Both tests confirmed $p < 0.0001$ for both variables.

---

### Q9: What is the difference between Relative Risk (RR) and Odds Ratio (OR)?
**Answer**:
- **Relative Risk (RR)**: Ratio of the probability of an outcome occurring in the exposed group versus the unexposed group:
  $$RR = \frac{P(\text{Default} \mid \text{Exposed})}{P(\text{Default} \mid \text{Unexposed})}$$
  In our study, for advance bookings vs same-day bookings:
  $$RR = \frac{28.52\%}{4.65\%} = 6.136$$
  An advance booking is **6.14 times more likely to result in a no-show** than a same-day booking.
- **Odds Ratio (OR)**: Ratio of the odds of default in the exposed group to the odds of default in the unexposed group:
  $$OR = \frac{P_1 / (1 - P_1)}{P_0 / (1 - P_0)} = \frac{0.2852 / 0.7148}{0.0465 / 0.9535} = 8.185$$
  The odds of defaulting for advance bookings are **8.19 times higher** than for same-day bookings.

---

## Section 5: Key Analytical Insights & The SMS Paradox

### Q10: What is the "SMS Reminder Paradox" in this dataset, and how do you explain it?
**Answer**:
In the raw data, patients who received an SMS reminder have a **27.58% no-show rate**, whereas patients who received no SMS have only a **16.69% no-show rate**. Superficially, this might suggest that sending an SMS *increases* the likelihood of a no-show.

**The Explanation (Confounding by Indication)**:
SMS reminders were **never sent for same-day or short-term appointments (lead time < 3 days)**. They were dispatched *exclusively* for advance appointments scheduled 3 or more days in advance. 
Because advance appointments already have an intrinsically high default baseline ($> 28\%$), comparing the SMS group against the unexposed group creates severe selection bias. When controlling for lead time (restricting to lead times $\ge 3$ days), SMS reminders marginally stabilize attendance, but cannot overcome the inertia of long waiting periods.

---

### Q11: How does comorbidity burden affect patient attendance?
**Answer**:
Counter-intuitively, patients with diagnosed chronic diseases attend appointments at higher rates:
- Patients with 0 chronic illnesses default at **20.92%**.
- Patients with 1 chronic illness default at **17.95%**.
- Patients with 2 or more chronic conditions (multimorbid) default at **17.65%**.
This occurs because patients with chronic illnesses (hypertension, diabetes) depend on outpatient visits for medication renewals, symptom management, and lab test reviews, creating higher personal motivation compared to young patients scheduling acute or routine check-ups.

---

## Section 6: Tableau Architecture & Visualization Design

### Q12: How are your four Tableau dashboards structured, and who are their target users?
**Answer**:
1. **Executive KPI & Attendance Overview**: Target: Chief Medical Officer & Clinic Directors. Displays high-level attendance KPIs, daily appointment volume trends, and day-of-week load.
2. **Patient Demographics & Clinical Profile**: Target: Population Health Analysts & Epidemiologists. Features age brackets, gender distribution, chronic comorbidity burdens, and welfare disparities.
3. **Operational & Scheduling Lead-Time Analysis**: Target: Clinic Operations & Scheduling Supervisors. Centers on the waiting-time curve, booking hours, and same-day access.
4. **Geographic & Clinic Neighborhood Attendance Insights**: Target: Regional Health Secretariat & Community Teams. Analyzes geographical variations across 81 municipal neighborhoods in Vitória, identifying high-risk clinic catchment zones.

---

### Q13: How did you construct the Donut Chart in Tableau?
**Answer**:
Tableau does not have a native "donut chart" mark type. We constructed it using a **Dual-Axis Pie Chart**:
1. Placed `MIN(0)` twice on the **Rows** shelf to create two identical centered axes.
2. For the first axis: Changed mark type to **Pie**, mapped `attendance_status` to Color, and `[Total Appointments]` to Angle and Label.
3. For the second axis: Changed mark type to **Circle**, colored it solid **White**, and decreased its size slightly.
4. Selected **Dual Axis** on the second pill, synchronized axes, and hid all headers, creating a hollow center displaying total volume.

---

### Q14: How are interactive Dashboard Actions implemented in Tableau?
**Answer**:
We configured **Filter Actions** under `Dashboard -> Actions`:
- **Source Sheet**: The driving visual (e.g. `WS_Lead_Time_Curve` or `WS_DayOfWeek_Breakdown`).
- **Run Action On**: `Select` (clicking a bar, line marker, or bubble).
- **Target Sheets**: All dependent analytical sheets.
- **Clearing Selection**: `Show all values`.
This allows an executive to click "Long Term (>30d)" on Dashboard 3 and instantly filter all demographic matrices to view the exact profile of patients in that queue.

---

## Section 7: Strategic Healthcare Management Recommendations

### Q15: Based on your analysis, what four policies would you recommend to a hospital director?
**Answer**:
1. **Reserve 25% of Daily Capacity for Same-Day / Open-Access Booking**: Same-day bookings have a 95.35% attendance compliance. Creating rapid-access slots ensures high utilization and minimal defaults.
2. **Dynamic Overbooking for $>14$-Day Bookings**: For appointments booked more than two weeks in advance (where default probability is $\approx 30\%$), overbook slots by 20% to neutralize expected dropouts without overwhelming clinical staff.
3. **Replace One-Way SMS with Two-Way Interactive Messaging**: Require patients to reply "1" to confirm or "2" to cancel 48 hours prior. Cancellations immediately recycle into the open-access pool.
4. **Deploy Mobile Primary Care Units to High-Default Neighborhoods**: Neighborhoods like Santos Dumont and Santa Cecília suffer $>27\%$ default rates due to geographical transit friction. Dispatching mobile clinic vans directly overcomes transit barriers.
