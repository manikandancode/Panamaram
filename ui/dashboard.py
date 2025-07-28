import sqlite3
import calendar
from datetime import datetime, timedelta

from PySide6.QtWidgets import (
    QWidget, QLabel, QTabWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QComboBox, QSpinBox, QScrollArea
)
from PySide6.QtCore import Qt, QDate, Signal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from utils import path_utils
from utils.smart_suggestions import get_suggestion
from db.bill_manager import ensure_bill_table, get_unpaid_bills, get_overdue_bills

DB_PATH = path_utils.get_secure_db_path(decrypted=True)

def get_current_month_year():
    today = QDate.currentDate()
    return today.month(), today.year()

class DashboardWidget(QWidget):
    periodChanged = Signal()  # Signal emitted on any period or tab change

    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)

        # Main tab widget
        self.tabs = QTabWidget(self)
        self.tabs.currentChanged.connect(lambda _: self.periodChanged.emit())

        # ==== Home tab ====
        self.home_tab = QWidget()
        home_layout = QVBoxLayout(self.home_tab)
        home_layout.setAlignment(Qt.AlignTop)
        home_layout.setContentsMargins(15, 15, 15, 15)

        # 1. Summary Tiles / Key Stats
        self.summary_tiles_layout = QHBoxLayout()
        self.summary_tiles_layout.setSpacing(15)

        self.tile_spending = self._create_summary_tile("💸 Spending This Month", "#d32f2f")
        self.tile_income = self._create_summary_tile("💰 Income This Month", "#388e3c")
        self.tile_balance = self._create_summary_tile("🧮 Balance", "#1976d2")
        self.tile_saving = self._create_summary_tile("📈 Savings Rate", "#ffa000")

        for tile in [self.tile_spending, self.tile_income, self.tile_balance, self.tile_saving]:
            self.summary_tiles_layout.addWidget(tile)

        home_layout.addLayout(self.summary_tiles_layout)

        # 2. Quick Actions / Shortcut buttons
        self.quick_actions_layout = QHBoxLayout()
        self.quick_actions_layout.setSpacing(10)
        action_definitions = [
            ("Add Expense", self._emit_add_expense),
            ("Add Income", self._emit_add_income),
            ("Show Expenses", self._emit_show_expenses),
            ("Show Income", self._emit_show_income),
            ("Open Reports", self._emit_open_reports),
            ("Change Currency", self._emit_change_currency),
            ("Export Backup", self._emit_export_backup),
            ("Import Backup", self._emit_import_backup),
            ("Add Bill", self._emit_add_bill),
            ("Show Bills", self._emit_show_bills),
        ]
        for label, slot in action_definitions:
            btn = QPushButton(label)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(40)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(slot)
            self.quick_actions_layout.addWidget(btn)
        home_layout.addLayout(self.quick_actions_layout)

        # 3. Smart Suggestions label
        self.suggestion_label = QLabel("")
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setStyleSheet(
            "color:#1976d2; font-weight:bold; font-size:14px; margin-top:12px;"
        )
        home_layout.addWidget(self.suggestion_label)

        # 4. Bill Reminders display section
        self.bills_widget = QLabel()
        self.bills_widget.setWordWrap(True)
        self.bills_widget.setTextFormat(Qt.RichText)
        self.bills_widget.setStyleSheet(
            "border-radius:10px; padding:16px; font-size:15px; margin:14px 0; background-color:#fff8e1; color:#111;"
        )
        self.bills_scroll_area = QScrollArea()
        self.bills_scroll_area.setWidgetResizable(True)
        self.bills_scroll_area.setFixedHeight(180)
        self.bills_scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.bills_scroll_area.setWidget(self.bills_widget)
        home_layout.addWidget(self.bills_scroll_area)

        # 5. Website link at bottom
        self.website_label = QLabel('🌐 Visit Project Website: due.im')
        self.website_label.setTextFormat(Qt.RichText)
        self.website_label.setOpenExternalLinks(True)
        self.website_label.setAlignment(Qt.AlignCenter)
        self.website_label.setStyleSheet("font-size: 13px; margin-top: 25px;")
        home_layout.addWidget(self.website_label)

        # Add Home tab to tabs
        self.tabs.addTab(self.home_tab, "Home")

        # Helper: Tab with internal period controls
        def create_tab_with_period_controls(tab_title):
            tab = QWidget()
            layout = QVBoxLayout(tab)
            layout.setContentsMargins(0, 0, 0, 0)

            label = QLabel(tab_title)
            label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
            label.setStyleSheet("font-weight:bold; font-size:15px;")
            layout.addWidget(label)

            # Period type selector
            period_type_layout = QHBoxLayout()
            period_type_label = QLabel("Select Period Type:")
            period_type_combo = QComboBox()
            period_type_combo.addItems(["Monthly", "Yearly"])
            period_type_layout.addWidget(period_type_label)
            period_type_layout.addWidget(period_type_combo)
            period_type_layout.addStretch()
            layout.addLayout(period_type_layout)

            # Month and Year selectors
            period_controls = QHBoxLayout()
            month_label = QLabel("Month:")
            month_combo = QComboBox()
            for i in range(1, 13):
                month_combo.addItem(calendar.month_name[i], i)
            period_controls.addWidget(month_label)
            period_controls.addWidget(month_combo)

            year_label = QLabel("Year:")
            year_spin = QSpinBox()
            year_spin.setRange(2000, QDate.currentDate().year())
            year_spin.setValue(QDate.currentDate().year())
            period_controls.addWidget(year_label)
            period_controls.addWidget(year_spin)
            period_controls.addStretch(1)
            layout.addLayout(period_controls)

            return (
                tab,
                layout,
                label,
                period_type_combo,
                period_type_label,
                month_combo,
                month_label,
                year_spin,
                year_label,
            )

        (
            self.trend_tab,
            trend_layout,
            self.label_trend,
            self.period_type_trend,
            self.period_type_label_trend,
            self.month_combo_trend,
            self.month_label_trend,
            self.year_spin_trend,
            self.year_label_trend,
        ) = create_tab_with_period_controls("Spending & Income Trend")
        self.trend_canvas = FigureCanvas(Figure(figsize=(7, 5)))
        trend_layout.addWidget(self.trend_canvas)

        (
            self.exp_tab,
            exp_layout,
            self.label_exp,
            self.period_type_exp,
            self.period_type_label_exp,
            self.month_combo_exp,
            self.month_label_exp,
            self.year_spin_exp,
            self.year_label_exp,
        ) = create_tab_with_period_controls("Expense Breakdown")
        self.exp_pie_canvas = FigureCanvas(Figure(figsize=(6, 5)))
        exp_layout.addWidget(self.exp_pie_canvas)

        (
            self.inc_tab,
            inc_layout,
            self.label_inc,
            self.period_type_inc,
            self.period_type_label_inc,
            self.month_combo_inc,
            self.month_label_inc,
            self.year_spin_inc,
            self.year_label_inc,
        ) = create_tab_with_period_controls("Income Breakdown")
        self.inc_pie_canvas = FigureCanvas(Figure(figsize=(6, 5)))
        inc_layout.addWidget(self.inc_pie_canvas)

        (
            self.sav_tab,
            sav_layout,
            self.label_sav,
            self.period_type_sav,
            self.period_type_label_sav,
            self.month_combo_sav,
            self.month_label_sav,
            self.year_spin_sav,
            self.year_label_sav,
        ) = create_tab_with_period_controls("Savings vs Expenses")
        self.sav_bar_canvas = FigureCanvas(Figure(figsize=(7, 5)))
        sav_layout.addWidget(self.sav_bar_canvas)

        (
            self.ratio_tab,
            ratio_layout,
            self.label_ratio,
            self.period_type_ratio,
            self.period_type_label_ratio,
            self.month_combo_ratio,
            self.month_label_ratio,
            self.year_spin_ratio,
            self.year_label_ratio,
        ) = create_tab_with_period_controls("Expense vs Income Ratio")
        self.ratio_pie_canvas = FigureCanvas(Figure(figsize=(7, 5)))
        ratio_layout.addWidget(self.ratio_pie_canvas)

        # Add tabs in order
        self.tabs.addTab(self.exp_tab, "Expense Breakdown")
        self.tabs.addTab(self.inc_tab, "Income Breakdown")
        self.tabs.addTab(self.sav_tab, "Savings vs Expenses")
        self.tabs.addTab(self.ratio_tab, "Expense vs Income Ratio")
        self.tabs.addTab(self.trend_tab, "Spending & Income Trend")

        main_layout.addWidget(self.tabs)

        # Store widgets for sync
        self._period_type_combos = [
            self.period_type_trend,
            self.period_type_exp,
            self.period_type_inc,
            self.period_type_sav,
            self.period_type_ratio,
        ]
        self._month_combos = [
            self.month_combo_trend,
            self.month_combo_exp,
            self.month_combo_inc,
            self.month_combo_sav,
            self.month_combo_ratio,
        ]
        self._year_spins = [
            self.year_spin_trend,
            self.year_spin_exp,
            self.year_spin_inc,
            self.year_spin_sav,
            self.year_spin_ratio,
        ]

        for pt_combo in self._period_type_combos:
            pt_combo.currentIndexChanged.connect(self._on_period_type_combo_changed)
            pt_combo.currentIndexChanged.connect(self._on_any_period_control_changed)
        for mc in self._month_combos:
            mc.currentIndexChanged.connect(self._on_any_period_control_changed)
        for ys in self._year_spins:
            ys.valueChanged.connect(self._on_any_period_control_changed)

        # Default to current month/year
        current_month, current_year = get_current_month_year()
        for pt_combo in self._period_type_combos:
            pt_combo.setCurrentText("Monthly")
        for mc in self._month_combos:
            mc.setCurrentIndex(current_month - 1)
        for ys in self._year_spins:
            ys.setValue(current_year)

        # Currency setup
        self.update_currency()

        # Initial data refresh
        self._sync_all_controls()
        self.periodChanged.connect(self.refresh_charts)
        self.refresh_home_tab()
        self.refresh_charts()

    def update_currency(self):
        """Update the cached currency symbol from settings table."""
        try:
            from db.db_manager import get_setting
            self.currency = get_setting("currency")
            if not self.currency:
                self.currency = "₹"
        except Exception:
            self.currency = "₹"

    def _create_summary_tile(self, title, color):
        tile = QLabel()
        tile.setAlignment(Qt.AlignCenter)
        tile.setWordWrap(True)
        tile.setText(f"{title}\nLoading...")
        tile.setStyleSheet(
            f"""
            background: #f5f5f5;
            border-radius: 12px;
            color: {color};
            font-weight: bold;
            font-size: 16px;
            padding: 20px;
            min-width: 150px;
            """
        )
        return tile

    def refresh_home_tab(self):
        self.update_currency()  # Always update currency before using in tiles
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            now = datetime.now()
            current_month_str = now.strftime("%Y-%m")

            # Current spending this month
            c.execute("SELECT IFNULL(SUM(amount),0) FROM expenses WHERE substr(date,1,7) = ?", (current_month_str,))
            current_spending = c.fetchone()[0] or 0

            # Current income this month
            c.execute("SELECT IFNULL(SUM(amount),0) FROM income WHERE substr(date,1,7) = ?", (current_month_str,))
            current_income = c.fetchone()[0] or 0

            current_balance = current_income - current_spending
            savings_rate = (100 * current_balance / current_income) if current_income > 0 else 0

            self.tile_spending.setText(f"💸 Spending This Month\n{self.currency}{current_spending:,.2f}")
            self.tile_income.setText(f"💰 Income This Month\n{self.currency}{current_income:,.2f}")
            self.tile_balance.setText(f"🧮 Balance\n{self.currency}{current_balance:,.2f}")
            self.tile_saving.setText(f"📈 Savings Rate\n{savings_rate:.1f}%")

            # Smart suggestion
            suggestion_msg = get_suggestion(DB_PATH)
            self.suggestion_label.setText(suggestion_msg)

            # Bill reminders
            ensure_bill_table()
            overdue_bills = get_overdue_bills()
            upcoming_bills = get_unpaid_bills(days_forward=7)
            self.bills_widget.setText(self.generate_bills_html(upcoming_bills, overdue_bills))

            conn.close()
        except Exception as e:
            self.suggestion_label.setText("Could not load data for suggestions.")
            print(f"Error refreshing Home tab: {e}")

    @staticmethod
    def generate_bills_html(upcomings, overdues):
        def format_ddmmyyyy(datestr):
            try:
                dt = datetime.strptime(datestr, "%Y-%m-%d")
                return dt.strftime("%d-%m-%Y")
            except Exception:
                return datestr

        html = ""
        if overdues:
            html += "<b>⏰ Overdue Bills:</b><br>"
            for b in overdues:
                due_str = format_ddmmyyyy(b[3])
                html += f"{b[1]}: {b[2]:.2f} due {due_str}<br>"

        if upcomings:
            html += "<b>📅 Upcoming Bills:</b><br>"
            for b in upcomings:
                due_str = format_ddmmyyyy(b[3])
                html += f"{b[1]}: {b[2]:.2f} due {due_str}<br>"

        if not html:
            html = "No due bills! 🎉"

        return html

    # Quick Action slots (call parent's methods if available)
    def _emit_add_expense(self):
        if self.parent() and hasattr(self.parent(), "open_add_expense"):
            self.parent().open_add_expense()
    def _emit_add_income(self):
        if self.parent() and hasattr(self.parent(), "open_add_income"):
            self.parent().open_add_income()
    def _emit_show_expenses(self):
        if self.parent() and hasattr(self.parent(), "open_expense_window"):
            self.parent().open_expense_window()
    def _emit_show_income(self):
        if self.parent() and hasattr(self.parent(), "open_income_window"):
            self.parent().open_income_window()
    def _emit_open_reports(self):
        if self.parent() and hasattr(self.parent(), "open_reports_window"):
            self.parent().open_reports_window()
    def _emit_change_currency(self):
        if self.parent() and hasattr(self.parent(), "open_currency_dialog"):
            self.parent().open_currency_dialog()
    def _emit_export_backup(self):
        if self.parent() and hasattr(self.parent(), "export_encrypted_backup"):
            self.parent().export_encrypted_backup()
    def _emit_import_backup(self):
        if self.parent() and hasattr(self.parent(), "import_encrypted_backup"):
            self.parent().import_encrypted_backup()
    def _emit_add_bill(self):
        if self.parent() and hasattr(self.parent(), "open_add_bill"):
            self.parent().open_add_bill()
    def _emit_show_bills(self):
        if self.parent() and hasattr(self.parent(), "open_bills_window"):
            self.parent().open_bills_window()

    def _on_any_period_control_changed(self, *args):
        self._sync_all_controls()
        self.periodChanged.emit()
        self.refresh_home_tab()

    def _sync_all_controls(self):
        sender = self.sender()
        if sender in self._period_type_combos:
            txt = sender.currentText()
        else:
            txt = self._period_type_combos[0].currentText()
        for ptc in self._period_type_combos:
            if ptc.currentText() != txt:
                ptc.blockSignals(True)
                ptc.setCurrentText(txt)
                ptc.blockSignals(False)
        monthly_selected = (txt == "Monthly")
        for mc, ml in zip(self._month_combos, [
            self.month_label_trend,
            self.month_label_exp,
            self.month_label_inc,
            self.month_label_sav,
            self.month_label_ratio,
        ]):
            mc.setEnabled(monthly_selected)
            ml.setEnabled(monthly_selected)
        if sender in self._month_combos:
            idx = sender.currentIndex()
        else:
            idx = self._month_combos[0].currentIndex()
        for mc in self._month_combos:
            if mc.currentIndex() != idx:
                mc.blockSignals(True)
                mc.setCurrentIndex(idx)
                mc.blockSignals(False)
        if sender in self._year_spins:
            val = sender.value()
        else:
            val = self._year_spins[0].value()
        for ys in self._year_spins:
            if ys.value() != val:
                ys.blockSignals(True)
                ys.setValue(val)
                ys.blockSignals(False)

    def _on_period_type_combo_changed(self, index):
        sender = self.sender()
        if sender is None:
            return
        curr_text = sender.currentText()
        monthly_selected = (curr_text == "Monthly")
        for mc, ml in zip(self._month_combos, [
            self.month_label_trend,
            self.month_label_exp,
            self.month_label_inc,
            self.month_label_sav,
            self.month_label_ratio,
        ]):
            mc.setEnabled(monthly_selected)
            ml.setEnabled(monthly_selected)
        for ptc in self._period_type_combos:
            if ptc != sender:
                ptc.blockSignals(True)
                ptc.setCurrentText(curr_text)
                ptc.blockSignals(False)
        self.periodChanged.emit()

    def get_selected_period(self):
        period_type = self._period_type_combos[0].currentText()
        year = self.year_spin_trend.value()
        if period_type == "Monthly":
            month = self.month_combo_trend.currentData()
            return "month", f"{year:04d}-{month:02d}"
        else:
            return "year", f"{year:04d}"

    def refresh_charts(self, *args):
        months, expenses, income = self.get_full_timeline_data()
        if not months:
            self.show_empty_message("No data available for Spending & Income Trend", self.trend_canvas)
        else:
            fig = self.trend_canvas.figure
            fig.clear()
            ax = fig.add_subplot(111)
            months_labels = [datetime.strptime(m, "%Y-%m").strftime("%b %Y") for m in months]
            ax.plot(months_labels, expenses, label="Expenses", marker="o", color="red")
            ax.plot(months_labels, income, label="Income", marker="o", color="green")
            ax.set_ylabel("Amount")
            ax.set_xlabel("Month")
            ax.legend()
            fig.tight_layout(pad=0.15)
            self.trend_canvas.draw()

        (
            exp_cats,
            exp_totals,
            inc_cats,
            inc_totals,
            total_expense,
            total_income,
        ) = self.get_period_filtered_data()

        self.draw_pie_chart(exp_cats, exp_totals, "No data available for Expense Breakdown", self.exp_pie_canvas)
        self.draw_pie_chart(inc_cats, inc_totals, "No data available for Income Breakdown", self.inc_pie_canvas)

        fig = self.sav_bar_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        savings = total_income - total_expense
        if total_income == 0 and total_expense == 0:
            self.show_empty_message("No data available for Savings vs Expenses", self.sav_bar_canvas)
        else:
            bars = ax.bar(["Savings", "Expenses"], [max(savings, 0), total_expense], color=["blue", "red"])
            for bar in bars:
                height = bar.get_height()
                ax.annotate(
                    f"{height:,.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                )
            ax.set_ylabel("Amount")
            fig.tight_layout(pad=0.15)
            self.sav_bar_canvas.draw()

        fig = self.ratio_pie_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        if total_income == 0:
            self.show_empty_message("No data available for Expense vs Income Ratio", self.ratio_pie_canvas)
        else:
            ratio = total_expense / total_income if total_income > 0 else 0
            sizes = [total_expense, max(total_income - total_expense, 0)]
            labels = ["Expenses", "Remaining Income"]
            colors = ["red", "green"]
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
            ax.set_title(f"Expense vs Income Ratio: {ratio:.1%}")
            fig.tight_layout(pad=0.15)
            self.ratio_pie_canvas.draw()

    def get_full_timeline_data(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT substr(date,1,7) as month, SUM(amount) FROM expenses GROUP BY month ORDER BY month")
        exp = c.fetchall()
        c.execute("SELECT substr(date,1,7) as month, SUM(amount) FROM income GROUP BY month ORDER BY month")
        inc = c.fetchall()
        conn.close()
        exp_dict = dict(exp)
        inc_dict = dict(inc)
        all_months = sorted(set(exp_dict.keys()) | set(inc_dict.keys()))
        expenses = [exp_dict.get(m, 0) for m in all_months]
        income = [inc_dict.get(m, 0) for m in all_months]
        return all_months, expenses, income

    def get_period_filtered_data(self):
        period_type, period_value = self.get_selected_period()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        if period_type == "month":
            c.execute(
                "SELECT category, SUM(amount) FROM expenses WHERE substr(date,1,7)=? GROUP BY category ORDER BY SUM(amount) DESC",
                (period_value,),
            )
            exp_rows = c.fetchall()
            c.execute(
                "SELECT source, SUM(amount) FROM income WHERE substr(date,1,7)=? GROUP BY source ORDER BY SUM(amount) DESC",
                (period_value,),
            )
            inc_rows = c.fetchall()
            c.execute("SELECT SUM(amount) FROM expenses WHERE substr(date,1,7)=?", (period_value,))
            total_exp = c.fetchone()[0] or 0
            c.execute("SELECT SUM(amount) FROM income WHERE substr(date,1,7)=?", (period_value,))
            total_inc = c.fetchone()[0] or 0
        else:  # year
            c.execute(
                "SELECT category, SUM(amount) FROM expenses WHERE substr(date,1,4)=? GROUP BY category ORDER BY SUM(amount) DESC",
                (period_value,),
            )
            exp_rows = c.fetchall()
            c.execute(
                "SELECT source, SUM(amount) FROM income WHERE substr(date,1,4)=? GROUP BY source ORDER BY SUM(amount) DESC",
                (period_value,),
            )
            inc_rows = c.fetchall()
            c.execute("SELECT SUM(amount) FROM expenses WHERE substr(date,1,4)=?", (period_value,))
            total_exp = c.fetchone()[0] or 0
            c.execute("SELECT SUM(amount) FROM income WHERE substr(date,1,4)=?", (period_value,))
            total_inc = c.fetchone()[0] or 0
        conn.close()
        exp_cats, exp_totals = zip(*exp_rows) if exp_rows else ([], [])
        inc_cats, inc_totals = zip(*inc_rows) if inc_rows else ([], [])
        return exp_cats, exp_totals, inc_cats, inc_totals, total_exp, total_inc

    def draw_pie_chart(self, categories, values, empty_msg, canvas):
        fig = canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        if values and sum(values) > 0:
            ax.pie(values, labels=categories, autopct="%1.1f%%", startangle=140)
            ax.set_title("")
        else:
            self.show_empty_message(empty_msg, canvas)
            return
        fig.tight_layout(pad=0.15)
        canvas.draw()

    def show_empty_message(self, message, canvas):
        fig = canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=13, color="gray")
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout(pad=0.15)
        canvas.draw()
