# auth/auth.py
import os
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import QThread
from db import db_manager
from utils import path_utils, key_manager
from worker.worker_unlock import UnlockWorker
import hashlib
import sqlite3

DB_PATH = path_utils.get_secure_db_path(decrypted=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def store_password_hash(password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM auth")
    cursor.execute("INSERT INTO auth (password_hash) VALUES (?)", (hash_password(password),))
    conn.commit()
    conn.close()

def verify_password(password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM auth LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row and row[0] == hash_password(password)

def is_password_set() -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM auth")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

class AuthWidget(QWidget):
    def __init__(self, on_auth_success):
        super().__init__()
        self.setWindowTitle("Panamaram - Unlock")
        self.setFixedSize(300, 150)

        self.on_auth_success = on_auth_success

        self.label = QLabel("Enter Password" if is_password_set() else "Set New Password")
        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.Password)

        self.button = QPushButton("Unlock" if is_password_set() else "Set Password")
        self.button.clicked.connect(self.handle_auth)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def handle_auth(self):
        password = self.input.text()
        if not password:
            QMessageBox.warning(self, "Error", "Password cannot be empty")
            return

        self.button.setDisabled(True)

        if is_password_set():
            # Call unlock via background thread
            self.unlock_thread = QThread()
            self.worker = UnlockWorker(
                password=password,
                decrypt_func=self.decrypt_db_file,
                init_db_func=db_manager.init_db,
                verify_password_func=verify_password
            )
            self.worker.moveToThread(self.unlock_thread)

            self.unlock_thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.finish_auth)
            self.worker.finished.connect(self.worker.deleteLater)
            self.unlock_thread.finished.connect(self.unlock_thread.deleteLater)
            self.worker.finished.connect(self.unlock_thread.quit)

            self.unlock_thread.start()
        else:
            store_password_hash(password)
            key_manager.set_encryption_password(password)
            QMessageBox.information(self, "Success", "Password set successfully")
            self.on_auth_success(password)
            self.close()

    def decrypt_db_file(self, password):
        from utils.secure_file_utils import decrypt_db_file
        from utils.path_utils import get_secure_db_path
        enc_path = get_secure_db_path(decrypted=False)
        dec_path = get_secure_db_path(decrypted=True)
        if not dec_path or not enc_path:
            return
        if not os.path.exists(dec_path) and os.path.exists(enc_path):
            decrypt_db_file(enc_path, dec_path, password)

    def finish_auth(self, success, message):
        self.button.setDisabled(False)
        if success:
            key_manager.set_encryption_password(self.input.text())
            self.on_auth_success(self.input.text())
            self.close()
        else:
            QMessageBox.critical(self, "Unlock Failed", message)
