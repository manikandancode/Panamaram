# ui/currency_chooser.py

from PySide6.QtWidgets import QDialog, QComboBox, QVBoxLayout, QLabel, QPushButton, QMessageBox
from db.db_manager import set_setting, get_setting

# Only a subset shown here for clarity — use the full list to replace or extend.
official_currencies = [
    ("INR", "₹", "Indian Rupee"),
    ("USD", "$", "US Dollar"),
    ("EUR", "€", "Euro"),
    ("GBP", "£", "British Pound"),
    ("JPY", "¥", "Japanese Yen"),
    ("CNY", "¥", "Chinese Yuan"),
    ("AUD", "A$", "Australian Dollar"),
    ("CAD", "CA$", "Canadian Dollar"),
    ("CHF", "CHF", "Swiss Franc"),
    ("RUB", "₽", "Russian Ruble"),
    ("BRL", "R$", "Brazilian Real"),
    ("ZAR", "R", "South African Rand"),
    ("KRW", "₩", "South Korean Won"),
    ("SGD", "S$", "Singapore Dollar"),
    ("MXN", "$", "Mexican Peso"),
    ("THB", "฿", "Thai Baht"),
    ("AED", "د.إ", "UAE Dirham")
    # Add more from ISO 4217 as needed
]

class CurrencyChooser(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choose Preferred Currency")
        self.setFixedSize(350, 200)

        self.combo = QComboBox()

        # Build dropdown list with code - symbol - name
        for code, symbol, name in official_currencies:
            self.combo.addItem(f"{code} - {symbol} - {name}", symbol)

        current_symbol = get_setting("currency", "₹")
        index = next((i for i, (_, symbol, _) in enumerate(official_currencies) if symbol == current_symbol), 0)
        self.combo.setCurrentIndex(index)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_currency)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select your preferred currency:"))
        layout.addWidget(self.combo)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

    def save_currency(self):
        selected_symbol = self.combo.currentData()
        set_setting("currency", selected_symbol)
        QMessageBox.information(self, "Saved", f"Currency set to {selected_symbol}")
        self.accept()
