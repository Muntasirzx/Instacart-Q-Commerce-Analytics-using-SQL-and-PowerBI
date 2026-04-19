-- Total Order & Customer Volume
SELECT 
    FORMAT(COUNT(DISTINCT order_id), 0) AS total_orders,
    FORMAT(COUNT(DISTINCT user_id), 0) AS total_customers
FROM orders;

-- Average Basket Size

WITH BasketSizes AS (
    SELECT 
        order_id, 
        COUNT(product_id) AS total_items
    FROM order_products
    GROUP BY order_id
)
SELECT 
    ROUND(AVG(total_items), 2) AS avg_basket_size 
FROM BasketSizes;

-- Global Reorder Rate

SELECT 
    CONCAT(ROUND((SUM(reordered) / COUNT(*)) * 100, 2), '%') AS global_reorder_rate
FROM order_products;

-- Average Days Between Orders

SELECT 
    ROUND(AVG(days_since_prior_order), 2) AS avg_days_between_orders
FROM orders
WHERE days_since_prior_order IS NOT NULL;