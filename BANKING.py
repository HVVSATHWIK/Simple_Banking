# BANKING.py

import sqlite3
import datetime

class User:
    def __init__(self, user_id, name, balance=0):
        self.user_id = user_id
        self.name = name
        self.balance = balance

class BankingSystem:
    def __init__(self):
        self.users = {}
        self.next_id = 1
        self.conn = sqlite3.connect("budget.db", check_same_thread=False)  # Allow multi-threaded access
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                id INTEGER PRIMARY KEY,
                                type TEXT,
                                category TEXT,
                                amount REAL,
                                date TEXT,
                                notes TEXT)''')
        self.conn.commit()
        self.budgets = {}

    def about(self):
        return "This Banking System allows you to create accounts, deposit, withdraw, check balance, and manage budgets."

    def create_account(self, name, initial_balance=0):
        user_id = self.next_id
        self.users[user_id] = User(user_id, name, initial_balance)
        self.next_id += 1
        return f"Account created for {name} with ID {user_id}. Initial balance: ${initial_balance}"

    def get_balance(self, user_id):
        user = self.users.get(user_id)
        if user:
            return f"User {user.name} has a balance of ${user.balance:.2f}"
        return "User not found."

    def deposit(self, user_id, amount):
        user = self.users.get(user_id)
        if user:
            user.balance += amount
            self.add_transaction("income", "Deposit", amount)
            return f"${amount:.2f} deposited to {user.name}'s account. New balance: ${user.balance:.2f}"
        return "User not found."

    def withdraw(self, user_id, amount):
        user = self.users.get(user_id)
        if user:
            if user.balance >= amount:
                user.balance -= amount
                self.add_transaction("expense", "Withdrawal", amount)
                return f"${amount:.2f} withdrawn from {user.name}'s account. New balance: ${user.balance:.2f}"
            return "Insufficient balance."
        return "User not found."

    def admin_panel(self):
        if not self.users:
            return "No users available."
        return "\n".join([f"ID: {u.user_id}, Name: {u.name}, Balance: ${u.balance:.2f}" for u in self.users.values()])

    def set_budget(self, category, amount):
        self.budgets[category] = amount
        print(f"Budget for {category} set to {amount}")

    def check_budget(self):
        budget_status = {}
        for category, limit in self.budgets.items():
            spent = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE category = ? AND type = 'expense'", (category,)).fetchone()[0] or 0
            budget_status[category] = {
                'spent': spent,
                'budget': limit,
                'remaining': limit - spent
            }
        return budget_status

    def add_transaction(self, type, category, amount, notes=""):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO transactions (type, category, amount, date, notes) VALUES (?, ?, ?, ?, ?)",
                            (type, category, amount, date, notes))
        self.conn.commit()

    def generate_report(self):
        income = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'").fetchone()[0] or 0
        expenses = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'").fetchone()[0] or 0
        balance = income - expenses
        return {
            'total_income': income,
            'total_expenses': expenses,
            'current_balance': balance
        }

    def close(self):
        self.conn.close()

banking_system = BankingSystem()
# BANKING.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    balance = db.Column(db.Float, default=0.0)

    def __init__(self, username, balance=0):
        self.username = username
        self.balance = balance
