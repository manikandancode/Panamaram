# utils/key_manager.py

import os
from utils import path_utils

def get_encryption_password():
    config_dir = path_utils.get_config_dir()
    key_file = os.path.join(config_dir, "encryption.key")
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            return f.read().strip()
    else:
        return None

def set_encryption_password(raw_password):
    config_dir = path_utils.get_config_dir()
    key_file = os.path.join(config_dir, "encryption.key")
    with open(key_file, "w") as f:
        f.write(raw_password)
