import sqlite3

def vulnerable_login(conn: sqlite3.Connection, login: str):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE login = '{login}'")
    return cursor.fetchall()

def secure_login(conn: sqlite3.Connection, login: str):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
    return cursor.fetchall()

def demo_injection():
    conn = sqlite3.connect('db/shoe_store.sqlite')
    
    print("--- Демонстрация уязвимости (f-строка) ---")

    result_vuln = vulnerable_login(conn, "' OR '1'='1")
    print(f"Найдено пользователей (уязвимый код): {len(result_vuln)}")
    
    print("\n--- Демонстрация защиты (параметризованный запрос) ---")
    result_secure = secure_login(conn, "' OR '1'='1")
    print(f"Найдено пользователей (защищенный код): {len(result_secure)}")
    
    conn.close() 