import sqlite3
import os

def get_db_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'shoe_store.sqlite')

def test_triggers():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    print("=== Тестирование триггеров ===\n")
    print("1. Проверка списания остатков...")

    cursor.execute("SELECT stock_item_id, quantity_available FROM stock_items LIMIT 1")
    stock_item = cursor.fetchone()
    
    if stock_item:
        stock_id, old_qty = stock_item
        cursor.execute("INSERT INTO orders (user_id, order_date) VALUES (1, datetime('now'))")
        order_id = cursor.lastrowid
        cursor.execute("INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, ?, 2, 1500)", 
                       (order_id, stock_id))
        
        cursor.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = ?", (stock_id,))
        new_qty = cursor.fetchone()[0]
        
        if new_qty == old_qty - 2:
            print(f"   [OK] Остаток уменьшился с {old_qty} до {new_qty}")
        else:
            print(f"   [ERROR] Остаток не изменился. Было: {old_qty}, стало: {new_qty}")
    else:
        print("   [SKIP] Таблица stock_items пуста.")

    print("\n2. Проверка защиты от удаления пользователя...")
    try:
        cursor.execute("DELETE FROM users WHERE user_id = 1")
        print("   [ERROR] Пользователь удалился, хотя у него есть заказы!")
    except sqlite3.IntegrityError as e:
        print(f"   [OK] Удаление прервано ошибкой: {e}")
    except sqlite3.OperationalError as e:

        if "RAISE" in str(e):
            print(f"   [OK] Удаление прервано триггером: {e}")
        else:
            print(f"   [ERROR] Неожиданная ошибка: {e}")

    print("\n3. Проверка вставки отрицательного количества...")
    try:
        cursor.execute("INSERT INTO stock_items (product_id, quantity_available) VALUES (1, -5)")
        print("   [ERROR] Запись с отрицательным количеством добавилась!")
    except sqlite3.IntegrityError as e:
        print(f"   [OK] Вставка прервана ошибкой: {e}")
    except sqlite3.OperationalError as e:
        if "RAISE" in str(e):
            print(f"   [OK] Вставка прервана триггером: {e}")
        else:
            print(f"   [ERROR] Неожиданная ошибка: {e}")

    print("\n4. Проверка логирования изменения цены...")
    cursor.execute("UPDATE products SET price = price + 10 WHERE product_id = 1")
    cursor.execute("SELECT table_name, operation, old_value, new_value FROM audit_log ORDER BY log_id DESC LIMIT 1")
    log_entry = cursor.fetchone()
    if log_entry and log_entry[0] == 'products' and log_entry[1] == 'UPDATE':
        print(f"   [OK] В лог записано: {log_entry}")
    else:
        print("   [ERROR] Запись в audit_log не найдена.")

    conn.rollback() 
    conn.close()
    print("\n=== Тестирование завершено (изменения откатаны) ===")

if __name__ == "__main__":
    test_triggers()