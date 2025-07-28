# db/recurring_manager.py

import sqlite3
from datetime import datetime, timedelta
from utils import path_utils

DB_PATH = path_utils.get_secure_db_path(decrypted=True)

def process_recurring_expenses(current_date: str):
    """
    Auto-generate recurring expenses up to the given date (YYYY-MM-DD).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, note, recurrence_interval, last_occurrence
        FROM expenses
        WHERE is_recurring=1
    """)
    
    for row in cursor.fetchall():
        expense_id, amount, category, note, interval, last_occurrence = row
        
        if interval is None or not last_occurrence:
            continue
        
        last = datetime.strptime(last_occurrence, "%Y-%m-%d")
        today = datetime.strptime(current_date, "%Y-%m-%d")

        while (last + timedelta(days=interval)) <= today:
            last += timedelta(days=interval)
            cursor.execute("""
                INSERT INTO expenses (amount, date, category, note, is_recurring, recurrence_interval, last_occurrence)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                amount,
                last.strftime("%Y-%m-%d"),
                category,
                note,
                1,
                interval,
                last.strftime("%Y-%m-%d")
            ))

            # Update master recurring expense's last_occurrence
            cursor.execute("UPDATE expenses SET last_occurrence=? WHERE id=?", (last.strftime("%Y-%m-%d"), expense_id))

    conn.commit()
    conn.close()
