import sqlite3
from utils import path_utils

DB_PATH = path_utils.get_secure_db_path(decrypted=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def add_expense(amount, date, category, note="", is_recurring=0, recurrence_interval=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount, date, category, note, is_recurring, recurrence_interval, last_occurrence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (amount, date, category, note, is_recurring, recurrence_interval, date if is_recurring else None))
    conn.commit()
    conn.close()

def get_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_expenses_page(page=1, page_size=20):
    offset = (page - 1) * page_size
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, amount, date, category, note, is_recurring, recurrence_interval FROM expenses ORDER BY date DESC LIMIT ? OFFSET ?",
        (page_size, offset)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def count_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM expenses")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def update_expense(expense_id, **fields):
    conn = get_connection()
    cursor = conn.cursor()
    columns = ", ".join(f"{key}=?" for key in fields.keys())
    values = list(fields.values()) + [expense_id]
    cursor.execute(f"UPDATE expenses SET {columns} WHERE id=?", values)
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
