# Анализ предметной области: Система продажи билетов в кинотеатр
## 1. Сущности и атрибуты

### 1.1 roles (Роли пользователей)
Справочник ролей. Независимая таблица.

| Атрибут | Тип | Ограничения | Описание |

| role_id | INTEGER | PK, AUTOINCREMENT | Идентификатор роли |
| role_name | TEXT | NOT NULL, UNIQUE | Название роли (Гость, Клиент, Администратор) |

### 1.2 users (Клиенты)
Зарегистрированные пользователи системы.

| Атрибут | Тип | Ограничения | Описание |

| user_id | INTEGER | PK, AUTOINCREMENT | Идентификатор клиента |
| full_name | TEXT | NOT NULL | ФИО |
| email | TEXT | NOT NULL, UNIQUE | Email (уникальный) |
| phone | TEXT | NOT NULL | Номер телефона |
| role_id | INTEGER | NOT NULL, FK → roles(role_id), ON DELETE RESTRICT | Роль клиента |

### 1.3 genres (Жанры)
Справочник жанров фильмов.

| Атрибут | Тип | Ограничения | Описание |

| genre_id | INTEGER | PK, AUTOINCREMENT | Идентификатор жанра |
| genre_name | TEXT | NOT NULL, UNIQUE | Название жанра |

### 1.4 age_ratings (Возрастные ограничения)
Справочник возрастных рейтингов (0+, 6+, 12+, 16+, 18+).

| Атрибут | Тип | Ограничения | Описание |

| rating_id | INTEGER | PK, AUTOINCREMENT | Идентификатор рейтинга |
| rating_code | TEXT | NOT NULL, UNIQUE | Код (0+, 6+, 12+, 16+, 18+) |
| min_age | INTEGER | NOT NULL, CHECK (min_age >= 0) | Минимальный возраст |

### 1.5 movies (Фильмы)
Информация о фильмах.

| Атрибут | Тип | Ограничения | Описание |

| movie_id | INTEGER | PK, AUTOINCREMENT | Идентификатор фильма |
| title | TEXT | NOT NULL | Название фильма |
| genre_id | INTEGER | NOT NULL, FK → genres(genre_id), ON DELETE RESTRICT | Жанр |
| duration_min | INTEGER | NOT NULL, CHECK (duration_min > 0) | Длительность в минутах |
| rating_id | INTEGER | NOT NULL, FK → age_ratings(rating_id), ON DELETE RESTRICT | Возрастное ограничение |
| poster_path | TEXT | NULL | Путь к постеру |

### 1.6 halls (Кинозалы)
Кинозалы с конфигурацией мест.

| Атрибут | Тип | Ограничения | Описание |

| hall_id | INTEGER | PK, AUTOINCREMENT | Идентификатор зала |
| hall_name | TEXT | NOT NULL, UNIQUE | Название зала |
| rows_count | INTEGER | NOT NULL, CHECK (rows_count > 0) | Количество рядов |
| seats_per_row | INTEGER | NOT NULL, CHECK (seats_per_row > 0) | Мест в ряду |

### 1.7 sessions (Сеансы)
Конкретный показ фильма в зале.

| Атрибут | Тип | Ограничения | Описание |

| session_id | INTEGER | PK, AUTOINCREMENT | Идентификатор сеанса |
| movie_id | INTEGER | NOT NULL, FK → movies(movie_id), ON DELETE RESTRICT | Фильм |
| hall_id | INTEGER | NOT NULL, FK → halls(hall_id), ON DELETE RESTRICT | Зал |
| start_datetime | TEXT | NOT NULL | Дата и время начала (ISO 8601) |
| base_price | REAL | NOT NULL, CHECK (base_price > 0) | Базовая цена билета |

### 1.8 tickets (Билеты)
Факт покупки билета клиентом на сеанс.

| Атрибут | Тип | Ограничения | Описание |

| ticket_id | INTEGER | PK, AUTOINCREMENT | Идентификатор билета |
| session_id | INTEGER | NOT NULL, FK → sessions(session_id), ON DELETE CASCADE | Сеанс |
| user_id | INTEGER | NOT NULL, FK → users(user_id), ON DELETE RESTRICT | Покупатель |
| row_num | INTEGER | NOT NULL, CHECK (row_num > 0) | Ряд |
| seat_num | INTEGER | NOT NULL, CHECK (seat_num > 0) | Место |
| final_price | REAL | NOT NULL, CHECK (final_price > 0) | Итоговая цена |
| UNIQUE (session_id, row_num, seat_num) | | | Одно место — один билет на сеанс |

## 2. Доказательство 3НФ (Третья нормальная форма)

### roles
Атрибуты `role_name` зависят только от `role_id`. Транзитивных зависимостей нет. Нет списков в ячейках. **3НФ — да.**

### users
`full_name`, `email`, `phone`, `role_id` зависят только от `user_id`. Название роли вынесено в `roles` — это устраняет транзитивную зависимость `user_id → role_id → role_name`. **3НФ — да.**

### genres
`genre_name` зависит только от `genre_id`. **3НФ — да.**

### age_ratings
`rating_code`, `min_age` зависят только от `rating_id`. **3НФ — да.**

### movies
`title`, `genre_id`, `duration_min`, `rating_id`, `poster_path` зависят только от `movie_id`. Название жанра и код рейтинга вынесены в справочники — устранены транзитивные зависимости. **3НФ — да.**

### halls
`hall_name`, `rows_count`, `seats_per_row` зависят только от `hall_id`. **3НФ — да.**

### sessions
`movie_id`, `hall_id`, `start_datetime`, `base_price` зависят только от `session_id`. Название фильма и зала не дублируются — они получаются через JOIN. **3НФ — да.**

### tickets
`session_id`, `user_id`, `row_num`, `seat_num`, `final_price` зависят только от `ticket_id`. Название фильма, зала, дата сеанса НЕ хранятся в билете (они зависят от `session_id`, а не от `ticket_id`) — это было бы нарушением 3НФ. **3НФ — да.**

## 3. Связи

- `roles` 1:N `users`
- `genres` 1:N `movies`
- `age_ratings` 1:N `movies`
- `movies` 1:N `sessions`
- `halls` 1:N `sessions`
- `sessions` 1:N `tickets`
- `users` 1:N `tickets`

**M:N связь** реализуется через `tickets`: клиент ↔ сеанс (покупка билета).

## 4. ER-диаграмма

Схема для draw.io (импортируйте или нарисуйте вручную по этой структуре):

**Кардинальность:**
- roles (1) ─── (N) users
- genres (1) ─── (N) movies
- age_ratings (1) ─── (N) movies
- movies (1) ─── (N) sessions
- halls (1) ─── (N) sessions
- sessions (1) ─── (N) tickets
- users (1) ─── (N) tickets

