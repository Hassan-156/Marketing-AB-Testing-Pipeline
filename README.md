# 📊 Data-Driven Ad Spend Optimization: A/B Testing & Revenue Impact Pipeline

## 🏢 Executive Summary
This project analyzes a marketing campaign containing over 588,000 users to determine if an ad campaign drove a statistically significant increase in user conversions compared to a public service announcement (PSA) control baseline. By engineering a custom data pipeline to cross-reference traffic volume against temporal trends, this analysis unmasked critical timeline inefficiencies, exposed sample-size illusions, and mapped an actionable strategy to recapture **$217,300 in incremental revenue** by reallocating wasted weekend ad spend to high-intent weekday windows.

---

## 🛠️ The Tech Stack & Architecture
* **Language:** Python 3.x
* **Database Management:** SQL Server (SSEXPRESS), SQLAlchemy, pyodbc
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Seaborn, Matplotlib
* **Framework:** STAR Method Analytical Reporting

---

## 🎯 The STAR Framework Deep-Dive

### 📂 1. Situation
The company deployed a massive ad campaign but faced a critical business blind spot: they could not definitively prove whether users were converting because of the creative ad exposure or if they would have bought organically anyway. Furthermore, raw campaign logs were highly distributed, masking hourly inefficiencies and temporal traps that were draining the marketing budget.

### 📋 2. Task
* Construct a secure relational database pipeline to transition raw logs into a queryable environment.
* Calculate the true baseline conversion lift of the test group over the control group.
* Isolate hourly and daily consumer behaviour patterns while filtering away background noise and sample size imbalances.
* Translate raw conversion counts into structured financial impact forecasting for executive stakeholders.

### ⚙️ 3. Action
* **Database Architecture:** Engineered a robust pipeline using `SQLAlchemy` and `pyodbc` to query a localised SQL Server database, aggregating more than half a million rows efficiently.
* **Volume Normalization:** Addressed a critical data illusion. Early line charts and heatmaps indicated a massive **5.3% conversion spike on Saturdays at 5:00 AM**. By implementing a volume-normalization script tracking total traffic (`COUNT(*)`) alongside conversions (`SUM(CASE...)`), I proved this "spike" was a small-sample artifact of only 94 people (resulting in just 2 extra purchases).
* **Outlier Tracking & Visualization:** Designed custom logarithmic-scaled boxplots to isolate ad exposure density and built multi-line temporal charts to track user interaction patterns hour-by-hour across different days of the week.<img width="1000" height="600" alt="Marketing_Box_Plot_Figure_1" src="https://github.com/user-attachments/assets/47733504-762f-4fa1-bfe2-18fdde654ff7" />

  

### 💰 4. Results & Financial Impact
The data ruthlessly disproved the initial hypothesis that weekends and paydays were prime conversion windows. Instead, the final data pipeline revealed three massive strategic takeaways:

1. **Definitive Lift Proven:** The ad campaign generated a **43% relative lift** in conversion probability over the control group ($2.555\%$ vs $1.785\%$). 
2. **The 3 PM Powerhouse Uncovered:** While Saturday and Monday afternoons attract identical crowd sizes (~6,000+ users), Monday at 3:00 PM yielded **284 conversions** compared to Saturday's dismal **132 conversions**. This isolates Monday afternoon as a high-intent, active buying window.
3. **Manufactured Revenue:** By preventing budget allocation toward unstable morning anomalies and shifting resources from distracted weekend browsers (Fridays/Saturdays) to intentional Monday blocks, the strategy directly maps to **4,346 incremental sales**, driving **$217,300 in pure incremental revenue** (assuming a conservative $50 Average Order Value).

---

## 📁 Repository Structure
* `notebooks_and_scripts/`: Production python scripts containing SQLAlchemy connections and pipeline logic.
* `visualizations/`: High-resolution analytical assets (Boxplots, Time-Series Line Graphs).

---
*Portfolio piece developed by Hassan — Data Analytics & Engineering Portfolio.*
