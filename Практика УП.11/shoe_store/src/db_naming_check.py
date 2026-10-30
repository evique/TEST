import sqlite3
import re

def check_name(name):
    errors = []
    if not name[0].isalpha():
        errors.append("Имя должно начинаться с буквы.")
    if not re.match(r"^[a-z][a-z0-9_]*$", name):
        errors.append("Имя должно содержать только строчные латинские буквы, цифры и подчёркивания (snake_case).")
    reserved_words = {"select", "from", "where", "order", "table", "column", "index", "group", "insert", "update", "delete"}
    if name.lower() in reserved_words:
        errors.append("Имя является зарезервированным словом SQL.")
    return errors

def check_database():
    conn = sqlite3.connect("db/shoe_store.sqlite")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    
    print("--- АУДИТ СХЕМЫ ИМЕНОВАНИЯ ---")
    has_errors = False
    
    for (table_name,) in tables:
        t_errors = check_name(table_name)
        if t_errors:
            has_errors = True
            print(f"Ошибка в таблице '{table_name}': {t_errors}")
        else:
            print(f"Таблица '{table_name}' соответствует правилам.")
            
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            col_name = col[1]
            c_errors = check_name(col_name)
            if c_errors:
                has_errors = True
                print(f"  Ошибка в поле '{table_name}.{col_name}': {c_errors}")
            else:
                print(f"  Поле '{col_name}' корректно.")
                
    conn.close()
    if not has_errors:
        print("\nВсе имена таблиц и полей полностью соответствуют требованиям!")

if __name__ == "__main__":
    check_database()