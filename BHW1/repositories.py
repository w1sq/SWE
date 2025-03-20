from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from models import BankAccount, Category, Operation


class Repository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, id):
        pass


class InMemoryBankAccountRepository(Repository):
    def __init__(self):
        self.accounts: Dict[int, BankAccount] = {}
        self.next_id = 1

    def get_all(self) -> List[BankAccount]:
        return list(self.accounts.values())

    def get_by_id(self, id: int) -> Optional[BankAccount]:
        return self.accounts.get(id)

    def add(self, entity: BankAccount) -> BankAccount:
        if entity.id is None or entity.id == 0:
            entity.id = self.next_id
            self.next_id += 1
        else:
            self.next_id = max(self.next_id, entity.id + 1)

        self.accounts[entity.id] = entity
        return entity

    def update(self, entity: BankAccount) -> BankAccount:
        if entity.id not in self.accounts:
            raise ValueError(f"Счет с ID {entity.id} не найден")
        self.accounts[entity.id] = entity
        return entity

    def delete(self, id: int) -> None:
        if id not in self.accounts:
            raise ValueError(f"Счет с ID {id} не найден")
        del self.accounts[id]


class InMemoryCategoryRepository(Repository):
    def __init__(self):
        self.categories: Dict[int, Category] = {}
        self.next_id = 1

    def get_all(self) -> List[Category]:
        return list(self.categories.values())

    def get_by_id(self, id: int) -> Optional[Category]:
        return self.categories.get(id)

    def add(self, entity: Category) -> Category:
        if entity.id is None or entity.id == 0:
            entity.id = self.next_id
            self.next_id += 1
        self.categories[entity.id] = entity
        return entity

    def update(self, entity: Category) -> Category:
        if entity.id not in self.categories:
            raise ValueError(f"Категория с ID {entity.id} не найдена")
        self.categories[entity.id] = entity
        return entity

    def delete(self, id: int) -> None:
        if id not in self.categories:
            raise ValueError(f"Категория с ID {id} не найдена")
        del self.categories[id]


class InMemoryOperationRepository(Repository):
    def __init__(self):
        self.operations: Dict[int, Operation] = {}
        self.next_id = 1

    def get_all(self) -> List[Operation]:
        return list(self.operations.values())

    def get_by_id(self, id: int) -> Optional[Operation]:
        return self.operations.get(id)

    def add(self, entity: Operation) -> Operation:
        if entity.id is None or entity.id == 0:
            entity.id = self.next_id
            self.next_id += 1
        self.operations[entity.id] = entity
        return entity

    def update(self, entity: Operation) -> Operation:
        if entity.id not in self.operations:
            raise ValueError(f"Операция с ID {entity.id} не найдена")
        self.operations[entity.id] = entity
        return entity

    def delete(self, id: int) -> None:
        if id not in self.operations:
            raise ValueError(f"Операция с ID {id} не найдена")
        del self.operations[id]
