class Account:

    def __init__(
        self,
        account_id,
        pin,
        balance,
        database
    ):

        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        self.database = database

    def check_balance(self):

        return self.balance

    def deposit(self, amount):

        if amount <= 0:
            return False

        self.balance += amount

        # Save balance
        self.database.update_balance(
            self.account_id,
            self.balance
        )

        # Save transaction
        self.database.add_transaction(
            self.account_id,
            "Deposit",
            amount,
            self.balance
        )

        return True

    def withdraw(self, amount):

        if amount <= 0:
            return False

        if amount > self.balance:
            return False

        self.balance -= amount

        # Save balance
        self.database.update_balance(
            self.account_id,
            self.balance
        )

        # Save transaction
        self.database.add_transaction(
            self.account_id,
            "Withdrawal",
            amount,
            self.balance
        )

        return True

    def change_pin(self, old_pin, new_pin):

        if old_pin != self.pin:
            return False

        if len(new_pin) != 4:
            return False

        if not new_pin.isdigit():
            return False

        self.pin = new_pin

        # Save new PIN
        self.database.update_pin(
            self.account_id,
            new_pin
        )

        return True

    def get_transactions(self):

        return self.database.get_transactions(
            self.account_id
        )