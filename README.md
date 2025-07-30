# Panamaram - Personal Finance Expense Tracker

[![Python](https://img.shields.io/badge/Python-3.13.3-blue?logo=python)](https://www.python.org/downloads/release/python-3133/)
[![PySide6](https://img.shields.io/badge/PySide6-6.9.1-brightgreen)](https://pypi.org/project/PySide6/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Platform](https://img.shields.io/badge/Platform-Windows%2011-blueviolet)](https://www.microsoft.com/software-download/windows11)
[![Stars](https://img.shields.io/github/stars/your-repo/panamaram?style=social)](https://github.com/manikandancode/Panamaram)

A **secure, modern, and user-friendly desktop app** to manage your personal finances, built in Python using PySide6 (Qt) and SQLite. Track expenses, incomes, recurring bills, visualize reports, and protect your data with robust encryption.

---

## 🌟 Features

- **Expense & Income Tracking:**  
  Add, view, edit, and delete transactions, with category, notes, and support for recurring entries.

- **Bill/Reminder System:**  
  Manage recurring and one-time bills, with overdue highlighting.

- **Home Dashboard:**  
  Instant stats and smart charts of your budget, balance, and spending patterns.

- **Multi-format Reports:**  
  Export reports as PDF, Excel (XLSX), and CSV.

- **Data Security:**  
  - Strong password protection
  - Database encryption (AES)
  - Encrypted backup and restore with user password validation
  - All sensitive info kept private

- **User Experience:**  
  - Modular, responsive UI with dark mode-ready design
  - One-click currency switching
  - Helpful error and warning dialogs
  - Easily installable and self-contained

---

## 🗂️ Project Structure
```bash
Panamaram/
│
├── assets/
│   ├── icon.png
│   ├── icon.ico
│   └── ...         # All static/icons/images
│
├── auth/
│   └── auth.py
│
├── db/
│   ├── expense_manager.py
│   ├── income_manager.py
│   ├── recurring_income_manager.py
│   ├── recurring_manager.py
│   ├── bill_manager.py
│   └── db_manager.py
│
├── worker/
│   └── worker_unlock
│
├── utils/
│   ├── path_utils.py
│   ├── key_manager.py
│   ├── secure_field_utils.py
│   ├── secure_file_utils.py
│   └── smart_suggestions.py
│
├── ui/
│   ├── main_window.py
│   ├── dashboard.py
│   ├── expense_table.py
│   ├── income_table.py
│   ├── expense_form.py
│   ├── income_form.py
│   ├── currency_chooser.py
│   ├── bill_form.py
│   ├── bill_table.py
│   ├── reports.py
│   └── ...          # Any extra UI component modules
│
├── main.py
├── requirements.txt
```

---

## 🖥️ How to Set Up (Windows 11 Guide)

### 1. Install Python 3.13.3

- Download the official installer:  
  [Python 3.13.3 Windows 64-bit](https://www.python.org/downloads/release/python-3133/)
- During install:
  - **Check** “Add Python to PATH”.
  - Choose “Customize installation”.
  - Complete the wizard.
- Verify:
```bash
python --version
```

- Output: Python 3.13.3

### 2. Create Your Project Directory

- Open your terminal or command prompt and run:
```bash
mkdir Panamaram
cd Panamaram
```
### 3. Create and Activate a Virtual Environment

- Create virtual environment
```bash
python -m venv venv
```
- Activate (on Windows)
```bash
venv\Scripts\activate
```
- If successful, your terminal will show:
(venv)
### 4. Install Required Packages
```bash
pip install PySide6
pip install appdirs pyAesCrypt cryptography
pip install matplotlib
pip install fpdf2
pip install openpyxl
```
- (Optional) Save package versions for later with:
```bash
pip freeze > requirements.txt
```
- **To install all at once in the future:**
```bash
pip install -r requirements.txt
```

### 5. Set Up VS Code for Development

- Open the `Panamaram/` folder in VS Code.
- Press `Ctrl + Shift + P`, type `Python: Select Interpreter`, and select `./venv/Scripts/python.exe`.
- *(If prompted, install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python))*

### 6. Useful Commands

| Command                                 | Use                       |
|------------------------------------------|---------------------------|
| `venv\Scripts\activate`                  | Activate venv             |
| `deactivate`                             | Deactivate venv           |
| `pip install -r requirements.txt`        | Install all dependencies  |

---

## 🚀 Quick Start

1. **Clone/download this repository.**
2. **Follow the steps above to set up the environment and install dependencies.**
3. **Run the app:**
python main.py


---

## 📦 Packaging/Distribution

- For packaging (e.g., .exe), consider tools like `PyInstaller`.
- For a Windows installer, look at NSIS or Inno Setup.
- (Request sample scripts or guidance if needed!)

---

## 📝 License

MIT License  
Copyright (c) 2025 Manikandan D

---

## 🙏 Acknowledgements

- **Python Software Foundation**  
For the language and runtime  
[Python.org](https://www.python.org/)

- **Qt Company & PySide**  
For the amazing cross-platform GUI framework  
[Qt for Python (PySide6)](https://doc.qt.io/qtforpython/)

- **Open Source Projects:**  
- `appdirs`
- `cryptography`
- `pyAesCrypt`
- `matplotlib`
- `fpdf2`
- `openpyxl`
- All other brilliant libraries used

- **Community & Testers:**  
Thanks to everyone who tested, gave feedback, and inspired features.

---

## 🙋‍♂️ Questions? Feedback?

Open an [issue](https://github.com/manikandancode/Panamaram) or contact the author  
Website: https://due.im

---
