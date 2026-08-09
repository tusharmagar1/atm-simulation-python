class ATM:

    def __init__(self, account):
        self.account = account

    def login(self):

        pin = input("\nEnter your PIN: ")

        if pin == self.account.pin:

            print("\n✅ Login successful!")

            return True

        print("\n❌ Invalid PIN!")

        return False

    def menu(self):

        while True:

            print("\n==============================")
            print("          🏧 ATM MENU")
            print("==============================")

            print("1. Check Balance")
            print("2. Withdraw Money")
            print("3. Deposit Money")
            print("4. Change PIN")
            print("5. Transaction History")
            print("6. Exit")

            choice = input("\nEnter your choice: ")

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

                print("\nThank you for using our ATM! 👋")

                break

            else:

                print("\n❌ Invalid choice.")

    def check_balance(self):

        balance = self.account.check_balance()

        print("\n==============================")
        print("        💰 BALANCE")
        print("==============================")

        print(f"Current Balance: ₹{balance:.2f}")

    def withdraw(self):

        try:

            amount = float(
                input("\nEnter withdrawal amount: ₹")
            )

            if self.account.withdraw(amount):

                print("\n✅ Withdrawal successful!")

                print(
                    f"Amount: ₹{amount:.2f}"
                )

                print(
                    f"Remaining Balance: "
                    f"₹{self.account.balance:.2f}"
                )

            else:

                print("\n❌ Withdrawal failed.")

                print(
                    "Check the amount or your balance."
                )

        except ValueError:

            print("\n❌ Please enter a valid number.")

    def deposit(self):

        try:

            amount = float(
                input("\nEnter deposit amount: ₹")
            )

            if self.account.deposit(amount):

                print("\n✅ Deposit successful!")

                print(
                    f"Amount: ₹{amount:.2f}"
                )

                print(
                    f"New Balance: "
                    f"₹{self.account.balance:.2f}"
                )

            else:

                print("\n❌ Invalid deposit amount.")

        except ValueError:

            print("\n❌ Please enter a valid number.")

    def change_pin(self):

        old_pin = input(
            "\nEnter current PIN: "
        )

        new_pin = input(
            "Enter new 4-digit PIN: "
        )

        if self.account.change_pin(
            old_pin,
            new_pin
        ):

            print(
                "\n✅ PIN changed successfully."
            )

        else:

            print(
                "\n❌ PIN change failed."
            )

            print(
                "Check your old PIN or "
                "new PIN format."
            )

    def show_transactions(self):

        print("\n==========================================")
        print("           🧾 TRANSACTION HISTORY")
        print("==========================================")

        transactions = (
            self.account.get_transactions()
        )

        if not transactions:

            print("No transactions yet.")

        else:

            for i, transaction in enumerate(
                transactions,
                start=1
            ):

                transaction_type = transaction[0]
                amount = transaction[1]
                balance_after = transaction[2]
                created_at = transaction[3]

                if transaction_type == "Deposit":

                    symbol = "+"

                else:

                    symbol = "-"

                print(
                    f"\n{i}. {transaction_type}"
                )

                print(
                    f"   Amount: "
                    f"{symbol}₹{amount:.2f}"
                )

                print(
                    f"   Balance: "
                    f"₹{balance_after:.2f}"
                )

                print(
                    f"   Date: "
                    f"{created_at}"
                )

        print("\n==========================================")