-- Список всех пользователей с ролями
SELECT u.user_id, u.login, u.last_name, u.first_name, r.role_name
FROM users u
JOIN roles r ON u.role_id = r.role_id;

-- Список всех товаров
SELECT product_id, category, manufacturer, name, price
FROM products;

-- Список всех размеров
SELECT size_id, size_value
FROM sizes;

-- Список всех заказов с ФИО клиентов и датой
SELECT o.order_id, o.order_date, u.last_name, u.first_name, u.login
FROM orders o
JOIN users u ON o.user_id = u.user_id;

-- Список всех товарных позиций на складе с наименованием товара и размером
SELECT si.stock_item_id, p.name AS product_name, s.size_value, si.quantity, p.price
FROM stock_items si
JOIN products p ON si.product_id = p.product_id
JOIN sizes s ON si.size_id = s.size_id;