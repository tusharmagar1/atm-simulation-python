"""CLI Application Entrypoint for ATM Simulation.

Run with:
    python main.py
"""

import sys
from database import Database
from account import Account
from atm import ATM


def main() -> None:
    """Initializes and runs the CLI ATM simulation."""
    print("==========================================")
    print("       🏧 WELCOME TO DIGITAL ATM")
    print("==========================================")

    # Initialize SQLite database
    database = Database()

    # Load account record from database
    account_data = database.get_account()

    if account_data:
        account_id, pin, balance = account_data

        # Instantiate Account domain model
        account = Account(
            account_id=account_id,
            pin=pin,
            balance=balance,
            database=database
        )

        # Initialize ATM terminal interface
        atm = ATM(account)

        # Authenticate and open main menu
        if atm.login():
            atm.menu()
    else:
        print("❌ Error: No bank account found in database.")
        print("Please check database configuration.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSession terminated. Goodbye! 👋")
        sys.exit(0)