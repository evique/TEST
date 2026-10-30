import os
import sqlite3

DB_PATH = os.path.join("db", "cinema.sqlite")

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def _prepare_test_data(conn):
    """Готовит тестовые данные: клиент, фильм, зал, сеанс, билет."""
    cur = conn.cursor()
  
    cur.execute("DELETE FROM tickets WHERE user_id IN (SELECT user_id FROM users WHERE email='test@example.com');")
    cur.execute("DELETE FROM sessions WHERE session_id NOT IN (SELECT DISTINCT session_id FROM tickets);")
    cur.execute("DELETE FROM users WHERE email='test@example.com';")

    cur.execute("SELECT role_id FROM roles WHERE role_name='Клиент';")
    role_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO users (full_name, email, phone, role_id) VALUES (?, ?, ?, ?);",
        ("Тестовый Клиент", "test@example.com", "+7-900-000-00-00", role_id),
    )
    user_id = cur.lastrowid

    cur.execute("SELECT genre_id FROM genres LIMIT 1;")
    genre_id = cur.fetchone()[0]
    cur.execute("SELECT rating_id FROM age_ratings LIMIT 1;")
    rating_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO movies (title, genre_id, duration_min, rating_id) VALUES (?, ?, ?, ?);",
        ("Тестовый Фильм", genre_id, 120, rating_id),
    )
    movie_id = cur.lastrowid

   
    cur.execute("SELECT hall_id FROM halls LIMIT 1;")
    hall_id = cur.fetchone()[0]

    
    cur.execute(
        "INSERT INTO sessions (movie_id, hall_id, start_datetime, base_price) VALUES (?, ?, ?, ?);",
        (movie_id, hall_id, "2025-06-01 18:30", 500.0),
    )
    session_id = cur.lastrowid

    conn.commit()
    return user_id, movie_id, session_id


def test_unique_email(conn):
    """1. Повторный email → UNIQUE constraint failed."""
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (full_name, email, phone, role_id) VALUES (?, ?, ?, ?);",
            ("Другой", "test@example.com", "+7-900-111-11-11", 1),
        )
        return "FAIL", "Вставка прошла без ошибки (ожидалась UNIQUE constraint failed)"
    except sqlite3.IntegrityError as e:
        return "OK", str(e)


def test_fk_nonexistent_session(conn):
    """2. Билет на несуществующий сеанс → FOREIGN KEY constraint failed."""
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE email='test@example.com';")
    user_id = cur.fetchone()[0]
    try:
        cur.execute(
            "INSERT INTO tickets (session_id, user_id, row_num, seat_num, final_price) "
            "VALUES (?, ?, ?, ?, ?);",
            (999999, user_id, 1, 1, 500.0),
        )
        return "FAIL", "Вставка прошла (ожидалась FOREIGN KEY constraint failed)"
    except sqlite3.IntegrityError as e:
        return "OK", str(e)


def test_check_negative_price(conn):
    """3. Отрицательная цена → CHECK constraint failed."""
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE email='test@example.com';")
    user_id = cur.fetchone()[0]
    cur.execute("SELECT session_id FROM sessions LIMIT 1;")
    session_id = cur.fetchone()[0]
    try:
        cur.execute(
            "INSERT INTO tickets (session_id, user_id, row_num, seat_num, final_price) "
            "VALUES (?, ?, ?, ?, ?);",
            (session_id, user_id, 1, 2, -100.0),
        )
        return "FAIL", "Вставка прошла (ожидалась CHECK constraint failed)"
    except sqlite3.IntegrityError as e:
        return "OK", str(e)


def test_check_negative_seat(conn):
    """4. Отрицательный номер места → CHECK constraint failed."""
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE email='test@example.com';")
    user_id = cur.fetchone()[0]
    cur.execute("SELECT session_id FROM sessions LIMIT 1;")
    session_id = cur.fetchone()[0]
    try:
        cur.execute(
            "INSERT INTO tickets (session_id, user_id, row_num, seat_num, final_price) "
            "VALUES (?, ?, ?, ?, ?);",
            (session_id, user_id, 1, -5, 500.0),
        )
        return "FAIL", "Вставка прошла (ожидалась CHECK constraint failed)"
    except sqlite3.IntegrityError as e:
        return "OK", str(e)


