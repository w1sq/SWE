from typing import Dict, List, Optional, TypeVar, Generic

from domain.repositories import (
    Repository,
    AnimalRepository,
    EnclosureRepository,
    FeedingScheduleRepository,
)
from domain.models import Animal, Enclosure, FeedingSchedule

T = TypeVar("T")


class InMemoryRepository(Repository[T], Generic[T]):
    def __init__(self):
        self._storage: Dict[str, T] = {}

    def add(self, entity: T) -> T:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, id: str) -> Optional[T]:
        return self._storage.get(id)

    def get_all(self) -> List[T]:
        return list(self._storage.values())

    def update(self, entity: T) -> T:
        if entity.id in self._storage:
            self._storage[entity.id] = entity
            return entity
        raise ValueError(f"Entity with id {entity.id} not found")

    def delete(self, id: str) -> bool:
        if id in self._storage:
            del self._storage[id]
            return True
        return False


class InMemoryAnimalRepository(InMemoryRepository[Animal], AnimalRepository):
    pass


class InMemoryEnclosureRepository(InMemoryRepository[Enclosure], EnclosureRepository):
    pass


class InMemoryFeedingScheduleRepository(
    InMemoryRepository[FeedingSchedule], FeedingScheduleRepository
):
    def get_by_animal_id(self, animal_id: str) -> List[FeedingSchedule]:
        return [
            schedule
            for schedule in self._storage.values()
            if schedule.animal_id == animal_id
        ]
