SELECT
    'fact_orders_without_customer' AS check_name,
    COUNT(*) AS failed_rows
FROM fact_orders o
LEFT JOIN dim_customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL

UNION ALL

SELECT
    'fact_orders_without_product' AS check_name,
    COUNT(*) AS failed_rows
FROM fact_orders o
LEFT JOIN dim_products p ON p.product_id = o.product_id
WHERE p.product_id IS NULL

UNION ALL

SELECT
    'orders_with_non_positive_revenue' AS check_name,
    COUNT(*) AS failed_rows
FROM fact_orders
WHERE net_revenue <= 0;
