# Анализ планов выполнения запросов (EXPLAIN QUERY PLAN)
## 1. Созданные индексы и их назначение

| № | Индекс | Таблица | Поля | Назначение |
|---|--------|---------|------|------------|
| 1 | `idx_products_category` | products | category | Ускорение фильтрации товаров по категории (частый запрос в каталоге) |
| 2 | `idx_orders_order_date` | orders | order_date | Ускорение сортировки и выборки по датам заказов (отчёты за период) |
| 3 | `idx_orders_user_id` | orders | user_id | Ускорение JOIN orders ↔ users, фильтра по клиенту |
| 4 | `idx_stock_items_product_id` | stock_items | product_id | Ускорение JOIN products ↔ stock_items |
| 5 | `idx_stock_items_size_id` | stock_items | size_id | Ускорение JOIN sizes ↔ stock_items |
| 6 | `idx_products_manufacturer_category` | products | manufacturer, category | Составной индекс: ускоряет выборку по производителю и по паре «производитель + категория» |

**Почему именно эти индексы:** поля `category`, `order_date` и внешние ключи (`user_id`, `product_id`, `size_id`) участвуют в `WHERE` и `JOIN` чаще всего. Составной индекс `(manufacturer, category)` логичен, т.к. в каталоге обуви фильтруют сначала по бренду, затем по категории.

## 2. EXPLAIN QUERY PLAN — до создания индекса

### 2.1. Поиск товаров по категории
```sql
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE category = 'Кроссовки';
Результат (до индекса):

--2.2. Поиск по производителю
sql
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE manufacturer = 'Nike';
Результат (до индекса):

--3. JOIN orders ↔ users
sql
EXPLAIN QUERY PLAN
SELECT * FROM orders o JOIN users u ON o.user_id = u.user_id;
Результат (после индекса idx_orders_user_id):

--4. Вывод: когда индекс ускоряет работу, а когда игнорируется
Индекс ускоряет:

WHERE по индексированному полю (особенно с высокой селективностью).
JOIN по внешним ключам — без индекса соединение больших таблиц может занять минуты.
ORDER BY по индексированному полю (SQLite может идти по индексу без сортировки).

--5. Проверка обновляемости представлений
sql
CREATE VIEW v_simple AS SELECT product_id, price FROM products;
UPDATE v_simple SET price = 100 WHERE product_id = 1;