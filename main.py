import sys
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from utils import path_utils, key_manager
from utils.secure_file_utils import decrypt_db_file, encrypt_db_file
from db.db_manager import init_db, get_setting
from db.recurring_manager import process_recurring_expenses
from db.recurring_income_manager import process_recurring_income
from auth.auth import AuthWidget
from ui.currency_chooser import CurrencyChooser
from ui.main_window import MainWindow

# Paths for app icons
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
ICON_PNG_PATH = os.path.join(ASSETS_DIR, "icon.png")
ICON_ICO_PATH = os.path.join(ASSETS_DIR, "icon.ico")

# Database paths: encrypted and decrypted versions
ENCRYPTED_DB_PATH = path_utils.get_secure_db_path(decrypted=False)
DECRYPTED_DB_PATH = path_utils.get_secure_db_path(decrypted=True)

main_app_window = None  # Will hold MainWindow instance


def get_app_icon():
    """Return appropriate app icon based on OS."""
    if sys.platform.startswith("win") and os.path.exists(ICON_ICO_PATH):
        return QIcon(ICON_ICO_PATH)
    return QIcon(ICON_PNG_PATH)


def cleanup_and_exit():
    """Encrypt the database on app exit and clean up decrypted copy."""
    print("🔐 Encrypting and cleaning up before exit...")
    password = key_manager.get_encryption_password()
    if os.path.exists(DECRYPTED_DB_PATH) and password:
        try:
            encrypt_db_file(DECRYPTED_DB_PATH, ENCRYPTED_DB_PATH, password)
            os.remove(DECRYPTED_DB_PATH)
            print("✅ DB encrypted and cleaned.")
        except Exception as e:
            print(f"❌ Error during encryption: {e}")
    else:
        print("⚠️ Skipping encryption (no decrypted DB or missing password).")
    sys.exit(0)


def launch_gui(password):
    """Launch the main app GUI after successful authentication."""
    global main_app_window

    key_manager.set_encryption_password(password)
    init_db()

    # Setup currency if not set (first launch)
    if not get_setting("currency"):
        chooser = CurrencyChooser()
        if chooser.exec() == 0:
            print("⚠️ Currency setup canceled. Quitting.")
            cleanup_and_exit()

    # Process recurring expenses and income for today
    today = datetime.now().strftime("%Y-%m-%d")
    process_recurring_expenses(today)
    process_recurring_income(today)

    # Initialize and show the main window
    main_app_window = MainWindow()
    main_app_window.setWindowIcon(get_app_icon())
    main_app_window.show()


def main():
    """Main entry point for Panamaram app."""
    print("🚀 Launching Panamaram...")

    # Decrypt DB if encrypted exists and decrypted missing
    if os.path.exists(ENCRYPTED_DB_PATH) and not os.path.exists(DECRYPTED_DB_PATH):
        password = key_manager.get_encryption_password()
        if password:
            try:
                print("🔓 Decrypting database...")
                decrypt_db_file(ENCRYPTED_DB_PATH, DECRYPTED_DB_PATH, password)
                print("✅ Decrypted successfully.")
            except Exception as e:
                print(f"❌ Decryption failed: {e}")
                sys.exit(1)
        else:
            # No password set, proceed with fresh db file
            print("🆕 No password - fresh DB will be created.")
            open(DECRYPTED_DB_PATH, "a").close()
    elif not os.path.exists(ENCRYPTED_DB_PATH):
        # First launch without any DBs; create decrypted DB file
        print("🆕 First launch - no encrypted DB found.")
        open(DECRYPTED_DB_PATH, "a").close()

    # Initialize DB tables if needed
    init_db()

    # Setup QApplication
    app = QApplication(sys.argv)
    app.setWindowIcon(get_app_icon())

    # Show authentication window first
    auth_window = AuthWidget(on_auth_success=launch_gui)
    auth_window.setWindowIcon(get_app_icon())
    auth_window.show()

    # Ensure DB gets encrypted and cleaned on app exit
    app.aboutToQuit.connect(cleanup_and_exit)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
