import sqlite3
from datetime import datetime

def calc_order_total(price, quantity):

    if quantity <= 0:
        return 0
    return price * quantity

def get_category_count(conn, category_name):
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products WHERE category = ?", (category_name,))
    return cursor.fetchone()[0]

def format_phone(phone):
    
    if not isinstance(phone, str):
        return phone
    
    digits = ''.join(filter(str.isdigit, phone))
    
    if len(digits) == 11 and digits.startswith('8'):
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"
    elif len(digits) == 10:
        return f"+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}"
    else:
        return phone

def create_order(conn, user_id, stock_item_id, quantity):
   
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT quantity_available FROM stock_items WHERE id = ?", (stock_item_id,))
        result = cursor.fetchone()
        
        if not result:
            print(f"Ошибка: Товар с ID {stock_item_id} не найден на складе.")
            return False
            
        available = result[0]
        if available < quantity:
            print(f"Ошибка: Недостаточно товара на складе (есть {available}, нужно {quantity}).")
            return False
            
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO orders (user_id, order_date) VALUES (?, ?)",
            (user_id, current_date)
        )
        order_id = cursor.lastrowid

        cursor.execute("SELECT price FROM stock_items WHERE id = ?", (stock_item_id,))
        price = cursor.fetchone()[0]
        
        cursor.execute(
            "INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, stock_item_id, quantity, price)
        )
        
        update_stock(conn, stock_item_id, quantity)
        

        conn.commit()
        print(f"Заказ #{order_id} успешно создан.")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Ошибка транзакции: {e}")
        return False

def update_stock(conn, stock_item_id, quantity_sold):

    cursor = conn.cursor()
    cursor.execute("SELECT quantity_available FROM stock_items WHERE id = ?", (stock_item_id,))
    current_qty = cursor.fetchone()[0]
    
    new_qty = current_qty - quantity_sold
    
    if new_qty < 0:
        raise ValueError("Остаток не может быть отрицательным. Транзакция прервана.")
        
    cursor.execute(
        "UPDATE stock_items SET quantity_available = ? WHERE id = ?",
        (new_qty, stock_item_id)
    )

def get_sales_report(conn, start_date, end_date):

    cursor = conn.cursor()
    query = """
    SELECT SUM(oi.quantity * oi.price) as total_revenue
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    WHERE o.order_date BETWEEN ? AND ?
    """
    cursor.execute(query, (start_date, end_date))
    revenue = cursor.fetchone()[0]
    
    if revenue is None:
        revenue = 0
        
    return f"С {start_date} по {end_date} продано товаров на сумму {revenue:.2f} руб."

# Пример регистрации функций в SQLite (для справки, обычно делается в основном скрипте)
# conn.create_function("calculate_total", 2, calc_order_total)
# conn.create_function("count_in_category", 1, get_category_count)
# conn.create_function("format_phone_func", 1, format_phone)

