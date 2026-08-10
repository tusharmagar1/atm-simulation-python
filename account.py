"""Account model for the ATM Simulation system.

Encapsulates account state, business logic, balance validation, PIN management,
and integration with the database persistence layer.
"""

import math
from typing import Any, List, Tuple


class Account:
    """Represents a bank account within the ATM system."""

    def __init__(
        self,
        account_id: int,
        pin: str,
        balance: float,
        database: Any
    ) -> None:
        """Initializes account with ID, PIN, balance, and database reference.

        Args:
            account_id: Unique integer account identifier.
            pin: 4-digit numeric PIN string.
            balance: Initial account balance.
            database: Database instance for persistence.
        """
        self.account_id = int(account_id)
        self.pin = str(pin).strip()
        self.balance = round(float(balance), 2)
        self.database = database

    def check_balance(self) -> float:
        """Returns the current account balance rounded to 2 decimal places.

        Returns:
            Current balance as a float.
        """
        return round(self.balance, 2)

    def deposit(self, amount: Any) -> bool:
        """Deposits a positive numerical amount into the account.

        Validates amount type and value, executes atomic database transaction,
        and updates local instance state on success.

        Args:
            amount: Amount to deposit (int or float).

        Returns:
            True if deposit succeeded, False otherwise.
        """
        # Explicitly reject boolean types (bool is a subclass of int in Python)
        if isinstance(amount, bool):
            return False

        if not isinstance(amount, (int, float)):
            try:
                amount = float(amount)
            except (ValueError, TypeError):
                return False

        # Guard against NaN, infinity, or non-positive values
        if math.isnan(amount) or math.isinf(amount) or amount <= 0:
            return False

        clean_amount = round(float(amount), 2)
        if clean_amount <= 0:
            return False

        new_balance = round(self.balance + clean_amount, 2)

        # Atomic transaction execution via database layer
        success = self.database.record_transaction(
            account_id=self.account_id,
            transaction_type="Deposit",
            amount=clean_amount,
            new_balance=new_balance
        )

        if success:
            self.balance = new_balance
            return True

        return False

    def withdraw(self, amount: Any) -> bool:
        """Withdraws a specified amount from the account balance if funds are sufficient.

        Args:
            amount: Amount to withdraw (int or float).

        Returns:
            True if withdrawal succeeded, False otherwise.
        """
        # Explicitly reject boolean types (bool is a subclass of int in Python)
        if isinstance(amount, bool):
            return False

        if not isinstance(amount, (int, float)):
            try:
                amount = float(amount)
            except (ValueError, TypeError):
                return False

        # Guard against NaN, infinity, or non-positive values
        if math.isnan(amount) or math.isinf(amount) or amount <= 0:
            return False

        clean_amount = round(float(amount), 2)
        if clean_amount <= 0:
            return False

        if clean_amount > self.balance:
            return False

        new_balance = round(self.balance - clean_amount, 2)

        # Atomic transaction execution via database layer
        success = self.database.record_transaction(
            account_id=self.account_id,
            transaction_type="Withdrawal",
            amount=clean_amount,
            new_balance=new_balance
        )

        if success:
            self.balance = new_balance
            return True

        return False

    def change_pin(self, old_pin: Any, new_pin: Any) -> bool:
        """Changes the account's 4-digit PIN after verifying the current PIN.

        Args:
            old_pin: Current 4-digit PIN.
            new_pin: New 4-digit PIN.

        Returns:
            True if PIN was updated successfully, False otherwise.
        """
        if old_pin is None or new_pin is None:
            return False

        old_pin_str = str(old_pin).strip()
        new_pin_str = str(new_pin).strip()

        # Validate old PIN matches
        if old_pin_str != self.pin:
            return False

        # Validate new PIN format (strictly 4 digits)
        if len(new_pin_str) != 4 or not new_pin_str.isdigit():
            return False

        success = self.database.update_pin(
            account_id=self.account_id,
            new_pin=new_pin_str
        )

        if success:
            self.pin = new_pin_str
            return True

        return False

    def get_transactions(self) -> List[Tuple[str, float, float, str]]:
        """Retrieves transaction history for this account.

        Returns:
            List of transaction tuples (type, amount, balance_after, timestamp).
        """
        return self.database.get_transactions(self.account_id)