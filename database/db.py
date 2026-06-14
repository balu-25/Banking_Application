import sqlite3
import hashlib
DB_NAME = "database/bank.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        phone TEXT,
        email TEXT,
        userid TEXT PRIMARY KEY,
        password TEXT,
        balance REAL DEFAULT 1000
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins(
        empid TEXT PRIMARY KEY,
        empname TEXT,
        designation TEXT,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT,
        amount REAL,
        balance REAL,
        function TEXT,
        date TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS loans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT,
        typeofloan TEXT,
        amount REAL,
        interest REAL,
        duration INTEGER,
        total_amount REAL,
        amtpaid REAL DEFAULT 0
    )
    """)
    cur.execute("""
        INSERT OR IGNORE INTO admins
        VALUES (?,?,?,?)
    """, (
        "2005",
        "Balu",
        "Manager",
        hashlib.sha256("admin2005".encode()).hexdigest()
    ))

    conn.commit()
    conn.close()
