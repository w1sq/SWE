from decimal import Decimal
from datetime import datetime

import pytest
from repositories import (
    InMemoryBankAccountRepository,
    InMemoryCategoryRepository,
    InMemoryOperationRepository,
)
from models import BankAccount, Category, Operation, TransactionType


class TestInMemoryBankAccountRepository:
    def test_add(self):
        repository = InMemoryBankAccountRepository()
        account = BankAccount(0, "Test Account", Decimal("100.0"))
        added_account = repository.add(account)

        assert added_account.id == 1
        assert added_account.name == "Test Account"
        assert added_account.balance == Decimal("100.0")
        assert repository.get_by_id(1) == added_account

    def test_add_with_id(self):
        repository = InMemoryBankAccountRepository()
        account = BankAccount(5, "Test Account", Decimal("100.0"))
        added_account = repository.add(account)

        assert added_account.id == 5
        assert repository.get_by_id(5) == added_account

    def test_get_all(self):
        repository = InMemoryBankAccountRepository()
        account1 = repository.add(BankAccount(0, "Account 1", Decimal("100.0")))
        account2 = repository.add(BankAccount(0, "Account 2", Decimal("200.0")))

        all_accounts = repository.get_all()
        assert len(all_accounts) == 2
        assert account1 in all_accounts
        assert account2 in all_accounts

    def test_update(self):
        repository = InMemoryBankAccountRepository()
        account = repository.add(BankAccount(0, "Account", Decimal("100.0")))

        account.name = "Updated Account"
        account.balance = Decimal("150.0")
        updated_account = repository.update(account)

        assert updated_account.name == "Updated Account"
        assert updated_account.balance == Decimal("150.0")
        assert repository.get_by_id(account.id).name == "Updated Account"

    def test_update_nonexistent(self):
        repository = InMemoryBankAccountRepository()
        account = BankAccount(999, "Account", Decimal("100.0"))

        with pytest.raises(ValueError):
            repository.update(account)

    def test_delete(self):
        repository = InMemoryBankAccountRepository()
        account = repository.add(BankAccount(0, "Account", Decimal("100.0")))

        repository.delete(account.id)
        assert repository.get_by_id(account.id) is None

    def test_delete_nonexistent(self):
        repository = InMemoryBankAccountRepository()

        with pytest.raises(ValueError):
            repository.delete(999)


class TestInMemoryCategoryRepository:
    def test_add(self):
        repository = InMemoryCategoryRepository()
        category = Category(0, "Test Category", TransactionType.INCOME)
        added_category = repository.add(category)

        assert added_category.id == 1
        assert added_category.name == "Test Category"
        assert added_category.type == TransactionType.INCOME
        assert repository.get_by_id(1) == added_category

    def test_add_with_id(self):
        repository = InMemoryCategoryRepository()
        category = Category(5, "Test Category", TransactionType.EXPENSE)
        added_category = repository.add(category)

        assert added_category.id == 5
        assert repository.get_by_id(5) == added_category

    def test_get_all(self):
        repository = InMemoryCategoryRepository()
        category1 = repository.add(
            Category(0, "Income Category", TransactionType.INCOME)
        )
        category2 = repository.add(
            Category(0, "Expense Category", TransactionType.EXPENSE)
        )

        all_categories = repository.get_all()
        assert len(all_categories) == 2
        assert category1 in all_categories
        assert category2 in all_categories

    def test_update(self):
        repository = InMemoryCategoryRepository()
        category = repository.add(Category(0, "Category", TransactionType.INCOME))

        category.name = "Updated Category"
        updated_category = repository.update(category)

        assert updated_category.name == "Updated Category"
        assert repository.get_by_id(category.id).name == "Updated Category"

    def test_update_nonexistent(self):
        repository = InMemoryCategoryRepository()
        category = Category(999, "Category", TransactionType.INCOME)

        with pytest.raises(ValueError):
            repository.update(category)

    def test_delete(self):
        repository = InMemoryCategoryRepository()
        category = repository.add(Category(0, "Category", TransactionType.INCOME))

        repository.delete(category.id)
        assert repository.get_by_id(category.id) is None

    def test_delete_nonexistent(self):
        repository = InMemoryCategoryRepository()

        with pytest.raises(ValueError):
            repository.delete(999)


class TestInMemoryOperationRepository:
    def test_add(self):
        repository = InMemoryOperationRepository()
        operation = Operation(
            0, TransactionType.INCOME, 1, Decimal("100.0"), datetime.now()
        )
        added_operation = repository.add(operation)

        assert added_operation.id == 1
        assert added_operation.type == TransactionType.INCOME
        assert added_operation.bank_account_id == 1
        assert added_operation.amount == Decimal("100.0")
        assert repository.get_by_id(1) == added_operation

    def test_add_with_id(self):
        repository = InMemoryOperationRepository()
        operation = Operation(
            5, TransactionType.INCOME, 1, Decimal("100.0"), datetime.now()
        )
        added_operation = repository.add(operation)

        assert added_operation.id == 5
        assert repository.get_by_id(5) == added_operation

    def test_get_all(self):
        repository = InMemoryOperationRepository()
        operation1 = repository.add(
            Operation(0, TransactionType.INCOME, 1, Decimal("100.0"), datetime.now())
        )
        operation2 = repository.add(
            Operation(0, TransactionType.EXPENSE, 1, Decimal("50.0"), datetime.now())
        )

        all_operations = repository.get_all()
        assert len(all_operations) == 2
        assert operation1 in all_operations
        assert operation2 in all_operations

    def test_update(self):
        repository = InMemoryOperationRepository()
        operation = repository.add(
            Operation(0, TransactionType.INCOME, 1, Decimal("100.0"), datetime.now())
        )

        operation.amount = Decimal("150.0")
        updated_operation = repository.update(operation)

        assert updated_operation.amount == Decimal("150.0")
        assert repository.get_by_id(operation.id).amount == Decimal("150.0")

    def test_update_nonexistent(self):
        repository = InMemoryOperationRepository()
        operation = Operation(
            999, TransactionType.INCOME, 1, Decimal("100.0"), datetime.now()
        )

        with pytest.raises(ValueError):
            repository.update(operation)

    def test_delete(self):
        repository = InMemoryOperationRepository()
        operation = repository.add(
            Operation(0, TransactionType.INCOME, 1, Decimal("100.0"), datetime.now())
        )

        repository.delete(operation.id)
        assert repository.get_by_id(operation.id) is None

    def test_delete_nonexistent(self):
        repository = InMemoryOperationRepository()

        with pytest.raises(ValueError):
            repository.delete(999)
