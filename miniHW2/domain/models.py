from enum import Enum
from uuid import uuid4
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AnimalStatus(str, Enum):
    HEALTHY = "healthy"
    SICK = "sick"
    INJURED = "injured"


class AnimalType(str, Enum):
    CARNIVORE = "carnivore"
    HERBIVORE = "herbivore"
    BIRD = "bird"
    AQUATIC = "aquatic"


class EnclosureType(str, Enum):
    CAGE = "cage"
    AQUARIUM = "aquarium"
    TERRARIUM = "terrarium"


class Animal(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    species: str
    name: str
    birth_date: datetime
    gender: str
    favorite_food: str
    status: AnimalStatus
    enclosure_id: Optional[str] = None

    def feed(self) -> None:
        pass

    def treat(self) -> None:
        pass

    def transfer_to_enclosure(self, enclosure_id: str) -> None:
        self.enclosure_id = enclosure_id


class Enclosure(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: EnclosureType
    size: float
    max_capacity: int
    current_animals: List[str] = Field(default_factory=list)  # List of animal IDs

    def add_animal(self, animal_id: str) -> bool:
        if len(self.current_animals) < self.max_capacity:
            self.current_animals.append(animal_id)
            return True
        return False

    def remove_animal(self, animal_id: str) -> bool:
        if animal_id in self.current_animals:
            self.current_animals.remove(animal_id)
            return True
        return False

    def clean(self) -> None:
        pass


class FeedingSchedule(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    animal_id: str
    feeding_time: datetime
    food_type: str
    completed: bool = False

    def mark_completed(self) -> None:
        self.completed = True

    def update_schedule(self, new_time: datetime) -> None:
        self.feeding_time = new_time
