<div align="center">

🏦 ATM Simulation & Digital Banking

A portfolio-ready fintech banking system built with Python, Streamlit & SQLite

<p>
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F2027,50:203A43,100:2C5364&height=220&section=header&text=ATM%20Simulation%20%26%20Digital%20Banking&fontSize=34&fontColor=ffffff&animation=fadeIn&desc=Python%20%E2%80%A2%20Streamlit%20%E2%80%A2%20SQLite%20%E2%80%A2%20OOP%20Banking%20Engine&descAlignY=64&descSize=17" width="100%" />
</p>

<p>
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1000&color=2C5364&center=true&vCenter=true&width=720&lines=%F0%9F%94%90+Secure+PIN+Authentication;%E2%9A%A1+ACID+Atomic+Transactions;%F0%9F%92%B3+Modern+Fintech+Dashboard;%F0%9F%92%BB+CLI+%2B+Web+Interface;%E2%9C%85+27+Automated+Unit+Tests" alt="Typing SVG" />
</p>

<p>
  <img src="https://skillicons.dev/icons?i=python,sqlite,git,vscode&theme=dark" alt="Tech stack" />
</p>

<p>
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-testing">Testing</a> •
  <a href="#-security">Security</a> •
  <a href="#-roadmap">Roadmap</a>
</p>

</div>

✨ Overview

ATM Simulation & Digital Banking is a high-fidelity banking application designed to demonstrate how a real-world ATM/banking workflow can be implemented with a clean architecture and transaction-safe persistence layer.

The project provides two complete user experiences:

🖥️ Web Banking Dashboard — a modern Streamlit fintech interface

⌨️ Terminal ATM — an interactive command-line banking experience

Both interfaces share the same underlying Python domain logic and SQLite database, keeping business rules and financial state consistent.

Portfolio focus: This project goes beyond a basic ATM menu by demonstrating OOP, database design, ACID transactions, validation, security practices, testing, and modern UI engineering.

🚀 Why It Stands Out

<table>
<tr>
<td align="center" width="25%">

⚡ ACID

Atomic transactions

</td>
<td align="center" width="25%">

🖥️ Dual UI

Web + CLI

</td>
<td align="center" width="25%">

🧪 27 Tests

Automated coverage

</td>
<td align="center" width="25%">

🎨 Fintech UI

Custom CSS system

</td>
</tr>
</table>

💳 Features

🏦 Core Banking

🔐 Secure PIN Authentication

4-digit PIN validation

Authentication checks

Error handling

Session-state protection

💰 Real-Time Balance

Instant balance inquiries

Auto-synchronized balance display

Banking-style balance card

📥 Deposits

Quick presets: ₹500, ₹1,000, ₹2,000, ₹5,000

Custom deposit amounts

Atomic database updates

📤 Withdrawals

Balance validation

Insufficient-funds protection

Denomination guidance

Atomic deductions

🧾 Transaction History

Reverse-chronological statements

Deposit / withdrawal indicators

Post-transaction balances

ISO timestamps

🔑 PIN Management

Current PIN verification

New 4-digit PIN validation

Confirmation matching

📊 Financial Insights

The dashboard provides real-time summary metrics including:

Lifetime deposits

Total cash withdrawals

Transaction activity

Current account balance

🎨 Interface

🖥️ Web Banking Dashboard

The Streamlit interface uses a custom fintech design system featuring:

Glassmorphism cards

High-contrast financial components

Balance hero section

Quick transaction actions

Interactive statements

Security indicators

Responsive layouts

Custom CSS animations

⌨️ Terminal ATM

The CLI provides a complete console banking flow with:

Interactive menus

Masked PIN input

Deposit workflow

Withdrawal workflow

Balance inquiry

Transaction operations

📸 Recommended: Add screenshots here once available.

assets/screenshots/dashboard.png

assets/screenshots/cli.png

🧠 Architecture

flowchart TD
    U[👤 User]

    U --> W[🖥️ Streamlit Web App]
    U --> C[⌨️ Terminal CLI]

    W --> D[🏦 Banking Domain Layer]
    C --> D

    D --> V[🔍 Validation & Business Rules]
    V --> DB[(🗄️ SQLite Database)]

    DB --> A[💳 Account Data]
    DB --> T[🧾 Transaction Logs]

    D --> TX[⚡ Atomic Transaction Manager]
    TX --> DB

🔄 Transaction Safety

Every financial transaction follows an atomic workflow:

