# db/income_manager.py

import sqlite3
from utils import path_utils

DB_PATH = path_utils.get_secure_db_path(decrypted=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def add_income(amount, date, source, note="", is_recurring=0, recurrence_interval=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO income (amount, date, source, note, is_recurring, recurrence_interval, last_occurrence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (amount, date, source, note, is_recurring, recurrence_interval, date if is_recurring else None),
    )
    conn.commit()
    conn.close()


def get_all_income():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM income ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_income_page(page=1, page_size=20):
    offset = (page - 1) * page_size
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, amount, date, source, note, is_recurring, recurrence_interval
        FROM income
        ORDER BY date DESC
        LIMIT ? OFFSET ?
        """,
        (page_size, offset),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def count_income():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM income")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def update_income(income_id, **fields):
    keys = ", ".join(f"{k}=?" for k in fields.keys())
    values = list(fields.values()) + [income_id]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE income SET {keys} WHERE id=?", values)
    conn.commit()
    conn.close()


def delete_income(income_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM income WHERE id=?", (income_id,))
    conn.commit()
    conn.close()
