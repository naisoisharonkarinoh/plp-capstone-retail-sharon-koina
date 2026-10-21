-- Query 1: Calculate total supermarket revenue
SELECT
    SUM(sales_amount) AS total_revenue
FROM transactions;


-- Query 2: Calculate revenue and units sold by branch
SELECT
    b.branch_name,
    SUM(t.sales_amount) AS total_revenue,
    SUM(t.quantity) AS units_sold
FROM transactions AS t
JOIN branches AS b
    ON t.branch_id = b.branch_id
GROUP BY b.branch_name
ORDER BY total_revenue DESC;


-- Query 3: Calculate revenue by product category
SELECT
    p.category,
    SUM(t.sales_amount) AS total_revenue
FROM transactions AS t
JOIN products AS p
    ON t.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- Query 4: Find customers spending more than KES 20,000
SELECT
    customer_id,
    SUM(sales_amount) AS total_spending
FROM transactions
GROUP BY customer_id
HAVING SUM(sales_amount) > 20000
ORDER BY total_spending DESC;


-- Query 5: Rank branches by revenue using a window function
WITH branch_revenue AS (
    SELECT
        b.branch_name,
        SUM(t.sales_amount) AS total_revenue
    FROM transactions AS t
    JOIN branches AS b
        ON t.branch_id = b.branch_id
    GROUP BY b.branch_name
)
SELECT
    branch_name,
    total_revenue,
    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank
FROM branch_revenue;


-- Query 6: Calculate monthly revenue
SELECT
    strftime('%Y-%m', date) AS sales_month,
    SUM(sales_amount) AS total_revenue,
    COUNT(DISTINCT transaction_id) AS total_transactions
FROM transactions
GROUP BY strftime('%Y-%m', date)
ORDER BY sales_month;
