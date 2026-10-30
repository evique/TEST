import sqlite3
import shutil
import os
from datetime import datetime

def backup_simple(db_path):
    backup_dir = os.path.join(os.path.dirname(db_path), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}.sqlite")
    
    shutil.copy2(db_path, backup_path)
    print(f"Простой бэкап создан: {backup_path}")
    return backup_path

def backup_safe(conn):
    backup_dir = os.path.join(os.path.dirname(conn.execute("PRAGMA database_list").fetchone()[2]), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    backup_path = os.path.join(backup_dir, f"safe_backup_{timestamp}.sqlite")
    
    with sqlite3.connect(backup_path) as dest_conn:
        conn.backup(dest_conn)
        
    print(f"Безопасный бэкап создан: {backup_path}")
    return backup_path

def check_integrity(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()[0]
    print(f"Результат integrity_check: {result}")
    return result

def restore(backup_path, db_path):
    print(f"Восстанавливаю базу из {backup_path} в {db_path}")
    shutil.copy2(backup_path, db_path)
    print("Восстановление завершено.")

def get_db_stats(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA page_size;")
    page_size = cursor.fetchone()[0]
    
    cursor.execute("PRAGMA page_count;")
    page_count = cursor.fetchone()[0]
    
    total_size = page_size * page_count
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    stats = {
        "page_size": page_size,
        "page_count": page_count,
        "total_size_bytes": total_size,
        "tables": tables
    }
    
    print(f"Статистика БД: {stats}")
    return stats

def clear_old_logs(conn, days=30):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM audit_log WHERE changed_at < date('now', ?)", (f"-{days} days",))
    deleted = cursor.rowcount
    conn.commit()
    print(f"Удалено старых записей из audit_log: {deleted}")