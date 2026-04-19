-- Department "Sticky" Factor (Reorder Rates)
SELECT 
    d.department,
    FORMAT(COUNT(op.product_id), 0) AS total_items_sold,
    CONCAT(ROUND((SUM(op.reordered) / COUNT(op.reordered)) * 100, 2), '%') AS reorder_rate
FROM order_products op
JOIN products p ON op.product_id = p.product_id
JOIN departments d ON p.department_id = d.department_id
GROUP BY d.department
ORDER BY (SUM(op.reordered) / COUNT(op.reordered)) DESC;