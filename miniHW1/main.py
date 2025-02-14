from zoo import Container
from animal_models import Monkey, Tiger, Rabbit

def main():
    container = Container()
    zoo = container.zoo()

    while True:
        print("\nМосковский зоопарк - Система учета")
        print("1. Добавить животное")
        print("2. Показать общее количество требуемой еды")
        print("3. Показать животных для контактного зоопарка")
        print("4. Показать инвентаризационный отчет")
        print("5. Выход")

        choice = input("Выберите действие (1-5): ")

        if choice == "1":
            animal_type = input("Введите тип животного (Monkey/Tiger/Rabbit): ")
            name = input("Введите имя животного: ")
            food = int(input("Введите количество еды в день (кг): "))
            inv_number = int(input("Введите инвентарный номер: "))
            friendliness = int(input("Введите уровень дружелюбия (0-10): "))

            animal_classes = {
                "Monkey": Monkey,
                "Tiger": Tiger,
                "Rabbit": Rabbit
            }

            if animal_type in animal_classes:
                animal = animal_classes[animal_type](
                    name=name,
                    _food_per_day=food,
                    _inventory_number=inv_number,
                    _friendliness=friendliness
                )
                if zoo.add_animal(animal):
                    print("Животное успешно добавлено!")
                else:
                    print("Животное не прошло медосмотр!")

        elif choice == "2":
            print(f"Общее количество требуемой еды: {zoo.get_total_food_required()} кг")

        elif choice == "3":
            friendly_animals = zoo.get_contact_zoo_animals()
            if friendly_animals:
                print("Животные для контактного зоопарка:")
                for animal in friendly_animals:
                    print(f"- {animal.name} (дружелюбие: {animal.friendliness})")
            else:
                print("Нет животных для контактного зоопарка")

        elif choice == "4":
            inventory = zoo.get_inventory_report()
            if inventory:
                print("Инвентаризационный отчет:")
                for name, number in inventory:
                    print(f"- {name}: №{number}")
            else:
                print("Нет животных в зоопарке")

        elif choice == "5":
            break

if __name__ == "__main__":
    main()
