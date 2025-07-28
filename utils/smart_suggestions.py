import sqlite3
from datetime import datetime, timedelta

SUGGESTION_CATEGORIES = [
    "Travel or Vacation",
    "Transportation",
    "Shopping",
    "Health and Fitness",
    "Groceries",
    "Electricity Bill",
    "Dining Out",
]

def get_suggestion(db_path):
    """
    Returns a smart suggestion for the Home dashboard, based on selected expense categories.
    """
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        now = datetime.now()
        current_month = now.strftime("%Y-%m")
        previous_month = (now.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

        best_category = None
        best_change = 0
        best_msg = ""

        for cat in SUGGESTION_CATEGORIES:
            # Get total amount for this category in current and previous month
            c.execute("SELECT IFNULL(SUM(amount), 0) FROM expenses WHERE category=? AND substr(date,1,7)=?", (cat, current_month))
            curr = c.fetchone()[0]
            c.execute("SELECT IFNULL(SUM(amount), 0) FROM expenses WHERE category=? AND substr(date,1,7)=?", (cat, previous_month))
            prev = c.fetchone()[0]

            # Only compare if there were any expenses in at least one month
            if prev == 0 and curr == 0:
                continue

            if prev > 0:
                change_pct = (curr - prev) / prev * 100
                if abs(change_pct) > abs(best_change):
                    if change_pct > 20:
                        best_category = cat
                        best_change = change_pct
                        best_msg = f"You spent {change_pct:.0f}% more on {cat} than last month."
                    elif change_pct < -15:
                        best_category = cat
                        best_change = change_pct
                        best_msg = f"{cat} expenses dropped by {-change_pct:.0f}% compared to last month."
            elif prev == 0 and curr > 0:
                # New spending in this category this month
                if curr > abs(best_change):
                    best_category = cat
                    best_change = curr
                    best_msg = f"New {cat} expenses added this month."

        conn.close()

        # Graceful fallback if nothing stands out
        if best_msg:
            return best_msg
        else:
            return "Your spending patterns this month are steady. Keep tracking for more insights!"
    except Exception:
        return "Could not load data for suggestions."
