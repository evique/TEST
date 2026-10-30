import sqlite3
from pathlib import Path

DB_PATH = Path("db/shoe_store.sqlite")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def drop_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;")
    tables = ["order_items", "orders", "stock_items", "sizes", "products", "users", "roles"]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()

def create_tables():
    conn = get_connection()
    drop_all_tables(conn)
    cursor = conn.cursor()
    
    # 1. Роли
    cursor.execute("""
    CREATE TABLE roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT NOT NULL UNIQUE
    );
    """)
    
    # 2. Размеры
    cursor.execute("""
    CREATE TABLE sizes (
        size_id INTEGER PRIMARY KEY AUTOINCREMENT,
        size_value REAL NOT NULL UNIQUE CHECK (size_value > 20 AND size_value < 50)
    );
    """)
    
    # 3. Пользователи
    cursor.execute("""
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        login TEXT NOT NULL UNIQUE CHECK (length(login) >= 3 AND length(login) <= 20),
        role_id INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT
    );
    """)
    
    # 4. Товары
    cursor.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        sub_category TEXT,
        manufacturer TEXT NOT NULL,
        product_name TEXT NOT NULL CHECK (length(product_name) > 0),
        image_path TEXT,
        composition TEXT,
        description TEXT,
        price REAL NOT NULL CHECK (price > 0 AND price < 1000000)
    );
    """)
    
    # 5. Складские позиции (stock_items)
    cursor.execute("""
    CREATE TABLE stock_items (
        stock_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        size_id INTEGER NOT NULL,
        quantity_available INTEGER NOT NULL DEFAULT 0 CHECK (quantity_available >= 0),
        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
        FOREIGN KEY (size_id) REFERENCES sizes(size_id) ON DELETE RESTRICT
    );
    """)
    
    # 6. Заказы
    cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
    );
    """)
    
    # 7. Состав заказа
    cursor.execute("""
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        stock_item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        price REAL NOT NULL CHECK (price > 0),
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
        FOREIGN KEY (stock_item_id) REFERENCES stock_items(stock_item_id) ON DELETE RESTRICT
    );
    """)
    
    # Создание индексов
    cursor.execute("CREATE INDEX idx_users_role_id ON users(role_id);")
    cursor.execute("CREATE INDEX idx_orders_user_id ON orders(user_id);")
    cursor.execute("CREATE INDEX idx_orders_date ON orders(order_date);")
    cursor.execute("CREATE INDEX idx_products_category ON products(category);")
    cursor.execute("CREATE INDEX idx_stock_product_id ON stock_items(product_id);")
    cursor.execute("CREATE INDEX idx_stock_size_id ON stock_items(size_id);")
    cursor.execute("CREATE INDEX idx_order_items_order_id ON order_items(order_id);")
    cursor.execute("CREATE INDEX idx_order_items_stock_id ON order_items(stock_item_id);")
    
    conn.commit()
    conn.close()
    print("База данных успешно создана и инициализирована.")

if __name__ == "__main__":
    create_tables()