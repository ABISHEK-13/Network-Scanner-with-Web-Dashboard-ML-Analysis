import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

DB_FILE = 'scanner.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY,
        target TEXT NOT NULL,
        scan_type TEXT,
        results TEXT,
        analysis TEXT,
        anomalies TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()

def register_user(username, password):
    password_hash = generate_password_hash(password)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False 
    conn.close()
    return True

def verify_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user[1], password):
        return user[0] 
    return None

def is_logged_in():
    return 'user_id' in session

def get_logged_in_user():
    if is_logged_in():
        return session.get('user_id')
    return None

def login_user(user_id):
    session['user_id'] = user_id

def logout_user():
    session.pop('user_id', None)
