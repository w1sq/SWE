from decimal import Decimal
from datetime import datetime

from factories import EntityFactory
from models import TransactionType


class TestEntityFactory:
    def setup_method(self):
        self.factory = EntityFactory()

    def test_create_bank_account(self):
        account = self.factory.create_bank_account("Test Account")
        assert account.id == 0
        assert account.name == "Test Account"
        assert account.balance == Decimal("0.0")

        account = self.factory.create_bank_account("Test Account", Decimal("100.50"))
        assert account.id == 0
        assert account.name == "Test Account"
        assert account.balance == Decimal("100.50")

    def test_create_category(self):
        category = self.factory.create_category("Income", TransactionType.INCOME)
        assert category.id == 0
        assert category.name == "Income"
        assert category.type == TransactionType.INCOME

        category = self.factory.create_category("Expense", TransactionType.EXPENSE)
        assert category.id == 0
        assert category.name == "Expense"
        assert category.type == TransactionType.EXPENSE

    def test_create_operation(self):
        date = datetime.now()
        operation = self.factory.create_operation(
            TransactionType.INCOME, 1, Decimal("500.0"), date
        )
        assert operation.id == 0
        assert operation.type == TransactionType.INCOME
        assert operation.bank_account_id == 1
        assert operation.amount == Decimal("500.0")
        assert operation.date == date
        assert operation.category_id is None
        assert operation.description == ""

        operation = self.factory.create_operation(
            TransactionType.EXPENSE, 2, Decimal("350.75"), date, 3, "Test description"
        )
        assert operation.id == 0
        assert operation.type == TransactionType.EXPENSE
        assert operation.bank_account_id == 2
        assert operation.amount == Decimal("350.75")
        assert operation.date == date
        assert operation.category_id == 3
        assert operation.description == "Test description"
