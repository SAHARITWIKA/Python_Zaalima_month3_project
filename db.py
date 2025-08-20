import sqlite3
import os

DB_NAME = "data/finance_data.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            category TEXT,
            amount REAL,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def insert_transaction(user_id, type_, category, amount, date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?,?,?,?,?)",
                   (user_id, type_, category, amount, date))
    conn.commit()
    conn.close()

def fetch_transactions(user_id, category=None, start_date=None, end_date=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT * FROM transactions WHERE user_id=?"
    params = [user_id]

    if category:
        query += " AND category=?"
        params.append(category)

    if start_date and end_date:
        query += " AND date BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return rows
