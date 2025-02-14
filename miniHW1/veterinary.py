from animal_models import Animal

class VeterinaryClinic:
    def check_health(self, animal: Animal) -> bool:
        return animal.is_healthy
