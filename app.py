"""ATM Banking & Digital Banking Simulation Application.

A high-fidelity, portfolio-grade Streamlit banking interface built with
Object-Oriented Architecture, SQLite persistence, atomic transactions,
and a modern fintech UI/UX design system.
"""

from datetime import datetime
import os
from typing import Optional
import streamlit as st

from account import Account
from database import Database

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ATM Banking | Digital Banking System",
    page_icon="🏧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. LOAD EXTERNAL FINTECH DESIGN SYSTEM (CSS)
# ============================================================

css_path = os.path.join(os.path.dirname(__file__), "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as css_file:
        st.html(f"<style>{css_file.read()}</style>")

# ============================================================
# 3. DATABASE & SESSION INITIALIZATION
# ============================================================

database = Database()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

if "withdraw_amount" not in st.session_state:
    st.session_state.withdraw_amount = 500.0

if "deposit_amount" not in st.session_state:
    st.session_state.deposit_amount = 500.0

if "flash_message" not in st.session_state:
    st.session_state.flash_message = None


def load_account_from_db() -> Optional[Account]:
    """Loads account model from SQLite database."""
    account_data = None
    if st.session_state.account is not None:
        try:
            account_data = database.get_account_by_id(st.session_state.account.account_id)
        except (TypeError, AttributeError):
            account_data = database.get_account()

    if not account_data:
        account_data = database.get_account()

    if account_data:
        acc_id, pin, balance = account_data
        return Account(
            account_id=acc_id,
            pin=pin,
            balance=balance,
            database=database
        )
    return None


def refresh_account_state() -> None:
    """Refreshes account object state from database."""
    fresh_account = load_account_from_db()
    if fresh_account:
        st.session_state.account = fresh_account


def get_time_greeting() -> str:
    """Returns time-appropriate user greeting."""
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning 👋"
    elif hour < 17:
        return "Good afternoon 👋"
    else:
        return "Good evening 👋"


def render_flash_message() -> None:
    """Renders temporary status alert and clears it."""
    if st.session_state.flash_message:
        msg = st.session_state.flash_message
        msg_type = msg.get("type", "success")
        title = msg.get("title", "")
        text = msg.get("text", "")
        icon = "✓" if msg_type == "success" else ("⚠️" if msg_type == "warning" else "❌")
        alert_class = f"custom-alert custom-alert-{msg_type}"

        st.html(
            f"""
            <div class="{alert_class}">
                <div class="alert-icon">{icon}</div>
                <div>
                    <div class="alert-title">{title}</div>
                    <div class="alert-text">{text}</div>
                </div>
            </div>
            """
        )
        st.session_state.flash_message = None


# ============================================================
# 4. SHARED UI & NAVIGATION COMPONENTS
# ============================================================

def render_top_navbar() -> None:
    """Renders persistent horizontal navigation tabs across all pages."""
    nav_cols = st.columns(7)
    current = st.session_state.current_page

    with nav_cols[0]:
        if st.button("🏠 Home", key="topnav_dash", type="primary" if current == "dashboard" else "secondary", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    with nav_cols[1]:
        if st.button("💸 Withdraw", key="topnav_with", type="primary" if current == "withdraw" else "secondary", use_container_width=True):
            st.session_state.current_page = "withdraw"
            st.rerun()
    with nav_cols[2]:
        if st.button("💵 Deposit", key="topnav_dep", type="primary" if current == "deposit" else "secondary", use_container_width=True):
            st.session_state.current_page = "deposit"
            st.rerun()
    with nav_cols[3]:
        if st.button("🧾 History", key="topnav_tx", type="primary" if current == "transactions" else "secondary", use_container_width=True):
            st.session_state.current_page = "transactions"
            st.rerun()
    with nav_cols[4]:
        if st.button("💰 Insights", key="topnav_bal", type="primary" if current == "balance" else "secondary", use_container_width=True):
            st.session_state.current_page = "balance"
            st.rerun()
    with nav_cols[5]:
        if st.button("🔑 PIN", key="topnav_pin", type="primary" if current == "change_pin" else "secondary", use_container_width=True):
            st.session_state.current_page = "change_pin"
            st.rerun()
    with nav_cols[6]:
        if st.button("🚪 Logout", key="topnav_logout", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.account = None
            st.session_state.current_page = "dashboard"
            st.session_state.flash_message = None
            st.rerun()


def render_top_header() -> None:
    """Renders the top greeting and live security status bar followed by the navigation menu."""
    greeting = get_time_greeting()
    st.html(
        f"""
        <div class="top-header-wrapper">
            <div>
                <h1 class="greeting-title">{greeting}</h1>
                <div class="greeting-subtitle">Manage your account and transactions securely.</div>
            </div>
            <div>
                <div class="status-pill">
                    <span class="status-dot-green"></span>
                    <span>Secure Online</span>
                </div>
            </div>
        </div>
        """
    )
    render_top_navbar()


def render_hero_balance_card(account: Account) -> None:
    """Renders the primary luxury dark balance card."""
    formatted_balance = f"₹{account.balance:,.2f}"
    st.html(
        f"""
        <div class="hero-balance-card">
            <div class="card-top-row">
                <div class="balance-badge-label">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <rect x="2" y="5" width="20" height="14" rx="2"></rect>
                        <line x1="2" y1="10" x2="22" y2="10"></line>
                    </svg>
                    AVAILABLE BALANCE
                </div>
                <div class="card-chip"></div>
            </div>
            <div class="balance-amount-display">{formatted_balance}</div>
            <div class="card-footer-row">
                <div class="card-footer-text">Account: ACC-{account.account_id:04d} • Active</div>
                <div class="card-sync-status">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Last updated just now
                </div>
            </div>
        </div>
        """
    )


def render_transactions_list(transactions: list, limit: Optional[int] = None) -> None:
    """Renders transaction items or a clean empty state card."""
    if not transactions:
        st.html(
            """
            <div class="empty-state-card">
                <div class="empty-state-icon">🧾</div>
                <div class="empty-state-title">No transactions yet</div>
                <div class="empty-state-desc">Your recent account activity and cash flows will appear right here.</div>
            </div>
            """
        )
        return

    items_to_show = transactions[:limit] if limit else transactions
    tx_html_items = []

    for tx in items_to_show:
        tx_type = tx[0]
        amount = tx[1]
        balance_after = tx[2]
        created_at = tx[3]

        if tx_type == "Deposit":
            icon = "💵"
            icon_class = "tx-icon-deposit"
            sign = "+"
            amount_class = "tx-amount-deposit"
        else:
            icon = "💸"
            icon_class = "tx-icon-withdraw"
            sign = "-"
            amount_class = "tx-amount-withdraw"

        tx_html_items.append(
            f"""
            <div class="tx-item-card">
                <div class="tx-left-col">
                    <div class="tx-icon-pill {icon_class}">{icon}</div>
                    <div>
                        <div class="tx-meta-type">{tx_type}</div>
                        <div class="tx-meta-date">{created_at}</div>
                    </div>
                </div>
                <div class="tx-right-col">
                    <div class="{amount_class}">{sign}₹{amount:,.2f}</div>
                    <div class="tx-balance-after">Balance: ₹{balance_after:,.2f}</div>
                </div>
            </div>
            """
        )

    st.html(f'<div class="transaction-list-wrap">{"".join(tx_html_items)}</div>')


# ============================================================
# 5. SIDEBAR NAVIGATION
# ============================================================

def render_sidebar() -> None:
    """Renders dark sidebar navigation and active indicators."""
    with st.sidebar:
        st.html(
            """
            <div class="sidebar-brand-wrapper">
                <div class="sidebar-brand-title">
                    <span>🏧</span>
                    <span>ATM Banking</span>
                </div>
                <div class="sidebar-brand-subtitle">Digital Banking System</div>
            </div>
            <div class="sidebar-section-title">Navigation Menu</div>
            """
        )

        nav_items = [
            ("dashboard", "🏠 Dashboard"),
            ("balance", "💰 Balance & Insights"),
            ("withdraw", "💸 Withdraw Money"),
            ("deposit", "💵 Deposit Money"),
            ("transactions", "🧾 Transaction History"),
            ("change_pin", "🔑 Change PIN"),
        ]

        current = st.session_state.current_page

        for page_key, label in nav_items:
            is_active = (current == page_key)
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"sidebar_nav_{page_key}", type=btn_type, use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

        st.html(
            """
            <div class="sidebar-footer-box">
                <div class="status-badge-sidebar">
                    <div class="pulse-dot"></div>
                    <span>Secure Session</span>
                </div>
            </div>
            """
        )

        if st.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.account = None
            st.session_state.current_page = "dashboard"
            st.session_state.flash_message = None
            st.rerun()


# ============================================================
# 6. VIEWS / PAGES
# ============================================================

def dashboard_page() -> None:
    """Main Banking Dashboard View."""
    refresh_account_state()
    account = st.session_state.account

    render_top_header()
    render_flash_message()
    render_hero_balance_card(account)

    # Quick Actions
    st.html(
        """
        <div class="section-title-wrap">
            <div class="section-title">Quick Actions</div>
            <div class="section-subtitle">Frequently used banking operations</div>
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.html(
            """
            <div class="quick-action-card">
                <div>
                    <div class="action-icon-circle action-icon-withdraw">💸</div>
                    <div class="action-card-title">Withdraw</div>
                    <div class="action-card-desc">Take money from your account safely</div>
                </div>
            </div>
            """
        )
        if st.button("Withdraw Cash", key="dash_btn_withdraw", use_container_width=True):
            st.session_state.current_page = "withdraw"
            st.rerun()

    with col2:
        st.html(
            """
            <div class="quick-action-card">
                <div>
                    <div class="action-icon-circle action-icon-deposit">💵</div>
                    <div class="action-card-title">Deposit</div>
                    <div class="action-card-desc">Add money to your balance instantly</div>
                </div>
            </div>
            """
        )
        if st.button("Deposit Cash", key="dash_btn_deposit", use_container_width=True):
            st.session_state.current_page = "deposit"
            st.rerun()

    with col3:
        st.html(
            """
            <div class="quick-action-card">
                <div>
                    <div class="action-icon-circle action-icon-history">🧾</div>
                    <div class="action-card-title">Transactions</div>
                    <div class="action-card-desc">View full account history & statement</div>
                </div>
            </div>
            """
        )
        if st.button("View Activity", key="dash_btn_tx", use_container_width=True):
            st.session_state.current_page = "transactions"
            st.rerun()

    # Recent Transactions List
    st.html(
        """
        <div class="section-title-wrap" style="margin-top: 1.75rem;">
            <div class="section-title">Recent Transactions</div>
            <div class="section-subtitle">Showing latest 5 account activities</div>
        </div>
        """
    )

    transactions = account.get_transactions()
    render_transactions_list(transactions, limit=5)


def balance_view_page() -> None:
    """Dedicated Account Balance & Financial Insights View."""
    refresh_account_state()
    account = st.session_state.account

    render_top_header()
    render_flash_message()
    render_hero_balance_card(account)

    transactions = account.get_transactions()
    total_deposits = sum(tx[1] for tx in transactions if tx[0] == "Deposit")
    total_withdrawals = sum(tx[1] for tx in transactions if tx[0] == "Withdrawal")
    total_tx_count = len(transactions)

    st.html(
        """
        <div class="section-title-wrap">
            <div class="section-title">Account Insights & Analytics</div>
            <div class="section-subtitle">Summary of all transactions recorded on this account</div>
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.html(
            f"""
            <div class="quick-action-card">
                <div>
                    <div class="action-icon-circle action-icon-deposit">📈</div>
                    <div class="action-card-title">₹{total_deposits:,.2f}</div>
                    <div class="action-card-desc">Total lifetime deposits added</div>
                </div>
            </div>
            """
        )

    with col2:
        st.html(
            f"""
            <div class="quick-action-card">
                <div>
                    <div class="action-icon-circle action-icon-withdraw">📉</div>
                    <div class="action-card-title">₹{total_withdrawals:,.2f}</div>
                    <div class="action-card-desc">Total lifetime cash withdrawals</div>
                </div>
            </div>
            """
        )

    with col3:
        st.html(
            f"""
            <div class="quick-action-card">
                <div>
                    <div class="action-icon-circle action-icon-history">🔢</div>
                    <div class="action-card-title">{total_tx_count} Events</div>
                    <div class="action-card-desc">Total transactions logged securely</div>
                </div>
            </div>
            """
        )


def withdraw_page() -> None:
    """Withdrawal View with quick presets and instant atomic feedback."""
    refresh_account_state()
    account = st.session_state.account

    render_top_header()
    render_flash_message()

    st.html(
        f"""
        <div class="standard-panel-card">
            <div class="panel-header">
                <div class="panel-title">💸 Withdraw Money</div>
                <div class="panel-desc">Available Balance: <b>₹{account.balance:,.2f}</b> • Cash dispensed in multiples of standard notes</div>
            </div>
            <div class="preset-title">Select Quick Preset Amount:</div>
        </div>
        """
    )

    # Preset buttons row
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        if st.button("₹500", key="w_p500", use_container_width=True):
            st.session_state.withdraw_amount = 500.0
            st.rerun()
    with p_col2:
        if st.button("₹1,000", key="w_p1000", use_container_width=True):
            st.session_state.withdraw_amount = 1000.0
            st.rerun()
    with p_col3:
        if st.button("₹2,000", key="w_p2000", use_container_width=True):
            st.session_state.withdraw_amount = 2000.0
            st.rerun()
    with p_col4:
        if st.button("₹5,000", key="w_p5000", use_container_width=True):
            st.session_state.withdraw_amount = 5000.0
            st.rerun()

    st.write("")

    with st.form("withdraw_form", clear_on_submit=False):
        amount = st.number_input(
            "Enter withdrawal amount (₹)",
            min_value=1.0,
            value=float(st.session_state.withdraw_amount),
            step=500.0,
            format="%.2f",
            key="withdraw_input_field"
        )
        submit_withdraw = st.form_submit_button("Confirm Withdrawal", type="primary", use_container_width=True)

        if submit_withdraw:
            if amount <= 0:
                st.session_state.flash_message = {
                    "type": "danger",
                    "title": "Invalid Amount",
                    "text": "Please enter a withdrawal amount greater than ₹0."
                }
                st.rerun()
            elif amount > account.balance:
                st.session_state.flash_message = {
                    "type": "danger",
                    "title": "Insufficient Balance",
                    "text": f"Requested ₹{amount:,.2f}, but your available balance is ₹{account.balance:,.2f}."
                }
                st.rerun()
            else:
                if account.withdraw(amount):
                    st.session_state.flash_message = {
                        "type": "success",
                        "title": "Withdrawal Successful",
                        "text": f"₹{amount:,.2f} successfully withdrawn. Remaining balance: ₹{account.balance:,.2f}."
                    }
                    st.session_state.account = account
                    st.rerun()
                else:
                    st.session_state.flash_message = {
                        "type": "danger",
                        "title": "Transaction Failed",
                        "text": "An error occurred while processing your withdrawal. Please try again."
                    }
                    st.rerun()


def deposit_page() -> None:
    """Deposit View with quick presets and instant atomic feedback."""
    refresh_account_state()
    account = st.session_state.account

    render_top_header()
    render_flash_message()

    st.html(
        f"""
        <div class="standard-panel-card">
            <div class="panel-header">
                <div class="panel-title">💵 Deposit Money</div>
                <div class="panel-desc">Current Balance: <b>₹{account.balance:,.2f}</b> • Funds are credited instantly to your account</div>
            </div>
            <div class="preset-title">Select Quick Preset Amount:</div>
        </div>
        """
    )

    # Preset buttons row
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        if st.button("₹500", key="d_p500", use_container_width=True):
            st.session_state.deposit_amount = 500.0
            st.rerun()
    with p_col2:
        if st.button("₹1,000", key="d_p1000", use_container_width=True):
            st.session_state.deposit_amount = 1000.0
            st.rerun()
    with p_col3:
        if st.button("₹2,000", key="d_p2000", use_container_width=True):
            st.session_state.deposit_amount = 2000.0
            st.rerun()
    with p_col4:
        if st.button("₹5,000", key="d_p5000", use_container_width=True):
            st.session_state.deposit_amount = 5000.0
            st.rerun()

    st.write("")

    with st.form("deposit_form", clear_on_submit=False):
        amount = st.number_input(
            "Enter deposit amount (₹)",
            min_value=1.0,
            value=float(st.session_state.deposit_amount),
            step=500.0,
            format="%.2f",
            key="deposit_input_field"
        )
        submit_deposit = st.form_submit_button("Confirm Deposit", type="primary", use_container_width=True)

        if submit_deposit:
            if amount <= 0:
                st.session_state.flash_message = {
                    "type": "danger",
                    "title": "Invalid Amount",
                    "text": "Deposit amount must be greater than ₹0."
                }
                st.rerun()
            else:
                if account.deposit(amount):
                    st.session_state.flash_message = {
                        "type": "success",
                        "title": "Deposit Successful",
                        "text": f"₹{amount:,.2f} successfully deposited. New balance: ₹{account.balance:,.2f}."
                    }
                    st.session_state.account = account
                    st.rerun()
                else:
                    st.session_state.flash_message = {
                        "type": "danger",
                        "title": "Deposit Failed",
                        "text": "Unable to complete deposit transaction. Please check database connection."
                    }
                    st.rerun()


def transactions_page() -> None:
    """Full Transaction History View."""
    refresh_account_state()
    account = st.session_state.account

    render_top_header()
    render_flash_message()

    transactions = account.get_transactions()
    total_count = len(transactions)

    st.html(
        f"""
        <div class="standard-panel-card">
            <div class="panel-header" style="border:none; margin-bottom:0; padding-bottom:0;">
                <div class="panel-title">🧾 Transaction History</div>
                <div class="panel-desc">All historical deposits and withdrawals ({total_count} transactions recorded)</div>
            </div>
        </div>
        """
    )

    render_transactions_list(transactions)


def change_pin_page() -> None:
    """Security & PIN Management View."""
    refresh_account_state()
    account = st.session_state.account

    render_top_header()
    render_flash_message()

    st.html(
        """
        <div class="standard-panel-card">
            <div class="panel-header">
                <div class="panel-title">🔑 Security & PIN Management</div>
                <div class="panel-desc">Update your secret 4-digit ATM authentication PIN</div>
            </div>
            <div class="criteria-box">
                <div class="criteria-title">PIN Security Requirements:</div>
                <div class="criteria-item">✓ Exactly 4 numeric digits</div>
                <div class="criteria-item">✓ Numbers only (0-9)</div>
                <div class="criteria-item">✓ New PIN and Confirmation must match</div>
            </div>
        </div>
        """
    )

    with st.form("pin_form"):
        old_pin = st.text_input(
            "Current PIN",
            type="password",
            max_chars=4,
            placeholder="Enter current 4-digit PIN"
        )
        col_pin1, col_pin2 = st.columns(2)
        with col_pin1:
            new_pin = st.text_input(
                "New PIN",
                type="password",
                max_chars=4,
                placeholder="Enter new 4 digits"
            )
        with col_pin2:
            confirm_pin = st.text_input(
                "Confirm New PIN",
                type="password",
                max_chars=4,
                placeholder="Re-enter new 4 digits"
            )

        submit_pin = st.form_submit_button("Update Security PIN", type="primary", use_container_width=True)

        if submit_pin:
            if not old_pin or not new_pin or not confirm_pin:
                st.session_state.flash_message = {
                    "type": "danger",
                    "title": "Missing Fields",
                    "text": "Please complete all PIN input fields."
                }
                st.rerun()
            elif len(new_pin) != 4 or not new_pin.isdigit():
                st.session_state.flash_message = {
                    "type": "danger",
                    "title": "Invalid PIN Format",
                    "text": "The new PIN must be exactly 4 numeric digits (0-9)."
                }
                st.rerun()
            elif new_pin != confirm_pin:
                st.session_state.flash_message = {
                    "type": "danger",
                    "title": "PIN Mismatch",
                    "text": "The new PIN and confirmation PIN do not match."
                }
                st.rerun()
            else:
                if account.change_pin(old_pin, new_pin):
                    st.session_state.flash_message = {
                        "type": "success",
                        "title": "PIN Updated Successfully",
                        "text": "Your security PIN has been updated. Please use the new PIN for future logins."
                    }
                    st.session_state.account = account
                    st.rerun()
                else:
                    st.session_state.flash_message = {
                        "type": "danger",
                        "title": "Authentication Failed",
                        "text": "Incorrect current PIN. Please verify and try again."
                    }
                    st.rerun()


# ============================================================
# 7. AUTHENTICATION (LOGIN SCREEN)
# ============================================================

def login_page() -> None:
    """Clean, centered, vertically optimized login interface."""
    _, center_col, _ = st.columns([1, 1.6, 1])

    with center_col:
        st.html(
            """
            <div class="login-wrapper-box">
                <div class="login-brand-icon">🏧</div>
                <div class="login-title">ATM Banking</div>
                <div class="login-subtitle">Secure Digital Banking System</div>
            </div>
            """
        )

        render_flash_message()

        with st.form("login_form", clear_on_submit=False):
            pin = st.text_input(
                "Enter your 4-digit PIN",
                type="password",
                max_chars=4,
                placeholder="••••",
                label_visibility="visible"
            )
            submit_login = st.form_submit_button("Login Securely", type="primary", use_container_width=True)

            if submit_login:
                if not pin or len(pin) != 4 or not pin.isdigit():
                    st.session_state.flash_message = {
                        "type": "danger",
                        "title": "Invalid PIN Format",
                        "text": "Please enter a valid 4-digit numeric PIN (e.g. 1234)."
                    }
                    st.rerun()
                else:
                    account = load_account_from_db()
                    if account and pin == account.pin:
                        st.session_state.logged_in = True
                        st.session_state.account = account
                        st.session_state.current_page = "dashboard"
                        st.session_state.flash_message = None
                        st.rerun()
                    else:
                        st.session_state.flash_message = {
                            "type": "danger",
                            "title": "Access Denied",
                            "text": "Incorrect PIN. Please try again."
                        }
                        st.rerun()

        st.html(
            """
            <div style="text-align:center; margin-top: 1rem;">
                <span style="font-size:0.78rem; color:#6B7280;">🔒 256-bit Encrypted Session • Default PIN: <b>1234</b></span>
            </div>
            """
        )


# ============================================================
# 8. ROUTING CONTROLLER
# ============================================================

def main() -> None:
    """Main application routing controller."""
    if not st.session_state.logged_in or st.session_state.account is None:
        login_page()
    else:
        render_sidebar()

        page = st.session_state.current_page
        if page == "dashboard":
            dashboard_page()
        elif page == "balance":
            balance_view_page()
        elif page == "withdraw":
            withdraw_page()
        elif page == "deposit":
            deposit_page()
        elif page == "transactions":
            transactions_page()
        elif page == "change_pin":
            change_pin_page()
        else:
            dashboard_page()


if __name__ == "__main__":
    main()