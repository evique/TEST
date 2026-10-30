import hashlib
import sqlite3
from datetime import datetime

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(conn: sqlite3.Connection, login: str, password: str) -> bool:
    password_hash = hash_password(password)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (login, password_hash) VALUES (?, ?)", 
            (login, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def check_password(conn: sqlite3.Connection, login: str, password: str) -> bool:
    password_hash = hash_password(password)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE login = ?", (login,))
    result = cursor.fetchone()
    
    status = 'отказ'
    if result and result[0] == password_hash:
        status = 'успех'

    cursor.execute(
        "INSERT INTO login_audit (login, status, login_time) VALUES (?, ?, ?)",
        (login, status, datetime.now().isoformat())
    )
    conn.commit()
     
    return status == 'успех'