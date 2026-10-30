import sqlite3
from datetime import datetime, date

def calc_discount(price, discount_percent):
    """Расчет цены со скидкой с обработкой None и граничных значений."""
    if price is None or discount_percent is None:
        return 0.0
    
    try:
        price = float(price)
        discount_percent = float(discount_percent)
    except (ValueError, TypeError):
        return 0.0

    if discount_percent < 0:
        discount_percent = 0
    if discount_percent > 100:
        discount_percent = 100
    
    result = price - (price * discount_percent / 100)
    return round(result, 2)

def pluralize_items(count):
    """Склонение слова 'товар' в зависимости от числа."""
    if count is None:
        return "0 товаров"
    
    try:
        count = int(count)
    except (ValueError, TypeError):
        return "0 товаров"

    if 11 <= (count % 100) <= 14:
        return f"{count} товаров"
    
    last_digit = count % 10
    if last_digit == 1:
        return f"{count} товар"
    elif 2 <= last_digit <= 4:
        return f"{count} товара"
    else:
        return f"{count} товаров"

def format_full_name(last, first, middle):
    """Форматирование ФИО в вид 'Фамилия И.О.' с обработкой пустых значений."""
    if not last or not first:
        return "Аноним"

    last = str(last).strip().title()
    first = str(first).strip().title()
    
    if middle and str(middle).strip():
        middle_initial = str(middle).strip()[0].upper() + "."
        return f"{last} {first[0]}.{middle_initial}"
    else:
        return f"{last} {first[0]}."

def get_client_tier(total_spent):
    """Определение уровня лояльности клиента по сумме покупок."""
    if total_spent is None or total_spent < 0:
        return "Без статуса"
    
    try:
        total_spent = float(total_spent)
    except (ValueError, TypeError):
        return "Без статуса"

    if total_spent < 5000:
        return "Новичок"
    elif total_spent < 20000:
        return "Бронза"
    elif total_spent < 50000:
        return "Серебро"
    elif total_spent < 100000:
        return "Золото"
    else:
        return "Платина"

def get_client_loyalty_days(first_order_date_str):
    """Расчет стажа клиента в днях с момента первого заказа."""
    if not first_order_date_str:
        return 0
    
    try:
        first_date = datetime.strptime(first_order_date_str, "%Y-%m-%d").date()
        today = date.today()
        delta = today - first_date
        return delta.days
    except (ValueError, TypeError):
        return 0

def place_order(conn, user_id, product_id, size_id, quantity):
    """
    Создание нового заказа. 
    Возвращает True при успехе, False при любой ошибке.
    """
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            return False

        cursor.execute(
            "SELECT stock_item_id, quantity_available, price FROM stock_items WHERE product_id = ? AND size_id = ?",
            (product_id, size_id)
        )
        stock_item = cursor.fetchone()
        if not stock_item:
            return False
        
        stock_item_id, available_qty, price = stock_item

        if available_qty < quantity:
            return False

        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO orders (user_id, order_date) VALUES (?, ?)",
            (user_id, order_date)
        )
        order_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, size_id, quantity, price) VALUES (?, ?, ?, ?, ?)",
            (order_id, product_id, size_id, quantity, price)
        )

        cursor.execute(
            "UPDATE stock_items SET quantity_available = quantity_available - ? WHERE stock_item_id = ?",
            (quantity, stock_item_id)
        )

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при создании заказа: {e}")
        return False

def cancel_order(conn, order_id):
    """
    Отмена заказа с возвратом товаров на склад.
    Возвращает True при успехе, False при ошибке.
    """
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT order_id FROM orders WHERE order_id = ?", (order_id,))
        if not cursor.fetchone():
            return False

        cursor.execute(
            "SELECT stock_item_id, quantity FROM order_items WHERE order_id = ?",
            (order_id,)
        )
        items = cursor.fetchall()

        for item in items:
            stock_item_id, quantity = item
            cursor.execute(
                "UPDATE stock_items SET quantity_available = quantity_available + ? WHERE stock_item_id = ?",
                (quantity, stock_item_id)
            )

        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при отмене заказа: {e}")
        return False