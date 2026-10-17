import sqlite3
import pandas as pd

file_name = "online_retail_II.xlsx.csv"

print(f"1. Reading {file_name}...")
try:
    df = pd.read_csv(file_name, encoding="ISO-8859-1")
except Exception:
    df = pd.read_csv(file_name, encoding="utf-8")

# Spaces trim karein
df.columns = [c.strip() for c in df.columns]

# Column names resolve karein
cust_col = 'Customer ID' if 'Customer ID' in df.columns else 'CustomerID'
inv_col = 'Invoice' if 'Invoice' in df.columns else 'InvoiceNo'
price_col = 'Price' if 'Price' in df.columns else 'UnitPrice'
date_col = 'InvoiceDate'

print("2. Data filter aur clean ho raha hai...")
df_clean = df.dropna(subset=[cust_col]).copy()
df_clean = df_clean[df_clean["Quantity"] > 0]
df_clean = df_clean[df_clean[price_col] > 0]
df_clean = df_clean[~df_clean[inv_col].astype(str).str.startswith("C")]

df_clean = df_clean.rename(columns={
    cust_col: 'CustomerID',
    inv_col: 'InvoiceNo',
    price_col: 'UnitPrice'
})

# Mixed date format handle karne ke liye format='mixed' aur dayfirst=True
print("3. Converting dates...")
df_clean['InvoiceDate'] = pd.to_datetime(df_clean[date_col], format='mixed', dayfirst=True)
df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['UnitPrice']

print("4. SQLite Database 'ecommerce.db' me save ho raha hai...")
conn = sqlite3.connect("ecommerce.db")
df_clean.to_sql("clean_retail", conn, if_exists="replace", index=False)
conn.close()

print("SUCCESS! 'ecommerce.db' database ready ho chuki hai.")