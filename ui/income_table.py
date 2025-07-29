from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QLabel, QWidget as QWidget_Container
)
from PySide6.QtCore import Qt, Signal
from datetime import datetime

from ui.income_form import IncomeForm
from db.income_manager import get_income_page, count_income, delete_income
from db.db_manager import get_setting

def format_ddmmyyyy(datestr):
    try:
        dt = datetime.strptime(datestr, "%Y-%m-%d")
        return dt.strftime("%d-%m-%Y")
    except Exception:
        return datestr

class IncomeTable(QWidget):
    dataChanged = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Income")
        self.resize(900, 550)
        self.page_size = 20
        self.current_page = 1
        self.currency = get_setting("currency", "₹")

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Amount", "Source", "Note", "Recurring", "Actions"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.add_btn = QPushButton("➕ Add Income")
        self.add_btn.clicked.connect(self.open_add_income)

        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignCenter)

        self.prev_btn.clicked.connect(self.goto_prev_page)
        self.next_btn.clicked.connect(self.goto_next_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.add_btn)
        main_layout.addWidget(self.table)
        pagination_layout = QHBoxLayout()
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_btn)
        pagination_layout.addStretch(1)
        main_layout.addLayout(pagination_layout)
        self.setLayout(main_layout)

        self.refresh_table()

    def update_currency(self):
        self.currency = get_setting("currency", "₹")

    def refresh_table(self):
        self.update_currency()
        self.table.clearContents()
        total_records = count_income()
        total_pages = max(1, -(-total_records // self.page_size))
        if self.current_page < 1:
            self.current_page = 1
        if self.current_page > total_pages:
            self.current_page = total_pages
        incomes = get_income_page(self.current_page, self.page_size)
        self.table.setRowCount(len(incomes))
        for row_idx, income in enumerate(incomes):
            income_id = income[0]
            amount = income[1]
            inc_date = income[2]
            source = income[3]
            note = income[4] or ""
            is_recurring = income[5]
            interval = income[6]
            self.table.setItem(row_idx, 0, QTableWidgetItem(format_ddmmyyyy(inc_date)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{self.currency}{amount:,.2f}"))
            self.table.setItem(row_idx, 2, QTableWidgetItem(source))
            self.table.setItem(row_idx, 3, QTableWidgetItem(note))
            self.table.setItem(
                row_idx,
                4,
                QTableWidgetItem(f"Yes ({interval} days)" if is_recurring else "No")
            )
            edit_btn = QPushButton("✏️ Edit")
            delete_btn = QPushButton("🗑️ Delete")
            edit_btn.clicked.connect(lambda _, inc=income: self.edit_income(inc))
            delete_btn.clicked.connect(lambda _, eid=income_id: self.delete_income(eid))
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch(1)
            action_widget = QWidget_Container()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row_idx, 5, action_widget)
        self.page_label.setText(f"Page {self.current_page} of {total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def open_add_income(self):
        dialog = IncomeForm(on_save_callback=self.refresh_table)
        if dialog.exec():
            self.current_page = 1
            self.refresh_table()
            self.dataChanged.emit()

    def edit_income(self, income_data):
        dialog = IncomeForm(edit_data=income_data, on_save_callback=self.refresh_table)
        if dialog.exec():
            self.refresh_table()
            self.dataChanged.emit()

    def delete_income(self, income_id):
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this income record?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            delete_income(income_id)
            if self.table.rowCount() == 1 and self.current_page > 1:
                self.current_page -= 1
            self.refresh_table()
            self.dataChanged.emit()

    def goto_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_table()

    def goto_next_page(self):
        total_records = count_income()
        total_pages = max(1, -(-total_records // self.page_size))
        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_table()
