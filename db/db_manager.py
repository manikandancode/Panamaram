# db/db_manager.py

import sqlite3
from utils import path_utils

# Get decrypted database path from platform-specific secure directory
DB_PATH = path_utils.get_secure_db_path(decrypted=True)

def get_connection():
    """Return a new SQLite database connection."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Create all required database tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Table: app lock password (hashed)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth (
            id INTEGER PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)

    # Table: application settings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    # Table: expenses (with recurring support)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            is_recurring INTEGER DEFAULT 0,  -- 1 = recurring
            recurrence_interval INTEGER,     -- in days
            last_occurrence TEXT
        )
    """)

    # ✅ New table: income (supports recurring too)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            source TEXT NOT NULL,
            note TEXT,
            is_recurring INTEGER DEFAULT 0,  -- 1 = recurring
            recurrence_interval INTEGER,     -- in days
            last_occurrence TEXT
        )
    """)

    conn.commit()
    conn.close()

# ----------------------------------------------
#                App Settings (Key-Value)
# ----------------------------------------------

def set_setting(key: str, value: str):
    """
    Insert or update an application-level setting in the 'settings' table.
    Arguments:
        key (str):     The setting name
        value (str):   The setting value
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO settings (key, value)
        VALUES (?, ?)
        ON CONFLICT (key) DO UPDATE SET value = excluded.value
    """, (key, value))
    conn.commit()
    conn.close()

def get_setting(key: str, default=None):
    """
    Retrieve a setting's value by key.
    Returns default if the key does not exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ? LIMIT 1", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default
