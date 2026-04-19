-- Customer Segmentation (Using Window Functions)
WITH UserStats AS (
    SELECT 
        user_id,
        MAX(order_number) AS lifetime_orders,
        ROUND(AVG(days_since_prior_order), 1) AS avg_days_between_orders
    FROM orders
    GROUP BY user_id
)
SELECT 
    user_id,
    lifetime_orders,
    avg_days_between_orders,
    CASE 
        WHEN lifetime_orders >= 40 THEN 'VIP Customer'
        WHEN lifetime_orders >= 15 THEN 'Loyal Customer'
        WHEN lifetime_orders >= 5 THEN 'Regular Customer'
        ELSE 'Occasional Customer'
    END AS customer_segment,
    -- Window Function to rank them
    RANK() OVER(ORDER BY lifetime_orders DESC) AS company_rank
FROM UserStats
ORDER BY lifetime_orders DESC
LIMIT 50;