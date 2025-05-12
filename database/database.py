import sqlite3
import os
import logging
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import random
import string
import smtplib
from email.mime.text import MIMEText
import hashlib

# --- Load Environment Variables ---
load_dotenv()

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- DB Path ---
DB_NAME = os.path.join(os.path.dirname(__file__), 'database.db')

# --- Encryption Key ---
FERNET_KEY = os.environ.get('FERNET_KEY')
fernet = Fernet(FERNET_KEY)

# --- Hashing Function ---
def hash_phone(phone):
    return hashlib.sha256(phone.encode()).hexdigest()

# --- Encrypt/Decrypt ---
def encrypt(data):
    return fernet.encrypt(data.encode()).decode()

def decrypt(data):
    return fernet.decrypt(data.encode()).decode()

# --- Initialize DB ---
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            phone_hash TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password TEXT NOT NULL,
            recovery_code TEXT,
            registration_ip TEXT,
            user_agent TEXT,
            failed_attempts INTEGER DEFAULT 0,
            is_blocked INTEGER DEFAULT 0,
            last_failed DATETIME,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        conn.execute('''CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            success INTEGER NOT NULL,
            ip_address TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    logging.info("Database initialized with users and login_logs tables.")

# --- Add User ---
def add_user(name, phone, password, email, ip=None, user_agent=None):
    try:
        hashed_pw = generate_password_hash(password)
        phone_hash = hash_phone(phone)
        encrypted_phone = encrypt(phone)
        encrypted_email = encrypt(email)
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('''INSERT INTO users 
                (name, phone, phone_hash, password, email, registration_ip, user_agent) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (name, encrypted_phone, phone_hash, hashed_pw, encrypted_email, ip, user_agent))
        logging.info(f"User {phone} registered successfully.")
        return True
    except sqlite3.IntegrityError:
        logging.warning(f"User registration failed: {phone} or email may already exist.")
        return False

# --- Get User by Phone ---
def get_user_by_phone(phone):
    phone_hash = hash_phone(phone)
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE phone_hash = ?", (phone_hash,))
        user = cur.fetchone()
        if user and user[10] == 1:
            logging.warning(f"Blocked user {phone} tried to log in.")
            return None
        return user

# --- Increment Failed Attempts ---
def increment_failed_attempts(phone):
    phone_hash = hash_phone(phone)
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT failed_attempts FROM users WHERE phone_hash = ?", (phone_hash,))
        row = cur.fetchone()
        if row:
            attempts = row[0] + 1
            is_blocked = 1 if attempts >= 5 else 0
            cur.execute('''UPDATE users 
                SET failed_attempts = ?, is_blocked = ?, last_failed = CURRENT_TIMESTAMP
                WHERE phone_hash = ?''', (attempts, is_blocked, phone_hash))

# --- Reset Failed Attempts ---
def reset_failed_attempts(phone):
    phone_hash = hash_phone(phone)
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''UPDATE users SET failed_attempts = 0, is_blocked = 0 WHERE phone_hash = ?''', (phone_hash,))

# --- List All Users (decrypted) ---
def list_users():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, phone, email, timestamp FROM users")
        users = cur.fetchall()
        return [
            (uid, name, decrypt(phone), decrypt(email), ts)
            for uid, name, phone, email, ts in users
        ]

# --- Log Login Attempt ---
def log_login_attempt(phone, success, ip_address=None):
    encrypted_phone = encrypt(phone)
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''INSERT INTO login_logs (phone, success, ip_address)
                        VALUES (?, ?, ?)''', (encrypted_phone, int(success), ip_address))
    logging.info(f"Login attempt for {phone} - {'Success' if success else 'Failure'} from {ip_address}")

# --- Set Recovery Code ---
def set_recovery_code(phone, code):
    phone_hash = hash_phone(phone)
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE users SET recovery_code = ? WHERE phone_hash = ?", (code, phone_hash))
        conn.commit()
    logging.info(f"Recovery code set for {phone}")

# --- Get User by Recovery Code ---
def get_user_by_recovery_code(code):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE recovery_code = ?", (code,))
        return cur.fetchone()

# --- Reset Password ---
def reset_password_db(phone, new_password):
    phone_hash = phone
    hashed_pw = generate_password_hash(new_password)
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE users SET password = ?, recovery_code = NULL WHERE phone_hash = ?", (hashed_pw, phone_hash))
    reset_failed_attempts(phone)
    logging.info(f"Password reset for {phone}")

# --- Generate Recovery Code ---
def generate_recovery_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# --- Send Recovery Email ---
def send_recovery_email(email, code):
    try:
        sender = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        msg = MIMEText(f"Your recovery code is: {code}")
        msg["Subject"] = "Password Recovery Code"
        msg["From"] = sender
        msg["To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)

        logging.info(f"Recovery code emailed to {email}")
    except Exception as e:
        logging.error(f"Email sending failed: {e}")

# --- Main Execution ---
if __name__ == '__main__':
    init_db()
    print("Database initiated successfully")
