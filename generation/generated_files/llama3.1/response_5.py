import sqlite3
from getpass import getpass
import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()

class FinancialApp:
    def __init__(self):
        self.conn = sqlite3.connect('financial_data.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                balance REAL NOT NULL DEFAULT 0.00,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        self.conn.commit()

    def authenticate(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashlib.sha256(password.encode()).hexdigest()))
        if self.cursor.fetchone():
            return True
        else:
            return False

    def create_account(self, user_id, balance=0.00):
        self.cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (?, ?)", (user_id, balance))
        self.conn.commit()

    def transfer_money(self, sender_username, recipient_username, amount):
        if not isinstance(amount, float) and amount <= 0:
            return "Invalid transaction"
        
        self.cursor.execute("SELECT id FROM users WHERE username = ?", (sender_username,))
        sender_id = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT id FROM users WHERE username = ?", (recipient_username,))
        recipient_id = self.cursor.fetchone()[0]

        if sender_id == recipient_id:
            return "Cannot transfer money to the same account"

        self.cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (sender_id,))
        sender_balance = self.cursor.fetchone()[0]
        
        if amount > sender_balance:
            return "Insufficient funds"

        self.cursor.execute("""
            UPDATE accounts
            SET balance = balance - ?
            WHERE user_id = ?;
        """, (amount, sender_id))

        self.cursor.execute("""
            UPDATE accounts
            SET balance = balance + ?
            WHERE user_id = ?;
        """, (amount, recipient_id))
        
        self.conn.commit()

    def get_transaction_history(self, username):
        self.cursor.execute("SELECT * FROM accounts")
        accounts = self.cursor.fetchall()
        
        transaction_history = {}
        
        for account in accounts:
            if account[1] == username:
                self.cursor.execute("""
                    SELECT balance, date
                    FROM transactions
                    WHERE user_id = ?;
                """, (account[0],))
                
                transactions = self.cursor.fetchall()
                
                transaction_history[account[0]] = transactions
        
        return transaction_history

def main():
    app = FinancialApp()

    while True:
        print("1. Authenticate")
        print("2. Create new account")
        print("3. Transfer money")
        print("4. Get transaction history")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = getpass()
            if app.authenticate(username, password):
                print("Authenticated successfully")
            else:
                print("Invalid username or password")
        elif choice == "2":
            username = input("Enter a new username: ")
            password = getpass()
            user = User(username, password)
            app.cursor.execute("""
                INSERT INTO users (username, password)
                VALUES (?, ?);
            """, (user.username, user.password))
            app.conn.commit()
        elif choice == "3":
            sender_username = input("Enter the sender's username: ")
            recipient_username = input("Enter the recipient's username: ")
            amount = float(input("Enter the transfer amount: "))
            print(app.transfer_money(sender_username, recipient_username, amount))
        elif choice == "4":
            username = input("Enter your username: ")
            print(app.get_transaction_history(username))
        elif choice == "5":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()