from database import Database
from account import Account
from atm import ATM


print("==============================")
print("       🏧 WELCOME TO ATM")
print("==============================")


# Create database
database = Database()


# Get account from database
account_data = database.get_account()


if account_data:

    account_id = account_data[0]
    pin = account_data[1]
    balance = account_data[2]

    # Create Account object
    account = Account(
        account_id=account_id,
        pin=pin,
        balance=balance,
        database=database
    )

    # Create ATM
    atm = ATM(account)

    # Login
    if atm.login():

        atm.menu()

else:

    print("❌ Account not found.")