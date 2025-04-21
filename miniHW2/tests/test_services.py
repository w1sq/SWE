from datetime import datetime
from unittest.mock import Mock

import pytest

from application.services import (
    AnimalTransferService,
    FeedingService,
    StatisticsService,
)
from domain.models import (
    Animal,
    Enclosure,
    AnimalStatus,
    EnclosureType,
    FeedingSchedule,
)
from domain.repositories import (
    AnimalRepository,
    EnclosureRepository,
    FeedingScheduleRepository,
)


@pytest.fixture
def animal_repository():
    return Mock(spec=AnimalRepository)


@pytest.fixture
def enclosure_repository():
    return Mock(spec=EnclosureRepository)


@pytest.fixture
def feeding_schedule_repository():
    return Mock(spec=FeedingScheduleRepository)


@pytest.fixture
def transfer_service(animal_repository, enclosure_repository):
    return AnimalTransferService(animal_repository, enclosure_repository)


@pytest.fixture
def feeding_service(animal_repository, feeding_schedule_repository):
    return FeedingService(animal_repository, feeding_schedule_repository)


@pytest.fixture
def statistics_service(animal_repository, enclosure_repository):
    return StatisticsService(animal_repository, enclosure_repository)


@pytest.fixture
def sample_animal():
    return Animal(
        id="animal1",
        species="Lion",
        name="Leo",
        birth_date=datetime(2020, 1, 1),
        gender="Male",
        favorite_food="Meat",
        status=AnimalStatus.HEALTHY,
    )


@pytest.fixture
def sample_enclosure():
    return Enclosure(
        id="enclosure1", type=EnclosureType.CAGE, size=100.0, max_capacity=2
    )


def test_animal_transfer(transfer_service, animal_repository, enclosure_repository):
    animal = Animal(
        id="test1",
        species="Lion",
        name="Leo",
        birth_date=datetime.now(),
        gender="Male",
        favorite_food="Meat",
        status=AnimalStatus.HEALTHY,
    )
    enclosure = Enclosure(
        id="enc1", type=EnclosureType.CAGE, size=100.0, max_capacity=2
    )

    animal_repository.get_by_id.return_value = animal
    enclosure_repository.get_by_id.return_value = enclosure
    enclosure_repository.update.return_value = True

    result = transfer_service.transfer_animal("test1", "enc1")

    assert result is True
    assert animal.enclosure_id == "enc1"
    animal_repository.get_by_id.assert_called_once_with("test1")
    enclosure_repository.get_by_id.assert_called_once_with("enc1")
    enclosure_repository.update.assert_called_once_with(enclosure)


def test_transfer_nonexistent_animal(transfer_service, animal_repository):
    animal_repository.get_by_id.return_value = None

    result = transfer_service.transfer_animal("nonexistent", "enc1")

    assert result is False
    animal_repository.get_by_id.assert_called_once_with("nonexistent")


def test_transfer_to_full_enclosure(
    transfer_service, animal_repository, enclosure_repository
):
    animal = Animal(
        id="test1",
        species="Lion",
        name="Leo",
        birth_date=datetime.now(),
        gender="Male",
        favorite_food="Meat",
        status=AnimalStatus.HEALTHY,
    )
    enclosure = Enclosure(
        id="enc1",
        type=EnclosureType.CAGE,
        size=100.0,
        max_capacity=2,
        current_animals=["animal1", "animal2"],
    )

    animal_repository.get_by_id.return_value = animal
    enclosure_repository.get_by_id.return_value = enclosure

    result = transfer_service.transfer_animal("test1", "enc1")

    assert result is False
    assert animal.enclosure_id is None


def test_create_feeding_schedule(
    feeding_service, animal_repository, feeding_schedule_repository
):
    animal = Animal(
        id="test1",
        species="Lion",
        name="Leo",
        birth_date=datetime.now(),
        gender="Male",
        favorite_food="Meat",
        status=AnimalStatus.HEALTHY,
    )
    schedule = FeedingSchedule(
        id="schedule1", animal_id="test1", feeding_time=datetime.now(), food_type="Meat"
    )

    animal_repository.get_by_id.return_value = animal
    feeding_schedule_repository.add.return_value = schedule

    result = feeding_service.create_feeding_schedule("test1", datetime.now(), "Meat")

    assert result == schedule
    animal_repository.get_by_id.assert_called_once_with("test1")
    feeding_schedule_repository.add.assert_called_once()


