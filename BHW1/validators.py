from typing import Any
from decimal import Decimal
from abc import ABC, abstractmethod

from models import BankAccount, Category, Operation, TransactionType


class EntityValidator(ABC):
    @abstractmethod
    def validate(self, entity: Any) -> bool:
        pass


class BankAccountValidator(EntityValidator):
    def validate(self, account: BankAccount) -> bool:
        if not account.name or len(account.name) < 2:
            raise ValueError("Название счета должно содержать минимум 2 символа")
        return True


class CategoryValidator(EntityValidator):
    def validate(self, category: Category) -> bool:
        if not category.name or len(category.name) < 2:
            raise ValueError("Название категории должно содержать минимум 2 символа")
        if category.type not in TransactionType:
            raise ValueError("Неправильный тип категории")
        return True


class OperationValidator(EntityValidator):
    def validate(self, operation: Operation) -> bool:
        if operation.amount <= Decimal("0.0"):
            raise ValueError("Сумма операции должна быть положительной")
        if operation.type not in TransactionType:
            raise ValueError("Неправильный тип операции")
        return True
