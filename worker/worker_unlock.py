# worker/worker_unlock.py

from PySide6.QtCore import QObject, Signal, Slot

class UnlockWorker(QObject):
    finished = Signal(bool, str)  # success, message

    def __init__(self, password, decrypt_func, init_db_func, verify_password_func):
        super().__init__()
        self.password = password
        self.decrypt_func = decrypt_func
        self.init_db_func = init_db_func
        self.verify_password_func = verify_password_func

    @Slot()
    def run(self):
        try:
            # 1. Decrypt
            self.decrypt_func(self.password)

            # 2. Initialize Database
            self.init_db_func()

            # 3. Verify unlock password
            if not self.verify_password_func(self.password):
                self.finished.emit(False, "Incorrect password")
                return

            self.finished.emit(True, "Unlock successful")
        except Exception as e:
            self.finished.emit(False, f"Unlock failed: {e}")
