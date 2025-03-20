import time
from typing import Any, List
from abc import ABC, abstractmethod

from models import Operation
from facades import OperationFacade


class Command(ABC):
    @abstractmethod
    def execute(self) -> Any:
        pass


class GetOperationsCommand(Command):
    def __init__(self, operation_facade: OperationFacade):
        self.operation_facade = operation_facade

    def execute(self) -> List[Operation]:
        return self.operation_facade.get_all_operations()


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
