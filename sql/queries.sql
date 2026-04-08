-- 1. Monthly revenue with running total (window function)
SELECT
    Month,
    ROUND(SUM(TotalPrice), 2) AS monthly_revenue,
    ROUND(SUM(SUM(TotalPrice)) OVER (ORDER BY Month), 2) AS cumulative_revenue
FROM orders
GROUP BY Month
ORDER BY Month;

-- 2. Top 10 customers by lifetime value (window function)
SELECT
    "Customer ID",
    COUNT(DISTINCT Invoice) AS total_orders,
    ROUND(SUM(TotalPrice), 2) AS lifetime_value,
    RANK() OVER (ORDER BY SUM(TotalPrice) DESC) AS revenue_rank
FROM orders
GROUP BY "Customer ID"
ORDER BY lifetime_value DESC
LIMIT 10;

-- 3. Top product per country (CTE + window function)
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

-- 4. Top 20% customers revenue contribution
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