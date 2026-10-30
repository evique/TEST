# Результаты тестирования ограничений БД cinema.sqlite

Скрипт: `src/cinema_test.py`
Дата: (укажите дату)

## Таблица результатов

| № | Проверка | Ограничение | Ожидаемый результат | Фактический результат | Статус |

| 1 | Добавление клиента с существующим email | UNIQUE | `UNIQUE constraint failed: users.email` | `UNIQUE constraint failed: users.email` |  PASS |
| 2 | Билет на несуществующий сеанс | FOREIGN KEY | `FOREIGN KEY constraint failed` | `FOREIGN KEY constraint failed` |  PASS |
| 3 | Билет с отрицательной ценой | CHECK (final_price > 0) | `CHECK constraint failed: final_price > 0` | `CHECK constraint failed: final_price > 0` |  PASS |
| 4 | Билет с отрицательным номером места | CHECK (seat_num > 0) | `CHECK constraint failed: seat_num > 0` | `CHECK constraint failed: seat_num > 0` |  PASS |
| 5 | Удаление фильма, на который есть билеты | ON DELETE RESTRICT | `FOREIGN KEY constraint failed` | `FOREIGN KEY constraint failed` |  PASS |
| 6 | Удаление сеанса с билетами | ON DELETE CASCADE | Билеты удалены автоматически | Билеты удалены каскадно (было 1, стало 0) |  PASS |

## Вывод
Все 6 проверок пройдены успешно. База данных корректно защищает от:
- дублирования email (UNIQUE);
- вставки билетов на несуществующие сеансы (FOREIGN KEY);
- отрицательных цен и номеров мест (CHECK);
- удаления фильмов с проданными билетами (RESTRICT);
- «висячих» билетов при удалении сеанса (CASCADE).

**База данных устойчива к ошибкам. Все ограничения работают.**