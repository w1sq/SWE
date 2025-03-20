import time
from functools import wraps
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable


class Command(ABC):
    @abstractmethod
    def execute(self) -> Any:
        pass


class PerformanceDecorator:
    def __init__(
        self, command: Command, scenario_name: str = None, performance_tracker=None
    ):
        self.command = command
        self.scenario_name = scenario_name or self.command.__class__.__name__
        self.performance_tracker = performance_tracker

    def execute(self) -> Any:
        start_time = time.time()
        result = self.command.execute()
        end_time = time.time()
        execution_time = end_time - start_time
        print(
            f"Время выполнения сценария '{self.scenario_name}': {execution_time:.6f} секунд"
        )

        # Сохраняем данные в трекере производительности, если он предоставлен
        if self.performance_tracker:
            self.performance_tracker.add_execution_time(
                self.scenario_name, execution_time
            )

        return result


# Декоратор для любой функции
def measure_execution_time(scenario_name: str = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = scenario_name or func.__name__
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Время выполнения сценария '{name}': {execution_time:.6f} секунд")

            # Сохраняем данные в трекере производительности, если есть доступ к контейнеру
            # через self (первый аргумент)
            if (
                args
                and hasattr(args[0], "container")
                and hasattr(args[0].container, "performance_tracker")
            ):
                args[0].container.performance_tracker.add_execution_time(
                    name, execution_time
                )

            return result

        return wrapper

    return decorator


class PerformanceTracker:
    """Класс для отслеживания производительности пользовательских сценариев"""

    def __init__(self):
        # Изменяем структуру для хранения всех измерений для каждого сценария
        self.performance_data: Dict[str, List[float]] = {}

    def add_execution_time(self, scenario_name: str, execution_time: float) -> None:
        """Добавляет время выполнения сценария"""
        if scenario_name not in self.performance_data:
            self.performance_data[scenario_name] = []

        self.performance_data[scenario_name].append(execution_time)

    def start_measuring(self, scenario_name: str) -> int:
        """Начинает измерение времени для указанного сценария"""
        if scenario_name not in self.performance_data:
            self.performance_data[scenario_name] = []

        # Добавляем отрицательное время как маркер начала измерения
        self.performance_data[scenario_name].append(-time.time())
        return len(self.performance_data[scenario_name]) - 1

    def stop_measuring(self, scenario_name: str, session_id: int) -> float:
        """Завершает измерение времени для указанного сценария"""
        if scenario_name not in self.performance_data:
            raise ValueError(f"Сценарий '{scenario_name}' не найден")

        if session_id >= len(self.performance_data[scenario_name]):
            raise ValueError(
                f"Сессия {session_id} не найдена для сценария '{scenario_name}'"
            )

        # Получаем отрицательное время начала и преобразуем в положительное
        start_time = -self.performance_data[scenario_name][session_id]
        execution_time = time.time() - start_time

        # Заменяем маркер начала на фактическое время выполнения
        self.performance_data[scenario_name][session_id] = execution_time

        print(
            f"Время выполнения сценария '{scenario_name}': {execution_time:.6f} секунд"
        )
        return execution_time

    def get_average_execution_time(self, scenario_name: str) -> float:
        """Возвращает среднее время выполнения сценария"""
        if (
            scenario_name not in self.performance_data
            or not self.performance_data[scenario_name]
        ):
            return 0.0

        # Фильтруем отрицательные значения (маркеры начала)
        times = [t for t in self.performance_data[scenario_name] if t > 0]
        if not times:
            return 0.0

        return sum(times) / len(times)

    def report(self) -> Dict[str, Dict[str, float]]:
        """Возвращает полный отчет о производительности для всех сценариев"""
        result = {}
        for scenario in self.performance_data:
            # Фильтруем отрицательные значения (маркеры начала измерения)
            times = [t for t in self.performance_data[scenario] if t > 0]
            if times:
                result[scenario] = {
                    "avg_time": sum(times) / len(times),
                    "min_time": min(times),
                    "max_time": max(times),
                    "executions": len(times),
                }

        return result

    def some_user_operation(self):
        # Отслеживаем время выполнения этой операции
        with self.track_operation("Специальная операция"):
            # Код операции
            print("Выполняем специальную операцию...")
            time.sleep(1)  # Имитация работы
            print("Операция выполнена!")
