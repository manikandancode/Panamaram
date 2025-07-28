# ui/expense_form.py

from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton,
    QDateEdit, QSpinBox, QCheckBox, QMessageBox
)
from PySide6.QtCore import QDate
from db.expense_manager import add_expense, update_expense

# Predefined categories (or you can load dynamically)
expense_categories = sorted([
    "Bank Fees or Charges", "Childcare", "Dining Out", "Education", "Electricity Bill",
    "Emergency or Medical", "Entertainment", "Events or Celebrations", "Gas Bill",
    "Gifts and Donations", "Groceries", "Health and Fitness", "Insurance",
    "Internet and Mobile", "Investments", "Loan EMIs", "Miscellaneous",
    "Other Utilities bill", "Personal Care", "Pet Care", "Repairs and Maintenance",
    "Rent or Mortgage", "Sanitation", "Savings and Investments", "Sewage or Drainage Fees",
    "Shopping", "Subscriptions", "Taxes", "Transportation", "Travel or Vacation", "Water Bill"
])

class ExpenseForm(QDialog):
    def __init__(self, edit_data=None, on_save_callback=None):
        super().__init__()
        self.setWindowTitle("Add Expense" if not edit_data else "Edit Expense")
        self.setFixedSize(400, 350)

        self.expense_id = edit_data[0] if edit_data else None
        self.on_save_callback = on_save_callback

        layout = QFormLayout()

        self.amount_input = QLineEdit()

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd-MM-yyyy")
        self.date_input.setDate(QDate.currentDate())

        self.category_input = QComboBox()
        self.category_input.addItems(expense_categories)

        self.note_input = QLineEdit()

        self.recurring_checkbox = QCheckBox("Recurring?")
        self.recur_input = QSpinBox()
        self.recur_input.setRange(1, 365)
        self.recur_input.setSuffix(" days")
        self.recur_input.setEnabled(False)
        self.recurring_checkbox.toggled.connect(self.recur_input.setEnabled)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_expense)

        layout.addRow("Amount*", self.amount_input)
        layout.addRow("Date*", self.date_input)
        layout.addRow("Category*", self.category_input)
        layout.addRow("Note", self.note_input)
        layout.addRow(self.recurring_checkbox)
        layout.addRow("Repeat every", self.recur_input)
        layout.addRow(self.save_btn)
        self.setLayout(layout)

        if edit_data:
            self.load_data(edit_data)

    def load_data(self, data):
        self.amount_input.setText(str(data[1]))
        self.date_input.setDate(QDate.fromString(data[2], "yyyy-MM-dd"))
        idx = self.category_input.findText(data[3])
        if idx != -1:
            self.category_input.setCurrentIndex(idx)
        self.note_input.setText(data[4] or "")
        if data[5]:
            self.recurring_checkbox.setChecked(True)
            self.recur_input.setValue(data[6] or 30)

    def save_expense(self):
        try:
            amount = float(self.amount_input.text().strip())
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")
            return

        date_val = self.date_input.date().toString("yyyy-MM-dd")
        category = self.category_input.currentText().strip()
        if not category:
            QMessageBox.warning(self, "Missing Category", "Please select a category.")
            return

        note = self.note_input.text().strip()[:255]  # Limit length
        is_recurring = int(self.recurring_checkbox.isChecked())
        recurrence = self.recur_input.value() if is_recurring else None

        try:
            if self.expense_id:
                update_expense(self.expense_id,
                               amount=amount,
                               date=date_val,
                               category=category,
                               note=note,
                               is_recurring=is_recurring,
                               recurrence_interval=recurrence)
            else:
                add_expense(amount, date_val, category, note, is_recurring, recurrence)

            if self.on_save_callback:
                self.on_save_callback()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save expense: {e}")
