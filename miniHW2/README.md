# Система управления зоопарком

Веб-приложение для автоматизации управления зоопарком, включая работу с животными, вольерами и расписанием кормления.

## Общее описание решения

Система управления зоопарком представляет собой веб-приложение, разработанное с применением принципов Domain-Driven Design (DDD) и Clean Architecture.

### Реализованный функционал:

1. **Управление животными**:
   - Добавление и удаление животных
   - Просмотр информации о животных
   - Перемещение животных между вольерами

2. **Управление вольерами**:
   - Создание и удаление вольеров
   - Отслеживание заполненности
   - Типизация вольеров (для хищников, травоядных, птиц, аквариумы)

3. **Управление кормлением**:
   - Создание расписания кормления
   - Отметка о выполнении кормления
   - Отслеживание типов корма

4. **Статистика**:
   - Общее количество животных
   - Статистика заполненности вольеров
   - Анализ распределения по типам вольеров

## Применение DDD и Clean Architecture

### Domain-Driven Design

1. **Сущности (Entities)**:
   - `Animal`: основная информация о животном
   - `Enclosure`: информация о вольере
   - `FeedingSchedule`: расписание кормления

2. **Value Objects**:
   - `EnclosureSize`: размер вольера
   - `EnclosureCapacity`: вместимость вольера
   - `FoodType`: тип корма

3. **События домена (Domain Events)**:
   - `AnimalMovedEvent`: событие перемещения животного
   - `FeedingTimeEvent`: событие времени кормления

### Clean Architecture

1. **Domain Layer** (ядро):
   - Модели предметной области
   - Бизнес-правила
   - События домена

2. **Application Layer**:
   - Сервисы приложения
   - Обработка бизнес-логики
   - Координация доменных объектов

3. **Infrastructure Layer**:
   - Реализация хранения данных
   - Внешние взаимодействия

4. **Presentation Layer**:
   - REST API endpoints
   - Контроллеры

## Структура проекта

```
zoo_management/
├── domain/              # Доменный слой
│   ├── models.py       # Основные модели (Animal, Enclosure, FeedingSchedule)
│   ├── events.py       # События домена
│   └── value_objects.py # Value Objects
├── application/         # Слой приложения
│   └── services.py     # Сервисы (AnimalTransfer, FeedingOrganization)
├── infrastructure/      # Слой инфраструктуры
│   └── repository.py   # Репозиторий для хранения данных
└── presentation/        # Слой представления
    └── api.py          # REST API endpoints

```

## Требования

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Pytest (для тестов)

## Установка и запуск

1. Установка зависимостей:
   ```bash
   pip install -r requirements.txt
   ```

2. Запуск приложения:
   ```bash
   python3 main.py
   ```

3. Доступ к API документации:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints

### Животные
- `POST /animals/`: Создание животного
- `GET /animals/`: Список всех животных
- `GET /animals/{animal_id}`: Информация о конкретном животном
- `DELETE /animals/{animal_id}`: Удаление животного

### Вольеры
- `POST /enclosures/`: Создание вольера
- `GET /enclosures/`: Список всех вольеров
- `POST /animals/{animal_id}/transfer/{enclosure_id}`: Перемещение животного
- `DELETE /enclosures/{enclosure_id}`: Удаление вольера

### Расписание кормления
- `POST /feeding-schedules/`: Создание расписания
- `GET /animals/{animal_id}/feeding-schedules`: Расписание для животного
- `POST /feeding-schedules/{schedule_id}/complete`: Отметка о кормлении
- `DELETE /feeding-schedules/{schedule_id}`: Удаление расписания
- `DELETE /animals/{animal_id}/feeding-schedules`: Удаление всех расписаний для животного

### Статистика
- `GET /statistics`: Общая статистика
- `GET /statistics/available-enclosures`: Доступные вольеры

## Тестирование

1. Запуск тестов:
   ```bash
   pytest
   ```

2. Запуск тестов с покрытием:
   ```bash
   pytest --cov=. --cov-report=term
   ```

3. Тестирование API через Swagger:
   ```
   http://localhost:8000/docs
   ```
