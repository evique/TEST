import os
import sqlite3


DB_PATH = os.path.join("db", "cinema.sqlite")


def check_structure(db_path: str = DB_PATH) -> None:
    if not os.path.exists(db_path):
        print(f"[ERROR] Файл БД не найден: {db_path}. Сначала запустите cinema_db_init.py")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """)
        tables = [row[0] for row in cursor.fetchall()]

        print("=" * 70)
        print(f"База данных: {db_path}")
        print(f"Найдено таблиц: {len(tables)}")
        print("=" * 70)

        for table in tables:
            print(f"\n--- Таблица: {table} ---")
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
           
            print(f"{'Поле':<20} {'Тип':<10} {'NOT NULL':<10} {'PK':<5}")
            print("-" * 50)
            for col in columns:
                cid, name, ctype, notnull, dflt, pk = col
                print(f"{name:<20} {ctype:<10} {('да' if notnull else 'нет'):<10} {('да' if pk else 'нет'):<5}")

            cursor.execute(f"PRAGMA foreign_key_list({table});")
            fks = cursor.fetchall()
            if fks:
                print("  Внешние ключи:")
                for fk in fks:

                    _, _, ref_table, from_col, to_col, on_upd, on_del, _ = fk
                    print(f"    {from_col} -> {ref_table}.{to_col} "
                          f"(ON UPDATE {on_upd}, ON DELETE {on_del})")
            else:
                print("  Внешние ключи: нет")

        
        cursor.execute("PRAGMA foreign_key_check;")
        violations = cursor.fetchall()
        print("\n" + "=" * 70)
        if violations:
            print(f"[WARN] Нарушения внешних ключей: {violations}")
        else:
            print("[OK] Нарушений ссылочной целостности не обнаружено.")
        print("=" * 70)

    finally:
        conn.close()


if __name__ == "__main__":
    check_structure()