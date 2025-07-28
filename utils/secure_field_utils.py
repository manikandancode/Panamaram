# utils/secure_field_utils.py

from cryptography.fernet import Fernet
import os
from utils import path_utils

def get_fernet_key():
    config_dir = path_utils.get_config_dir()
    key_file = os.path.join(config_dir, "fernet.key")
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    # Generate and store on first run
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)
    return key

FERNET_KEY = get_fernet_key()
fernet = Fernet(FERNET_KEY)

def encrypt_field(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt_field(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
