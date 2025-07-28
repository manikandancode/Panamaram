from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDoubleSpinBox,
    QComboBox, QDateEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from db.bill_manager import add_bill

class BillForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Bill Reminder")
        self.setFixedWidth(410)
        layout = QVBoxLayout(self)

        # --- Bill Name ---
        name_row = QHBoxLayout()
        name_label = QLabel("Bill Name*:")
        name_label.setMinimumWidth(90)
        self.name_edit = QLineEdit()
        self.name_edit.setMaxLength(32)  # max 32 chars for bill name
        self.name_edit.setPlaceholderText("e.g. Rent, Internet")
        name_row.addWidget(name_label)
        name_row.addWidget(self.name_edit)
        layout.addLayout(name_row)

        # --- Amount ---
        amount_row = QHBoxLayout()
        amount_label = QLabel("Amount*:")
        amount_label.setMinimumWidth(90)
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setMaximum(9999999.99)
        self.amount_edit.setDecimals(2)
        self.amount_edit.setMinimum(0.01)  # must be positive
        self.amount_edit.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.amount_edit.setFixedWidth(135)
        amount_row.addWidget(amount_label)
        amount_row.addWidget(self.amount_edit)
        layout.addLayout(amount_row)

        # --- Due Date ---
        date_row = QHBoxLayout()
        date_label = QLabel("Due Date*:")
        date_label.setMinimumWidth(90)
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        date_row.addWidget(date_label)
        date_row.addWidget(self.date_edit)
        layout.addLayout(date_row)

        # --- Recurring Type ---
        recur_row = QHBoxLayout()
        recur_label = QLabel("Recurring:")
        recur_label.setMinimumWidth(90)
        self.recurring_combo = QComboBox()
        self.recurring_combo.addItems(["None", "Monthly", "Yearly"])
        recur_row.addWidget(recur_label)
        recur_row.addWidget(self.recurring_combo)
        layout.addLayout(recur_row)

        # --- Notes (single-line input to match Add Expense) ---
        notes_row = QHBoxLayout()
        notes_label = QLabel("Notes:")
        notes_label.setMinimumWidth(90)
        self.notes_edit = QLineEdit()
        self.notes_edit.setMaxLength(64)  # short notes
        self.notes_edit.setPlaceholderText("Optional")
        notes_row.addWidget(notes_label)
        notes_row.addWidget(self.notes_edit)
        layout.addLayout(notes_row)

        # --- Buttons ---
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save)
        btn_row.addWidget(self.save_btn)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def save(self):
        name = self.name_edit.text().strip()[:32]
        amount = round(self.amount_edit.value(), 2)
        due_date_qt = self.date_edit.date()
        due_date = due_date_qt.toString("yyyy-MM-dd")
        recurring = self.recurring_combo.currentText()
        notes = self.notes_edit.text().strip()[:64]

        if not name:
            QMessageBox.warning(self, "Validation Error", "Bill Name is required.")
            self.name_edit.setFocus()
            return

        if amount <= 0:
            QMessageBox.warning(self, "Validation Error", "Amount must be positive.")
            self.amount_edit.setFocus()
            return

        if not due_date_qt.isValid():
            QMessageBox.warning(self, "Validation Error", "A valid Due Date is required.")
            self.date_edit.setFocus()
            return

        # Add the bill to DB
        add_bill(
            name,
            amount,
            due_date,
            None if recurring == "None" else recurring.lower(),
            notes
        )
        self.accept()
