# db/recurring_income_manager.py

import sqlite3
from datetime import datetime, timedelta
from utils import path_utils

DB_PATH = path_utils.get_secure_db_path(decrypted=True)

def process_recurring_income(current_date: str):
    """
    Insert recurring income entries that are due up to current_date (YYYY-MM-DD).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, amount, source, note, recurrence_interval, last_occurrence
        FROM income
        WHERE is_recurring=1
    """)
    for row in cursor.fetchall():
        income_id, amount, source, note, interval, last_occurrence = row
        if interval is None or not last_occurrence:
            continue
        
        last = datetime.strptime(last_occurrence, "%Y-%m-%d")
        today = datetime.strptime(current_date, "%Y-%m-%d")
        
        next_due = last + timedelta(days=interval)
        inserted = False

        while next_due <= today:
            cursor.execute("""
                INSERT INTO income (amount, date, source, note, is_recurring, recurrence_interval, last_occurrence)
                VALUES (?, ?, ?, ?, 1, ?, ?)
            """, (amount, next_due.strftime("%Y-%m-%d"), source, note, interval, next_due.strftime("%Y-%m-%d")))
            inserted = True
            next_due += timedelta(days=interval)

        if inserted:
            new_last = (next_due - timedelta(days=interval)).strftime("%Y-%m-%d")
            cursor.execute("UPDATE income SET last_occurrence=? WHERE id=?", (new_last, income_id))

    conn.commit()
    conn.close()
