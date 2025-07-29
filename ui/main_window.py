import os
import sys
import shutil

from PySide6.QtWidgets import (
    QMainWindow, QMenuBar, QMenu, QFileDialog,
    QMessageBox
)
from PySide6.QtGui import QAction, QIcon

from ui.dashboard import DashboardWidget
from ui.expense_table import ExpenseTable
from ui.income_table import IncomeTable
from ui.expense_form import ExpenseForm
from ui.income_form import IncomeForm
from ui.currency_chooser import CurrencyChooser

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panamaram - Personal Finance Expense Tracker")
        self.resize(1100, 680)

        # Set application icon depending on OS
        base_dir = os.path.dirname(os.path.dirname(__file__))
        assets_dir = os.path.join(base_dir, "assets")
        icon_path = os.path.join(assets_dir, "icon.ico" if sys.platform.startswith("win") else "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Initialize child windows as None (for single window instances)
        self.expense_window = None
        self.income_window = None
        self.report_window = None
        self.bills_window = None

        # Main dashboard widget setup
        self.dashboard = DashboardWidget()
        self.setCentralWidget(self.dashboard)

        # Set up menus
        self._setup_menubar()

    def refresh_dashboard_home_tiles(self):
        """Refresh the summary tiles and home data on the dashboard."""
        self.dashboard.refresh_home_tab()

    def _setup_menubar(self):
        menu_bar = self.menuBar()

        # ----------- File Menu -----------
        file_menu = QMenu("File", self)

        add_expense_action = QAction("Add Expense", self)
        add_expense_action.triggered.connect(self.open_add_expense)
        file_menu.addAction(add_expense_action)

        add_income_action = QAction("Add Income", self)
        add_income_action.triggered.connect(self.open_add_income)
        file_menu.addAction(add_income_action)

        add_bill_action = QAction("Add Bill Reminder", self)
        add_bill_action.triggered.connect(self.open_add_bill)
        file_menu.addAction(add_bill_action)
        file_menu.addSeparator()

        export_backup_action = QAction("Export Backup", self)
        export_backup_action.setToolTip("Backup encrypted database file (.aes) to a safe location")
        export_backup_action.triggered.connect(self.export_encrypted_backup)
        file_menu.addAction(export_backup_action)

        import_backup_action = QAction("Import Backup", self)
        import_backup_action.setToolTip("Restore encrypted database file (.aes) from backup, overwriting current data")
        import_backup_action.triggered.connect(self.import_encrypted_backup)
        file_menu.addAction(import_backup_action)
        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        menu_bar.addMenu(file_menu)

        # ----------- View Menu -----------
        view_menu = QMenu("View", self)

        show_expense_action = QAction("Show Expenses", self)
        show_expense_action.triggered.connect(self.open_expense_window)
        view_menu.addAction(show_expense_action)

        show_income_action = QAction("Show Income", self)
        show_income_action.triggered.connect(self.open_income_window)
        view_menu.addAction(show_income_action)

        show_bills_action = QAction("Show Bills", self)
        show_bills_action.triggered.connect(self.open_bills_window)
        view_menu.addAction(show_bills_action)

        show_report_action = QAction("Reports", self)
        show_report_action.triggered.connect(self.open_reports_window)
        view_menu.addAction(show_report_action)

        menu_bar.addMenu(view_menu)

        # ----------- Settings Menu -----------
        settings_menu = QMenu("Settings", self)
        currency_action = QAction("Change Currency", self)
        currency_action.triggered.connect(self.open_currency_dialog)
        settings_menu.addAction(currency_action)
        menu_bar.addMenu(settings_menu)

        # ----------- Help Menu -----------
        help_menu = QMenu("Help", self)
        license_action = QAction("License", self)
        license_action.triggered.connect(self.show_license_dialog)
        help_menu.addAction(license_action)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        menu_bar.addMenu(help_menu)

        # ----------- Optional Refresh Dashboard action -----------
        refresh_action = QAction("Refresh Dashboard", self)
        refresh_action.triggered.connect(self.dashboard.refresh_charts)
        menu_bar.addAction(refresh_action)

    # ==== File Menu Actions ====

    def open_add_expense(self):
        dialog = ExpenseForm()
        if dialog.exec():
            self.refresh_dashboard_home_tiles()
            self.dashboard.refresh_charts()
            if self.expense_window:
                self.expense_window.refresh_table()

    def open_add_income(self):
        dialog = IncomeForm()
        if dialog.exec():
            self.refresh_dashboard_home_tiles()
            self.dashboard.refresh_charts()
            if self.income_window:
                self.income_window.refresh_table()

    def open_add_bill(self):
        try:
            from ui.bill_form import BillForm
        except ImportError:
            QMessageBox.warning(self, "Error", "Bill Form not found or not implemented yet.")
            return
        dialog = BillForm()
        if dialog.exec():
            self.refresh_dashboard_home_tiles()
            self.dashboard.refresh_charts()

    # ==== View Menu Actions ====

    def open_expense_window(self):
        if self.expense_window is None:
            self.expense_window = ExpenseTable()
            self.expense_window.dataChanged.connect(self.refresh_dashboard_home_tiles)
            self.expense_window.dataChanged.connect(self.dashboard.refresh_charts)
        self.expense_window.show()
        self.expense_window.raise_()
        self.expense_window.activateWindow()

    def open_income_window(self):
        if self.income_window is None:
            self.income_window = IncomeTable()
            self.income_window.dataChanged.connect(self.refresh_dashboard_home_tiles)
            self.income_window.dataChanged.connect(self.dashboard.refresh_charts)
            self.dashboard._emit_add_income = self._wrapped_add_income_with_refresh
        self.income_window.show()
        self.income_window.raise_()
        self.income_window.activateWindow()

    def _wrapped_add_income_with_refresh(self):
        dialog = IncomeForm()
        if dialog.exec():
            self.refresh_dashboard_home_tiles()
            self.dashboard.refresh_charts()
            if self.income_window:
                self.income_window.refresh_table()

    def open_reports_window(self):
        if self.report_window is None:
            try:
                from ui.reports import ReportWindow
                self.report_window = ReportWindow()
            except ImportError:
                QMessageBox.warning(self, "Error", "Reports window not found or not implemented yet.")
                return
        self.report_window.show()
        self.report_window.raise_()
        self.report_window.activateWindow()

    def open_bills_window(self):
        try:
            from ui.bill_table import BillTable
        except ImportError:
            QMessageBox.warning(self, "Error", "Bill Table not found or not implemented yet.")
            return
        if self.bills_window is None:
            self.bills_window = BillTable(self)
        self.bills_window.show()
        self.bills_window.raise_()
        self.bills_window.activateWindow()

    # ==== Settings Menu Actions ====

    def open_currency_dialog(self):
        dialog = CurrencyChooser()
        if dialog.exec():
            self.dashboard.update_currency()
            self.refresh_dashboard_home_tiles()
            self.dashboard.refresh_charts()
            if self.expense_window:
                self.expense_window.refresh_table()
            if self.income_window:
                self.income_window.update_currency()
                self.income_window.refresh_table()

    # ==== Help Menu Actions ====

    def show_license_dialog(self):
        license_text = (
            "MIT License\n\n"
            "Copyright (c) 2025 Manikandan D\n\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            "of this software and associated documentation files (the \"Software\"), to deal\n"
            "in the Software without restriction, including without limitation the rights\n"
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            "copies of the Software, and to permit persons to whom the Software is\n"
            "furnished to do so, subject to the following conditions:\n\n"
            "The above copyright notice and this permission notice shall be included in all\n"
            "copies or substantial portions of the Software.\n\n"
            "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
            "SOFTWARE.\n\n"
            "Project website: https://due.im"
        )
        QMessageBox.information(self, "License - MIT", license_text)

    def show_about_dialog(self):
        about_text = (
            "Panamaram - Personal Finance Expense Tracker\n"
            "Version 1.0.0\n"
            "Developed by Manikandan D\n"
            "Website: https://due.im"
        )
        QMessageBox.about(self, "About Panamaram", about_text)

    # ==== Secure Encrypted Backup Methods ====

    def export_encrypted_backup(self):
        try:
            from utils import path_utils
            db_encrypted_path = path_utils.get_secure_db_path(decrypted=False)
        except Exception as e:
            QMessageBox.warning(self, "Backup Failed", f"Could not find encrypted database file.\n{e}")
            return
        if not os.path.exists(db_encrypted_path):
            QMessageBox.warning(self, "Backup Failed", f"Encrypted database file not found:\n{db_encrypted_path}")
            return

        dest_file, _ = QFileDialog.getSaveFileName(
            self,
            "Export Backup",
            "panamaram-backup.db.aes",
            "Encrypted DB Files (*.aes);;All Files (*)"
        )
        if not dest_file:
            return
        try:
            shutil.copy2(db_encrypted_path, dest_file)
            QMessageBox.information(
                self,
                "Backup Successful",
                f"Backup was saved successfully to:\n{dest_file}\n\n"
                "This backup file is encrypted and can only be used in Panamaram with the correct password."
            )
        except Exception as e:
            QMessageBox.critical(self, "Backup Failed", f"Failed to save backup:\n{str(e)}")

    def import_encrypted_backup(self):
        try:
            from utils import path_utils
            db_encrypted_path = path_utils.get_secure_db_path(decrypted=False)
            decrypted_db_path = path_utils.get_secure_db_path(decrypted=True)
        except Exception as e:
            QMessageBox.warning(self, "Restore Failed", f"Could not find encrypted database path.\n{e}")
            return
        src_file, _ = QFileDialog.getOpenFileName(
            self,
            "Import Backup",
            "",
            "Encrypted DB Files (*.aes);;All Files (*)"
        )
        if not src_file:
            return
        reply = QMessageBox.question(
            self,
            "Confirm Restore",
            (
                "Restoring a backup will replace your current database and "
                "all current data will be lost.\n\n"
                "Make sure you have backed up your current data if needed.\n\n"
                "Proceed with restoring this backup?"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        try:
            shutil.copy2(src_file, db_encrypted_path)
            if os.path.exists(decrypted_db_path):
                try:
                    os.remove(decrypted_db_path)
                except Exception as e:
                    QMessageBox.warning(
                        self,
                        "Warning",
                        f"Could not remove decrypted database file:\n{str(e)}\n"
                        "You may need to restart your computer or close any app using the database."
                    )
            QMessageBox.information(
                self,
                "Restore Successful",
                "Backup was restored successfully.\n\n"
                "The application will now close. Please restart and unlock with the correct password to access your data."
            )
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Restore Failed", f"Failed to restore backup:\n{str(e)}")
