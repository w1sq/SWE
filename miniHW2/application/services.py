from datetime import datetime
from typing import List, Dict, Any, Optional

from domain.models import (
    Enclosure,
    FeedingSchedule,
)
from domain.repositories import (
    AnimalRepository,
    EnclosureRepository,
    FeedingScheduleRepository,
)


class AnimalTransferService:
    def __init__(
        self,
        animal_repository: AnimalRepository,
        enclosure_repository: EnclosureRepository,
    ):
        self.animal_repository = animal_repository
        self.enclosure_repository = enclosure_repository

    def transfer_animal(self, animal_id: str, enclosure_id: str) -> bool:
        animal = self.animal_repository.get_by_id(animal_id)
        enclosure = self.enclosure_repository.get_by_id(enclosure_id)

        if not animal or not enclosure:
            return False

        if len(enclosure.current_animals) >= enclosure.max_capacity:
            return False

        animal.transfer_to_enclosure(enclosure_id)
        self.animal_repository.update(animal)

        enclosure.add_animal(animal_id)
        self.enclosure_repository.update(enclosure)

        return True

    def delete_animal(self, animal_id: str) -> bool:
        animal = self.animal_repository.get_by_id(animal_id)
        if not animal:
            return False

        if animal.enclosure_id:
            enclosure = self.enclosure_repository.get_by_id(animal.enclosure_id)
            if enclosure:
                enclosure.remove_animal(animal_id)
                self.enclosure_repository.update(enclosure)

        return self.animal_repository.delete(animal_id)

    def delete_enclosure(self, enclosure_id: str) -> bool:
        enclosure = self.enclosure_repository.get_by_id(enclosure_id)
        if not enclosure:
            return False

        if enclosure.current_animals:
            return False

        return self.enclosure_repository.delete(enclosure_id)


class FeedingService:
    def __init__(
        self,
        animal_repository: AnimalRepository,
        feeding_schedule_repository: FeedingScheduleRepository,
    ):
        self.animal_repository = animal_repository
        self.feeding_schedule_repository = feeding_schedule_repository

    def create_feeding_schedule(
        self, animal_id: str, feeding_time: datetime, food_type: str
    ) -> Optional[FeedingSchedule]:
        animal = self.animal_repository.get_by_id(animal_id)
        if not animal:
            return None

        schedule = FeedingSchedule(
            animal_id=animal_id, feeding_time=feeding_time, food_type=food_type
        )
        return self.feeding_schedule_repository.add(schedule)

    def mark_feeding_complete(self, schedule_id: str) -> bool:
        schedule = self.feeding_schedule_repository.get_by_id(schedule_id)
        if not schedule:
            return False

        schedule.mark_completed()
        self.feeding_schedule_repository.update(schedule)
        return True

    def get_animal_schedules(self, animal_id: str) -> List[FeedingSchedule]:
        return self.feeding_schedule_repository.get_by_animal_id(animal_id)

    def delete_schedule(self, schedule_id: str) -> bool:
        schedule = self.feeding_schedule_repository.get_by_id(schedule_id)
        if not schedule:
            return False

        return self.feeding_schedule_repository.delete(schedule_id)

    def delete_animal_schedules(self, animal_id: str) -> bool:
        schedules = self.feeding_schedule_repository.get_by_animal_id(animal_id)
        success = True
        for schedule in schedules:
            if not self.feeding_schedule_repository.delete(schedule.id):
                success = False
        return success


class StatisticsService:
    def __init__(
        self,
        animal_repository: AnimalRepository,
        enclosure_repository: EnclosureRepository,
    ):
        self.animal_repository = animal_repository
        self.enclosure_repository = enclosure_repository

    def get_statistics(self) -> Dict[str, Any]:
        animals = self.animal_repository.get_all()
        enclosures = self.enclosure_repository.get_all()

        total_animals = len(animals)
        total_enclosures = len(enclosures)

        occupancy_by_type = {}
        for enclosure in enclosures:
            enclosure_type = str(enclosure.type).split(".")[-1].lower()
            if enclosure_type not in occupancy_by_type:
                occupancy_by_type[enclosure_type] = 0.0
            if enclosure.max_capacity > 0:
                occupancy = len(enclosure.current_animals) / enclosure.max_capacity
                if occupancy > occupancy_by_type[enclosure_type]:
                    occupancy_by_type[enclosure_type] = occupancy

        available_enclosures = sum(
            1 for e in enclosures if len(e.current_animals) < e.max_capacity
        )

        return {
            "total_animals": total_animals,
            "total_enclosures": total_enclosures,
            "available_enclosures": available_enclosures,
            "occupancy_by_type": occupancy_by_type,
        }

    def get_available_enclosures(self) -> List[Enclosure]:
        enclosures = self.enclosure_repository.get_all()
        return [e for e in enclosures if not e.current_animals]
