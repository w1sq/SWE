import pytest

from pydantic import ValidationError

from domain.value_objects import EnclosureSize, EnclosureCapacity, FoodType


def test_enclosure_size_valid():
    size = EnclosureSize(value=100.0)
    assert size.value == 100.0
    assert size.unit == "square_meters"


def test_enclosure_size_invalid():
    with pytest.raises(ValidationError):
        EnclosureSize(value=-10.0)

    with pytest.raises(ValidationError):
        EnclosureSize(value=0)


def test_enclosure_capacity_valid():
    capacity = EnclosureCapacity(value=50)
    assert capacity.value == 50


def test_enclosure_capacity_invalid():
    with pytest.raises(ValidationError):
        EnclosureCapacity(value=0)

    with pytest.raises(ValidationError):
        EnclosureCapacity(value=-5)

    with pytest.raises(ValidationError):
        EnclosureCapacity(value=101)


def test_food_type_valid():
    food = FoodType(
        name="Meat", quantity=1.5, unit="kg", nutritional_value="High protein"
    )
    assert food.name == "Meat"
    assert food.quantity == 1.5
    assert food.unit == "kg"
    assert food.nutritional_value == "High protein"


def test_food_type_invalid_quantity():
    with pytest.raises(ValidationError):
        FoodType(
            name="Meat", quantity=-1.0, unit="kg", nutritional_value="High protein"
        )

    with pytest.raises(ValidationError):
        FoodType(name="Meat", quantity=0, unit="kg", nutritional_value="High protein")
