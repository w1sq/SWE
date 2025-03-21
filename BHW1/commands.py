import time
from decimal import Decimal
from typing import Any, List
from datetime import datetime
from abc import ABC, abstractmethod

from models import Operation, BankAccount, Category, TransactionType
from facades import OperationFacade, BankAccountFacade, CategoryFacade


class Command(ABC):
    @abstractmethod
    def execute(self) -> Any:
        pass


class GetOperationsCommand(Command):
    def __init__(self, operation_facade: OperationFacade):
        self.operation_facade = operation_facade

    def execute(self) -> List[Operation]:
        return self.operation_facade.get_all_operations()


class CreateAccountCommand(Command):
    def __init__(
        self,
        bank_account_facade: BankAccountFacade,
        name: str,
        initial_balance: Decimal,
    ):
        self.bank_account_facade = bank_account_facade
        self.name = name
        self.initial_balance = initial_balance

    def execute(self) -> BankAccount:
        return self.bank_account_facade.create_account(self.name, self.initial_balance)


class CreateCategoryCommand(Command):
    def __init__(
        self, category_facade: CategoryFacade, name: str, type: TransactionType
    ):
        self.category_facade = category_facade
        self.name = name
        self.type = type

    def execute(self) -> Category:
        return self.category_facade.create_category(self.name, self.type)


class CreateOperationCommand(Command):
    def __init__(
        self,
        operation_facade: OperationFacade,
        type: TransactionType,
        account_id: int,
        amount: Decimal,
        date: datetime,
        category_id: int = None,
        description: str = "",
    ):
        self.operation_facade = operation_facade
        self.type = type
        self.account_id = account_id
        self.amount = amount
        self.date = date
        self.category_id = category_id
        self.description = description

    def execute(self) -> Operation:
        return self.operation_facade.create_operation(
            self.type,
            self.account_id,
            self.amount,
            self.date,
            self.category_id,
            self.description,
        )


class PerformanceDecorator:
    def __init__(self, command: Command):
        self.command = command

    def execute(self) -> Any:
        start_time = time.time()
        result = self.command.execute()
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения команды: {execution_time:.6f} секунд")
        return result
