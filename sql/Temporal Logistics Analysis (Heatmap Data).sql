-- Temporal Logistics Analysis (Heatmap Data)
SELECT 
    order_dow AS day_of_week,
    order_hour_of_day AS hour_of_day,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY order_dow, order_hour_of_day
ORDER BY total_orders DESC;