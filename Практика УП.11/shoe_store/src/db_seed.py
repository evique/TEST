import sqlite3
from db_init import get_connection

def seed_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.executemany("INSERT OR IGNORE INTO roles (role_name) VALUES (?);", [
        ("администратор",), ("менеджер",), ("авторизованный пользователь",)
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO users (last_name, first_name, middle_name, login, role_id) VALUES (?, ?, ?, ?, ?);", [
        ("Смирнов", "Алексей", "Викторович", "admin", 1),
        ("Иванова", "Елена", "Петровна", "manager", 2),
        ("Петров", "Дмитрий", None, "user", 3)
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO sizes (size_value) VALUES (?);", [
        (36.0,), (37.5,), (38.0,), (39.0,), (40.0,)
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO products (category, sub_category, manufacturer, product_name, price) VALUES (?, ?, ?, ?, ?);", [
        ("Кроссовки", "Спортивная", "Nike", "Air Force 1", 8999.00),
        ("Ботинки", "Зимняя", "Ecco", "Winter Track", 14999.50),
        ("Туфли", "Классика", "Rendez-Vous", "Classic Office", 7499.00)
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO stock_items (product_id, size_id, quantity_available) VALUES (?, ?, ?);", [
        (1, 1, 10), (1, 3, 5), (2, 4, 8), (3, 2, 12)
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO orders (order_date, user_id) VALUES (?, ?);", [
        ("2026-06-01", 3), ("2026-06-05", 2)
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, ?, ?, ?);", [
        (1, 1, 1, 8999.00), (2, 3, 2, 14999.50)
    ])
    
    conn.commit()
    conn.close()
    print("Тестовые данные успешно добавлены в базу.")

if __name__ == "__main__":
    seed_db()