<p align="center">
  <img src="assets/icon.png" alt="Panamaram App Icon" width="120"/>
</p>

# Panamaram - Personal Finance Expense Tracker

[![Python](https://img.shields.io/badge/Python-3.13.3-blue?logo=python)](https://www.python.org/downloads/release/python-3133/)
[![PySide6](https://img.shields.io/badge/PySide6-6.9.1-brightgreen)](https://pypi.org/project/PySide6/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Windows 11](https://img.shields.io/badge/Platform-Windows%2011-blueviolet)](https://www.microsoft.com/software-download/windows11)
[![Platform: Linux](https://img.shields.io/badge/Platform-Linux-success)](https://www.kernel.org/)
[![Platform: macOS](https://img.shields.io/badge/Platform-macOS-lightgrey)](https://www.apple.com/macos/)
[![Stars](https://img.shields.io/github/stars/manikandancode/Panamaram?style=social)](https://github.com/manikandancode/Panamaram)
![GitHub all releases](https://img.shields.io/github/downloads/manikandancode/Panamaram/total)
[![PyPI Version](https://img.shields.io/pypi/v/panamaram.svg)](https://pypi.org/project/panamaram/)
[![Python Versions](https://img.shields.io/pypi/pyversions/panamaram.svg)](https://pypi.org/project/panamaram/)
[![Downloads](https://pepy.tech/badge/panamaram)](https://pepy.tech/project/panamaram)
[![Download .DEB](https://img.shields.io/badge/Download-.DEB-E95420?logo=ubuntu&logoColor=white)](https://github.com/manikandancode/Panamaram/releases/latest)


Panamaram is a secure, offline personal finance app designed to help you effortlessly manage expenses, income, bills, and budgets. Track your daily spending, set reminders for recurring payments, and get smart insights with visual dashboards and exportable reports. With strong password protection and advanced encryption, your financial data stays private and protected. Enjoy a clean, modern interface with dark mode, multi-currency support, and a smooth user experience—no internet required.

<img width="1102" height="712" alt="image" src="https://github.com/user-attachments/assets/ca11abae-c02e-470f-ae7d-b27169d6e45a" />

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

## 🌳 Panamaram – The Money Tree of Personal Finance

The name **"Panamaram"** is a creative compound word derived from Tamil:

- **பணம் (Paṇam)** – _Money_  
- **மரம் (Maram)** – _Tree_

### 📝 Word Formation in Tamil

> **பணம்** + **மரம்** = **பணமரம் (Panamaram)**  
> _Literally translates to_ **“Money Tree”**

---

### 🌿 Meaning & Symbolism

- **மரம் (Maram)** – Symbolizes **growth**, **stability**, and **life**
- **பணம் (Paṇam)** – Represents **wealth**, **income**, and **financial resources**

---

### 💡 Why *Panamaram*?

- 🌱 A **tree of wealth** – like your finances growing steadily over time  
- 🌼 A **source or tracker** that helps your money **flourish**  
- 🧠 A **personal finance tool** that **nurtures and manages** your expenses and income wisely — just like watering a tree for steady growth

---

> _Panamaram isn't just a name — it's a philosophy of growing your money the natural way._

##  📥 How to Install Panamaram

You can install Panamaram either using the Windows installer for easy setup or by using pip to install it as a Python package.

### 🪟 1. Windows Installer (Recommended for Windows Users)

Download the latest Windows installer from the official GitHub releases page:

[Download PanamaramInstaller-1.0.0.exe](https://github.com/manikandancode/Panamaram/releases/download/v1.0.0/PanamaramInstaller-1.0.0.exe)

**Steps:**

- Download the installer `.exe` file linked above.
- Run the installer and follow the on-screen instructions.
- The installer will set up Panamaram on your PC.
- After installation, you can launch Panamaram from the Start Menu or desktop shortcut.

### 🐍📦 2. Pip Installation (Cross-platform) (Linux, Windows, MacOS)

You can also install Panamaram via pip in a Python environment. This method works on Windows, macOS, Linux, and other platforms.

**Requirements:**

- Python 3.13 or above  
- pip package manager

**Installation Steps:**

1. Open a terminal or command prompt.

2. *(Optional but recommended)* Create and activate a new virtual environment:

```bash
python -m venv venv
source panamaram-env/bin/activate # Linux/macOS
panamaram-env\Scripts\activate # Windows
```
[OR]
```bash
python3.13 -m venv panamaram-env
source panamaram-env/bin/activate # Linux/macOS
panamaram-env\Scripts\activate # Windows
```

3. Upgrade pip:
```bash
pip install --upgrade pip
```

4. Install Panamaram from PyPI:
```bash
pip install panamaram
```

This will also install all required dependencies automatically.

5. After installation, you can run Panamaram using the command:
```bash
panamaram
```
### 🐧 3.How to Install Panamaram via .deb Packages

**1. Prerequisites**

- You need a Debian-based Linux distribution (e.g., Ubuntu 25.04 [Tested].
- Download these two package files from release page and save in your Downloads directory
  - [python3-pyaescrypt_6.1.1-1_all.deb](https://github.com/manikandancode/Panamaram/releases/download/v1.0.0/python3-pyaescrypt_6.1.1-1_all.deb)
  - [panamaram_1.0.0-1_amd64.deb](https://github.com/manikandancode/Panamaram/releases/download/v1.0.0/panamaram_1.0.0-1_amd64.deb)

**2. Open a Terminal and navigate to the download directory**
```bash
cd ~/Downloads
```

**3. Install the python3-pyaescrypt dependency first** 
```bash
sudo apt install ./python3-pyaescrypt_6.1.1-1_all.deb
```

**4. Install the Panamaram package**
```bash
sudo apt install ./panamaram_1.0.0-1_amd64.deb
```
> Both commands will automatically install any additional dependencies from the Ubuntu repositories.

**5. Launch Panamaram**
```bash
panamaram
```
**Troubleshooting**

- If you encounter errors about missing dependencies, ensure your system has internet access so `apt` can download required packages.
- If the Panamaram icon does not appear immediately, try logging out and logging back in or restarting your system.

**Notes**

- Replace the version numbers in the commands above if you have newer package versions.
- For convenience, you can copy both `.deb` files into the same folder before running these commands.
- To uninstall Panamaram:
```bash
sudo apt remove panamaram
sudo apt remove python3-pyaescrypt
```


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

Open an [issue](https://github.com/manikandancode/Panamaram/issues) or contact the author  
Website: https://due.im

---
