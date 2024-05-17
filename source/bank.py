from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Float)

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'))
    account_from_id = Column(Integer, ForeignKey('accounts.account_id'))
    amount = Column(Float)
    transaction_type = Column(String)
    transaction_date = Column(DateTime, default=datetime.now)