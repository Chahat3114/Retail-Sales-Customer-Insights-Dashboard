import pandas as pd
import sqlite3
import os

df = pd.read_csv('data/clean_data.csv')

conn = sqlite3.connect('retail.db')

# Load full orders table
df.to_sql('orders', conn, if_exists='replace', index=False)

# Monthly summary table
monthly = df.groupby('Month').agg(
    total_revenue    = ('TotalPrice', 'sum'),
    total_orders     = ('Invoice', 'nunique'),
    unique_customers = ('Customer ID', 'nunique')
).reset_index()
monthly.to_sql('monthly_summary', conn, if_exists='replace', index=False)

# Top products table
top_products = df.groupby('Description')['TotalPrice'].sum().nlargest(10).reset_index()
top_products.to_sql('top_products', conn, if_exists='replace', index=False)

# Customer LTV table
customer_ltv = df.groupby('Customer ID').agg(
    total_orders  = ('Invoice', 'nunique'),
    total_revenue = ('TotalPrice', 'sum')
).reset_index().sort_values('total_revenue', ascending=False)
customer_ltv.to_sql('customer_ltv', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print("retail.db created with 4 tables:")
print("  - orders")
print("  - monthly_summary")
print("  - top_products")
print("  - customer_ltv")