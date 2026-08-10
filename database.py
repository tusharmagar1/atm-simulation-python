"""Database management layer for the ATM Simulation system.

Handles SQLite connections, schema initialization, default account seeding,
atomic transaction processing, and data persistence with foreign key constraints.
"""

import sqlite3
from typing import Any, List, Optional, Tuple


class Database:
    """Manages SQLite database operations for the ATM system."""

    def __init__(self, db_name: str = "atm.db") -> None:
        """Initializes the database connection parameters and schema.

        Args:
            db_name: Filepath of the SQLite database file.
        """
        self.db_name = db_name
        self.create_tables()
        self.create_default_account()

    def connect(self) -> sqlite3.Connection:
        """Creates and returns an active SQLite connection with foreign keys enabled.

        Returns:
            An active sqlite3.Connection object.
        """
        connection = sqlite3.connect(
            self.db_name,
            timeout=10.0,
            check_same_thread=False
        )
        # Enforce foreign key constraints in SQLite
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection

    def create_tables(self) -> None:
        """Creates accounts and transactions tables if they do not already exist."""
        with self.connect() as connection:
            cursor = connection.cursor()

            # Accounts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pin TEXT NOT NULL,
                    balance REAL NOT NULL
                )
            """)

            # Transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    balance_after REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id)
                        REFERENCES accounts(id)
                        ON DELETE CASCADE
                )
            """)

            connection.commit()

    def create_default_account(self) -> None:
        """Seeds the initial default account if no accounts currently exist."""
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM accounts")
            result = cursor.fetchone()
            count = result[0] if result else 0

            if count == 0:
                cursor.execute("""
                    INSERT INTO accounts (pin, balance)
                    VALUES (?, ?)
                """, ("1234", 10000.00))
                connection.commit()

    def get_account(self, account_id: Optional[int] = None) -> Optional[Tuple[int, str, float]]:
        """Retrieves account details by ID or fetches the default first account.

        Args:
            account_id: Optional account ID to query.

        Returns:
            Tuple of (id, pin, balance) if found, else None.
        """
        with self.connect() as connection:
            cursor = connection.cursor()
            if account_id is not None:
                cursor.execute("""
                    SELECT id, pin, balance
                    FROM accounts
                    WHERE id = ?
                    LIMIT 1
                """, (account_id,))
            else:
                cursor.execute("""
                    SELECT id, pin, balance
                    FROM accounts
                    ORDER BY id ASC
                    LIMIT 1
                """)
            account = cursor.fetchone()
            if account:
                return (account[0], str(account[1]), round(float(account[2]), 2))
            return None

    def get_account_by_id(self, account_id: int) -> Optional[Tuple[int, str, float]]:
        """Convenience method to retrieve account by explicit account ID.

        Args:
            account_id: Unique account identifier.

        Returns:
            Tuple of (id, pin, balance) if found, else None.
        """
        return self.get_account(account_id=account_id)

    def update_balance(self, account_id: int, balance: float) -> bool:
        """Updates the account balance in SQLite.

        Args:
            account_id: Unique account ID.
            balance: New numerical balance.

        Returns:
            True if update was successful, False otherwise.
        """
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE accounts
                    SET balance = ?
                    WHERE id = ?
                """, (round(float(balance), 2), account_id))
                connection.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def update_pin(self, account_id: int, new_pin: str) -> bool:
        """Updates the 4-digit security PIN for an account.

        Args:
            account_id: Unique account ID.
            new_pin: String representation of the 4-digit PIN.

        Returns:
            True if update succeeded, False otherwise.
        """
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE accounts
                    SET pin = ?
                    WHERE id = ?
                """, (str(new_pin).strip(), account_id))
                connection.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def add_transaction(
        self,
        account_id: int,
        transaction_type: str,
        amount: float,
        balance_after: float
    ) -> bool:
        """Inserts a transaction record for an account.

        Args:
            account_id: Unique account ID.
            transaction_type: "Deposit" or "Withdrawal".
            amount: Transaction numerical amount.
            balance_after: Resulting balance after transaction.

        Returns:
            True if inserted successfully, False otherwise.
        """
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO transactions (
                        account_id,
                        transaction_type,
                        amount,
                        balance_after
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    account_id,
                    transaction_type,
                    round(float(amount), 2),
                    round(float(balance_after), 2)
                ))
                connection.commit()
                return True
        except sqlite3.Error:
            return False

    def record_transaction(
        self,
        account_id: int,
        transaction_type: str,
        amount: float,
        new_balance: float
    ) -> bool:
        """Executes an atomic balance update and transaction logging operation.

        Uses an explicit SQLite transaction to guarantee that the balance update
        and transaction history entry succeed or fail together.

        Args:
            account_id: Account ID.
            transaction_type: 'Deposit' or 'Withdrawal'.
            amount: Amount transacted.
            new_balance: New account balance.

        Returns:
            True if both operations succeed atomically, False otherwise.
        """
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                # 1. Update account balance
                cursor.execute("""
                    UPDATE accounts
                    SET balance = ?
                    WHERE id = ?
                """, (round(float(new_balance), 2), account_id))

                if cursor.rowcount == 0:
                    connection.rollback()
                    return False

                # 2. Insert transaction entry
                cursor.execute("""
                    INSERT INTO transactions (
                        account_id,
                        transaction_type,
                        amount,
                        balance_after
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    account_id,
                    transaction_type,
                    round(float(amount), 2),
                    round(float(new_balance), 2)
                ))

                connection.commit()
                return True
        except sqlite3.Error:
            return False

    def get_transactions(self, account_id: int) -> List[Tuple[str, float, float, str]]:
        """Fetches all transactions for an account in reverse chronological order.

        Args:
            account_id: Unique account ID.

        Returns:
            List of tuples (transaction_type, amount, balance_after, created_at).
        """
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT
                        transaction_type,
                        amount,
                        balance_after,
                        created_at
                    FROM transactions
                    WHERE account_id = ?
                    ORDER BY id DESC
                """, (account_id,))
                rows = cursor.fetchall()
                return [
                    (
                        str(row[0]),
                        round(float(row[1]), 2),
                        round(float(row[2]), 2),
                        str(row[3])
                    )
                    for row in rows
                ]
        except sqlite3.Error:
            return []