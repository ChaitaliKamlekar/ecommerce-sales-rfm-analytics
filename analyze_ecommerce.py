import sqlite3
import pandas as pd

conn = sqlite3.connect("ecommerce.db")

print("========== 1. Monthly Revenue & MoM Growth % ==========")
query_mom = """
WITH monthly_revenue AS (
    SELECT 
        strftime('%Y-%m', InvoiceDate) AS sales_month,
        ROUND(SUM(TotalAmount), 2) AS current_revenue
    FROM clean_retail
    GROUP BY sales_month
)
SELECT 
    sales_month,
    current_revenue,
    LAG(current_revenue) OVER (ORDER BY sales_month) AS prev_month_revenue,
    ROUND(
        100.0 * (current_revenue - LAG(current_revenue) OVER (ORDER BY sales_month)) 
        / LAG(current_revenue) OVER (ORDER BY sales_month), 
        2
    ) AS mom_growth_pct
FROM monthly_revenue;
"""
df_mom = pd.read_sql_query(query_mom, conn)
print(df_mom)


print("\n========== 2. Top 10 Best Selling Products ==========")
query_top_products = """
SELECT 
    Description,
    SUM(Quantity) AS total_units_sold,
    ROUND(SUM(TotalAmount), 2) AS total_revenue
FROM clean_retail
GROUP BY Description
ORDER BY total_revenue DESC
LIMIT 10;
"""
df_products = pd.read_sql_query(query_top_products, conn)
print(df_products)


print("\n========== 3. RFM Customer Segmentation (NTILE) ==========")
query_rfm = """
WITH rfm_base AS (
    SELECT 
        CustomerID,
        CAST(julianday((SELECT MAX(InvoiceDate) FROM clean_retail)) - julianday(MAX(InvoiceDate)) AS INT) AS recency_days,
        COUNT(DISTINCT InvoiceNo) AS frequency,
        ROUND(SUM(TotalAmount), 2) AS monetary
    FROM clean_retail
    GROUP BY CustomerID
),
rfm_scores AS (
    SELECT 
        CustomerID,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM rfm_base
)
SELECT 
    CustomerID,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    CASE 
        WHEN r_score >= 4 AND (f_score + m_score) >= 8 THEN 'Champions'
        WHEN r_score >= 3 AND (f_score + m_score) >= 6 THEN 'Loyal Customers'
        WHEN r_score <= 2 AND (f_score + m_score) >= 6 THEN 'At Risk'
        WHEN r_score <= 2 AND (f_score + m_score) <= 4 THEN 'Lost'
        ELSE 'Potential Loyalists'
    END AS segment
FROM rfm_scores;
"""
df_rfm = pd.read_sql_query(query_rfm, conn)
print(df_rfm.head(10))

# Power BI ke liye clean data export karein
print("\nExporting files for Power BI...")
df_rfm.to_csv("rfm_customer_segments.csv", index=False)

# Main transaction data export
query_all = "SELECT InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, TotalAmount, CustomerID, Country FROM clean_retail"
df_clean = pd.read_sql_query(query_all, conn)
df_clean.to_csv("clean_retail_data.csv", index=False)

print("SUCCESS: 'rfm_customer_segments.csv' aur 'clean_retail_data.csv' ready hain!")
conn.close()