# Финальный набор ограничений (CHECK)

| Таблица | Поле | Ограничение | Обоснование |
| :--- | :--- | :--- | :--- |
| `users` | `login` | `CHECK (length(login) >= 3 AND length(login) <= 20)` | Ограничение допустимой длины учетной записи[cite: 42] |
| `products` | `name` | `CHECK (length(name) > 0)` | Наименование товара не может быть пустым[cite: 41] |
| `products` | `price` | `CHECK (price > 0 AND price < 1000000)` | Цена находится в разумном коммерческом диапазоне[cite: 42] |
| `sizes` | `size_value` | `CHECK (size_value > 20 AND size_value < 50)` | Ограничение стандартного размерного ряда обуви[cite: 42] |
| `stock_items` | `quantity` | `CHECK (quantity >= 0)` | Количество на складе не может быть отрицательным[cite: 41, 42] |
| `order_items` | `quantity` | `CHECK (quantity > 0)` | В заказе должно быть приобретено не менее 1 единицы товара[cite: 41, 42] |
| `order_items` | `unit_price` | `CHECK (unit_price > 0)` | Историческая цена позиции заказа строго положительная[cite: 42] |