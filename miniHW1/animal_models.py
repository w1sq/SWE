from dataclasses import dataclass

from interfaces import IAlive, IInventory

@dataclass
class Animal(IAlive, IInventory):
    name: str
    _food_per_day: int
    _inventory_number: int
    _friendliness: int = 0
    is_healthy: bool = True

    @property
    def food_per_day(self) -> int:
        return self._food_per_day

    @property
    def inventory_number(self) -> int:
        return self._inventory_number

    @property
    def friendliness(self) -> int:
        return self._friendliness

class Herbo(Animal):
    pass

class Predator(Animal):
    pass

class Monkey(Animal):
    pass

class Rabbit(Animal):
    pass

class Tiger(Animal):
    pass

class Wolf(Animal):
    pass
