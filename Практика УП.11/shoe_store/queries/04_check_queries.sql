SELECT * FROM roles;
SELECT u.user_id, u.login, u.last_name, r.role_name FROM users u JOIN roles r ON u.role_id = r.role_id;
SELECT * FROM products;
SELECT * FROM sizes;
SELECT o.order_id, o.order_date, u.login FROM orders o JOIN users u ON o.user_id = u.user_id;
SELECT si.stock_item_id, p.product_name, s.size_value, si.quantity_available FROM stock_items si JOIN products p ON si.product_id = p.product_id JOIN sizes s ON si.size_id = s.size_id;