
# 📊 E-Commerce Sales Performance & RFM Customer Segmentation

An end-to-end data analytics and business intelligence project tracking monthly sales trends, best-selling products, and customer behavior segments using **Python**, **SQLite**, and **Power BI**.

---

## 📌 Executive Summary
Understanding customer retention and revenue concentration is critical for retail growth. This project processes transactional records to identify high-value customer cohorts, track month-over-month (MoM) revenue shifts, and provide actionable marketing segments through RFM (Recency, Frequency, Monetary) modeling.

---

## 🛠️ Tech Stack & Tools
- **Language & Libraries:** Python (Pandas)
- **Database:** SQLite
- **Visualization & BI:** Microsoft Power BI (DAX, Power Query)
- **Techniques:** SQL Window Functions (`LAG()`, `NTILE()`), RFM Segmentation, MoM Growth Analysis

---

## ⚙️ Architecture & Data Pipeline
1. **Data Ingestion & Cleaning:**
   - Filtered out negative quantities, unit prices, and cancelled invoices (`InvoiceNo` starting with 'C').
   - Handled missing Customer IDs and parsed irregular datetime formats.
   - Loaded structured data into an SQLite database (`ecommerce.db`).
2. **SQL Analytical Transformation:**
   - **MoM Revenue Growth:** Evaluated monthly revenue fluctuations using `LAG()` window functions.
   - **Top 10 Products:** Aggregated total units sold and gross revenue per item.
   - **RFM Segmentation:** Calculated Recency, Frequency, and Monetary metrics per customer, ranking cohorts into 5 quintiles using `NTILE(5)`.
3. **Power BI Dashboards:**
   - **Page 1: Sales Overview:** Key business KPIs, monthly revenue growth trendline, top product sales distribution, and geographical slicers.
   - **Page 2: RFM Customer Segmentation:** Treemap of revenue contribution across segments, scatter plot analyzing Recency vs. Frequency, and customer drill-down matrix.

---

## 🎯 Key Business Insights
- **Pareto Principle in Action:** The top customer cohorts (*Champions* and *Loyal Customers*) drive over 60% of total revenue despite making up a smaller portion of the overall customer base.
- **At-Risk Interventions:** Identified high-spending customers with high recency values (churn risk), enabling targeted retention campaigns before permanent attrition.

---

## 🚀 How to Run Locally

### 1. Database Setup & Analytical Queries
```bash
python "import sqlite3.py"
python analyze_ecommerce.py
