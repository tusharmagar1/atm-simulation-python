"""Unit tests for the CLI ATM interface."""

import io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

from account import Account
from atm import ATM
from database import Database


class TestATM(unittest.TestCase):
    """Test suite for CLI ATM interactions and menu operations."""

    def setUp(self) -> None:
        """Create a temporary database and ATM instance."""
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
        self.atm = ATM(self.account)

    def tearDown(self) -> None:
        """Clean up the test database file."""
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    @patch("builtins.input", side_effect=["1234"])
    def test_login_success(self, mock_input) -> None:
        """Verify CLI login succeeds with correct PIN."""
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            result = self.atm.login()
            self.assertTrue(result)
            self.assertIn("Login successful", fake_out.getvalue())

    @patch("builtins.input", side_effect=["9999"])
    def test_login_failure(self, mock_input) -> None:
        """Verify CLI login fails with incorrect PIN."""
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            result = self.atm.login()
            self.assertFalse(result)
            self.assertIn("Invalid PIN", fake_out.getvalue())

    def test_check_balance(self) -> None:
        """Verify CLI check balance output."""
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.atm.check_balance()
            self.assertIn("10,000.00", fake_out.getvalue())

    @patch("builtins.input", side_effect=["2000"])
    def test_withdraw_cli_success(self, mock_input) -> None:
        """Verify CLI withdrawal transaction."""
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.atm.withdraw()
            self.assertEqual(self.account.check_balance(), 8000.00)
            self.assertIn("Withdrawal successful", fake_out.getvalue())

    @patch("builtins.input", side_effect=["5000"])
    def test_deposit_cli_success(self, mock_input) -> None:
        """Verify CLI deposit transaction."""
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.atm.deposit()
            self.assertEqual(self.account.check_balance(), 15000.00)
            self.assertIn("Deposit successful", fake_out.getvalue())

    @patch("builtins.input", side_effect=["1234", "5678", "5678"])
    def test_change_pin_cli_success(self, mock_input) -> None:
        """Verify CLI PIN change."""
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.atm.change_pin()
            self.assertEqual(self.account.pin, "5678")
            self.assertIn("PIN changed successfully", fake_out.getvalue())

    def test_show_transactions_cli(self) -> None:
        """Verify CLI transaction history printout."""
        self.account.deposit(1000.0)
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.atm.show_transactions()
            self.assertIn("TRANSACTION HISTORY", fake_out.getvalue())
            self.assertIn("DEPOSIT", fake_out.getvalue())
            self.assertIn("1,000.00", fake_out.getvalue())


if __name__ == "__main__":
    unittest.main()
