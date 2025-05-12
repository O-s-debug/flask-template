import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def add_user(name, phone, password):
    try:
        hashed_pw = generate_password_hash(password)
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("INSERT INTO users (name, phone, password) VALUES (?, ?, ?)", (name, phone, hashed_pw))
            return True
    except sqlite3.IntegrityError:
        return False

def get_user_by_phone(phone):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE phone = ?", (phone,))
        return cur.fetchone()
