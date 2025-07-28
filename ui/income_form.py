# ui/income_form.py

from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton,
    QDateEdit, QSpinBox, QCheckBox, QMessageBox
)
from PySide6.QtCore import QDate
from db.income_manager import add_income, update_income

income_categories = sorted([
    "App/Web Earnings", "Business Income", "Capital Gains", "Cashback / Rewards",
    "Commission / Bonuses", "Consultancy Fees", "Cryptocurrency Gains", "Dividends",
    "Family Support", "Freelance / Contract Work", "Gifts / Donations Received",
    "Government Benefits / Subsidies", "Insurance Payouts", "Interest Income",
    "Legal Settlements", "Lottery / Contest Winnings", "Miscellaneous Income",
    "Mutual Fund Payouts", "Part-time Job Income", "Pension / Retirement Income",
    "Referral Bonuses", "Refunds / Rebates", "Rental Income", "Royalties",
    "Sale of Assets", "Salary", "Scholarship / Stipend", "Stock Profits",
    "Tax Refunds", "Tips / Gratuity"
])

class IncomeForm(QDialog):
    def __init__(self, edit_data=None, on_save_callback=None):
        super().__init__()
        self.setWindowTitle("Add Income" if not edit_data else "Edit Income")
        self.setFixedSize(400, 350)

        self.income_id = edit_data[0] if edit_data else None
        self.on_save_callback = on_save_callback

        layout = QFormLayout()

        self.amount_input = QLineEdit()

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd-MM-yyyy")
        self.date_input.setDate(QDate.currentDate())

        self.source_input = QComboBox()
        self.source_input.addItems(income_categories)

        self.note_input = QLineEdit()

        self.recurring_checkbox = QCheckBox("Recurring?")
        self.recur_input = QSpinBox()
        self.recur_input.setRange(1, 365)
        self.recur_input.setSuffix(" days")
        self.recur_input.setEnabled(False)
        self.recurring_checkbox.toggled.connect(self.recur_input.setEnabled)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_income)

        layout.addRow("Amount*", self.amount_input)
        layout.addRow("Date*", self.date_input)
        layout.addRow("Source*", self.source_input)
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
        idx = self.source_input.findText(data[3])
        if idx != -1:
            self.source_input.setCurrentIndex(idx)
        self.note_input.setText(data[4] or "")
        if data[5]:
            self.recurring_checkbox.setChecked(True)
            self.recur_input.setValue(data[6] or 30)

    def save_income(self):
        try:
            amount = float(self.amount_input.text().strip())
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")
            return

        date_val = self.date_input.date().toString("yyyy-MM-dd")
        source = self.source_input.currentText().strip()
        if not source:
            QMessageBox.warning(self, "Missing Source", "Please select an income source.")
            return

        note = self.note_input.text().strip()[:255]
        is_recurring = int(self.recurring_checkbox.isChecked())
        recurrence = self.recur_input.value() if is_recurring else None

        try:
            if self.income_id:
                update_income(self.income_id,
                              amount=amount,
                              date=date_val,
                              source=source,
                              note=note,
                              is_recurring=is_recurring,
                              recurrence_interval=recurrence)
            else:
                add_income(amount, date_val, source, note, is_recurring, recurrence)

            if self.on_save_callback:
                self.on_save_callback()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save income: {e}")
