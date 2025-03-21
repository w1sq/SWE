from decimal import Decimal
from datetime import datetime

import pytest

from validators import BankAccountValidator, CategoryValidator, OperationValidator
from models import BankAccount, Category, Operation, TransactionType


class TestBankAccountValidator:
    def setup_method(self):
        self.validator = BankAccountValidator()

    def test_validate_valid_account(self):
        account = BankAccount(1, "Test Account", Decimal("100.0"))
        assert self.validator.validate(account) is True

    def test_validate_invalid_name_empty(self):
        account = BankAccount(1, "", Decimal("100.0"))
        with pytest.raises(ValueError):
            self.validator.validate(account)

    def test_validate_invalid_name_too_short(self):
        account = BankAccount(1, "A", Decimal("100.0"))
        with pytest.raises(ValueError):
            self.validator.validate(account)


class TestCategoryValidator:
    def setup_method(self):
        self.validator = CategoryValidator()

    def test_validate_valid_category(self):
        category = Category(1, "Food", TransactionType.EXPENSE)
        assert self.validator.validate(category) is True

    def test_validate_invalid_name(self):
        category = Category(1, "", TransactionType.EXPENSE)
        with pytest.raises(ValueError):
            self.validator.validate(category)

    def test_validate_invalid_type(self):
        category = Category(1, "Test", None)
        with pytest.raises(ValueError):
            self.validator.validate(category)


class TestOperationValidator:
    def setup_method(self):
        self.validator = OperationValidator()

    def test_validate_valid_operation(self):
        operation = Operation(
            1, TransactionType.INCOME, 1, Decimal("100.0"), datetime.now()
        )
        assert self.validator.validate(operation) is True

    def test_validate_invalid_amount_zero(self):
        operation = Operation(
            1, TransactionType.INCOME, 1, Decimal("0.0"), datetime.now()
        )
        with pytest.raises(ValueError):
            self.validator.validate(operation)

    def test_validate_invalid_amount_negative(self):
        operation = Operation(
            1, TransactionType.INCOME, 1, Decimal("-10.0"), datetime.now()
        )
        with pytest.raises(ValueError):
            self.validator.validate(operation)

    def test_validate_invalid_type(self):
        operation = Operation(1, None, 1, Decimal("100.0"), datetime.now())
        with pytest.raises(ValueError):
            self.validator.validate(operation)
