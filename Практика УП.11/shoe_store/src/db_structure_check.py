import sqlite3

def check_database():
    conn = sqlite3.connect("db/shoe_store.sqlite")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Найденные таблицы ({len(tables)}): {tables}")
    
    for table in tables:
        print(f"\n--- Таблица: {table} ---")
        cursor.execute(f"PRAGMA table_info({table});")
        for col in cursor.fetchall():
            print(f"  Поле: {col[1]}, Тип: {col[2]}, NOT NULL: {col[3]}, PK: {col[5]}")
            
        cursor.execute(f"PRAGMA foreign_key_list({table});")
        fks = cursor.fetchall()
        if fks:
            for fk in fks:
                print(f"  FK: {fk[3]} -> {fk[2]}({fk[4]}) [ON DELETE {fk[5]}]")
                
    conn.close()

if __name__ == "__main__":
    check_database()   