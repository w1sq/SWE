from infrastructure.repository import (
    InMemoryAnimalRepository,
    InMemoryEnclosureRepository,
    InMemoryFeedingScheduleRepository,
)
from application.services import (
    AnimalTransferService,
    FeedingService,
    StatisticsService,
)
from presentation.api import app


def create_services():
    animal_repo = InMemoryAnimalRepository()
    enclosure_repo = InMemoryEnclosureRepository()
    feeding_repo = InMemoryFeedingScheduleRepository()

    transfer_service = AnimalTransferService(
        animal_repository=animal_repo, enclosure_repository=enclosure_repo
    )

    feeding_service = FeedingService(
        animal_repository=animal_repo, feeding_schedule_repository=feeding_repo
    )

    statistics_service = StatisticsService(
        animal_repository=animal_repo, enclosure_repository=enclosure_repo
    )

    return transfer_service, feeding_service, statistics_service


if __name__ == "__main__":
    import uvicorn

    transfer_service, feeding_service, statistics_service = create_services()

    app.dependency_overrides = {
        "transfer_service": lambda: transfer_service,
        "feeding_service": lambda: feeding_service,
        "statistics_service": lambda: statistics_service,
    }

    uvicorn.run(app, host="0.0.0.0", port=8000)