def test_mark_feeding_complete(feeding_service, feeding_schedule_repository):
    schedule = FeedingSchedule(
        id="schedule1", animal_id="test1", feeding_time=datetime.now(), food_type="Meat"
    )

    feeding_schedule_repository.get_by_id.return_value = schedule
    feeding_schedule_repository.update.return_value = True

    result = feeding_service.mark_feeding_complete("schedule1")

    assert result is True
    assert schedule.completed is True
    feeding_schedule_repository.get_by_id.assert_called_once_with("schedule1")
    feeding_schedule_repository.update.assert_called_once_with(schedule)


def test_mark_nonexistent_feeding_complete(
    feeding_service, feeding_schedule_repository
):
    feeding_schedule_repository.get_by_id.return_value = None

    result = feeding_service.mark_feeding_complete("nonexistent")

    assert result is False
    feeding_schedule_repository.get_by_id.assert_called_once_with("nonexistent")


def test_get_animal_schedules(feeding_service, feeding_schedule_repository):
    schedules = [
        FeedingSchedule(
            id="schedule1",
            animal_id="test1",
            feeding_time=datetime.now(),
            food_type="Meat",
        )
    ]

    feeding_schedule_repository.get_by_animal_id.return_value = schedules

    result = feeding_service.get_animal_schedules("test1")

    assert result == schedules
    feeding_schedule_repository.get_by_animal_id.assert_called_once_with("test1")


def test_zoo_statistics(statistics_service, animal_repository, enclosure_repository):
    animals = [
        Animal(
            id="test1",
            species="Lion",
            name="Leo",
            birth_date=datetime.now(),
            gender="Male",
            favorite_food="Meat",
            status=AnimalStatus.HEALTHY,
            enclosure_id="enc1",
        )
    ]
    enclosures = [
        Enclosure(
            id="enc1",
            type=EnclosureType.CAGE,
            size=100.0,
            max_capacity=2,
            current_animals=["test1"],
        ),
        Enclosure(
            id="enc2",
            type=EnclosureType.AQUARIUM,
            size=200.0,
            max_capacity=3,
            current_animals=[],
        ),
    ]

    animal_repository.get_all.return_value = animals
    enclosure_repository.get_all.return_value = enclosures

    stats = statistics_service.get_statistics()

    assert stats["total_animals"] == 1
    assert stats["total_enclosures"] == 2
    assert stats["available_enclosures"] == 2
    assert stats["occupancy_by_type"]["cage"] == 0.5
    assert stats["occupancy_by_type"]["aquarium"] == 0.0


def test_get_available_enclosures(
    statistics_service, animal_repository, enclosure_repository
):
    animals = [
        Animal(
            id="test1",
            species="Lion",
            name="Leo",
            birth_date=datetime.now(),
            gender="Male",
            favorite_food="Meat",
            status=AnimalStatus.HEALTHY,
            enclosure_id="enc1",
        )
    ]
    enclosures = [
        Enclosure(
            id="enc1",
            type=EnclosureType.CAGE,
            size=100.0,
            max_capacity=2,
            current_animals=["test1"],
        ),
        Enclosure(
            id="enc2",
            type=EnclosureType.AQUARIUM,
            size=200.0,
            max_capacity=3,
            current_animals=[],
        ),
    ]

    animal_repository.get_all.return_value = animals
    enclosure_repository.get_all.return_value = enclosures

    available = statistics_service.get_available_enclosures()

    assert len(available) == 1
    assert available[0].id == "enc2"


def test_delete_animal(transfer_service, animal_repository, enclosure_repository):
    animal = Animal(
        id="test1",
        species="Lion",
        name="Leo",
        birth_date=datetime.now(),
        gender="Male",
        favorite_food="Meat",
        status=AnimalStatus.HEALTHY,
        enclosure_id="enc1",
    )
    enclosure = Enclosure(
        id="enc1",
        type=EnclosureType.CAGE,
        size=100.0,
        max_capacity=2,
        current_animals=["test1"],
    )

    animal_repository.get_by_id.return_value = animal
    enclosure_repository.get_by_id.return_value = enclosure
    animal_repository.delete.return_value = True

    result = transfer_service.delete_animal("test1")

    assert result is True
    animal_repository.get_by_id.assert_called_once_with("test1")
    enclosure_repository.get_by_id.assert_called_once_with("enc1")
    animal_repository.delete.assert_called_once_with("test1")
    enclosure_repository.update.assert_called_once_with(enclosure)
    assert "test1" not in enclosure.current_animals


