SELECT
    SUBSTR(CAST(order_date AS TEXT), 1, 7) AS month,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_id) AS active_customers,
    ROUND(SUM(net_revenue), 2) AS net_revenue,
    ROUND(AVG(net_revenue), 2) AS average_order_value
FROM fact_orders
GROUP BY SUBSTR(CAST(order_date AS TEXT), 1, 7)
ORDER BY month;
