import pytest

from zoo import Container
from animal_models import Monkey, Tiger
from inventory_models import Table, Computer

@pytest.fixture
def zoo():
    container = Container()
    return container.zoo()

def test_add_healthy_animal(zoo):
    monkey = Monkey(
        name="Дима",
        _food_per_day=5,
        _inventory_number=1,
        _friendliness=7,
        is_healthy=True
    )
    assert zoo.add_animal(monkey) == True
    assert len(zoo.animals) == 1

def test_add_unhealthy_animal(zoo):
    tiger = Tiger(
        name="Цезарь",
        _food_per_day=10,
        _inventory_number=2,
        _friendliness=3,
        is_healthy=False
    )
    assert zoo.add_animal(tiger) == False
    assert len(zoo.animals) == 0

def test_get_total_food_required(zoo):
    monkey = Monkey(name="Дима", _food_per_day=5, _inventory_number=1)
    tiger = Tiger(name="Цезарь", _food_per_day=10, _inventory_number=2)
    zoo.add_animal(monkey)
    zoo.add_animal(tiger)
    assert zoo.get_total_food_required() == 15

def test_get_contact_zoo_animals(zoo):
    monkey = Monkey(name="Дима", _food_per_day=5, _inventory_number=1, _friendliness=7, is_healthy=True)
    tiger = Tiger(name="Цезарь", _food_per_day=10, _inventory_number=2, _friendliness=3, is_healthy=True)
    zoo.add_animal(monkey)
    zoo.add_animal(tiger)
    friendly_animals = zoo.get_contact_zoo_animals()
    assert len(friendly_animals) == 1
    assert friendly_animals[0].name == "Дима"

def test_inventory_management(zoo):
    table = Table(name="Рабочий стол", _inventory_number=101, width=120, length=60)
    computer = Computer(name="ПК", _inventory_number=102, processor="Intel i5", display_size=27)
    
    zoo.add_inventory_item(table)
    zoo.add_inventory_item(computer)
    
    inventory_report = zoo.get_inventory_report()
    assert len(inventory_report) == 2
    assert any(item[1] == 101 for item in inventory_report)
    assert any(item[1] == 102 for item in inventory_report)