def test_delete_nonexistent_animal(transfer_service, animal_repository):
    animal_repository.get_by_id.return_value = None

    result = transfer_service.delete_animal("nonexistent")

    assert result is False
    animal_repository.get_by_id.assert_called_once_with("nonexistent")
    animal_repository.delete.assert_not_called()


def test_delete_empty_enclosure(transfer_service, enclosure_repository):
    enclosure = Enclosure(
        id="enc1",
        type=EnclosureType.CAGE,
        size=100.0,
        max_capacity=2,
        current_animals=[],
    )

    enclosure_repository.get_by_id.return_value = enclosure
    enclosure_repository.delete.return_value = True

    result = transfer_service.delete_enclosure("enc1")

    assert result is True
    enclosure_repository.get_by_id.assert_called_once_with("enc1")
    enclosure_repository.delete.assert_called_once_with("enc1")


def test_delete_nonempty_enclosure(transfer_service, enclosure_repository):
    enclosure = Enclosure(
        id="enc1",
        type=EnclosureType.CAGE,
        size=100.0,
        max_capacity=2,
        current_animals=["test1"],
    )

    enclosure_repository.get_by_id.return_value = enclosure

    result = transfer_service.delete_enclosure("enc1")

    assert result is False
    enclosure_repository.get_by_id.assert_called_once_with("enc1")
    enclosure_repository.delete.assert_not_called()


def test_delete_feeding_schedule(feeding_service, feeding_schedule_repository):
    schedule = FeedingSchedule(
        id="schedule1", animal_id="test1", feeding_time=datetime.now(), food_type="Meat"
    )

    feeding_schedule_repository.get_by_id.return_value = schedule
    feeding_schedule_repository.delete.return_value = True

    result = feeding_service.delete_schedule("schedule1")

    assert result is True
    feeding_schedule_repository.get_by_id.assert_called_once_with("schedule1")
    feeding_schedule_repository.delete.assert_called_once_with("schedule1")


def test_delete_nonexistent_schedule(feeding_service, feeding_schedule_repository):
    feeding_schedule_repository.get_by_id.return_value = None

    result = feeding_service.delete_schedule("nonexistent")

    assert result is False
    feeding_schedule_repository.get_by_id.assert_called_once_with("nonexistent")
    feeding_schedule_repository.delete.assert_not_called()


def test_delete_animal_schedules(feeding_service, feeding_schedule_repository):
    schedules = [
        FeedingSchedule(
            id="schedule1",
            animal_id="test1",
            feeding_time=datetime.now(),
            food_type="Meat",
        ),
        FeedingSchedule(
            id="schedule2",
            animal_id="test1",
            feeding_time=datetime.now(),
            food_type="Fish",
        ),
    ]

    feeding_schedule_repository.get_by_animal_id.return_value = schedules
    feeding_schedule_repository.delete.return_value = True

    result = feeding_service.delete_animal_schedules("test1")

    assert result is True
    feeding_schedule_repository.get_by_animal_id.assert_called_once_with("test1")
    assert feeding_schedule_repository.delete.call_count == 2
    feeding_schedule_repository.delete.assert_any_call("schedule1")
    feeding_schedule_repository.delete.assert_any_call("schedule2")


def test_delete_animal_schedules_partial_failure(
    feeding_service, feeding_schedule_repository
):
    schedules = [
        FeedingSchedule(
            id="schedule1",
            animal_id="test1",
            feeding_time=datetime.now(),
            food_type="Meat",
        ),
        FeedingSchedule(
            id="schedule2",
            animal_id="test1",
            feeding_time=datetime.now(),
            food_type="Fish",
        ),
    ]

    feeding_schedule_repository.get_by_animal_id.return_value = schedules
    feeding_schedule_repository.delete.side_effect = [
        True,
        False,
    ]  # First succeeds, second fails

    result = feeding_service.delete_animal_schedules("test1")

    assert result is False  # Overall operation failed
    feeding_schedule_repository.get_by_animal_id.assert_called_once_with("test1")
    assert feeding_schedule_repository.delete.call_count == 2
    feeding_schedule_repository.delete.assert_any_call("schedule1")
    feeding_schedule_repository.delete.assert_any_call("schedule2")
