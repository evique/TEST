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
    
    UPDATE stock_items 
    SET quantity_available = quantity_available - p_qty 
    WHERE id = p_stock_item_id;
END;
$$;

CREATE OR PROCEDURE safe_update_stock(p_stock_item_id INTEGER, p_qty INTEGER)
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
