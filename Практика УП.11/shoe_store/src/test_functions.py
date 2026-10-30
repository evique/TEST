from app_functions import (
    calc_discount, pluralize_items, format_full_name, 
    get_client_tier, get_client_loyalty_days
)
import sqlite3
from app_functions import place_order, cancel_order
from datetime import date, timedelta

def test_calc_discount():
    assert calc_discount(1000, 20) == 800.0
    assert calc_discount(1000, 0) == 1000.0
    assert calc_discount(1000, 100) == 0.0
    assert calc_discount(1000, -10) == 1000.0
    assert calc_discount(1000, 150) == 0.0
    assert calc_discount(None, 10) == 0.0
    assert calc_discount(1000, None) == 0.0
    assert calc_discount("1000", "20") == 800.0
    assert calc_discount("abc", 10) == 0.0

def test_pluralize_items():
    assert pluralize_items(1) == "1 товар"
    assert pluralize_items(2) == "2 товара"
    assert pluralize_items(5) == "5 товаров"
    assert pluralize_items(21) == "21 товар"
    assert pluralize_items(22) == "22 товара"
    assert pluralize_items(11) == "11 товаров"
    assert pluralize_items(0) == "0 товаров"
    assert pluralize_items(None) == "0 товаров"
    assert pluralize_items("5") == "5 товаров"

def test_format_full_name():
    assert format_full_name("иванов", "иван", "иванович") == "Иванов И.И."
    assert format_full_name("ПЕТРОВ", "петр", None) == "Петров П."
    assert format_full_name("  сидоров  ", "  сидор  ", "  ") == "Сидоров С."
    assert format_full_name("", "иван", "иванович") == "Аноним"
    assert format_full_name(None, None, None) == "Аноним"

def test_client_tier():
    assert get_client_tier(4999) == "Новичок"
    assert get_client_tier(5000) == "Бронза"
    assert get_client_tier(19999) == "Бронза"
    assert get_client_tier(20000) == "Серебро"
    assert get_client_tier(49999) == "Серебро"
    assert get_client_tier(50000) == "Золото"
    assert get_client_tier(99999) == "Золото"
    assert get_client_tier(100000) == "Платина"
    assert get_client_tier(150000) == "Платина"
    assert get_client_tier(None) == "Без статуса"
    assert get_client_tier(-100) == "Без статуса"

def test_loyalty_days():
    today_str = date.today().strftime("%Y-%m-%d")
    yesterday_str = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    assert get_client_loyalty_days(today_str) == 0
    assert get_client_loyalty_days(yesterday_str) == 1
    assert get_client_loyalty_days(None) == 0
    assert get_client_loyalty_days("invalid") == 0

def setup_in_memory_db():
    """Создает временную БД со структурой для тестов транзакций."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE users (user_id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE sizes (size_id INTEGER PRIMARY KEY, size TEXT);
        CREATE TABLE stock_items (
            stock_item_id INTEGER PRIMARY KEY, 
            product_id INTEGER, 
            size_id INTEGER, 
            quantity_available INTEGER, 
            price REAL
        );
        CREATE TABLE orders (order_id INTEGER PRIMARY KEY, user_id INTEGER, order_date TEXT);
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY, 
            order_id INTEGER, 
            product_id INTEGER, 
            size_id INTEGER, 
            quantity INTEGER, 
            price REAL
        );
    """)

    cursor.execute("INSERT INTO users (user_id, name) VALUES (1, 'Test User')")
    cursor.execute("INSERT INTO products (product_id, name) VALUES (1, 'Sneakers')")
    cursor.execute("INSERT INTO sizes (size_id, size) VALUES (1, '42')")
    cursor.execute("INSERT INTO stock_items (product_id, size_id, quantity_available, price) VALUES (1, 1, 10, 5000)")
    
    conn.commit()
    return conn

def test_place_order_success():
    conn = setup_in_memory_db()
    success = place_order(conn, 1, 1, 1, 2)
    assert success is True
    
    cursor = conn.cursor()
    cursor.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = 1")
    assert cursor.fetchone()[0] == 8  # 10 - 2
    
    cursor.execute("SELECT COUNT(*) FROM orders")
    assert cursor.fetchone()[0] == 1
    conn.close()

def test_place_order_insufficient_stock():
    conn = setup_in_memory_db()
    success = place_order(conn, 1, 1, 1, 20) # Запрашиваем больше, чем есть
    assert success is False
    
    cursor = conn.cursor()
    cursor.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = 1")
    assert cursor.fetchone()[0] == 10
    conn.close()

def test_place_order_invalid_user():
    conn = setup_in_memory_db()
    success = place_order(conn, 999, 1, 1, 1) 
    assert success is False
    conn.close()

def test_cancel_order_success():
    conn = setup_in_memory_db()
    place_order(conn, 1, 1, 1, 3)
    
    cursor = conn.cursor()
    cursor.execute("SELECT order_id FROM orders")
    order_id = cursor.fetchone()[0]

    success = cancel_order(conn, order_id)
    assert success is True
    
    cursor.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = 1")
    assert cursor.fetchone()[0] == 10 
    
    cursor.execute("SELECT COUNT(*) FROM orders")
    assert cursor.fetchone()[0] == 0 
    conn.close()

def test_cancel_order_invalid_id():
    conn = setup_in_memory_db()
    success = cancel_order(conn, 9999)
    assert success is False
    conn.close()

if __name__ == "__main__":
    test_calc_discount()
    test_pluralize_items()
    test_format_full_name()
    test_client_tier()
    test_loyalty_days()
    test_place_order_success()
    test_place_order_insufficient_stock()
    test_place_order_invalid_user()
    test_cancel_order_success()
    test_cancel_order_invalid_id()
    print("Все тесты пройдены успешно.")