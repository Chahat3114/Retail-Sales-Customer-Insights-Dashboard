import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/clean_data.csv')

# --- 1. Monthly Revenue Trend ---
monthly = df.groupby('Month')['TotalPrice'].sum().reset_index()
plt.figure(figsize=(12, 4))
sns.lineplot(data=monthly, x='Month', y='TotalPrice', marker='o', color='steelblue')
plt.xticks(rotation=45)
plt.title('Monthly Revenue Trend')
plt.tight_layout()
plt.savefig('exports/monthly_revenue.png')
plt.show()

# --- 2. Top 10 Products ---
top_products = df.groupby('Description')['TotalPrice'].sum().nlargest(10).reset_index()
plt.figure(figsize=(10, 5))
sns.barplot(data=top_products, x='TotalPrice', y='Description', hue='Description', palette='Blues_r', legend=False)
plt.title('Top 10 Revenue-Generating Products')
plt.tight_layout()
plt.savefig('exports/top_products.png')
plt.show()

# --- 3. Revenue by Country ---
country_rev = df.groupby('Country')['TotalPrice'].sum().nlargest(10).reset_index()
print(country_rev)

# --- 4. RFM Summary ---
snapshot_date = pd.to_datetime(df['InvoiceDate']).max()   # ← safe conversion
rfm = df.groupby('Customer ID').agg(
    Recency   = ('InvoiceDate', lambda x: (snapshot_date - pd.to_datetime(x).max()).days),
    Frequency = ('Invoice', 'nunique'),      # ← fixed: Invoice not InvoiceNo
    Monetary  = ('TotalPrice', 'sum')
).reset_index()

rfm['Segment'] = pd.cut(rfm['Monetary'],
    bins=[0, 200, 1000, 5000, 999999],
    labels=['Low', 'Mid', 'High', 'VIP'])

rfm.to_csv('exports/rfm_segments.csv', index=False)       # ← only once
print(rfm['Segment'].value_counts())                       # ← only once