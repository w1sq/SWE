from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass


class AnimalRepository(Repository):
    pass


class EnclosureRepository(Repository):
    pass


class FeedingScheduleRepository(Repository):
    @abstractmethod
    def get_by_animal_id(self, animal_id: str) -> List:
        pass
