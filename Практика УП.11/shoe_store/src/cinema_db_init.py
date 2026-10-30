import os
import sqlite3

DB_PATH = os.path.join("db", "cinema.sqlite")

def create_database(db_path: str = DB_PATH) -> None:
    """Создаёт файл БД и все таблицы. Идемпотентен: можно запускать многократно."""

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
       
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                role_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                role_name TEXT NOT NULL UNIQUE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS genres (
                genre_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                genre_name TEXT NOT NULL UNIQUE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS age_ratings (
                rating_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                rating_code TEXT NOT NULL UNIQUE,
                min_age     INTEGER NOT NULL CHECK (min_age >= 0)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS halls (
                hall_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                hall_name     TEXT NOT NULL UNIQUE,
                rows_count    INTEGER NOT NULL CHECK (rows_count > 0),
                seats_per_row INTEGER NOT NULL CHECK (seats_per_row > 0)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email     TEXT NOT NULL UNIQUE,
                phone     TEXT NOT NULL,
                role_id   INTEGER NOT NULL,
                FOREIGN KEY (role_id) REFERENCES roles(role_id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                movie_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                title        TEXT NOT NULL,
                genre_id     INTEGER NOT NULL,
                duration_min INTEGER NOT NULL CHECK (duration_min > 0),
                rating_id    INTEGER NOT NULL,
                poster_path  TEXT,
                FOREIGN KEY (genre_id)  REFERENCES genres(genre_id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                FOREIGN KEY (rating_id) REFERENCES age_ratings(rating_id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id       INTEGER NOT NULL,
                hall_id        INTEGER NOT NULL,
                start_datetime TEXT NOT NULL,           -- ISO 8601: '2025-06-01 18:30'
                base_price     REAL NOT NULL CHECK (base_price > 0),
                FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                FOREIGN KEY (hall_id)  REFERENCES halls(hall_id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  INTEGER NOT NULL,
                user_id     INTEGER NOT NULL,
                row_num     INTEGER NOT NULL CHECK (row_num > 0),
                seat_num    INTEGER NOT NULL CHECK (seat_num > 0),
                final_price REAL    NOT NULL CHECK (final_price > 0),
                UNIQUE (session_id, row_num, seat_num),
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (user_id)    REFERENCES users(user_id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            );
        """)
    
        conn.commit()
        print(f"[OK] База данных успешно создана: {db_path}")

    except sqlite3.Error as exc:
        conn.rollback()
        print(f"[ERROR] Ошибка при создании БД: {exc}")
        raise
    finally:
        conn.close()

def seed_reference_data(db_path: str = DB_PATH) -> None:
    """Заполняет справочники базовыми значениями (идемпотентно)."""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.executemany(
            "INSERT OR IGNORE INTO roles (role_name) VALUES (?);",
            [("Гость",), ("Клиент",), ("Администратор",)],
        )
       
        cursor.executemany(
            "INSERT OR IGNORE INTO genres (genre_name) VALUES (?);",
            [("Боевик",), ("Комедия",), ("Драма",), ("Фантастика",), ("Ужасы",)],
        )
        
        cursor.executemany(
            "INSERT OR IGNORE INTO age_ratings (rating_code, min_age) VALUES (?, ?);",
            [("0+", 0), ("6+", 6), ("12+", 12), ("16+", 16), ("18+", 18)],
        )
        
        cursor.executemany(
            "INSERT OR IGNORE INTO halls (hall_name, rows_count, seats_per_row) VALUES (?, ?, ?);",
            [("Зал 1", 10, 12), ("Зал 2", 8, 10), ("VIP-зал", 5, 6)],
        )

        conn.commit()
        print("[OK] Справочные данные заполнены.")
    except sqlite3.Error as exc:
        conn.rollback()
        print(f"[ERROR] Ошибка при заполнении справочников: {exc}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()
    seed_reference_data()