def test_restrict_movie_delete(conn, movie_id):
    """5. Удаление фильма с билетами → FOREIGN KEY constraint failed (RESTRICT)."""
    cur = conn.cursor()
    
    cur.execute("SELECT user_id FROM users WHERE email='test@example.com';")
    user_id = cur.fetchone()[0]
    cur.execute("SELECT session_id FROM sessions WHERE movie_id = ? LIMIT 1;", (movie_id,))
    row = cur.fetchone()
    if not row:
        cur.execute(
            "INSERT INTO sessions (movie_id, hall_id, start_datetime, base_price) "
            "VALUES (?, 1, '2025-06-02 12:00', 400.0);",
            (movie_id,),
        )
        session_id = cur.lastrowid
    else:
        session_id = row[0]

    cur.execute(
        "INSERT INTO tickets (session_id, user_id, row_num, seat_num, final_price) "
        "VALUES (?, ?, ?, ?, ?);",
        (session_id, user_id, 2, 3, 500.0),
    )
    conn.commit()

    try:
        cur.execute("DELETE FROM movies WHERE movie_id = ?;", (movie_id,))
        conn.commit()
        return "FAIL", "Удаление прошло (ожидалась FOREIGN KEY constraint failed / RESTRICT)"
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return "OK", str(e)


def test_cascade_session_delete(conn, session_id):
    """6. Удаление сеанса → билеты должны удалиться (CASCADE)."""
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tickets WHERE session_id = ?;", (session_id,))
    before = cur.fetchone()[0]
    if before == 0:

        cur.execute("SELECT user_id FROM users WHERE email='test@example.com';")
        user_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO tickets (session_id, user_id, row_num, seat_num, final_price) "
            "VALUES (?, ?, ?, ?, ?);",
            (session_id, user_id, 3, 4, 500.0),
        )
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM tickets WHERE session_id = ?;", (session_id,))
        before = cur.fetchone()[0]

    try:
        cur.execute("DELETE FROM sessions WHERE session_id = ?;", (session_id,))
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM tickets WHERE session_id = ?;", (session_id,))
        after = cur.fetchone()[0]
        if after == 0 and before > 0:
            return "OK", f"Билеты удалены каскадно (было {before}, стало {after})"
        return "FAIL", f"CASCADE не сработал (было {before}, стало {after})"
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return "FAIL", f"Неожиданная ошибка: {e}"


def main():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Файл БД не найден: {DB_PATH}. Запустите cinema_db_init.py")
        return

    results = []

    conn = _connect()
    try:
        user_id, movie_id, session_id = _prepare_test_data(conn)

        results.append(("1. UNIQUE email", "UNIQUE constraint failed",
                        *test_unique_email(conn)))
        results.append(("2. FK на несуществующий сеанс", "FOREIGN KEY constraint failed",
                        *test_fk_nonexistent_session(conn)))
        results.append(("3. CHECK: цена < 0", "CHECK constraint failed",
                        *test_check_negative_price(conn)))
        results.append(("4. CHECK: место < 0", "CHECK constraint failed",
                        *test_check_negative_seat(conn)))
        results.append(("5. RESTRICT: удаление фильма с билетами", "FOREIGN KEY constraint failed",
                        *test_restrict_movie_delete(conn, movie_id)))
        results.append(("6. CASCADE: удаление сеанса", "Билеты удалены",
                        *test_cascade_session_delete(conn, session_id)))

    finally:
        conn.close()

    print("\n" + "=" * 100)
    print(f"{'№':<3} {'Ограничение':<40} {'Ожидание':<35} {'Факт':<50} {'Статус':<6}")
    print("-" * 100)
    for i, (name, expected, status, fact) in enumerate(results, 1):

        fact_short = fact[:48] + "..." if len(fact) > 51 else fact
        print(f"{i:<3} {name:<40} {expected:<35} {fact_short:<50} {status:<6}")
    print("=" * 100)


if __name__ == "__main__":
    main()