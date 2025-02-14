from dataclasses import dataclass

from interfaces import IInventory

@dataclass
class Thing(IInventory):
    name: str
    _inventory_number: int

    @property
    def inventory_number(self) -> int:
        return self._inventory_number

@dataclass
class Table(Thing):
    width: float
    length: float

@dataclass
class Computer(Thing):
    processor: str
    display_size: float
