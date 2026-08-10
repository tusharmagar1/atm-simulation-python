"""Unit tests for the Database persistence layer."""

import os
import tempfile
import unittest
from database import Database


class TestDatabase(unittest.TestCase):
    """Test suite for SQLite Database operations and atomicity."""

    def setUp(self) -> None:
        """Create a temporary database file for isolated testing."""
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        self.database = Database(db_name=self.db_path)

    def tearDown(self) -> None:
        """Clean up the temporary database file after tests."""
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def test_default_account_creation(self) -> None:
        """Verify default account is seeded with 1234 PIN and ₹10,000 balance."""
        account_data = self.database.get_account()
        self.assertIsNotNone(account_data)
        acc_id, pin, balance = account_data
        self.assertEqual(acc_id, 1)
        self.assertEqual(pin, "1234")
        self.assertEqual(balance, 10000.00)

    def test_get_account_by_id(self) -> None:
        """Verify account retrieval by explicit account ID."""
        account_data = self.database.get_account_by_id(1)
        self.assertIsNotNone(account_data)
        self.assertEqual(account_data[0], 1)

        # Non-existent account
        non_existent = self.database.get_account_by_id(999)
        self.assertIsNone(non_existent)

    def test_update_balance(self) -> None:
        """Verify balance update in database."""
        success = self.database.update_balance(1, 15000.50)
        self.assertTrue(success)

        account = self.database.get_account(1)
        self.assertEqual(account[2], 15000.50)

    def test_update_pin(self) -> None:
        """Verify PIN update in database."""
        success = self.database.update_pin(1, "4321")
        self.assertTrue(success)

        account = self.database.get_account(1)
        self.assertEqual(account[1], "4321")

    def test_add_and_retrieve_transactions(self) -> None:
        """Verify transaction logging and reverse-chronological ordering."""
        self.database.add_transaction(1, "Deposit", 5000.0, 15000.0)
        self.database.add_transaction(1, "Withdrawal", 2000.0, 13000.0)

        transactions = self.database.get_transactions(1)
        self.assertEqual(len(transactions), 2)

        # Most recent transaction should appear first (Withdrawal)
        self.assertEqual(transactions[0][0], "Withdrawal")
        self.assertEqual(transactions[0][1], 2000.0)
        self.assertEqual(transactions[0][2], 13000.0)

        # Older transaction (Deposit)
        self.assertEqual(transactions[1][0], "Deposit")
        self.assertEqual(transactions[1][1], 5000.0)
        self.assertEqual(transactions[1][2], 15000.0)

    def test_atomic_record_transaction(self) -> None:
        """Verify atomic transaction operation updates balance and logs history together."""
        success = self.database.record_transaction(1, "Deposit", 1000.0, 11000.0)
        self.assertTrue(success)

        account = self.database.get_account(1)
        self.assertEqual(account[2], 11000.0)

        txs = self.database.get_transactions(1)
        self.assertEqual(len(txs), 1)
        self.assertEqual(txs[0][0], "Deposit")
        self.assertEqual(txs[0][1], 1000.0)
        self.assertEqual(txs[0][2], 11000.0)

    def test_atomic_record_transaction_invalid_account(self) -> None:
        """Verify atomic transaction fails safely for non-existent account."""
        success = self.database.record_transaction(999, "Deposit", 500.0, 500.0)
        self.assertFalse(success)

    def test_database_persistence_across_reconnects(self) -> None:
        """Verify data persists when database is reopened."""
        self.database.record_transaction(1, "Deposit", 5000.0, 15000.0)
        self.database.update_pin(1, "9876")

        # Open new database instance pointing to the same file
        new_db_instance = Database(db_name=self.db_path)
        account = new_db_instance.get_account(1)
        self.assertEqual(account[1], "9876")
        self.assertEqual(account[2], 15000.0)

        txs = new_db_instance.get_transactions(1)
        self.assertEqual(len(txs), 1)


if __name__ == "__main__":
    unittest.main()
