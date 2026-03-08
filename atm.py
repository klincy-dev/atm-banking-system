import json
import hashlib
import datetime

DAILY_LIMIT = 10000

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# -------------------------------
# Load Users
# -------------------------------
def load_users():
    with open("users.json", "r") as file:
        return json.load(file)


# -------------------------------
# Save Users
# -------------------------------
def save_users(data):
    with open("users.json", "w") as file:
        json.dump(data, file, indent=4)


# -------------------------------
# Hash PIN
# -------------------------------
def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


# -------------------------------
# Generate Account Number
# -------------------------------
def generate_account_number(users):

    if users:
        last_acc = max(map(int, users.keys()))
        return str(last_acc + 1)
    else:
        return "1001"


# -------------------------------
# Transaction Receipt
# -------------------------------
def generate_receipt(acc_no, transaction, amount, balance):

    now = datetime.datetime.now()

    print("\n------ TRANSACTION RECEIPT ------")
    print("Account Number:", acc_no)
    print("Transaction:", transaction)
    print("Amount:", amount)
    print("Balance:", balance)
    print("Date:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("---------------------------------")


# -------------------------------
# Register
# -------------------------------
def register():

    users = load_users()

    acc_no = generate_account_number(users)

    name = input("Enter name: ")
    pin = input("Create PIN: ")
    balance = float(input("Initial deposit: "))

    users[acc_no] = {
        "name": name,
        "pin": hash_pin(pin),
        "balance": balance,
        "transactions": [],
        "daily_withdraw": 0,
        "failed_attempts": 0,
        "locked": False
    }

    save_users(users)

    print("\nAccount created successfully")
    print("Your Account Number:", acc_no)


# -------------------------------
# Login
# -------------------------------
def login():

    users = load_users()

    acc_no = input("Enter account number: ")

    if acc_no not in users:
        print("Account not found")
        return

    if users[acc_no]["locked"]:
        print("Account is locked. Contact admin.")
        return

    pin = input("Enter PIN: ")

    if users[acc_no]["pin"] == hash_pin(pin):

        print("Login successful")

        users[acc_no]["failed_attempts"] = 0
        users[acc_no]["daily_withdraw"] = 0

        save_users(users)

        atm_menu(acc_no)

    else:

        users[acc_no]["failed_attempts"] += 1

        if users[acc_no]["failed_attempts"] >= 3:
            users[acc_no]["locked"] = True
            print("Account locked after 3 incorrect attempts")

        else:
            print("Incorrect PIN")

        save_users(users)


# -------------------------------
# Check Balance
# -------------------------------
def check_balance(acc_no):

    users = load_users()

    balance = users[acc_no]["balance"]

    print("Current Balance:", balance)

    generate_receipt(acc_no, "Balance Check", 0, balance)


# -------------------------------
# Deposit
# -------------------------------
def deposit(acc_no):

    users = load_users()

    amount = float(input("Enter amount to deposit: "))

    users[acc_no]["balance"] += amount

    users[acc_no]["transactions"].append(f"Deposited {amount}")

    save_users(users)

    generate_receipt(acc_no, "Deposit", amount, users[acc_no]["balance"])


# -------------------------------
# Withdraw
# -------------------------------
def withdraw(acc_no):

    users = load_users()

    amount = float(input("Enter amount to withdraw: "))

    if users[acc_no]["daily_withdraw"] + amount > DAILY_LIMIT:
        print("Daily withdrawal limit exceeded")
        return

    if amount <= users[acc_no]["balance"]:

        users[acc_no]["balance"] -= amount
        users[acc_no]["daily_withdraw"] += amount

        users[acc_no]["transactions"].append(f"Withdrawn {amount}")

        save_users(users)

        generate_receipt(acc_no, "Withdraw", amount, users[acc_no]["balance"])

    else:
        print("Insufficient balance")


# -------------------------------
# Transaction History
# -------------------------------
def history(acc_no):

    users = load_users()

    print("\nTransaction History")

    if not users[acc_no]["transactions"]:
        print("No transactions")

    for t in users[acc_no]["transactions"]:
        print(t)


# -------------------------------
# Change PIN
# -------------------------------
def change_pin(acc_no):

    users = load_users()

    new_pin = input("Enter new PIN: ")

    users[acc_no]["pin"] = hash_pin(new_pin)

    save_users(users)

    print("PIN changed successfully")


# -------------------------------
# ATM Menu
# -------------------------------
def atm_menu(acc_no):

    while True:

        print("\n====== ATM MENU ======")
        print("1 Check Balance")
        print("2 Deposit")
        print("3 Withdraw")
        print("4 Transaction History")
        print("5 Change PIN")
        print("6 Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            check_balance(acc_no)

        elif choice == "2":
            deposit(acc_no)

        elif choice == "3":
            withdraw(acc_no)

        elif choice == "4":
            history(acc_no)

        elif choice == "5":
            change_pin(acc_no)

        elif choice == "6":
            print("Logged out successfully")
            break

        else:
            print("Invalid choice")


# -------------------------------
# View Locked Accounts
# -------------------------------
def view_locked_accounts():

    users = load_users()

    print("\nLocked Accounts")

    found = False

    for acc_no, data in users.items():

        if data["locked"]:
            print("Account:", acc_no, "| Name:", data["name"])
            found = True

    if not found:
        print("No locked accounts")


# -------------------------------
# Unlock Account
# -------------------------------
def unlock_account():

    users = load_users()

    acc_no = input("Enter account number to unlock: ")

    if acc_no in users:

        users[acc_no]["locked"] = False
        users[acc_no]["failed_attempts"] = 0

        save_users(users)

        print("Account unlocked successfully")

    else:
        print("Account not found")


# -------------------------------
# Admin Menu
# -------------------------------
def admin_menu():

    while True:

        print("\n===== ADMIN PANEL =====")
        print("1 View Locked Accounts")
        print("2 Unlock Account")
        print("3 Back")

        choice = input("Enter choice: ")

        if choice == "1":
            view_locked_accounts()

        elif choice == "2":
            unlock_account()

        elif choice == "3":
            break

        else:
            print("Invalid choice")


# -------------------------------
# Admin Login
# -------------------------------
def admin_login():

    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Admin login successful")
        admin_menu()
    else:
        print("Invalid admin credentials")


# -------------------------------
# Main Menu
# -------------------------------
def main_menu():

    while True:

        print("\n====== ATM SYSTEM ======")
        print("1 Register")
        print("2 Login")
        print("3 Admin Login")
        print("4 Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            register()

        elif choice == "2":
            login()

        elif choice == "3":
            admin_login()

        elif choice == "4":
            print("Thank you for using ATM")
            break

        else:
            print("Invalid choice")


# -------------------------------
# Start Program
# -------------------------------
main_menu()