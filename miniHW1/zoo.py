from typing import List

from dependency_injector.providers import Singleton
from dependency_injector.containers import DeclarativeContainer

from animal_models import Animal
from inventory_models import Thing
from veterinary import VeterinaryClinic

class Zoo:
    def __init__(self, vet_clinic: VeterinaryClinic):
        self.animals: List[Animal] = []
        self.inventory: List[Thing] = []
        self.vet_clinic = vet_clinic

    def add_animal(self, animal: Animal) -> bool:
        if self.vet_clinic.check_health(animal):
            self.animals.append(animal)
            return True
        return False
    
    def add_inventory_item(self, item: Thing) -> None:
        self.inventory.append(item)

    def get_total_food_required(self) -> int:
        return sum(animal.food_per_day for animal in self.animals)

    def get_contact_zoo_animals(self) -> List[Animal]:
        return [animal for animal in self.animals 
                if animal.friendliness >= 5]

    def get_inventory_report(self) -> List[tuple]:
        animals_report = [(f"Животное: {animal.name}", animal.inventory_number) 
                         for animal in self.animals]
        things_report = [(f"Инвентарь: {thing.name}", thing.inventory_number) 
                        for thing in self.inventory]
        return animals_report + things_report

class Container(DeclarativeContainer):
    vet_clinic = Singleton(VeterinaryClinic)
    zoo = Singleton(Zoo, vet_clinic=vet_clinic)
