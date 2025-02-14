from abc import ABC, abstractmethod

class IAlive(ABC):
    @property
    @abstractmethod
    def food_per_day(self) -> int:
        pass

class IInventory(ABC):
    @property
    @abstractmethod
    def inventory_number(self) -> int:
        pass
