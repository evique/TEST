SELECT 
    p.name AS product_name, 
    p.price, 
    calc_discount(p.price, 20) AS price_with_discount
FROM products p;

SELECT 
    format_full_name(c.last_name, c.first_name, c.middle_name) AS formatted_name
FROM clients c
WHERE c.middle_name IS NULL OR TRIM(c.middle_name) = '';

SELECT 
    oi.order_id,
    SUM(oi.quantity) AS total_units,
    pluralize_items(SUM(oi.quantity)) AS units_text
FROM order_items oi
GROUP BY oi.order_id;

SELECT 
    format_full_name(c.last_name, c.first_name, c.middle_name) AS client_name,
    SUM(oi.quantity * oi.price) AS total_sum,
    calc_discount(SUM(oi.quantity * oi.price), 10) AS total_with_discount
FROM orders o
JOIN clients c ON o.client_id = c.client_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, c.client_id;

SELECT 
    c.client_id,
    format_full_name(c.last_name, c.first_name, c.middle_name) AS client_name,
    COALESCE(SUM(oi.quantity * oi.price), 0) AS total_spent,
    get_client_tier(COALESCE(SUM(oi.quantity * oi.price), 0)) AS tier,
    get_client_loyalty_days(c.first_order_date) AS loyalty_days
FROM clients c
LEFT JOIN orders o ON c.client_id = o.client_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.client_id;