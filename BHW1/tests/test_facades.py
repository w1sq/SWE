from decimal import Decimal
from datetime import datetime

import pytest

from facades import BankAccountFacade, CategoryFacade, OperationFacade
from repositories import (
    InMemoryBankAccountRepository,
    InMemoryCategoryRepository,
    InMemoryOperationRepository,
)
from validators import BankAccountValidator, CategoryValidator, OperationValidator
from models import BankAccount, TransactionType


class TestBankAccountFacade:
    def setup_method(self):
        self.repository = InMemoryBankAccountRepository()
        self.validator = BankAccountValidator()
        self.facade = BankAccountFacade(self.repository, self.validator)

    def test_create_account(self):
        account = self.facade.create_account("Test Account", Decimal("100.0"))

        assert account.id == 1
        assert account.name == "Test Account"
        assert account.balance == Decimal("100.0")

    def test_create_account_invalid(self):
        with pytest.raises(ValueError):
            self.facade.create_account("", Decimal("100.0"))

    def test_get_all_accounts(self):
        self.facade.create_account("Account 1", Decimal("100.0"))
        self.facade.create_account("Account 2", Decimal("200.0"))

        accounts = self.facade.get_all_accounts()
        assert len(accounts) == 2

    def test_get_account(self):
        created = self.facade.create_account("Test Account", Decimal("100.0"))
        retrieved = self.facade.get_account(created.id)

        assert retrieved.id == created.id
        assert retrieved.name == created.name

    def test_update_account(self):
        account = self.facade.create_account("Test Account", Decimal("100.0"))
        account.name = "Updated Account"

        updated = self.facade.update_account(account)
        assert updated.name == "Updated Account"

        retrieved = self.facade.get_account(account.id)
        assert retrieved.name == "Updated Account"

    def test_delete_account(self):
        account = self.facade.create_account("Test Account", Decimal("100.0"))
        self.facade.delete_account(account.id)

        assert self.facade.get_account(account.id) is None

    def test_get_account_nonexistent(self):
        """Test retrieving a non-existent account returns None."""
        retrieved = self.facade.get_account(999)
        assert retrieved is None

    def test_update_account_nonexistent(self):
        """Test updating a non-existent account raises an error."""
        non_existent_account = BankAccount(999, "Non-existent", Decimal("100.0"))

        with pytest.raises(ValueError):
            self.facade.update_account(non_existent_account)

    def test_delete_account_nonexistent(self):
        """Test deleting a non-existent account raises an error."""
        with pytest.raises(ValueError):
            self.facade.delete_account(999)

    def test_create_account_negative_balance(self):
        """Test creating an account with negative balance.
        Note: If your implementation allows negative balances, remove the pytest.raises.
        """
        account = self.facade.create_account(
            "Negative Balance Account", Decimal("-100.0")
        )
        assert account.balance == Decimal("-100.0")
    
    def test_create_account_zero_balance(self):
        """Test creating an account with zero balance is valid."""
        account = self.facade.create_account("Zero Balance Account", Decimal("0.0"))
        assert account.id == 1
        assert account.name == "Zero Balance Account"
        assert account.balance == Decimal("0.0")

    def test_get_all_accounts_empty(self):
        """Test getting all accounts when repository is empty."""
        accounts = self.facade.get_all_accounts()
        assert len(accounts) == 0
        assert isinstance(accounts, list)

    def test_update_account_balance(self):
        """Test updating an account's balance."""
        account = self.facade.create_account("Test Account", Decimal("100.0"))

        account.balance = Decimal("250.0")
        updated = self.facade.update_account(account)

        assert updated.balance == Decimal("250.0")

        retrieved = self.facade.get_account(account.id)
        assert retrieved.balance == Decimal("250.0")

    def test_create_account_minimum_name_length(self):
        """Test creating an account with minimum valid name length."""
        account = self.facade.create_account("AB", Decimal("100.0"))
        assert account.name == "AB"

        with pytest.raises(ValueError):
            self.facade.create_account("A", Decimal("100.0"))


