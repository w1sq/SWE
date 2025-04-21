from unittest.mock import Mock

from domain.repositories import (
    AnimalRepository,
    EnclosureRepository,
    FeedingScheduleRepository,
)
from application.services import (
    AnimalTransferService,
    FeedingService,
    StatisticsService,
)


def create_test_services():
    animal_repo = Mock(spec=AnimalRepository)
    enclosure_repo = Mock(spec=EnclosureRepository)
    feeding_schedule_repo = Mock(spec=FeedingScheduleRepository)

    transfer_service = AnimalTransferService(animal_repo, enclosure_repo)
    feeding_service = FeedingService(animal_repo, feeding_schedule_repo)
    statistics_service = StatisticsService(animal_repo, enclosure_repo)

    return transfer_service, feeding_service, statistics_service
