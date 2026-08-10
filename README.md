# 🏧 ATM Simulation & Digital Banking System

A modern, portfolio-ready **ATM Simulation and Digital Banking Application** developed with **Python**, **Streamlit**, **SQLite**, and **Object-Oriented Programming (OOP)**. Features a luxury fintech design system, atomic database transactions, resilient session state management, and an automated unit testing suite.

---

## 🌟 Key Features

- **🔐 Secure Authentication**: 4-digit PIN authentication with masked input, strict validation, and session security.
- **💰 Real-Time Balance & Analytics**: Live balance tracking, luxury Hero card, and account insight metrics (lifetime deposits, withdrawals, and event counts).
- **💵 Instant Cash Deposits**: Single-click preset buttons (`₹500`, `₹1,000`, `₹2,000`, `₹5,000`) and custom amount inputs with atomic balance synchronization.
- **💸 Safe Cash Withdrawals**: Insufficient fund protections, physical denomination hints, and atomic balance deductions.
- **🧾 Chronological Transaction Statements**: Color-coded transaction logs (green for deposits, red for withdrawals) sorted newest-first with post-transaction balance records and timestamps.
- **🔑 PIN Management**: Self-service security PIN changes with current PIN verification, numeric format checking, and confirmation matching.
- **⚡ Atomic Transactions (ACID)**: SQLite operations wrapped in atomic `BEGIN`, `COMMIT`, and `ROLLBACK` blocks to ensure balance updates and transaction records never desynchronize.
- **📱 Fully Responsive Design**: Seamless experience across Desktop (1440px+), Tablet (768px), and Mobile (375px+).
- **🧪 Comprehensive Automated Test Suite**: Built-in unit tests covering the database layer, account domain model, and CLI ATM interface.

---

## 🏗️ Architecture & Project Structure

```
ATM-Simulation/
│
├── main.py                # Terminal CLI Application Entrypoint
├── app.py                 # Streamlit Web Application & UI/UX Design System
├── atm.py                 # Terminal ATM Interface Controller
├── account.py             # Domain Model & Banking Business Logic
├── database.py            # SQLite Persistence Layer & Atomic Transactions
│
├── tests/                 # Automated Unit Testing Suite
│   ├── __init__.py
│   ├── test_database.py   # Database & Transaction Tests
│   ├── test_account.py    # Domain Logic & Validation Tests
│   └── test_atm.py        # CLI ATM Interface Tests
│
├── README.md              # Project Documentation
├── .gitignore             # Git Ignore Configuration
└── LICENSE                # MIT License
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Streamlit (`pip install streamlit`)

### 2. Run the Streamlit Web Application

```bash
streamlit run app.py
```
*Opens automatically at `http://localhost:8501` in your browser.*

### 3. Run the Terminal / CLI Application

```bash
python main.py
```

---

## 🔑 Default Credentials

| Field | Default Value |
| :--- | :--- |
| **Initial Account ID** | `ACC-0001` |
| **Default Security PIN** | `1234` |
| **Initial Starting Balance** | `₹10,000.00` |

---

## 🧪 Running Automated Tests

Run the complete test suite with Python's built-in `unittest` runner:

```bash
python -m unittest discover tests -v
```

All test cases run in isolated temporary database files and clean up automatically upon completion.

---

## 🛡️ Database & Security Notes

- **Foreign Key Constraints**: `PRAGMA foreign_keys = ON;` is enforced on every database connection.
- **Atomic Operations**: `Database.record_transaction()` guarantees that the `accounts` table balance update and the `transactions` table insert succeed or fail as a single unit.
- **Precision**: Monetary figures are rounded to 2 decimal places to prevent floating-point representation drift.
- **SQL Injection Prevention**: All queries utilize parameterized SQL placeholders (`?`).
- **Data Persistence**: Account balances and transaction records persist across application restarts in `atm.db`. If `atm.db` is deleted, the default `₹10,000.00` / `1234` account is automatically seeded.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
