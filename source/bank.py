from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

# Permet de définir des modèles (les classes en POO, ici: Account & Transaction)
# création de table (et colonnes) SQLAlchemy pour chaque classe Python
Base = declarative_base()

# Table Account
class Account(Base):
    # Columns
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Float)
    
    def __init__(self, account_id):
        self.account_id = account_id
        self.balance = 0
    
    def __repr__(self) -> str:
        return f'Account(account_id={self.account_id}, balance={self.balance}'
    
    def get_balance(self):
        return f"Account {self.account_id}'s balance is {self.balance} $"

# Table Transaction
class Transaction(Base):
    # Columns
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'))
    account_from_id = Column(Integer, ForeignKey('accounts.account_id'))
    amount = Column(Float)
    transaction_type = Column(String)
    transaction_date = Column(DateTime, default=datetime.now)
    
    def __repr__(self) -> str:
        return f"Transaction(id={self.transaction_id}, account_id={self.account_id}, amount={self.amount:.2f}, type={self.transaction_type})"
    
    def deposit(self, session, account_id, amount):
        account = session.get(Account, account_id)
        if not isinstance(amount, (float, int)) or amount <= 0:
            transaction = "Deposit failed. Please enter a valid number."
        else:
            account.balance += amount
            transaction = Transaction(account_id=account_id, amount=amount, transaction_type='deposit', transaction_date=datetime.now())
            session.add(transaction)
            session.commit()
        return transaction

    def withdraw(self, session, account_id, amount):
        account = session.get(Account, account_id)
        if not isinstance(amount, (float, int)) or amount <= 0:
            return f"Please enter a valid number."
        else:
            account.balance -= amount
            transaction = Transaction(account_id=account_id, amount=amount, transaction_type='withdraw', transaction_date=datetime.now())
            session.add(transaction)
            session.commit()
        return transaction
              
    def transfer(self, session, account_from, account_to, amount):
        account_from_obj = session.get(Account, account_from)
        account_to_obj = session.get(Account, account_to)
        if not isinstance(amount, (float, int))  or amount <= 0:
            return f"Please enter a valid number."
        else:
            account_from_obj.balance -= amount
            account_to_obj.balance += amount
            transaction = Transaction(account_from_id=account_from, account_id=account_to, amount=amount, transaction_type='transfer', transaction_date=datetime.now())
            session.add(transaction)
            session.commit()
        return transaction