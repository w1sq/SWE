from enum import Enum
from decimal import Decimal
from typing import Optional
from datetime import datetime


class TransactionType(Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


class BankAccount:
    def __init__(self, id: int, name: str, balance: Decimal = Decimal("0.0")):
        self.id = id
        self.name = name
        self.balance = balance

    def deposit(self, amount: Decimal) -> None:
        if amount <= Decimal("0.0"):
            raise ValueError("Сумма должна быть положительной")
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if amount <= Decimal("0.0"):
            raise ValueError("Сумма должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount


class Category:
    def __init__(self, id: int, name: str, type: TransactionType):
        self.id = id
        self.name = name
        self.type = type


class Operation:
    def __init__(
        self,
        id: int,
        type: TransactionType,
        bank_account_id: int,
        amount: Decimal,
        date: datetime,
        category_id: Optional[int] = None,
        description: str = "",
    ):
        self.id = id
        self.type = type
        self.bank_account_id = bank_account_id
        self.amount = amount
        self.date = date
        self.category_id = category_id
        self.description = description
