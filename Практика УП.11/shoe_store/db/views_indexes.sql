DROP VIEW IF EXISTS v_orders_full;
CREATE VIEW v_orders_full AS
SELECT
    o.order_id                                   AS order_id,
    o.order_date                                 AS order_date,
    u.last_name || ' ' || u.first_name           AS client_fio,
    SUM(oi.quantity * oi.price)                  AS total_sum
FROM orders o
JOIN users u        ON o.user_id   = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, o.order_date, u.last_name, u.first_name;

DROP VIEW IF EXISTS v_products_with_stock;
CREATE VIEW v_products_with_stock AS
SELECT
    p.model_name                 AS model_name,
    p.price                      AS price,
    s.size_value                 AS size_value,
    si.quantity                  AS quantity_in_stock
FROM products p
JOIN stock_items si ON si.product_id = p.product_id
JOIN sizes s        ON s.size_id     = si.size_id;

DROP VIEW IF EXISTS v_user_stats;
CREATE VIEW v_user_stats AS
SELECT
    u.last_name || ' ' || u.first_name AS client_fio,
    u.login                            AS login,
    COUNT(o.order_id)                  AS orders_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.user_id
GROUP BY u.user_id, u.last_name, u.first_name, u.login;

SELECT * FROM v_orders_full        LIMIT 3;
SELECT * FROM v_products_with_stock LIMIT 3;
SELECT * FROM v_user_stats         LIMIT 3;

CREATE INDEX IF NOT EXISTS idx_products_category
    ON products (category);

CREATE INDEX IF NOT EXISTS idx_orders_order_date
    ON orders (order_date);

CREATE INDEX IF NOT EXISTS idx_orders_user_id
    ON orders (user_id);

CREATE INDEX IF NOT EXISTS idx_stock_items_product_id
    ON stock_items (product_id);

CREATE INDEX IF NOT EXISTS idx_stock_items_size_id
    ON stock_items (size_id);

CREATE INDEX IF NOT EXISTS idx_products_manufacturer_category
    ON products (manufacturer, category);

SELECT name, tbl_name, sql
FROM sqlite_master
WHERE type = 'index' AND sql IS NOT NULL;

DROP VIEW IF EXISTS v_simple;
CREATE VIEW v_simple AS
SELECT product_id, price FROM products;

UPDATE v_simple SET price = 100 WHERE product_id = 1;