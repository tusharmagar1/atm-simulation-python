import sqlite3


class Database:

    def __init__(self, db_name="atm.db"):
        self.db_name = db_name
        self.create_tables()
        self.create_default_account()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):

        connection = self.connect()
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
            )
        """)

        connection.commit()
        connection.close()

    def create_default_account(self):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM accounts")

        count = cursor.fetchone()[0]

        if count == 0:

            cursor.execute("""
                INSERT INTO accounts (pin, balance)
                VALUES (?, ?)
            """, ("1234", 10000))

            connection.commit()

        connection.close()

    def get_account(self):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, pin, balance
            FROM accounts
            LIMIT 1
        """)

        account = cursor.fetchone()

        connection.close()

        return account

    def update_balance(self, account_id, balance):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE id = ?
        """, (balance, account_id))

        connection.commit()
        connection.close()

    def update_pin(self, account_id, new_pin):

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE accounts
            SET pin = ?
            WHERE id = ?
        """, (new_pin, account_id))

        connection.commit()
        connection.close()

    def add_transaction(
        self,
        account_id,
        transaction_type,
        amount,
        balance_after
    ):

        connection = self.connect()
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
            amount,
            balance_after
        ))

        connection.commit()
        connection.close()

    def get_transactions(self, account_id):

        connection = self.connect()
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

        transactions = cursor.fetchall()

        connection.close()

        return transactions