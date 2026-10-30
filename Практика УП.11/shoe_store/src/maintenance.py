from backup_restore import backup_safe, check_integrity, get_db_stats, clear_old_logs

def run_maintenance(conn):
    print("=== Запуск обслуживания базы данных ===")
    
    integrity = check_integrity(conn)
    if integrity != "ok":
        print("ОШИБКА: База данных повреждена! Бэкап не выполняется.")
        return
        
    backup_safe(conn)
    
    get_db_stats(conn)
    
    clear_old_logs(conn, days=30)

    print("=== Обслуживание завершено успешно ===") 