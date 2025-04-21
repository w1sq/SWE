from datetime import datetime
from unittest.mock import Mock

from fastapi.testclient import TestClient

from domain.models import Animal, Enclosure, FeedingSchedule
from presentation.api import app
from tests.test_config import create_test_services

transfer_service, feeding_service, statistics_service = create_test_services()

app.dependency_overrides = {
    "transfer_service": lambda: transfer_service,
    "feeding_service": lambda: feeding_service,
    "statistics_service": lambda: statistics_service,
}

client = TestClient(app)


def test_create_animal():
    animal_data = {
        "id": "test1",
        "species": "Lion",
        "name": "Leo",
        "birth_date": "2020-01-01T00:00:00",
        "gender": "Male",
        "favorite_food": "Meat",
        "status": "healthy",
    }

    transfer_service.animal_repository.add.return_value = Animal(**animal_data)

    response = client.post("/animals/", json=animal_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Leo"
    assert data["species"] == "Lion"


def test_get_animals():
    transfer_service.animal_repository.get_all.return_value = []

    response = client.get("/animals/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_animal():
    animal_data = {
        "id": "test2",
        "species": "Tiger",
        "name": "Tigger",
        "birth_date": "2020-01-01T00:00:00",
        "gender": "Male",
        "favorite_food": "Meat",
        "status": "healthy",
    }

    transfer_service.animal_repository.get_by_id.return_value = Animal(**animal_data)

    response = client.get("/animals/test2")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Tigger"


def test_get_nonexistent_animal():
    transfer_service.animal_repository.get_by_id.return_value = None

    response = client.get("/animals/nonexistent")
    assert response.status_code == 404


def test_create_enclosure():
    enclosure_data = {"id": "enc1", "type": "cage", "size": 100.0, "max_capacity": 2}

    transfer_service.enclosure_repository.add.return_value = Enclosure(**enclosure_data)

    response = client.post("/enclosures/", json=enclosure_data)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "cage"
    assert data["size"] == 100.0


def test_get_enclosures():
    transfer_service.enclosure_repository.get_all.return_value = []

    response = client.get("/enclosures/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_transfer_animal():
    animal_data = {
        "id": "test3",
        "species": "Lion",
        "name": "Leo",
        "birth_date": "2020-01-01T00:00:00",
        "gender": "Male",
        "favorite_food": "Meat",
        "status": "healthy",
    }
    enclosure_data = {"id": "enc2", "type": "cage", "size": 100.0, "max_capacity": 2}

    transfer_service.animal_repository.get_by_id.return_value = Animal(**animal_data)
    transfer_service.enclosure_repository.get_by_id.return_value = Enclosure(
        **enclosure_data
    )
    transfer_service.transfer_animal = Mock(return_value=True)

    response = client.post(f"/animals/test3/transfer/enc2")
    assert response.status_code == 200
    assert response.json()["message"] == "Animal transferred successfully"


def test_create_feeding_schedule():
    animal_data = {
        "id": "test4",
        "species": "Lion",
        "name": "Leo",
        "birth_date": "2020-01-01T00:00:00",
        "gender": "Male",
        "favorite_food": "Meat",
        "status": "healthy",
    }

    feeding_service.animal_repository.get_by_id.return_value = Animal(**animal_data)
    feeding_service.feeding_schedule_repository.add.return_value = FeedingSchedule(
        id="schedule1", animal_id="test4", feeding_time=datetime.now(), food_type="Meat"
    )

    schedule_data = {
        "animal_id": "test4",
        "feeding_time": "2024-01-01T12:00:00",
        "food_type": "Meat",
    }
    response = client.post("/feeding-schedules/", json=schedule_data)
    assert response.status_code == 200
    data = response.json()
    assert data["animal_id"] == "test4"
    assert data["food_type"] == "Meat"


def test_get_animal_feeding_schedules():
    feeding_service.feeding_schedule_repository.get_by_animal_id.return_value = [
        FeedingSchedule(
            id="schedule1",
            animal_id="test5",
            feeding_time=datetime.now(),
            food_type="Meat",
        )
    ]

    response = client.get(f"/animals/test5/feeding-schedules")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["animal_id"] == "test5"


def test_mark_feeding_complete():
    feeding_service.feeding_schedule_repository.get_by_id.return_value = (
        FeedingSchedule(
            id="schedule1",
            animal_id="test6",
            feeding_time=datetime.now(),
            food_type="Meat",
        )
    )
    feeding_service.mark_feeding_complete = Mock(return_value=True)

    response = client.post(f"/feeding-schedules/schedule1/complete")
    assert response.status_code == 200
    assert response.json()["message"] == "Feeding marked as complete"


def test_get_statistics():
    statistics_service.get_statistics = Mock(
        return_value={
            "total_animals": 10,
            "total_enclosures": 5,
            "available_enclosures": 2,
            "occupancy_by_type": {"cage": 0.8, "aquarium": 0.5},
        }
    )

    response = client.get("/statistics")
    assert response.status_code == 200
    data = response.json()
    assert "total_animals" in data
    assert "total_enclosures" in data
    assert "available_enclosures" in data
    assert "occupancy_by_type" in data


def test_get_available_enclosures():
    statistics_service.get_available_enclosures = Mock(
        return_value=[Enclosure(id="enc1", type="cage", size=100.0, max_capacity=2)]
    )

    response = client.get("/statistics/available-enclosures")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
