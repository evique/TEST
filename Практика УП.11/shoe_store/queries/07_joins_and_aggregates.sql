Запрос 1. Список всех заказов с датой и ФИО клиента (INNER JOIN orders + users)

SELECT
    o.order_id,
    o.order_date,
    u.last_name,
    u.first_name
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id
ORDER BY o.order_id;

Запрос 2. Все товарные позиции (stock_items) с названием модели и размером.

SELECT
    si.stock_item_id,
    p.product_name,
    s.size_value,
    si.quantity_in_stock
FROM stock_items si
INNER JOIN products p ON si.product_id = p.product_id
INNER JOIN sizes    s ON si.size_id   = s.size_id
ORDER BY p.product_name, s.size_value;

Запрос 3. Все заказы с товарами: ФИО клиента и название товара.

SELECT
    o.order_id,
    o.order_date,
    u.last_name,
    u.first_name,
    p.product_name,
    oi.quantity,
    oi.price
FROM orders o
INNER JOIN users        u  ON o.user_id       = u.user_id
INNER JOIN order_items  oi ON o.order_id      = oi.order_id
INNER JOIN stock_items  si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products     p  ON si.product_id   = p.product_id
ORDER BY o.order_id, p.product_name;

 Запрос 4. LEFT JOIN: все пользователи и количество их заказов.

SELECT
    u.user_id,
    u.last_name,
    u.first_name,
    o.order_id
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
ORDER BY u.user_id;

Запрос 5. Общее количество пользователей

SELECT COUNT(*) AS total_users
FROM users;

 Запрос 6. Средняя цена всех товаров каталога

SELECT AVG(price) AS avg_price
FROM products;

 Запрос 7. Самый дорогой и самый дешёвый товар

SELECT
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM products;

 Запрос 8. Общая выручка: SUM(quantity * price) по order_items

SELECT
    SUM(quantity * price) AS total_revenue
FROM order_items;

 Запрос 9. Количество товаров в каждой категории

SELECT
    category,
    COUNT(*) AS products_count
FROM products
GROUP BY category
ORDER BY products_count DESC;

 Запрос 10. Список производителей и средняя цена их товаров

SELECT
    manufacturer,
    AVG(price) AS avg_price
FROM products
GROUP BY manufacturer
ORDER BY avg_price DESC;

Запрос 11. Для каждого пользователя — ФИО и общая сумма его заказов.

SELECT
    u.user_id,
    u.last_name,
    u.first_name,
    SUM(oi.quantity * oi.price) AS total_spent
FROM users u
INNER JOIN orders      o  ON u.user_id   = o.user_id
INNER JOIN order_items oi ON o.order_id  = oi.order_id
GROUP BY u.user_id, u.last_name, u.first_name
ORDER BY total_spent DESC;

 Запрос 12. Статистика по продажам каждой модели обуви:

SELECT
    p.product_name,
    SUM(oi.quantity) AS pairs_sold
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
GROUP BY p.product_name
ORDER BY pairs_sold DESC;

 Запрос 13. Список размеров и количество товарных позиций в каждом размере

SELECT
    s.size_value,
    COUNT(si.stock_item_id) AS stock_items_count
FROM sizes s
INNER JOIN stock_items si ON s.size_id = si.size_id
GROUP BY s.size_value
ORDER BY s.size_value;

Запрос 14. Категории, в которых больше 3 моделей

SELECT
    category,
    COUNT(*) AS models_count
FROM products
GROUP BY category
HAVING COUNT(*) > 3
ORDER BY models_count DESC;

 Запрос 15. Клиенты (ФИО), сделавшие больше 2 заказов

SELECT
    u.user_id,
    u.last_name,
    u.first_name,
    COUNT(o.order_id) AS orders_count
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.last_name, u.first_name
HAVING COUNT(o.order_id) > 2
ORDER BY orders_count DESC;

 Запрос 16. Модели обуви, сумма продаж которых превысила 100 000 рублей

SELECT
    p.product_name,
    SUM(oi.quantity * oi.price) AS total_sales
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
GROUP BY p.product_name
HAVING SUM(oi.quantity * oi.price) > 100000
ORDER BY total_sales DESC;

 Запрос 17. Топ-3 самых популярных размера обуви (по количеству проданных пар)

SELECT
    s.size_value,
    SUM(oi.quantity) AS total_pairs
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN sizes       s  ON si.size_id      = s.size_id
GROUP BY s.size_value
ORDER BY total_pairs DESC
LIMIT 3;
 
 Запрос 18. Пользователи, которые ни разу ничего не заказали

SELECT
    u.user_id,
    u.last_name,
    u.first_name
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id IS NULL
ORDER BY u.user_id;

Запрос 19. Средний чек (средняя стоимость одного заказа).

SELECT
    AVG(order_total) AS avg_order_value
FROM (
    SELECT
        order_id,
        SUM(quantity * price) AS order_total
    FROM order_items
    GROUP BY order_id
) AS order_sums;

Запрос 20. Производитель с наибольшей выручкой

SELECT
    p.manufacturer,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
GROUP BY p.manufacturer
ORDER BY total_revenue DESC
LIMIT 1;