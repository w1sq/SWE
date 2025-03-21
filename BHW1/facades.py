from decimal import Decimal
from datetime import datetime
from typing import List, Optional

from models import BankAccount, Category, Operation, TransactionType
from repositories import (
    InMemoryBankAccountRepository,
    InMemoryCategoryRepository,
    InMemoryOperationRepository,
)
from validators import BankAccountValidator, CategoryValidator, OperationValidator


class BankAccountFacade:
    def __init__(
        self, repository: InMemoryBankAccountRepository, validator: BankAccountValidator
    ):
        self.repository = repository
        self.validator = validator

    def create_account(
        self, name: str, balance: Decimal = Decimal("0.0")
    ) -> BankAccount:
        account = BankAccount(0, name, balance)
        self.validator.validate(account)
        return self.repository.add(account)

    def get_all_accounts(self) -> List[BankAccount]:
        return self.repository.get_all()

    def get_account(self, id: int) -> Optional[BankAccount]:
        return self.repository.get_by_id(id)

    def update_account(self, account: BankAccount) -> BankAccount:
        self.validator.validate(account)
        return self.repository.update(account)

    def delete_account(self, id: int) -> None:
        self.repository.delete(id)


class CategoryFacade:
    def __init__(
        self, repository: InMemoryCategoryRepository, validator: CategoryValidator
    ):
        self.repository = repository
        self.validator = validator

    def create_category(self, name: str, type: TransactionType) -> Category:
        category = Category(0, name, type)
        self.validator.validate(category)
        return self.repository.add(category)

    def get_all_categories(self) -> List[Category]:
        return self.repository.get_all()

    def get_category(self, id: int) -> Optional[Category]:
        return self.repository.get_by_id(id)

    def update_category(self, category: Category) -> Category:
        self.validator.validate(category)
        return self.repository.update(category)

    def delete_category(self, id: int) -> None:
        self.repository.delete(id)


class OperationFacade:
    def __init__(
        self,
        repository: InMemoryOperationRepository,
        validator: OperationValidator,
        account_repository: InMemoryBankAccountRepository,
    ):
        self.repository = repository
        self.validator = validator
        self.account_repository = account_repository

    def create_operation(
        self,
        type: TransactionType,
        bank_account_id: int,
        amount: Decimal,
        date: datetime,
        category_id: Optional[int] = None,
        description: str = "",
    ) -> Operation:
        operation = Operation(
            0, type, bank_account_id, amount, date, category_id, description
        )
        self.validator.validate(operation)

        account = self.account_repository.get_by_id(bank_account_id)
        if not account:
            raise ValueError(f"Счет с ID {bank_account_id} не найден")

        if type == TransactionType.INCOME:
            account.deposit(amount)
        else:
            account.withdraw(amount)

        self.account_repository.update(account)
        return self.repository.add(operation)

    def get_all_operations(self) -> List[Operation]:
        return self.repository.get_all()

    def get_operation(self, id: int) -> Optional[Operation]:
        return self.repository.get_by_id(id)

    def update_operation(self, operation: Operation) -> Operation:
        self.validator.validate(operation)
        return self.repository.update(operation)

    def delete_operation(self, id: int) -> None:
        self.repository.delete(id)
