# Day 8 — Subqueries and Window Functions: результаты

## Запрос 1. Товары дороже средней цены
**Задача:** найти товары с ценой выше средней по магазину.
**Приём:** скалярный подзапрос в `WHERE` — `(SELECT AVG(price) FROM products)`.
**Результат (первые строки):**

| product_name | price |
|---|---|
| ... | ... |

## Запрос 2. Клиент с самым дорогим заказом
**Задача:** определить ФИО покупателя, чей заказ имеет максимальную сумму.
**Приём:** вложенный подзапрос в `HAVING` (MAX по суммам заказов) + агрегация.
**Результат:**

| last_name |
|---|
| ... |

## Запрос 3. Клиенты с заказами (IN)
**Приём:** `WHERE user_id IN (SELECT user_id FROM orders)`.
**Результат (первые строки):**

| last_name |
|---|
| ... |

## Запрос 4. Клиенты без заказов (NOT EXISTS)
**Приём:** коррелированный подзапрос `NOT EXISTS (... WHERE o.user_id = u.user_id)`.
**Результат (первые строки):**

| last_name |
|---|
| ... |


## Запрос 5. Товары без заказов (NOT IN)
**Приём:** `NOT IN (SELECT product_id FROM order_items)`.
**Результат (первые строки):**

| product_name |
|---|
| ... |

## Запрос 6. Ранг клиентов по сумме заказов (RANK)
**Приём:** `RANK() OVER (ORDER BY SUM(...) DESC)`.
**Результат (первые строки):**

| last_name | total | rank |
|---|---|---|
| ... | ... | 1 |

## Запрос 7. Порядковый номер заказа клиента (ROW_NUMBER)
**Приём:** `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date)`.
**Результат (первые строки):**

| order_id | last_name | order_seq |
|---|---|---|
| ... | ... | 1 |

## Запрос 8. Нумерация товаров внутри категории
**Приём:** `ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC)`.
**Результат (первые строки):**

| category_name | product_name | price | rn |
|---|---|---|---|
| ... | ... | ... | 1 |

## Запрос 9. Топ-1 товар в каждой категории (табличный подзапрос)
**Приём:** подзапрос в `FROM` + фильтр `WHERE rn = 1`.
**Результат:**

| category_name | product_name | price |
|---|---|---|
| ... | ... | ... |

## Запрос 10. Накопительная сумма выручки по датам
**Приём:** `SUM(SUM(...)) OVER (ORDER BY order_date)`.
**Результат (первые строки):**

| order_id | order_date | order_total | cumulative_total |
|---|---|---|---|
| ... | ... | ... | ... |

## Запрос 11. Дата предыдущего заказа клиента и разница в днях (LAG)
**Приём:** `LAG(order_date) OVER (PARTITION BY user_id ORDER BY order_date)` + `julianday()`.
**Результат (первые строки):**

| order_id | last_name | current_date | prev_date | days_gap |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |