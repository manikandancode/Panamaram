# utils/path_utils.py
import os
import platform

def get_app_data_dir() -> str:
    app_name = "Panamaram"
    if platform.system() == "Windows":
        base_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif platform.system() == "Linux":
        base_dir = os.path.join(os.path.expanduser("~"), ".local", "share")
    else:
        base_dir = os.path.expanduser("~")
    app_dir = os.path.join(base_dir, app_name)
    os.makedirs(app_dir, exist_ok=True)
    return app_dir

def get_secure_db_path(decrypted=False) -> str:
    app_dir = get_app_data_dir()
    filename = "panamaram.db" if decrypted else "panamaram.db.aes"
    return os.path.join(app_dir, filename)

def get_config_dir() -> str:
    app_dir = get_app_data_dir()
    config_dir = os.path.join(app_dir, "config")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir
