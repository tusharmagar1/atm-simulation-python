# 🏧 ATM Simulation & Digital Banking System

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-27%20Passed-success?style=for-the-badge)]()

A high-fidelity, portfolio-ready **ATM Simulation and Digital Banking Application** built with **Python**, **Streamlit**, **SQLite**, and **Object-Oriented Programming (OOP)**. The project provides both a modern web-based banking dashboard with a luxury fintech design system and a full-featured terminal CLI interface.

---

## 📸 Key Interfaces

- **Web GUI (Streamlit)**: High-contrast fintech dashboard featuring balance hero cards, instant transaction presets, interactive statements, and real-time security alerts.
- **Terminal CLI (Command Line)**: Full console-based ATM experience with interactive menus, masked PIN inputs, and tabular receipts.

---

## 🌟 Features & Highlights

### 💳 Core Banking Operations
- **🔐 Secure PIN Authentication**: 4-digit numeric PIN authentication with validation, error handling, and session state protection.
- **💰 Real-Time Balance Tracking**: Instant balance inquiries displayed via a luxury debit card component with auto-sync indicators.
- **📈 Financial Insights & Analytics**: Real-time summary metrics tracking lifetime deposits, total cash withdrawals, and logged transaction events.
- **💵 Quick & Custom Deposits**: Instant preset deposit buttons (`₹500`, `₹1,000`, `₹2,000`, `₹5,000`) and custom amount inputs with atomic balance synchronization.
- **💸 Safe Cash Withdrawals**: Real-time balance validation, insufficient funds warnings, denomination guidelines, and atomic deductions.
- **🧾 Comprehensive Transaction History**: Reverse-chronological transaction statements with color-coded badges (`+` green for deposits, `-` red for withdrawals), post-transaction balances, and ISO timestamps.
- **🔑 Self-Service PIN Management**: PIN change flow with current PIN authentication, 4-digit numeric validation, and match confirmation.

### 🛡️ Enterprise Architecture & Security
- **⚡ ACID Atomic Transactions**: Database balance updates and transaction logging are executed within atomic `BEGIN TRANSACTION`, `COMMIT`, and `ROLLBACK` blocks to prevent desynchronization.
- **🔒 SQL Injection Prevention**: All database queries utilize parameterized SQL placeholders (`?`).
- **🔗 Relational Data Integrity**: SQLite foreign key constraints (`PRAGMA foreign_keys = ON;`) enforced across accounts and transactions.
- **🎨 Custom Fintech Design System**: Pure CSS design tokens (`style.css`), Inter typography, glassmorphism cards, glowing pulse indicators, and responsive mobile breakpoints.

---

## 🏗️ Project Architecture & File Structure

```
ATM-Simulation/
│
├── app.py                 # Streamlit Web Application (Frontend & Routing Controller)
├── style.css              # Custom Fintech Design System (CSS3 Styles & Animations)
├── main.py                # Terminal CLI Application Entrypoint
├── atm.py                 # Terminal ATM Controller & Interactive Menu Logic
├── account.py             # Domain Model & Banking Business Logic
├── database.py            # SQLite Persistence Layer & Atomic Transactions
├── atm.db                 # Persistent SQLite Database (Auto-generated on first run)
│
├── tests/                 # Automated Unit Testing Suite (27 Test Cases)
│   ├── __init__.py
│   ├── test_account.py    # Account Model & Validation Tests
│   ├── test_database.py   # SQLite Transactions & Atomicity Tests
│   └── test_atm.py        # CLI ATM Interface Tests
│
├── pyrefly.toml           # Project Configuration
├── README.md              # Project Documentation
├── .gitignore             # Git Ignore Configuration
└── LICENSE                # MIT License
```

---

## 🛠️ Tech Stack & Concepts

| Component | Technology / Pattern |
| :--- | :--- |
| **Language** | Python 3.8+ (Type-hinted, PEP 8 compliant) |
| **Web Framework** | Streamlit |
| **Styling** | Custom CSS3 (`style.css`), Google Inter Fonts, Flexbox/Grid |
| **Database** | SQLite3 (Embedded, persistent relational storage) |
| **Design Paradigm** | Object-Oriented Programming (OOP) & Domain-Driven Design |
| **Testing** | Python standard `unittest` framework |

---

## 🚀 Quick Start Guide

### 1. Clone the Repository

```bash
git clone https://github.com/tusharmagar1/atm-simulation-python.git
cd ATM-Simulation
```

### 2. Install Dependencies

Ensure Python is installed, then install Streamlit:

```bash
pip install streamlit
```

### 3. Launch the Web Application

```bash
streamlit run app.py
```
> The web app will launch automatically at **`http://localhost:8501`**.

### 4. Launch the Terminal CLI (Optional)

```bash
python main.py
```

---

## 🔑 Default Credentials

The database is pre-seeded with a default demo account upon first launch:

| Credential | Default Value |
| :--- | :--- |
| **Account ID** | `ACC-0001` (ID: `1`) |
| **Default Security PIN** | `1234` |
| **Initial Starting Balance** | `₹10,000.00` |

---

## 🧪 Automated Testing

The project includes an automated test suite containing **27 unit tests** covering the domain layer, database persistence, transaction rollbacks, and CLI menus.

Run all tests from the root directory:

```bash
python -m unittest discover tests -v
```

### Test Coverage Highlights:
- ✅ **`test_account.py`**: Initial balance integrity, positive deposits, zero/negative rejection, insufficient funds handling, and PIN update validations.
- ✅ **`test_database.py`**: SQLite schema creation, default seeding, parameterized updates, atomic rollbacks on failure, and persistence across reconnects.
- ✅ **`test_atm.py`**: CLI login authentication, masked PIN input, withdrawal/deposit workflows, and balance inquiries.

---

## 🛡️ Security & Reliability Features

1. **Foreign Key Enforcement**: `PRAGMA foreign_keys = ON;` is enforced on every database connection.
2. **Transaction Rollback Protection**: If any error occurs while logging a transaction, the entire transaction is rolled back so balances never go out of sync.
3. **Floating Point Rounding**: Monetary amounts are rounded to 2 decimal places to eliminate floating point imprecision.
4. **Auto-Recovery**: If `atm.db` is deleted or corrupted, the system automatically recreates tables and seeds the default demo account on startup.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/tusharmagar1/atm-simulation-python/issues).

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
