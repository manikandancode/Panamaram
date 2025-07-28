from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QLabel
)
from PySide6.QtCore import Qt
from ui.expense_form import ExpenseForm
from db.expense_manager import get_expenses_page, count_expenses, delete_expense
from db.db_manager import get_setting

class ExpenseTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Expenses")
        self.resize(900, 550)

        # Pagination parameters
        self.page_size = 20
        self.current_page = 1

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Amount", "Category", "Note", "Recurring", "Actions"]
        )

        # Add Expense button
        self.add_btn = QPushButton("➕ Add Expense")
        self.add_btn.clicked.connect(self.open_add_expense)

        # Pagination controls
        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignCenter)

        self.prev_btn.clicked.connect(self.goto_prev_page)
        self.next_btn.clicked.connect(self.goto_next_page)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.add_btn)
        layout.addWidget(self.table)

        pagination_layout = QHBoxLayout()
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_btn)
        pagination_layout.addStretch(1)

        layout.addLayout(pagination_layout)
        self.setLayout(layout)

        self.refresh_table()

    def refresh_table(self):
        self.table.clearContents()

        # Get total expenses and compute page count
        total_records = count_expenses()
        total_pages = max(1, -(-total_records // self.page_size))  # Ceiling division

        # Clamp current_page
        if self.current_page < 1:
            self.current_page = 1
        if self.current_page > total_pages:
            self.current_page = total_pages

        expenses = get_expenses_page(self.current_page, self.page_size)
        currency = get_setting("currency", "₹")

        self.table.setRowCount(len(expenses))
        for row_idx, exp in enumerate(expenses):
            id, amount, date, category, note, is_recurring, interval = exp[0:7]

            formatted_date = f"{date[8:10]}-{date[5:7]}-{date[0:4]}"

            self.table.setItem(row_idx, 0, QTableWidgetItem(formatted_date))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{currency}{amount:,.2f}"))
            self.table.setItem(row_idx, 2, QTableWidgetItem(category))
            self.table.setItem(row_idx, 3, QTableWidgetItem(note or ""))
            self.table.setItem(row_idx, 4, QTableWidgetItem(f"Yes ({interval} days)" if is_recurring else "No"))

            # Edit / Delete buttons
            btn_edit = QPushButton("✏️ Edit")
            btn_delete = QPushButton("🗑️ Delete")
            btn_edit.clicked.connect(lambda _, data=exp: self.edit_expense(data))
            btn_delete.clicked.connect(lambda _, eid=id: self.delete_expense(eid))

            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0)
            hbox.addWidget(btn_edit)
            hbox.addWidget(btn_delete)

            action_widget = QWidget()
            action_widget.setLayout(hbox)

            self.table.setCellWidget(row_idx, 5, action_widget)

        self.page_label.setText(f"Page {self.current_page} of {total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def open_add_expense(self):
        dialog = ExpenseForm(on_save_callback=self.refresh_table)
        if dialog.exec():
            self.current_page = 1  # reset to first page after add
            self.refresh_table()

    def edit_expense(self, data):
        dialog = ExpenseForm(edit_data=data, on_save_callback=self.refresh_table)
        if dialog.exec():
            self.refresh_table()

    def delete_expense(self, eid):
        confirm = QMessageBox.question(self, "Delete", "Delete this expense?")
        if confirm == QMessageBox.Yes:
            delete_expense(eid)
            # Adjust page if last record removed on last page
            if self.table.rowCount() == 1 and self.current_page > 1:
                self.current_page -= 1
            self.refresh_table()

    def goto_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_table()

    def goto_next_page(self):
        total_records = count_expenses()
        total_pages = max(1, -(-total_records // self.page_size))
        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_table()