class TestCategoryFacade:
    def setup_method(self):
        self.repository = InMemoryCategoryRepository()
        self.validator = CategoryValidator()
        self.facade = CategoryFacade(self.repository, self.validator)

    def test_create_category(self):
        income_category = self.facade.create_category("Salary", TransactionType.INCOME)
        assert income_category.id == 1
        assert income_category.name == "Salary"
        assert income_category.type == TransactionType.INCOME

        expense_category = self.facade.create_category("Food", TransactionType.EXPENSE)
        assert expense_category.id == 2
        assert expense_category.name == "Food"
        assert expense_category.type == TransactionType.EXPENSE

    def test_create_category_invalid(self):
        with pytest.raises(ValueError):
            self.facade.create_category("", TransactionType.INCOME)

    def test_get_all_categories(self):
        self.facade.create_category("Salary", TransactionType.INCOME)
        self.facade.create_category("Food", TransactionType.EXPENSE)

        categories = self.facade.get_all_categories()
        assert len(categories) == 2

        category_names = [c.name for c in categories]
        assert "Salary" in category_names
        assert "Food" in category_names

    def test_get_category(self):
        created = self.facade.create_category("Salary", TransactionType.INCOME)
        retrieved = self.facade.get_category(created.id)

        assert retrieved.id == created.id
        assert retrieved.name == "Salary"
        assert retrieved.type == TransactionType.INCOME

    def test_update_category(self):
        category = self.facade.create_category("Salary", TransactionType.INCOME)
        category.name = "Updated Salary"

        updated = self.facade.update_category(category)
        assert updated.name == "Updated Salary"

        retrieved = self.facade.get_category(category.id)
        assert retrieved.name == "Updated Salary"

    def test_delete_category(self):
        category = self.facade.create_category("Salary", TransactionType.INCOME)
        self.facade.delete_category(category.id)

        assert self.facade.get_category(category.id) is None


class TestOperationFacade:
    def setup_method(self):
        self.operation_repo = InMemoryOperationRepository()
        self.validator = OperationValidator()
        self.account_repo = InMemoryBankAccountRepository()
        self.facade = OperationFacade(
            self.operation_repo, self.validator, self.account_repo
        )

        self.test_account = self.account_repo.add(
            BankAccount(0, "Test Account", Decimal("1000.0"))
        )

    def test_create_income_operation(self):
        date = datetime.now()
        operation = self.facade.create_operation(
            TransactionType.INCOME,
            self.test_account.id,
            Decimal("500.0"),
            date,
            None,
            "Test income",
        )

        assert operation.id == 1
        assert operation.type == TransactionType.INCOME
        assert operation.bank_account_id == self.test_account.id
        assert operation.amount == Decimal("500.0")
        assert operation.date == date
        assert operation.description == "Test income"

        account = self.account_repo.get_by_id(self.test_account.id)
        assert account.balance == Decimal("1500.0")

    def test_create_expense_operation(self):
        date = datetime.now()
        operation = self.facade.create_operation(
            TransactionType.EXPENSE,
            self.test_account.id,
            Decimal("300.0"),
            date,
            None,
            "Test expense",
        )

        assert operation.id == 1
        assert operation.type == TransactionType.EXPENSE
        assert operation.bank_account_id == self.test_account.id
        assert operation.amount == Decimal("300.0")
        assert operation.date == date
        assert operation.description == "Test expense"

        account = self.account_repo.get_by_id(self.test_account.id)
        assert account.balance == Decimal("700.0")

    def test_create_operation_account_not_found(self):
        with pytest.raises(ValueError):
            self.facade.create_operation(
                TransactionType.INCOME,
                999,
                Decimal("500.0"),
                datetime.now(),
            )

    def test_get_all_operations(self):
        self.facade.create_operation(
            TransactionType.INCOME,
            self.test_account.id,
            Decimal("500.0"),
            datetime.now(),
        )
        self.facade.create_operation(
            TransactionType.EXPENSE,
            self.test_account.id,
            Decimal("200.0"),
            datetime.now(),
        )

        operations = self.facade.get_all_operations()
        assert len(operations) == 2
        assert operations[0].type == TransactionType.INCOME
        assert operations[1].type == TransactionType.EXPENSE

    def test_get_operation(self):
        created = self.facade.create_operation(
            TransactionType.INCOME,
            self.test_account.id,
            Decimal("500.0"),
            datetime.now(),
        )
        retrieved = self.facade.get_operation(created.id)

        assert retrieved.id == created.id
        assert retrieved.amount == Decimal("500.0")

    def test_update_operation(self):
        operation = self.facade.create_operation(
            TransactionType.INCOME,
            self.test_account.id,
            Decimal("500.0"),
            datetime.now(),
        )
        operation.description = "Updated description"

        updated = self.facade.update_operation(operation)
        assert updated.description == "Updated description"

        retrieved = self.facade.get_operation(operation.id)
        assert retrieved.description == "Updated description"

    def test_delete_operation(self):
        operation = self.facade.create_operation(
            TransactionType.INCOME,
            self.test_account.id,
            Decimal("500.0"),
            datetime.now(),
        )
        self.facade.delete_operation(operation.id)

        assert self.facade.get_operation(operation.id) is None
