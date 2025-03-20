from typing import List, Optional, Dict

from models import Operation
from repositories import Repository, InMemoryOperationRepository


class OperationRepositoryProxy(Repository):
    def __init__(self, real_repository: InMemoryOperationRepository):
        self.real_repository = real_repository
        self.cache: Dict = {}
        self.is_cache_valid = False

    def get_all(self) -> List[Operation]:
        if not self.is_cache_valid:
            self.cache["all"] = self.real_repository.get_all()
            self.is_cache_valid = True
        return self.cache["all"]

    def get_by_id(self, id: int) -> Optional[Operation]:
        cache_key = f"id_{id}"
        if cache_key not in self.cache:
            self.cache[cache_key] = self.real_repository.get_by_id(id)
        return self.cache[cache_key]

    def add(self, entity: Operation) -> Operation:
        result = self.real_repository.add(entity)
        self.is_cache_valid = False
        return result

    def update(self, entity: Operation) -> Operation:
        result = self.real_repository.update(entity)
        self.is_cache_valid = False
        cache_key = f"id_{entity.id}"
        if cache_key in self.cache:
            del self.cache[cache_key]
        return result

    def delete(self, id: int) -> None:
        self.real_repository.delete(id)
        self.is_cache_valid = False
        cache_key = f"id_{id}"
        if cache_key in self.cache:
            del self.cache[cache_key]
