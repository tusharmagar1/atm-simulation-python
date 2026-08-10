"""CLI interface for the ATM Simulation system.

Provides interactive terminal-based authentication, balance inquiries,
deposits, withdrawals, PIN management, and transaction history review.
"""

import sys
from account import Account


class ATM:
    """Terminal-based ATM interface handler."""

    def __init__(self, account: Account) -> None:
        """Initializes ATM with an authenticated or active account object.

        Args:
            account: Account domain model instance.
        """
        self.account = account

    def login(self) -> bool:
        """Prompts the user for a 4-digit PIN and verifies authentication.

        Returns:
            True if login succeeded, False otherwise.
        """
        try:
            pin = input("\nEnter your 4-digit PIN: ").strip()

            if pin == self.account.pin:
                print("\n✅ Login successful! Welcome to Digital ATM.")
                return True

            print("\n❌ Invalid PIN! Access denied.")
            return False
        except (KeyboardInterrupt, EOFError):
            print("\n\nOperation cancelled. Goodbye! 👋")
            return False

    def menu(self) -> None:
        """Runs the main terminal menu loop for ATM operations."""
        while True:
            try:
                print("\n==============================")
                print("          🏧 ATM MENU")
                print("==============================")
                print("1. Check Balance")
                print("2. Withdraw Money")
                print("3. Deposit Money")
                print("4. Change PIN")
                print("5. Transaction History")
                print("6. Exit")
                print("==============================")

                choice = input("\nEnter your choice (1-6): ").strip()

                if choice == "1":
                    self.check_balance()
                elif choice == "2":
                    self.withdraw()
                elif choice == "3":
                    self.deposit()
                elif choice == "4":
                    self.change_pin()
                elif choice == "5":
                    self.show_transactions()
                elif choice == "6":
                    print("\nThank you for banking with us! Have a great day! 👋\n")
                    break
                else:
                    print("\n❌ Invalid choice! Please select an option between 1 and 6.")
            except (KeyboardInterrupt, EOFError):
                print("\n\nSession terminated. Goodbye! 👋\n")
                break

    def check_balance(self) -> None:
        """Displays current available account balance."""
        balance = self.account.check_balance()
        print("\n==============================")
        print("        💰 BALANCE")
        print("==============================")
        print(f"Current Available Balance: ₹{balance:,.2f}")
        print("==============================")

    def withdraw(self) -> None:
        """Prompts for withdrawal amount and performs withdrawal transaction."""
        try:
            amount_input = input("\nEnter withdrawal amount: ₹").strip()
            amount = float(amount_input)

            if amount <= 0:
                print("\n❌ Invalid amount. Withdrawal amount must be greater than ₹0.")
                return

            if self.account.withdraw(amount):
                print("\n✅ Withdrawal successful!")
                print(f"Amount Withdrawn: ₹{amount:,.2f}")
                print(f"Remaining Balance: ₹{self.account.balance:,.2f}")
            else:
                if amount > self.account.balance:
                    print("\n❌ Withdrawal failed: Insufficient funds.")
                    print(f"Your current balance is: ₹{self.account.balance:,.2f}")
                else:
                    print("\n❌ Withdrawal failed. Please verify the amount.")
        except ValueError:
            print("\n❌ Please enter a valid numerical amount.")
        except (KeyboardInterrupt, EOFError):
            print("\n\nOperation cancelled.")

    def deposit(self) -> None:
        """Prompts for deposit amount and performs deposit transaction."""
        try:
            amount_input = input("\nEnter deposit amount: ₹").strip()
            amount = float(amount_input)

            if amount <= 0:
                print("\n❌ Invalid deposit amount. Must be greater than ₹0.")
                return

            if self.account.deposit(amount):
                print("\n✅ Deposit successful!")
                print(f"Amount Deposited: ₹{amount:,.2f}")
                print(f"New Balance: ₹{self.account.balance:,.2f}")
            else:
                print("\n❌ Deposit failed. Please enter a valid positive amount.")
        except ValueError:
            print("\n❌ Please enter a valid numerical amount.")
        except (KeyboardInterrupt, EOFError):
            print("\n\nOperation cancelled.")

    def change_pin(self) -> None:
        """Prompts for current and new PIN to update account security credentials."""
        try:
            old_pin = input("\nEnter current PIN: ").strip()
            new_pin = input("Enter new 4-digit PIN: ").strip()
            confirm_pin = input("Confirm new 4-digit PIN: ").strip()

            if new_pin != confirm_pin:
                print("\n❌ PIN change failed: New PIN and Confirmation do not match.")
                return

            if len(new_pin) != 4 or not new_pin.isdigit():
                print("\n❌ PIN change failed: New PIN must be exactly 4 numeric digits (0-9).")
                return

            if self.account.change_pin(old_pin, new_pin):
                print("\n✅ PIN changed successfully. Please remember your new PIN.")
            else:
                print("\n❌ PIN change failed. Incorrect current PIN.")
        except (KeyboardInterrupt, EOFError):
            print("\n\nOperation cancelled.")

    def show_transactions(self) -> None:
        """Displays complete reverse-chronological transaction history."""
        print("\n========================================================")
        print("               🧾 TRANSACTION HISTORY")
        print("========================================================")

        transactions = self.account.get_transactions()

        if not transactions:
            print("No transactions recorded yet.")
        else:
            for i, transaction in enumerate(transactions, start=1):
                transaction_type, amount, balance_after, created_at = transaction
                symbol = "+" if transaction_type == "Deposit" else "-"
                print(f"\n{i}. [{transaction_type.upper()}] - {created_at}")
                print(f"   Amount: {symbol}₹{amount:,.2f}")
                print(f"   Balance After: ₹{balance_after:,.2f}")

        print("========================================================")