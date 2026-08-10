"""Unit tests for the Account domain model and banking operations."""

import math
import os
import tempfile
import unittest

from account import Account
from database import Database


class TestAccount(unittest.TestCase):
    """Test suite for Account balance checks, deposits, withdrawals, and PIN changes."""

    def setUp(self) -> None:
        """Create an isolated test database and Account object."""
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        self.database = Database(db_name=self.db_path)

        acc_data = self.database.get_account()
        self.account = Account(
            account_id=acc_data[0],
            pin=acc_data[1],
            balance=acc_data[2],
            database=self.database
        )

    def tearDown(self) -> None:
        """Remove the temporary test database."""
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def test_initial_balance(self) -> None:
        """Verify initial balance is ₹10,000.00."""
        self.assertEqual(self.account.check_balance(), 10000.00)

    def test_deposit_valid_amounts(self) -> None:
        """Test depositing standard positive denominations."""
        # Deposit ₹5,000
        self.assertTrue(self.account.deposit(5000.0))
        self.assertEqual(self.account.check_balance(), 15000.00)

        # Deposit ₹1,000
        self.assertTrue(self.account.deposit(1000.0))
        self.assertEqual(self.account.check_balance(), 16000.00)

        # Verify transaction log in DB
        txs = self.account.get_transactions()
        self.assertEqual(len(txs), 2)
        self.assertEqual(txs[0][0], "Deposit")
        self.assertEqual(txs[0][1], 1000.0)
        self.assertEqual(txs[0][2], 16000.0)

    def test_deposit_zero_and_negative(self) -> None:
        """Reject deposits of ₹0 and negative amounts."""
        self.assertFalse(self.account.deposit(0))
        self.assertEqual(self.account.check_balance(), 10000.00)

        self.assertFalse(self.account.deposit(-100))
        self.assertEqual(self.account.check_balance(), 10000.00)

        self.assertFalse(self.account.deposit(-0.01))
        self.assertEqual(self.account.check_balance(), 10000.00)

        # Ensure no transactions were created
        self.assertEqual(len(self.account.get_transactions()), 0)

    def test_deposit_invalid_types_and_values(self) -> None:
        """Reject NaN, inf, strings, None without crashing."""
        self.assertFalse(self.account.deposit(float("nan")))
        self.assertFalse(self.account.deposit(float("inf")))
        self.assertFalse(self.account.deposit("abc"))
        self.assertFalse(self.account.deposit(None))
        self.assertFalse(self.account.deposit(True))
        self.assertEqual(self.account.check_balance(), 10000.00)

    def test_withdraw_valid_amounts(self) -> None:
        """Test standard valid withdrawals."""
        self.assertTrue(self.account.withdraw(2000.0))
        self.assertEqual(self.account.check_balance(), 8000.00)

        self.assertTrue(self.account.withdraw(500.0))
        self.assertEqual(self.account.check_balance(), 7500.00)

        txs = self.account.get_transactions()
        self.assertEqual(len(txs), 2)
        self.assertEqual(txs[0][0], "Withdrawal")
        self.assertEqual(txs[0][1], 500.0)
        self.assertEqual(txs[0][2], 7500.0)

    def test_withdraw_insufficient_funds(self) -> None:
        """Reject withdrawal exceeding available balance."""
        self.assertFalse(self.account.withdraw(15000.0))
        self.assertEqual(self.account.check_balance(), 10000.00)
        self.assertEqual(len(self.account.get_transactions()), 0)

    def test_withdraw_zero_and_negative(self) -> None:
        """Reject ₹0 and negative withdrawals."""
        self.assertFalse(self.account.withdraw(0))
        self.assertFalse(self.account.withdraw(-500))
        self.assertEqual(self.account.check_balance(), 10000.00)
        self.assertEqual(len(self.account.get_transactions()), 0)

    def test_withdraw_invalid_types(self) -> None:
        """Reject invalid types in withdrawal."""
        self.assertFalse(self.account.withdraw("invalid"))
        self.assertFalse(self.account.withdraw(None))
        self.assertFalse(self.account.withdraw(float("nan")))
        self.assertFalse(self.account.withdraw(float("inf")))
        self.assertEqual(self.account.check_balance(), 10000.00)

    def test_change_pin_success(self) -> None:
        """Verify successful PIN change with correct old PIN and valid 4-digit format."""
        self.assertTrue(self.account.change_pin("1234", "5678"))
        self.assertEqual(self.account.pin, "5678")

        # Verify persisted in SQLite
        db_acc = self.database.get_account(self.account.account_id)
        self.assertEqual(db_acc[1], "5678")

    def test_change_pin_wrong_old_pin(self) -> None:
        """Reject PIN change when old PIN is incorrect."""
        self.assertFalse(self.account.change_pin("9999", "5678"))
        self.assertEqual(self.account.pin, "1234")

    def test_change_pin_invalid_formats(self) -> None:
        """Reject PIN changes with invalid length or non-digits."""
        self.assertFalse(self.account.change_pin("1234", "123"))     # 3 digits
        self.assertFalse(self.account.change_pin("1234", "12345"))   # 5 digits
        self.assertFalse(self.account.change_pin("1234", "abcd"))    # alpha
        self.assertFalse(self.account.change_pin("1234", "12a4"))    # alphanumeric
        self.assertFalse(self.account.change_pin("1234", ""))        # empty
        self.assertEqual(self.account.pin, "1234")

    def test_sequential_deposit_and_withdrawal_flow(self) -> None:
        """Verify full user scenario: Deposit ₹5000 -> Withdraw ₹2000 -> Deposit ₹1000."""
        self.assertTrue(self.account.deposit(5000.0))    # Balance: 15,000
        self.assertTrue(self.account.withdraw(2000.0))   # Balance: 13,000
        self.assertTrue(self.account.deposit(1000.0))    # Balance: 14,000

        self.assertEqual(self.account.check_balance(), 14000.00)

        txs = self.account.get_transactions()
        self.assertEqual(len(txs), 3)

        # 1st in list = latest (Deposit 1000, balance 14000)
        self.assertEqual(txs[0][0], "Deposit")
        self.assertEqual(txs[0][1], 1000.0)
        self.assertEqual(txs[0][2], 14000.0)

        # 2nd in list = Withdrawal 2000, balance 13000
        self.assertEqual(txs[1][0], "Withdrawal")
        self.assertEqual(txs[1][1], 2000.0)
        self.assertEqual(txs[1][2], 13000.0)

        # 3rd in list = Deposit 5000, balance 15000
        self.assertEqual(txs[2][0], "Deposit")
        self.assertEqual(txs[2][1], 5000.0)
        self.assertEqual(txs[2][2], 15000.0)


if __name__ == "__main__":
    unittest.main()
