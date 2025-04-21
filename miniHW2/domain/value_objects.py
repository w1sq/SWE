from typing import NewType

from pydantic import BaseModel, Field, field_validator


class EnclosureSize(BaseModel):

    value: float = Field(gt=0)
    unit: str = "square_meters"

    @field_validator("value")
    @classmethod
    def validate_size(cls, v):
        if v <= 0:
            raise ValueError("Size must be positive")
        return v


class EnclosureCapacity(BaseModel):

    value: int = Field(gt=0)

    @field_validator("value")
    @classmethod
    def validate_capacity(cls, v):
        if v <= 0:
            raise ValueError("Capacity must be positive")
        if v > 100:
            raise ValueError("Capacity cannot exceed 100 animals")
        return v


class FoodType(BaseModel):

    name: str
    quantity: float
    unit: str
    nutritional_value: str

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v


AnimalId = NewType("AnimalId", str)
EnclosureId = NewType("EnclosureId", str)
ScheduleId = NewType("ScheduleId", str)
