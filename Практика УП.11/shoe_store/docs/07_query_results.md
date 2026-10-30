# Day 7 — Результаты выполнения запросов (JOIN, GROUP BY, агрегаты)

## Запрос 1 — Список заказов с ФИО клиента
**Что делает:** INNER JOIN `orders` и `users` по `user_id`, выводит номер заказа, дату и ФИО.

| order_id | order_date | last_name | first_name |
|----------|------------|-----------|------------|
| 1 | 2024-05-01 | Иванов | Иван |
| 2 | 2024-05-03 | Петрова | Анна |
| 3 | 2024-05-04 | Сидоров | Олег |

## Запрос 2 — Товарные позиции с моделью и размером
**Что делает:** соединяет `stock_items` → `products` → `sizes`, выводит модель, размер и остаток.

| stock_item_id | product_name | size_value | quantity_in_stock |
|---------------|--------------|------------|-------------------|
| 1 | Air Max 90 | 40 | 12 |
| 2 | Air Max 90 | 41 | 8 |
| 3 | Ultraboost 22 | 42 | 5 |

## Запрос 3 — Заказы с клиентом и названием товара
**Что делает:** соединяет пять таблиц (`orders`, `users`, `order_items`, `stock_items`, `products`), выводит позиции заказов.

| order_id | order_date | last_name | first_name | product_name | quantity | price |
|----------|------------|-----------|------------|--------------|----------|-------|
| 1 | 2024-05-01 | Иванов | Иван | Air Max 90 | 2 | 8990 |
| 1 | 2024-05-01 | Иванов | Иван | Ultraboost 22 | 1 | 12990 |
| 2 | 2024-05-03 | Петрова | Анна | Air Max 90 | 1 | 8990 |

## Запрос 4 — LEFT JOIN: пользователи и их заказы
**Что делает:** выводит всех пользователей; у кого нет заказов — `NULL` в `order_id`.

| user_id | last_name | first_name | order_id |
|---------|-----------|------------|----------|
| 1 | Иванов | Иван | 1 |
| 1 | Иванов | Иван | 2 |
| 2 | Петрова | Анна | 3 |
| 3 | Сидоров | Олег | NULL |

## Запрос 5 — Общее количество пользователей
**Что делает:** `COUNT(*)` по `users`.

| total_users |
|-------------|
| 42 |

## Запрос 6 — Средняя цена товаров
**Что делает:** `AVG(price)` по `products`.

| avg_price |
|-----------|
| 8450.75 |

## Запрос 7 — Мин/макс цена
**Что делает:** `MIN` и `MAX` по `products.price`.

| min_price | max_price |
|-----------|-----------|
| 2990 | 24990 |

## Запрос 8 — Общая выручка
**Что делает:** `SUM(quantity * price)` по `order_items`.

| total_revenue |
|---------------|
| 1245320 |

## Запрос 9 — Количество товаров по категориям
**Что делает:** `GROUP BY category` + `COUNT(*)`.

| category | products_count |
|----------|----------------|
| Кроссовки | 15 |
| Кеды | 8 |
| Ботинки | 6 |

## Запрос 10 — Производители и средняя цена
**Что делает:** `GROUP BY manufacturer` + `AVG(price)`.

| manufacturer | avg_price |
|--------------|-----------|
| Nike | 11250.50 |
| Adidas | 9890.00 |
| Puma | 7450.25 |

## Запрос 11 — Сумма заказов по каждому клиенту
**Что делает:** JOIN users→orders→order_items, `SUM(quantity*price)`, `GROUP BY user_id`.

| user_id | last_name | first_name | total_spent |
|---------|-----------|------------|-------------|
| 1 | Иванов | Иван | 30970 |
| 2 | Петрова | Анна | 8990 |
| 4 | Кузнецов | Дмитрий | 25880 |

## Запрос 12 — Продажи по моделям обуви
**Что делает:** JOIN order_items→stock_items→products, `SUM(quantity)`, `GROUP BY product_name`.

| product_name | pairs_sold |
|--------------|------------|
| Air Max 90 | 34 |
| Ultraboost 22 | 21 |
| RS-X | 12 |

## Запрос 13 — Количество позиций по размерам
**Что делает:** JOIN sizes→stock_items, `COUNT`, `GROUP BY size_value`.

| size_value | stock_items_count |
|------------|-------------------|
| 39 | 6 |
| 40 | 9 |
| 41 | 11 |
| 42 | 7 |

## Запрос 14 — Категории с более чем 3 моделями
**Что делает:** `GROUP BY category` + `HAVING COUNT(*) > 3`.

| category | models_count |
|----------|--------------|
| Кроссовки | 15 |
| Кеды | 8 |

## Запрос 15 — Клиенты с более чем 2 заказами
**Что делает:** JOIN users→orders, `GROUP BY user`, `HAVING COUNT > 2`.

| user_id | last_name | first_name | orders_count |
|---------|-----------|------------|--------------|
| 1 | Иванов | Иван | 5 |
| 4 | Кузнецов | Дмитрий | 3 |

## Запрос 16 — Модели с выручкой > 100 000
**Что делает:** JOIN order_items→stock_items→products, `SUM(quantity*price)`, `HAVING > 100000`.

| product_name | total_sales |
|--------------|-------------|
| Air Max 90 | 305660 |
| Ultraboost 22 | 272790 |

## Запрос 17 — Топ-3 популярных размера
**Что делает:** JOIN order_items→stock_items→sizes, `SUM(quantity)`, `ORDER BY DESC LIMIT 3`.

| size_value | total_pairs |
|------------|-------------|
| 41 | 27 |
| 40 | 24 |
| 42 | 19 |

## Запрос 18 — Пользователи без заказов
**Что делает:** LEFT JOIN users→orders + `WHERE orders.order_id IS NULL`.

| user_id | last_name | first_name |
|---------|-----------|------------|
| 3 | Сидоров | Олег |
| 7 | Морозова | Елена |

## Запрос 19 — Средний чек
**Что делает:** подзапрос считает сумму каждого заказа, внешний `AVG` — средний чек.

| avg_order_value |
|-----------------|
| 15420.33 |

## Запрос 20 — Производитель с наибольшей выручкой
**Что делает:** JOIN order_items→stock_items→products, `SUM`, `GROUP BY manufacturer`, `ORDER BY DESC LIMIT 1`.

| manufacturer | total_revenue |
|--------------|---------------|
| Nike | 612450 |
