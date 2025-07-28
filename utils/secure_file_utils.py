# utils/secure_file_utils.py

import pyAesCrypt
import os

BUFFER_SIZE = 64 * 1024  # 64 KB

def decrypt_db_file(encrypted_path: str, decrypted_path: str, password: str):
    try:
        pyAesCrypt.decryptFile(encrypted_path, decrypted_path, password, BUFFER_SIZE)
    except Exception as e:
        print(f"[!] Error decrypting file: {e}")
        raise

def encrypt_db_file(decrypted_path: str, encrypted_path: str, password: str):
    try:
        pyAesCrypt.encryptFile(decrypted_path, encrypted_path, password, BUFFER_SIZE)
    except Exception as e:
        print(f"[!] Error encrypting file: {e}")
        raise
