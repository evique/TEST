import sqlite3
import os
from db_init import create_tables, get_connection

def test_constraints():
    if os.path.exists("db/shoe_store.sqlite"):
        os.remove("db/shoe_store.sqlite")
    create_tables()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO roles (role_name) VALUES ('администратор');")
    cursor.execute("INSERT INTO users (last_name, first_name, login, role_id) VALUES ('Иванов', 'Иван', 'admin', 1);")
    
    # 1. Тест UNIQUE на login
    try:
        cursor.execute("INSERT INTO users (last_name, first_name, login, role_id) VALUES ('Петров', 'Петр', 'admin', 1);")
        conn.commit()
        print("Ошибка: UNIQUE на login не сработал!")
    except sqlite3.IntegrityError:
        print("Пройдено: ограничение UNIQUE на login работает.")

    # 2. Тест NOT NULL на last_name
    try:
        cursor.execute("INSERT INTO users (first_name, login, role_id) VALUES ('Сидор', 'sidor', 1);")
        conn.commit()
        print("Ошибка: NOT NULL не сработал!")
    except sqlite3.IntegrityError:
        print("Пройдено: ограничение NOT NULL работает.")

    # 3. Тест CHECK на price
    try:
        cursor.execute("INSERT INTO products (category, manufacturer, product_name, price) VALUES ('Обувь', 'Nike', 'Air', -500);")
        conn.commit()
        print("Ошибка: CHECK на price не сработал!")
    except sqlite3.IntegrityError:
        print("Пройдено: ограничение CHECK на price работает.")

    # 4. Тест ON DELETE RESTRICT
    try:
        cursor.execute("DELETE FROM roles WHERE role_id = 1;")
        conn.commit()
        print("Ошибка: ON DELETE RESTRICT не сработал!")
    except sqlite3.IntegrityError:
        print("Пройдено: стратегия ON DELETE RESTRICT работает.")

    conn.close()

if __name__ == "__main__":
    test_constraints()