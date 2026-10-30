-- Запрос 1. Товары дороже средней цены всех товаров
SELECT
    product_name,
    price
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;

-- Запрос 2. ФИО пользователя, сделавшего самый дорогой заказ
SELECT
    u.last_name
FROM users u
JOIN orders o        ON o.user_id = u.user_id
JOIN order_items oi  ON oi.order_id = o.order_id
GROUP BY u.user_id
HAVING SUM(oi.price * oi.quantity) = (
    SELECT MAX(total)
    FROM (
        SELECT SUM(oi2.price * oi2.quantity) AS total
        FROM orders o2
        JOIN order_items oi2 ON oi2.order_id = o2.order_id
        GROUP BY o2.order_id
    )
);

-- Запрос 3. Клиенты, у которых есть хотя бы один заказ (IN)
SELECT last_name
FROM users
WHERE user_id IN (SELECT user_id FROM orders)
ORDER BY last_name;

-- Запрос 4. Пользователи без заказов (NOT EXISTS)
SELECT u.last_name
FROM users u
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.user_id
)
ORDER BY u.last_name;

-- Запрос 5. Товары, которые ни разу не заказывали (NOT IN)
SELECT p.product_name
FROM products p
WHERE p.product_id NOT IN (
    SELECT oi.product_id
    FROM order_items oi
)
ORDER BY p.product_name;

-- Запрос 6. Клиенты и сумма заказов, ранг по убыванию суммы
SELECT
    u.last_name,
    SUM(oi.price * oi.quantity) AS total,
    RANK() OVER (ORDER BY SUM(oi.price * oi.quantity) DESC) AS rank
FROM users u
JOIN orders o        ON o.user_id = u.user_id
JOIN order_items oi  ON oi.order_id = o.order_id
GROUP BY u.user_id
ORDER BY rank;

-- Запрос 7. Для каждого заказа — ФИО клиента и порядковый номер заказа клиента
SELECT
    o.order_id,
    u.last_name,
    ROW_NUMBER() OVER (
        PARTITION BY o.user_id
        ORDER BY o.order_date
    ) AS order_seq
FROM orders o
JOIN users u ON u.user_id = o.user_id
ORDER BY u.last_name, order_seq;

-- Запрос 8. Нумерация товаров внутри категории по убыванию цены
SELECT
    c.category_name,
    p.product_name,
    p.price,
    ROW_NUMBER() OVER (
        PARTITION BY p.category_id
        ORDER BY p.price DESC
    ) AS rn
FROM products p
JOIN categories c ON c.category_id = p.category_id
ORDER BY c.category_name, rn;

-- Запрос 9. Самый дорогой товар в каждой категории (через табличный подзапрос)
SELECT
    category_name,
    product_name,
    price
FROM (
    SELECT
        c.category_name,
        p.product_name,
        p.price,
        ROW_NUMBER() OVER (
            PARTITION BY p.category_id
            ORDER BY p.price DESC
        ) AS rn
    FROM products p
    JOIN categories c ON c.category_id = p.category_id
) AS ranked
WHERE rn = 1
ORDER BY category_name;

-- Запрос 10. Накопительная сумма выручки по датам заказов
SELECT
    o.order_id,
    o.order_date,
    SUM(oi.price * oi.quantity) AS order_total,
    SUM(SUM(oi.price * oi.quantity)) OVER (
        ORDER BY o.order_date
    ) AS cumulative_total
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id
ORDER BY o.order_date;

-- Запрос 11. Дата текущего и предыдущего заказа клиента + разница в днях
SELECT
    o.order_id,
    u.last_name,
    o.order_date                                AS current_date,
    LAG(o.order_date) OVER (
        PARTITION BY o.user_id
        ORDER BY o.order_date
    )                                           AS prev_date,
    julianday(o.order_date) - julianday(
        LAG(o.order_date) OVER (
            PARTITION BY o.user_id
            ORDER BY o.order_date
        )
    )                                           AS days_gap
FROM orders o
JOIN users u ON u.user_id = o.user_id
ORDER BY u.last_name, o.order_date;