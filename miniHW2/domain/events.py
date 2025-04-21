from datetime import datetime

from pydantic import BaseModel


class DomainEvent(BaseModel):

    occurred_on: datetime = datetime.now()


class AnimalMovedEvent(DomainEvent):

    animal_id: str
    from_enclosure_id: str | None
    to_enclosure_id: str
    moved_at: datetime = datetime.now()


class FeedingTimeEvent(DomainEvent):

    animal_id: str
    schedule_id: str
    feeding_time: datetime
    food_type: str
