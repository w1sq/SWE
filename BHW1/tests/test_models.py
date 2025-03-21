from decimal import Decimal
from datetime import datetime

import pytest

from models import BankAccount, Category, Operation, TransactionType


class TestBankAccount:
    def test_init(self):
        account = BankAccount(1, "Test Account", Decimal("100.0"))
        assert account.id == 1
        assert account.name == "Test Account"
        assert account.balance == Decimal("100.0")

    def test_deposit(self):
        account = BankAccount(1, "Test Account", Decimal("100.0"))
        account.deposit(Decimal("50.0"))
        assert account.balance == Decimal("150.0")

    def test_deposit_negative_amount(self):
        account = BankAccount(1, "Test Account", Decimal("100.0"))
        with pytest.raises(ValueError):
            account.deposit(Decimal("-10.0"))

    def test_withdraw(self):
        account = BankAccount(1, "Test Account", Decimal("100.0"))
        account.withdraw(Decimal("50.0"))
        assert account.balance == Decimal("50.0")

    def test_withdraw_negative_amount(self):
        account = BankAccount(1, "Test Account", Decimal("100.0"))
        with pytest.raises(ValueError):
            account.withdraw(Decimal("-10.0"))

    def test_withdraw_insufficient_funds(self):
        account = BankAccount(1, "Test Account", Decimal("100.0"))
        with pytest.raises(ValueError):
            account.withdraw(Decimal("150.0"))


class TestCategory:
    def test_init(self):
        category = Category(1, "Food", TransactionType.EXPENSE)
        assert category.id == 1
        assert category.name == "Food"
        assert category.type == TransactionType.EXPENSE


class TestOperation:
    def test_init(self):
        now = datetime.now()
        operation = Operation(
            1, TransactionType.INCOME, 2, Decimal("100.0"), now, 3, "Test"
        )
        assert operation.id == 1
        assert operation.type == TransactionType.INCOME
        assert operation.bank_account_id == 2
        assert operation.amount == Decimal("100.0")
        assert operation.date == now
        assert operation.category_id == 3
        assert operation.description == "Test"
