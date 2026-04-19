-- Market Basket Analysis (Product Affinity)

SELECT 
    p1.product_name AS product_A,
    p2.product_name AS product_B,
    COUNT(*) AS times_bought_together
FROM order_products op1
-- Self joining the order_products table on the exact same order
JOIN order_products op2 
    ON op1.order_id = op2.order_id 
    AND op1.product_id < op2.product_id -- The '<' prevents duplicates like (Banana, Apple) and (Apple, Banana)
JOIN products p1 ON op1.product_id = p1.product_id
JOIN products p2 ON op2.product_id = p2.product_id
GROUP BY p1.product_name, p2.product_name
ORDER BY times_bought_together DESC
LIMIT 20;