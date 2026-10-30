import sqlite3

PERMISSIONS = {
    "admin_db": ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"],
    "developer": ["SELECT", "INSERT", "UPDATE"],
    "reader": ["SELECT"]
}

def add_admin_roles(conn):
    roles = [
        ("admin_db", "Полный доступ к базе данных"),
        ("developer", "Разработка и изменение данных"),
        ("reader", "Только чтение данных")
    ]
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)", roles)
    conn.commit()
    print("Роли успешно добавлены или уже существовали.")

def check_permission(conn, user_id, action):
    cursor = conn.cursor()
    cursor.execute("SELECT r.name FROM users u JOIN roles r ON u.role_id = r.id WHERE u.id = ?", (user_id,))
    result = cursor.fetchone()
    
    if not result:
        return False
        
    role_name = result[0]
    
    allowed_actions = PERMISSIONS.get(role_name, [])
    return action.upper() in allowed_actions

def test_permissions(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE login = 'reader_user'") 
    reader_id = cursor.fetchone()
    cursor.execute("SELECT id FROM users WHERE login = 'admin_user'")
    admin_id = cursor.fetchone()
    
    if reader_id:
        can_delete = check_permission(conn, reader_id[0], "DELETE")
        print(f"Пользователь reader может DELETE: {can_delete}")
        
    if admin_id:
        can_delete = check_permission(conn, admin_id[0], "DELETE")
        print(f"Пользователь admin может DELETE: {can_delete}")