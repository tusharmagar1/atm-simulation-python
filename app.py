import streamlit as st

from database import Database
from account import Account


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ATM Simulation",
    page_icon="🏧",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

    .atm-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .atm-subtitle {
        text-align: center;
        color: #888888;
        margin-bottom: 30px;
    }

    .balance-card {
        padding: 32px;
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            #111827,
            #1f2937
        );
        color: white;
        text-align: center;
        margin: 20px 0;
    }

    .balance-label {
        font-size: 15px;
        color: #d1d5db;
        letter-spacing: 2px;
        font-weight: 500;
    }

    .balance-value {
        font-size: 42px;
        font-weight: 700;
        margin-top: 10px;
    }

    .transaction-card {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #dddddd;
        margin-bottom: 12px;
    }

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# DATABASE
# ============================================================

database = Database()


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None


# ============================================================
# LOAD ACCOUNT
# ============================================================

def load_account():

    account_data = database.get_account()

    if account_data:

        account_id = account_data[0]
        pin = account_data[1]
        balance = account_data[2]

        return Account(
            account_id=account_id,
            pin=pin,
            balance=balance,
            database=database
        )

    return None


# ============================================================
# LOGIN
# ============================================================

def login_page():

    st.markdown(
        '<div class="atm-title">🏧 ATM Simulation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="atm-subtitle">Secure Digital Banking</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("🔐 ATM Login")

    pin = st.text_input(
        "Enter your PIN",
        type="password",
        max_chars=4,
        placeholder="Enter 4-digit PIN"
    )

    if st.button(
        "🔓 Login",
        use_container_width=True,
        type="primary"
    ):

        account = load_account()

        if account and pin == account.pin:

            st.session_state.logged_in = True
            st.session_state.account = account

            st.success("Login successful!")

            st.rerun()

        else:

            st.error("❌ Invalid PIN")


# ============================================================
# BALANCE
# ============================================================

def show_balance():

    account = st.session_state.account

    # IMPORTANT:
    # st.html() renders HTML directly.
    # It will NOT turn the HTML into a Markdown code block.

    st.html(
        f"""
        <div class="balance-card">

            <div class="balance-label">
                AVAILABLE BALANCE
            </div>

            <div class="balance-value">
                ₹{account.balance:,.2f}
            </div>

        </div>
        """
    )


# ============================================================
# WITHDRAW
# ============================================================

def withdraw_page():

    account = st.session_state.account

    st.subheader("💸 Withdraw Money")

    amount = st.number_input(
        "Enter withdrawal amount",
        min_value=1.0,
        step=500.0,
        format="%.2f"
    )

    if st.button(
        "Withdraw",
        use_container_width=True,
        type="primary"
    ):

        if account.withdraw(amount):

            st.success(
                f"₹{amount:,.2f} withdrawn successfully!"
            )

            st.session_state.account = account

            st.rerun()

        else:

            st.error(
                "❌ Withdrawal failed. "
                "Check your balance."
            )


# ============================================================
# DEPOSIT
# ============================================================

def deposit_page():

    account = st.session_state.account

    st.subheader("💵 Deposit Money")

    amount = st.number_input(
        "Enter deposit amount",
        min_value=1.0,
        step=500.0,
        format="%.2f"
    )

    if st.button(
        "Deposit",
        use_container_width=True,
        type="primary"
    ):

        if account.deposit(amount):

            st.success(
                f"₹{amount:,.2f} deposited successfully!"
            )

            st.session_state.account = account

            st.rerun()

        else:

            st.error("❌ Invalid deposit amount.")


# ============================================================
# TRANSACTIONS
# ============================================================

def transaction_page():

    account = st.session_state.account

    st.subheader("🧾 Transaction History")

    transactions = account.get_transactions()

    if not transactions:

        st.info("No transactions yet.")

        return

    for transaction in transactions:

        transaction_type = transaction[0]
        amount = transaction[1]
        balance_after = transaction[2]
        created_at = transaction[3]

        if transaction_type == "Deposit":

            icon = "💵"
            sign = "+"

        else:

            icon = "💸"
            sign = "-"

        st.html(
            f"""
            <div class="transaction-card">

                <b>{icon} {transaction_type}</b>

                <br><br>

                Amount:
                <b>{sign}₹{amount:,.2f}</b>

                <br>

                Balance:
                ₹{balance_after:,.2f}

                <br>

                <small>{created_at}</small>

            </div>
            """
        )


# ============================================================
# CHANGE PIN
# ============================================================

def change_pin_page():

    account = st.session_state.account

    st.subheader("🔑 Change PIN")

    old_pin = st.text_input(
        "Current PIN",
        type="password",
        max_chars=4
    )

    new_pin = st.text_input(
        "New PIN",
        type="password",
        max_chars=4
    )

    confirm_pin = st.text_input(
        "Confirm New PIN",
        type="password",
        max_chars=4
    )

    if st.button(
        "Change PIN",
        use_container_width=True,
        type="primary"
    ):

        if len(new_pin) != 4 or not new_pin.isdigit():

            st.error(
                "❌ New PIN must contain exactly 4 digits."
            )

            return

        if new_pin != confirm_pin:

            st.error(
                "❌ New PINs do not match."
            )

            return

        if account.change_pin(
            old_pin,
            new_pin
        ):

            st.success(
                "✅ PIN changed successfully!"
            )

            st.session_state.account = account

        else:

            st.error(
                "❌ Current PIN is incorrect."
            )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    st.markdown(
        '<div class="atm-title">🏧 ATM Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="atm-subtitle">Welcome back</div>',
        unsafe_allow_html=True
    )

    menu = st.radio(
        "Select Operation",
        [
            "💰 Balance",
            "💸 Withdraw",
            "💵 Deposit",
            "🧾 Transactions",
            "🔑 Change PIN"
        ],
        horizontal=True
    )

    st.divider()

    # --------------------------------------------------------
    # SELECTED OPERATION
    # --------------------------------------------------------

    if menu == "💰 Balance":

        show_balance()

    elif menu == "💸 Withdraw":

        show_balance()

        st.divider()

        withdraw_page()

    elif menu == "💵 Deposit":

        show_balance()

        st.divider()

        deposit_page()

    elif menu == "🧾 Transactions":

        show_balance()

        st.divider()

        transaction_page()

    elif menu == "🔑 Change PIN":

        change_pin_page()

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.account = None

        st.rerun()


# ============================================================
# MAIN APPLICATION
# ============================================================

if st.session_state.logged_in:

    dashboard()

else:

    login_page()