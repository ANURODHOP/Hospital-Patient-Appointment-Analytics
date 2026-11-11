# Hospital Patient & Appointment Analytics: Statistical Summary Report

## 1. Executive Summary
- **Total Validated Records Analyzed**: 110,516
- **Overall Hospital No-Show Rate**: 20.19%
- **Overall Attendance Compliance Rate**: 79.81%

---

## 2. Chi-Square ($\chi^2$) Test of Independence Results
Testing the null hypothesis ($H_0$) that patient attendance is independent of each categorical factor ($\alpha = 0.05$).

| Feature Tested | Chi-Square ($\chi^2$) | df | p-value | Cramér's V | Effect Size | Significant? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `gender` | 1.836 | 1 | 0.1755 | 0.0027 | Negligible | No |
| `scholarship_desc` | 93.873 | 1 | < 0.0001 | 0.029 | Negligible | Yes (p < 0.05) |
| `hypertension_desc` | 140.088 | 1 | < 0.0001 | 0.0355 | Negligible | Yes (p < 0.05) |
| `diabetes_desc` | 25.207 | 1 | < 0.0001 | 0.0148 | Negligible | Yes (p < 0.05) |
| `alcoholism_desc` | 0.001 | 1 | 0.9715 | 0.0 | Negligible | No |
| `sms_desc` | 1769.295 | 1 | < 0.0001 | 0.1265 | Small | Yes (p < 0.05) |
| `has_handicap` | 6.723 | 1 | 0.0095 | 0.0072 | Negligible | Yes (p < 0.05) |
| `age_group` | 747.595 | 4 | < 0.0001 | 0.082 | Negligible | Yes (p < 0.05) |
| `lead_time_bracket` | 9623.121 | 5 | < 0.0001 | 0.295 | Small | Yes (p < 0.05) |
| `scheduled_time_of_day` | 206.887 | 3 | < 0.0001 | 0.043 | Negligible | Yes (p < 0.05) |
| `appointment_day_of_week` | 27.756 | 5 | < 0.0001 | 0.0143 | Negligible | Yes (p < 0.05) |
| `comorbidity_category` | 118.735 | 2 | < 0.0001 | 0.0325 | Negligible | Yes (p < 0.05) |
| `is_same_day` | 8876.205 | 1 | < 0.0001 | 0.2834 | Small | Yes (p < 0.05) |

---

## 3. Continuous Variable Hypothesis Testing

### 3.1 Patient Age Analysis
- **Showed Up Mean (SD)**: 37.79 years (±23.34) | Median: 38.0
- **No-Show Mean (SD)**: 34.31 years (±21.95) | Median: 33.0
- **Welch's t-test**: $t = 20.896$, $p = 2.1519e-96$
- **Mann-Whitney U test**: $U = 1070733961.0$, $p = 2.4178e-92$
- **Conclusion**: Statistically significant difference ($p < 0.001$). Patients who attend appointments are on average older than patients who default.

### 3.2 Scheduling Lead Time (Waiting Duration in Days)
- **Showed Up Mean (SD)**: 8.75 days (±14.55) | Median: 2.0 days
- **No-Show Mean (SD)**: 15.84 days (±16.61) | Median: 11.0 days
- **Welch's t-test**: $t = -58.284$, $p = 0.0000e+00$
- **Mann-Whitney U test**: $U = 593784411.5$, $p = 0.0000e+00$
- **Conclusion**: Statistically significant difference ($p < 0.001$). Lead time is the single strongest operational predictor of default. Same-day appointments experience only ~4.6% no-shows, whereas appointments scheduled over 30 days in advance exhibit no-show rates exceeding 32%.

---

## 4. Relative Risk (RR) and Odds Ratio (OR) Analysis

| Risk Factor Comparison | Exposed Rate (%) | Unexposed Rate (%) | Relative Risk (RR) | Odds Ratio (OR) |
| :--- | :--- | :--- | :--- | :--- |
| **SMS Received** | 27.58% | 16.69% | 1.652 | 1.9 |
| **Bolsa Família Scholarship** | 23.74% | 19.8% | 1.199 | 1.261 |
| **Same Day Booking** | 28.52% | 4.65% | 6.136 | 8.185 |
| **Has Chronic Condition** | 17.84% | 20.92% | 0.853 | 0.821 |
| **Hypertension** | 17.3% | 20.9% | 0.828 | 0.792 |
| **Diabetes** | 18.0% | 20.36% | 0.884 | 0.859 |
| **Alcoholism** | 20.15% | 20.19% | 0.998 | 0.997 |

---

## 5. Key Empirical Takeaways for Hospital Management
1. **Lead Time Dominance**: Waiting lead time is the primary operational lever. Reducing lead times through open-access scheduling or reconfirming long-lead bookings can drastically decrease no-show volume.
2. **Age & Youth Vulnerability**: Adolescents and young adults (ages 13–24) have the highest default rates (~24–25%), whereas seniors (65+) are the most compliant (~15%).
3. **Chronic Disease Effect**: Patients with chronic hypertension or diabetes are significantly more compliant, likely due to medication dependence and established doctor-patient relationships.
4. **SMS Paradox**: SMS reminders are only sent for longer advance bookings (>=3 days), which inherently suffer higher baseline default rates; among long-lead appointments, reminder timing needs optimization.
