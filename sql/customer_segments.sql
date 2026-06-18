WITH customer_metrics AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.city,
        c.state,
        COUNT(DISTINCT o.order_id) AS orders,
        ROUND(SUM(o.net_revenue), 2) AS lifetime_value
    FROM dim_customers c
    JOIN fact_orders o ON o.customer_id = c.customer_id
    GROUP BY c.customer_id, c.customer_name, c.city, c.state
)
SELECT
    customer_id,
    customer_name,
    city,
    state,
    orders,
    lifetime_value,
    CASE
        WHEN lifetime_value >= 2000 THEN 'high_value'
        WHEN orders >= 2 THEN 'recurring'
        ELSE 'standard'
    END AS customer_segment
FROM customer_metrics
ORDER BY lifetime_value DESC;
