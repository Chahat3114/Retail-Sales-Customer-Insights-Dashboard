import sqlite3
import pandas as pd

conn = sqlite3.connect('retail.db')

# ── Query 1: Monthly revenue with running total ────────────────
q1 = """
SELECT
    Month,
    ROUND(SUM(TotalPrice), 2) AS monthly_revenue,
    ROUND(SUM(SUM(TotalPrice)) OVER (ORDER BY Month), 2) AS cumulative_revenue
FROM orders
GROUP BY Month
ORDER BY Month;
"""

# ── Query 2: Top 10 customers by lifetime value ────────────────
q2 = """
SELECT
    "Customer ID",
    COUNT(DISTINCT Invoice) AS total_orders,
    ROUND(SUM(TotalPrice), 2) AS lifetime_value,
    RANK() OVER (ORDER BY SUM(TotalPrice) DESC) AS revenue_rank
FROM orders
GROUP BY "Customer ID"
ORDER BY lifetime_value DESC
LIMIT 10;
"""

# ── Query 3: Top product per country (CTE) ────────────────────
q3 = """
WITH product_country AS (
    SELECT
        Country,
        Description,
        ROUND(SUM(TotalPrice), 2) AS revenue,
        RANK() OVER (PARTITION BY Country ORDER BY SUM(TotalPrice) DESC) AS rnk
    FROM orders
    GROUP BY Country, Description
)
SELECT * FROM product_country
WHERE rnk = 1
ORDER BY revenue DESC
LIMIT 10;
"""

# ── Query 4: Top 20% customers revenue contribution ───────────
q4 = """
WITH customer_rev AS (
    SELECT "Customer ID", SUM(TotalPrice) AS rev
    FROM orders GROUP BY "Customer ID"
),
total AS (SELECT SUM(rev) AS total_rev FROM customer_rev)
SELECT
    ROUND(100.0 * SUM(rev) / (SELECT total_rev FROM total), 1)
    AS top20_percent_revenue
FROM (
    SELECT rev FROM customer_rev
    ORDER BY rev DESC
    LIMIT (SELECT COUNT(*)/5 FROM customer_rev)
);
"""

# ── Run all & print results ────────────────────────────────────
queries = {
    "Monthly Revenue Trend"         : q1,
    "Top 10 Customers by LTV"       : q2,
    "Top Product per Country"       : q3,
    "Top 20% Customers Revenue %"   : q4
}

for title, query in queries.items():
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))

# ── Export results to CSV ──────────────────────────────────────
pd.read_sql_query(q1, conn).to_csv('exports/monthly_revenue_sql.csv',   index=False)
pd.read_sql_query(q2, conn).to_csv('exports/top_customers.csv',         index=False)
pd.read_sql_query(q3, conn).to_csv('exports/top_product_country.csv',   index=False)

conn.close()
print("\nAll query results exported to exports/ folder!")