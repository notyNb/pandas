SELECT
    p.category,
    p.product_name,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.net_revenue), 2) AS net_revenue,
    ROUND(SUM(o.net_revenue - (o.quantity * p.unit_cost)), 2) AS estimated_margin
FROM fact_orders o
JOIN dim_products p ON p.product_id = o.product_id
GROUP BY p.category, p.product_name
ORDER BY net_revenue DESC
LIMIT 10;
