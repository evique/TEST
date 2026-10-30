## 1. Чем отличается функция от процедуры 
- Функция — это вычислительный инструмент. Её главная задача — принять данные, произвести расчет и обязательно вернуть результат (число, строку или таблицу). Функция работает по принципу «вопрос — ответ». В SQL она вызывается внутри SELECT и, как правило, не должна изменять данные в таблицах (не делает INSERT или UPDATE).

- Процедура — это исполнитель задач. Её цель — выполнить последовательность действий, которые меняют состояние базы данных (например, оформить заказ, списать товар, обновить профиль пользователя). Процедура вызывается командой CALL. Она не обязана возвращать значение (хотя может выводить сообщения), но она управляет транзакциями: если что-то пошло не так, процедура сама откатывает изменения, чтобы не оставить базу в промежуточном, сломанном состоянии.

## 2. Код и результаты выполнения Python-функций (Блок 1)

- Код функций: 

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

## Результаты выполнения (пример вывода скрипта):

- Задание 1.1: Вызов calc_order_total(2500, 2) вернул 5000. Вызов calc_order_total(1000, 0) вернул 0.
- Задание 1.2: Вызов get_category_count(conn, "Кроссовки") вернул 14.
- Задание 1.3: Вызов format_phone("89991234567") вернул +7 (999) 123-45-67. Вызов для строки test вернул исходную строку test.

## 3. Реализация транзакций (откат при ошибке) в процедурах Блока 2

- Транзакции реализованы через стандартный контекст try-except с использованием методов соединения commit() и rollback().

Процедура create_order: Весь код обернут в блок try. Перед началом изменений выполняется проверка остатка. Если товара не хватает, функция сразу возвращает False, и commit() не вызывается. Если на любом этапе (создание заказа, вставка позиции, обновление склада) возникает ошибка, срабатывает блок except. В нем вызывается conn.rollback(), который отменяет все SQL-команды, выполненные с момента последней фиксации, и возвращает базу в исходное состояние. Только если все шаги прошли успешно, вызывается conn.commit().
Процедура update_stock: Здесь используется более жесткий контроль. Перед обновлением записи вычисляется new_qty. Если new_qty < 0, функция принудительно выбрасывает исключение ValueError. Это исключение перехватывается в вызывающей процедуре create_order, что инициирует немедленный откат всей транзакции заказа. Это гарантирует, что в таблице stock_items никогда не появится отрицательное количество товара.

## 4. Код из Блока 3 (SQL для PostgreSQL)

CREATE OR REPLACE FUNCTION calc_total_pg(price NUMERIC, quantity INTEGER)
RETURNS NUMERIC AS $$
BEGIN
    RETURN price * quantity;
END;
$$ LANGUAGE plpgsql;
 
CREATE OR REPLACE PROCEDURE create_order_pg(p_user_id INTEGER, p_stock_item_id INTEGER, p_qty INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    v_order_id INTEGER;
    v_price NUMERIC;
BEGIN

INSERT INTO orders (user_id, order_date) VALUES (p_user_id, NOW()) RETURNING id INTO v_order_id;
    
    SELECT price INTO v_price FROM stock_items WHERE id = p_stock_item_id;
    INSERT INTO order_items (order_id, stock_item_id, quantity, price) 
    VALUES (v_order_id, p_stock_item_id, p_qty, v_price);
    
    -- Обновить stock_items
    UPDATE stock_items 
    SET quantity_available = quantity_available - p_qty 
    WHERE id = p_stock_item_id;
END;
$$;

CREATE OR REPLACE PROCEDURE safe_update_stock(p_stock_item_id INTEGER, p_qty INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    v_current_qty INTEGER;
BEGIN
    SELECT quantity_available INTO v_current_qty FROM stock_items WHERE id = p_stock_item_id;
    
    IF v_current_qty < p_qty THEN
        RAISE NOTICE 'Недостаточно товара на складе! Требуется: %, в наличии: %', p_qty, v_current_qty;
        RETURN;
    END IF;
    
    UPDATE stock_items 
    SET quantity_available = quantity_available - p_qty 
    WHERE id = p_stock_item_id;
    
EXCEPTION
    WHEN others THEN
        RAISE NOTICE 'Произошла непредвиденная ошибка: %', SQLERRM;
END;
$$;