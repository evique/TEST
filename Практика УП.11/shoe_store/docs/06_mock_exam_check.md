# Проверка структуры БД cinema.sqlite

Дата проверки: (укажите дату)
Скрипт проверки: `src/cinema_check.py`

## Сводная таблица

| Таблица | Кол-во полей | PK | FK | Статус |
|---------|--------------|----|----|--------|
| roles | 2 | role_id | — |  OK |
| genres | 2 | genre_id | — | OK |
| age_ratings | 3 | rating_id | — |  OK |
| halls | 4 | hall_id | — |  OK |
| users | 5 | user_id | role_id → roles |  OK |
| movies | 6 | movie_id | genre_id → genres, rating_id → age_ratings |  OK |
| sessions | 5 | session_id | movie_id → movies, hall_id → halls | OK |
| tickets | 6 | ticket_id | session_id → sessions, user_id → users |  OK |

## Детальная проверка

### roles
- Поля: role_id (INTEGER, PK), role_name (TEXT, NOT NULL, UNIQUE)
- PK на месте, FK нет (справочник)
- Типы данных корректны

### genres
- Поля: genre_id (INTEGER, PK), genre_name (TEXT, NOT NULL, UNIQUE)
- PK на месте, FK нет (справочник)

### age_ratings
- Поля: rating_id (INTEGER, PK), rating_code (TEXT, NOT NULL, UNIQUE), min_age (INTEGER, NOT NULL, CHECK ≥ 0)
- PK на месте, FK нет (справочник)

### halls
- Поля: hall_id (INTEGER, PK), hall_name (TEXT, NOT NULL, UNIQUE), rows_count (INTEGER, NOT NULL, CHECK > 0), seats_per_row (INTEGER, NOT NULL, CHECK > 0)
- PK на месте, FK нет (справочник)

### users
- Поля: user_id (INTEGER, PK), full_name (TEXT, NOT NULL), email (TEXT, NOT NULL, UNIQUE), phone (TEXT, NOT NULL), role_id (INTEGER, NOT NULL, FK)
- PK: user_id 
- FK: role_id → roles(role_id), ON DELETE RESTRICT, ON UPDATE CASCADE 

### movies
- Поля: movie_id (INTEGER, PK), title (TEXT, NOT NULL), genre_id (INTEGER, NOT NULL, FK), duration_min (INTEGER, NOT NULL, CHECK > 0), rating_id (INTEGER, NOT NULL, FK), poster_path (TEXT)
- PK: movie_id 
- FK: genre_id → genres, rating_id → age_ratings (оба ON DELETE RESTRICT) 

### sessions
- Поля: session_id (INTEGER, PK), movie_id (INTEGER, NOT NULL, FK), hall_id (INTEGER, NOT NULL, FK), start_datetime (TEXT, NOT NULL), base_price (REAL, NOT NULL, CHECK > 0)
- PK: session_id 
- FK: movie_id → movies, hall_id → halls (оба ON DELETE RESTRICT) 

### tickets
- Поля: ticket_id (INTEGER, PK), session_id (INTEGER, NOT NULL, FK), user_id (INTEGER, NOT NULL, FK), row_num (INTEGER, NOT NULL, CHECK > 0), seat_num (INTEGER, NOT NULL, CHECK > 0), final_price (REAL, NOT NULL, CHECK > 0)
- PK: ticket_id 
- FK: session_id → sessions (ON DELETE CASCADE), user_id → users (ON DELETE RESTRICT) 
- UNIQUE (session_id, row_num, seat_num) 

## Итог
Все 8 таблиц созданы. Первичные и внешние ключи на месте. Типы данных соответствуют ER-диаграмме. Ограничения CHECK и UNIQUE присутствуют. Нарушений ссылочной целостности нет. **Структура БД корректна.**