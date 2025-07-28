import sqlite3
from datetime import datetime, timedelta, date
from utils import path_utils

DB_PATH = path_utils.get_secure_db_path(decrypted=True)

def ensure_bill_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            due_date TEXT NOT NULL,
            recurring TEXT,
            notes TEXT,
            paid INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()

def add_bill(name, amount, due_date, recurring, notes):
    ensure_bill_table()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO bills (name, amount, due_date, recurring, notes, paid)
                    VALUES (?, ?, ?, ?, ?, 0)""",
              (name, amount, due_date, recurring, notes))
    conn.commit()
    conn.close()

def update_bill(bill_id, name, amount, due_date, recurring, notes, paid):
    ensure_bill_table()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""UPDATE bills SET name=?, amount=?, due_date=?, recurring=?, notes=?, paid=? WHERE id=?""",
              (name, amount, due_date, recurring, notes, paid, bill_id))
    conn.commit()
    conn.close()

def delete_bill(bill_id):
    ensure_bill_table()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM bills WHERE id=?", (bill_id,))
    conn.commit()
    conn.close()

def get_unpaid_bills(days_forward=30):
    ensure_bill_table()
    today = date.today()
    to_date = today + timedelta(days=days_forward)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, name, amount, due_date, recurring, notes, paid
        FROM bills
        WHERE paid=0 AND due_date >= ? AND due_date <= ?
        ORDER BY due_date ASC
    """, (today.isoformat(), to_date.isoformat()))
    bills = c.fetchall()
    conn.close()
    return bills

def get_overdue_bills():
    ensure_bill_table()
    today = date.today()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, name, amount, due_date, recurring, notes, paid
        FROM bills
        WHERE paid=0 AND due_date < ?
        ORDER BY due_date ASC
    """, (today.isoformat(),))
    bills = c.fetchall()
    conn.close()
    return bills

def get_all_bills():
    ensure_bill_table()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT id, name, amount, due_date, recurring, notes, paid FROM bills ORDER BY due_date ASC""")
    bills = c.fetchall()
    conn.close()
    return bills

def mark_bill_paid(bill_id):
    ensure_bill_table()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE bills SET paid=1 WHERE id=?", (bill_id,))
    c.execute("SELECT due_date, recurring, name, amount, notes FROM bills WHERE id=?", (bill_id,))
    row = c.fetchone()
    if row:
        due_date, recurring, name, amount, notes = row
        if recurring and recurring.lower() in ("monthly", "yearly"):
            next_due = get_next_due_date(due_date, recurring.lower())
            c.execute("""INSERT INTO bills (name, amount, due_date, recurring, notes, paid)
                         VALUES (?, ?, ?, ?, ?, 0)""",
                      (name, amount, next_due, recurring, notes))
    conn.commit()
    conn.close()

def get_next_due_date(current, recurring_type):
    dt = datetime.strptime(current, "%Y-%m-%d")
    if recurring_type == "monthly":
        year, month = dt.year, dt.month + 1
        if month > 12:
            month, year = 1, year + 1
        return dt.replace(year=year, month=month).strftime("%Y-%m-%d")
    elif recurring_type == "yearly":
        return dt.replace(year=dt.year + 1).strftime("%Y-%m-%d")
    return dt.strftime("%Y-%m-%d")
