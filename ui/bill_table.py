from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QWidget
)
from PySide6.QtCore import Qt
from datetime import datetime, date
from db.bill_manager import get_all_bills, mark_bill_paid, delete_bill
from ui.bill_form import BillForm

def format_ddmmyyyy(datestr):
    try:
        dt = datetime.strptime(datestr, "%Y-%m-%d")
        return dt.strftime("%d-%m-%Y")
    except Exception:
        return datestr

class BillTable(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bills & Reminders")
        self.setMinimumSize(750, 380)

        layout = QVBoxLayout(self)

        # Add Bill button at the top
        topbar = QHBoxLayout()
        self.add_btn = QPushButton("Add Bill")
        self.add_btn.clicked.connect(self.add_bill)
        topbar.addStretch(1)
        topbar.addWidget(self.add_btn)
        layout.addLayout(topbar)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.load()

    def showEvent(self, event):
        self.load()
        if self.parent() and hasattr(self.parent(), "dashboard"):
            self.parent().dashboard.refresh_home_tab()
        super().showEvent(event)

    def load(self):
        bills = get_all_bills()
        headers = ["Name", "Amount", "Due Date", "Recurring", "Notes", "Paid", "Actions"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(bills))
        for i, bill in enumerate(bills):
            # bill columns: id, name, amount, due_date, recurring, notes, paid
            self.table.setItem(i, 0, QTableWidgetItem(str(bill[1])))
            self.table.setItem(i, 1, QTableWidgetItem(f"{bill[2]:.2f}"))
            self.table.setItem(i, 2, QTableWidgetItem(format_ddmmyyyy(str(bill[3]))))
            self.table.setItem(i, 3, QTableWidgetItem(str(bill[4]) if bill[4] else ""))
            self.table.setItem(i, 4, QTableWidgetItem(str(bill[5]) if bill[5] else ""))
            self.table.setItem(i, 5, QTableWidgetItem("Yes" if bill[6] == 1 else "No"))

            # Per-row Mark Paid/Delete buttons
            button_widget = QWidget()
            btn_layout = QHBoxLayout(button_widget)
            btn_layout.setContentsMargins(1, 1, 1, 1)

            pay_btn = QPushButton("Mark Paid")
            pay_btn.setEnabled(not bill[6])
            # Use lambda with default arg to capture bill_id
            pay_btn.clicked.connect(lambda _, bid=bill[0]: self.mark_paid(bid))

            del_btn = QPushButton("Delete")
            del_btn.clicked.connect(lambda _, bid=bill[0]: self.delete(bid))

            btn_layout.addWidget(pay_btn)
            btn_layout.addWidget(del_btn)
            btn_layout.addStretch(1)
            button_widget.setLayout(btn_layout)
            self.table.setCellWidget(i, 6, button_widget)

            # Highlight overdue bills (unpaid, due date before today)
            try:
                dt = date.fromisoformat(bill[3])
                if bill[6] == 0 and dt < date.today():
                    for j in range(len(headers)-1):  # all columns except actions
                        item = self.table.item(i, j)
                        if item:
                            item.setBackground(Qt.red)
            except Exception:
                pass  # silently ignore bad date formats

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def add_bill(self):
        dlg = BillForm(self)
        if dlg.exec():
            self.load()
            if self.parent() and hasattr(self.parent(), "dashboard"):
                self.parent().dashboard.refresh_home_tab()

    def mark_paid(self, bill_id):
        mark_bill_paid(bill_id)
        QMessageBox.information(self, "Paid", "Marked bill as paid. If recurring, next instance scheduled.")
        self.load()
        if self.parent() and hasattr(self.parent(), "dashboard"):
            self.parent().dashboard.refresh_home_tab()

    def delete(self, bill_id):
        if QMessageBox.question(self, "Delete?", "Are you sure you want to delete this reminder?") != QMessageBox.Yes:
            return
        delete_bill(bill_id)
        self.load()
        if self.parent() and hasattr(self.parent(), "dashboard"):
            self.parent().dashboard.refresh_home_tab()