sequenceDiagram
    participant User
    participant App
    participant DB as SQLite

    User->>App: Withdraw ₹2,000
    App->>DB: BEGIN TRANSACTION
    App->>DB: Validate balance

    alt Sufficient funds
        App->>DB: UPDATE balance
        App->>DB: INSERT transaction
        App->>DB: COMMIT
        DB-->>App: Success
        App-->>User: ✅ New balance
    else Insufficient funds / error
        App->>DB: ROLLBACK
        DB-->>App: No changes
        App-->>User: ⚠️ Transaction declined
    end

💡 Core Guarantee

A balance update and its transaction record either both succeed or both fail.

This prevents inconsistent states where money is deducted without a corresponding transaction record.

🏗️ Architecture & Project Structure

ATM-Simulation/
│
├── app.py                 # Streamlit web application
├── style.css              # Custom fintech design system
├── main.py                # Terminal CLI entrypoint
├── atm.py                 # ATM controller & menu logic
├── account.py             # Account domain model & business rules
├── database.py            # SQLite persistence & transactions
├── atm.db                 # Auto-generated SQLite database
│
├── tests/
│   ├── __init__.py
│   ├── test_account.py    # Account validation tests
│   ├── test_database.py   # Database & transaction tests
│   └── test_atm.py        # CLI workflow tests
│
├── pyrefly.toml           # Project configuration
├── README.md              # Documentation
├── .gitignore             # Git ignore rules
└── LICENSE                # MIT License

🛠️ Tech Stack

Layer

Technology

🐍 Language

Python 3.8+

🌐 Web UI

Streamlit

🎨 Styling

Custom CSS3

🗄️ Database

SQLite3

🧱 Architecture

OOP + Domain-Driven Design

🧪 Testing

Python unittest

🔧 Version Control

Git / GitHub

✍️ Code Quality

Type hints + PEP 8

🔐 Security & Reliability

The project implements several practices designed to keep financial state reliable:

Protection

Implementation

🔑 PIN Validation

Strict 4-digit validation

🛡️ SQL Injection Protection

Parameterized SQL queries

🔗 Referential Integrity

SQLite foreign-key enforcement

⚡ Atomicity

BEGIN / COMMIT / ROLLBACK

💵 Monetary Precision

Amounts rounded to 2 decimals

♻️ Auto Recovery

Database recreated when missing/corrupted

🔒 Transaction Consistency

Balance + transaction log updated atomically

Database Integrity

PRAGMA foreign_keys = ON;

All database queries use parameterized placeholders rather than dynamically constructed SQL.

🚀 Quick Start

1️⃣ Clone

git clone https://github.com/tusharmagar1/atm-simulation-python.git
cd ATM-Simulation

2️⃣ Install Dependencies

pip install streamlit

3️⃣ Launch the Web Dashboard

streamlit run app.py

Open:

http://localhost:8501

4️⃣ Launch the CLI

python main.py

🔑 Demo Account

A demo account is automatically seeded on first launch.

Credential

Value

🪪 Account ID

ACC-0001

🔢 Internal ID

1

🔐 Security PIN

1234

💰 Starting Balance

₹10,000.00

⚠️ This is demo data for local development only. Do not use real financial credentials.

🧪 Testing

The project includes 27 automated unit tests covering the domain layer, database persistence, transaction safety, and CLI workflows.

Run the complete suite:

python -m unittest discover tests -v

Test Coverage

test_account.py

Initial balance integrity

Positive deposits

Zero / negative amount rejection

Insufficient funds

PIN update validation

test_database.py

Schema creation

Default account seeding

Parameterized updates

Atomic rollback behavior

Persistence across reconnects

test_atm.py

CLI authentication

Masked PIN input

Deposit workflows

Withdrawal workflows

Balance inquiries

📈 Roadmap

The next planned improvements include:

👥 Multi-account support

📄 CSV / PDF statement export

💹 Savings account & interest simulation

🐳 Docker deployment

👨‍💼 Role-based admin dashboard

🔔 Advanced transaction notifications

📊 Expanded financial analytics

🤝 Contributing

Contributions, bug reports, and feature requests are welcome.

Fork the repository

Create a feature branch

Make your changes

Run the test suite

Open a pull request

For issues and feature requests, visit the repository's GitHub Issues page.

📄 License

This project is distributed under the MIT License.

See LICENSE for details.

👨‍💻 Author

<div align="center">

Tushar Magar

Python • AI/ML • Software Development

<p>
  <a href="https://github.com/tusharmagar1">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <a href="https://www.linkedin.com/in/tushar-magar-7b80a2255">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</p>

</div>

<div align="center">

⭐ Like the project?

Give it a star on GitHub — it helps a lot!

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2C5364,50:203A43,100:0F2027&height=150&section=footer" width="100%" />

</div>
