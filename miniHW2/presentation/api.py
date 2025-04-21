from typing import List

from fastapi import FastAPI, Depends, HTTPException

from domain.models import Animal, Enclosure, FeedingSchedule
from application.services import (
    AnimalTransferService,
    FeedingService,
    StatisticsService,
)


app = FastAPI()


def get_transfer_service() -> AnimalTransferService:
    return app.dependency_overrides.get(
        "transfer_service", lambda: AnimalTransferService()
    )()


def get_feeding_service() -> FeedingService:
    return app.dependency_overrides.get("feeding_service", lambda: FeedingService())()


def get_statistics_service() -> StatisticsService:
    return app.dependency_overrides.get(
        "statistics_service", lambda: StatisticsService()
    )()


@app.post("/animals/", response_model=Animal)
def create_animal(
    animal: Animal,
    transfer_service: AnimalTransferService = Depends(get_transfer_service),
):
    return transfer_service.animal_repository.add(animal)


@app.get("/animals/", response_model=List[Animal])
def get_animals(
    transfer_service: AnimalTransferService = Depends(get_transfer_service),
):
    return transfer_service.animal_repository.get_all()


@app.get("/animals/{animal_id}", response_model=Animal)
def get_animal(
    animal_id: str,
    transfer_service: AnimalTransferService = Depends(get_transfer_service),
):
    animal = transfer_service.animal_repository.get_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@app.delete("/animals/{animal_id}")
def delete_animal(
    animal_id: str,
    transfer_service: AnimalTransferService = Depends(get_transfer_service),
):
    success = transfer_service.delete_animal(animal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Animal not found")
    return {"message": "Animal deleted successfully"}


@app.post("/enclosures/", response_model=Enclosure)
def create_enclosure(
    enclosure: Enclosure,
    transfer_service: AnimalTransferService = Depends(get_transfer_service),
):
    return transfer_service.enclosure_repository.add(enclosure)


@app.get("/enclosures/", response_model=List[Enclosure])
def get_enclosures(
    transfer_service: AnimalTransferService = Depends(get_transfer_service),
):
    return transfer_service.enclosure_repository.get_all()


@app.delete("/enclosures/{enclosure_id}")
def delete_enclosure(
    enclosure_id: str,
    transfer_service: AnimalTransferService = Depends(get_transfer_service),
):
    success = transfer_service.delete_enclosure(enclosure_id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete enclosure: either not found or not empty",
        )
    return {"message": "Enclosure deleted successfully"}


@app.post("/animals/{animal_id}/transfer/{enclosure_id}")
def transfer_animal(
    animal_id: str,
    enclosure_id: str,
    transfer_service: AnimalTransferService = Depends(get_transfer_service),
):
    success = transfer_service.transfer_animal(animal_id, enclosure_id)
    if not success:
        raise HTTPException(status_code=400, detail="Transfer failed")
    return {"message": "Animal transferred successfully"}


@app.post("/feeding-schedules/", response_model=FeedingSchedule)
def create_feeding_schedule(
    schedule: FeedingSchedule,
    feeding_service: FeedingService = Depends(get_feeding_service),
):
    return feeding_service.feeding_schedule_repository.add(schedule)


@app.get("/animals/{animal_id}/feeding-schedules", response_model=List[FeedingSchedule])
def get_animal_feeding_schedules(
    animal_id: str, feeding_service: FeedingService = Depends(get_feeding_service)
):
    return feeding_service.feeding_schedule_repository.get_by_animal_id(animal_id)


@app.delete("/feeding-schedules/{schedule_id}")
def delete_feeding_schedule(
    schedule_id: str,
    feeding_service: FeedingService = Depends(get_feeding_service),
):
    success = feeding_service.delete_schedule(schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feeding schedule not found")
    return {"message": "Feeding schedule deleted successfully"}


@app.delete("/animals/{animal_id}/feeding-schedules")
def delete_animal_feeding_schedules(
    animal_id: str,
    feeding_service: FeedingService = Depends(get_feeding_service),
):
    success = feeding_service.delete_animal_schedules(animal_id)
    if not success:
        raise HTTPException(
            status_code=400, detail="Failed to delete feeding schedules"
        )
    return {"message": "All feeding schedules deleted successfully"}


@app.post("/feeding-schedules/{schedule_id}/complete")
def mark_feeding_complete(
    schedule_id: str, feeding_service: FeedingService = Depends(get_feeding_service)
):
    success = feeding_service.mark_feeding_complete(schedule_id)
    if not success:
        raise HTTPException(
            status_code=400, detail="Failed to mark feeding as complete"
        )
    return {"message": "Feeding marked as complete"}


@app.get("/statistics")
def get_statistics(
    statistics_service: StatisticsService = Depends(get_statistics_service),
):
    return statistics_service.get_statistics()


@app.get("/statistics/available-enclosures")
def get_available_enclosures(
    statistics_service: StatisticsService = Depends(get_statistics_service),
):
    return statistics_service.get_available_enclosures()
