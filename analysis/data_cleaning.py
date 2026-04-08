import pandas as pd
import numpy as np
import os

# Load data
raw_path = r"C:\Users\singh\Downloads\retail_data\online_retail_II.csv"

print("Loading dataset...")
df = pd.read_csv(raw_path, encoding='ISO-8859-1')

print(f"Raw shape: {df.shape}")
print(f"\nColumn names:\n{df.columns.tolist()}")
print(f"\nFirst 3 rows:\n{df.head(3)}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nData types:\n{df.dtypes}")

df.columns = df.columns.str.strip()          

before = len(df)
df.dropna(subset=['Customer ID'], inplace=True)
print(f"\nRows after dropping null CustomerID: {len(df)} (removed {before - len(df)})")

df = df[~df['Invoice'].astype(str).str.startswith('C')] 
df = df[df['Quantity'] > 0]
df = df[df['Price'] > 0]

print(f"Rows after removing cancellations/bad rows: {len(df)}")

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Customer ID'] = df['Customer ID'].astype(int)
df['Description'] = df['Description'].str.strip()

df['TotalPrice']  = df['Quantity'] * df['Price']
df['Month']       = df['InvoiceDate'].dt.to_period('M').astype(str)
df['Year']        = df['InvoiceDate'].dt.year
df['DayOfWeek']   = df['InvoiceDate'].dt.day_name()
df['Hour']        = df['InvoiceDate'].dt.hour

q1  = np.percentile(df['TotalPrice'], 1)
q99 = np.percentile(df['TotalPrice'], 99)
before = len(df)
df = df[(df['TotalPrice'] >= q1) & (df['TotalPrice'] <= q99)]
print(f"Rows after outlier removal: {len(df)} (removed {before - len(df)})")

print(f"\nFinal dataset shape: {df.shape}")
print(f"Date range: {df['InvoiceDate'].min()} → {df['InvoiceDate'].max()}")
print(f"Unique customers: {df['Customer ID'].nunique()}")
print(f"Unique products:  {df['Description'].nunique()}")
print(f"Total revenue:    £{df['TotalPrice'].sum():,.2f}")

# Save Clean Data
output_path = r"data\clean_data.csv"
os.makedirs("data", exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\nClean data saved to: {output_path}")
