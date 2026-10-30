## Таблица roles
- role_id - идентификатор роли PK
- role_name - название роли UK
## Таблица users
- user_id - идентификатор пользователя PK
- last_name - фамилия
- first_name - имя
- middle_name - отчество
- login - логин UK
- role_id - ссылка на роль FK
## Таблица Orders
- order_id - идентификатор заказа PK
- order_date - дата заказа 
- user_id - идентификатор пользователя FK
## Таблица OREDER_ITEMS
- order_item_id - идентификатор предмета в заказе PK
- order_id - идентификатор заказа FK
- stock_item_id - идентификатор предмета на складе FK
- quantity - количество 
- unit_price - цена за единицу товара
## Таблица STOCK_ITEMS
- stock_item_id -идентификатор предмета на складе PK
- product_id -идентификатор продукта FK
- size_id -идентификатор размера FK
- quantity - количество
## Таблица PRODUCTS
- product_id -идентификатор продукта PK
- category - категория
- sub_categoty - дополнительная категория
- manufacturer - производитель 
- name - название
- image_path - путь к изображению
- composition - материал
- description - описание 
- price - цена
## Таблица SIZES
- size_id -идентификатор размера PK
- size_value -цена размера UK

# Таблицы типов данных для всех сущностей

## Таблица roles
| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
| :--- | :--- | :--- | :--- | :--- | :--- |
| role_id | INTEGER | Идентификатор роли | да | - | PRIMARY KEY AUTOINCREMENT |
| role_name | TEXT | Название роли | да | - | UNIQUE |

## Таблица users
| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
| :--- | :--- | :--- | :--- | :--- | :--- |
| user_id | INTEGER | Идентификатор пользователя | да | - | PRIMARY KEY AUTOINCREMENT |
| last_name | TEXT | Фамилия | да | - | - |
| first_name | TEXT | Имя | да | - | - |
| middle_name | TEXT | Отчество | нет | NULL | - |
| login | TEXT | Логин | да | - | UNIQUE |
| role_id | INTEGER | Ссылка на роль | да | - | FOREIGN KEY (roles) |

## Таблица products
| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
| :--- | :--- | :--- | :--- | :--- | :--- |
| product_id | INTEGER | Идентификатор товара | да | - | PRIMARY KEY AUTOINCREMENT |
| category | TEXT | Категория | да | - | - |
| sub_category | TEXT | Подкатегория | нет | NULL | - |
| manufacturer | TEXT | Производитель | да | - | - |
| name | TEXT | Наименование | да | - | - |
| image_path | TEXT | Путь к изображению | нет | NULL | - |
| composition | TEXT | Состав | нет | NULL | - |
| description | TEXT | Описание | нет | NULL | - |
| price | NUMERIC | Цена | да | - | CHECK (price > 0) |

## Таблица sizes
| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
| :--- | :--- | :--- | :--- | :--- | :--- |
| size_id | INTEGER | Идентификатор размера | да | - | PRIMARY KEY AUTOINCREMENT |
| size_value | REAL | Значение размера | да | - | UNIQUE |

## Таблица stock_items
| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
| :--- | :--- | :--- | :--- | :--- | :--- |
| stock_item_id | INTEGER | Идентификатор позиции | да | - | PRIMARY KEY AUTOINCREMENT |
| product_id | INTEGER | Ссылка на товар | да | - | FOREIGN KEY (products) |
| size_id | INTEGER | Ссылка на размер | да | - | FOREIGN KEY (sizes) |
| quantity | INTEGER | Количество на складе | да | 0 | CHECK (quantity >= 0) |

## Таблица orders
| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
| :--- | :--- | :--- | :--- | :--- | :--- |
| order_id | INTEGER | Идентификатор заказа | да | - | PRIMARY KEY AUTOINCREMENT |
| order_date | TEXT | Дата заказа (ISO 8601) | да | DATE('now') | - |
| user_id | INTEGER | Ссылка на пользователя | да | - | FOREIGN KEY (users) |

## Таблица order_items
| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
| :--- | :--- | :--- | :--- | :--- | :--- |
| order_item_id | INTEGER | Идентификатор строки заказа | да | - | PRIMARY KEY AUTOINCREMENT |
| order_id | INTEGER | Ссылка на заказ | да | - | FOREIGN KEY (orders) ON DELETE CASCADE |
| stock_item_id | INTEGER | Ссылка на товарную позицию | да | - | FOREIGN KEY (stock_items) |
| quantity | INTEGER | Количество в заказе | да | - | CHECK (quantity > 0) |
| unit_price | NUMERIC | Цена за единицу | да | - | CHECK (unit_price > 0) |