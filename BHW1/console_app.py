import os
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import List, Dict
from models import TransactionType, BankAccount, Category, Operation
from container import FinanceModuleContainer
from commands import GetOperationsCommand, PerformanceDecorator
from performance import measure_execution_time


class ConsoleApp:
    def __init__(self):
        self.container = FinanceModuleContainer()
        self.running = True

    def display_menu(self):
        print("\n===== МОДУЛЬ УЧЕТА ФИНАНСОВ =====")
        print("1. Управление счетами")
        print("2. Управление категориями")
        print("3. Управление операциями")
        print("4. Аналитика")
        print("5. Экспорт данных")
        print("6. Импорт данных")
        print("7. Управление балансами")
        print("8. Статистика производительности")
        print("0. Выход")
        print("==================================")

    def accounts_menu(self):
        while True:
            print("\n===== УПРАВЛЕНИЕ СЧЕТАМИ =====")
            print("1. Создать новый счет")
            print("2. Список всех счетов")
            print("3. Просмотр счета по ID")
            print("4. Обновление счета")
            print("5. Удаление счета")
            print("0. Назад")
            print("==============================")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.list_accounts()
            elif choice == "3":
                self.view_account()
            elif choice == "4":
                self.update_account()
            elif choice == "5":
                self.delete_account()
            elif choice == "0":
                break
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.")

    def categories_menu(self):
        while True:
            print("\n===== УПРАВЛЕНИЕ КАТЕГОРИЯМИ =====")
            print("1. Создать новую категорию")
            print("2. Список всех категорий")
            print("3. Просмотр категории по ID")
            print("4. Обновление категории")
            print("5. Удаление категории")
            print("0. Назад")
            print("==================================")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.create_category()
            elif choice == "2":
                self.list_categories()
            elif choice == "3":
                self.view_category()
            elif choice == "4":
                self.update_category()
            elif choice == "5":
                self.delete_category()
            elif choice == "0":
                break
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.")

    def operations_menu(self):
        while True:
            print("\n===== УПРАВЛЕНИЕ ОПЕРАЦИЯМИ =====")
            print("1. Создать новую операцию")
            print("2. Список всех операций")
            print("3. Просмотр операции по ID")
            print("4. Удаление операции")
            print("0. Назад")
            print("=================================")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.create_operation()
            elif choice == "2":
                self.list_operations()
            elif choice == "3":
                self.view_operation()
            elif choice == "4":
                self.delete_operation()
            elif choice == "0":
                break
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.")

    def analytics_menu(self):
        while True:
            print("\n===== АНАЛИТИКА =====")
            print("1. Баланс за период")
            print("2. Группировка по категориям")
            print("0. Назад")
            print("=====================")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.balance_for_period()
            elif choice == "2":
                self.group_by_category()
            elif choice == "0":
                break
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.")

    def export_menu(self):
        while True:
            print("\n===== ЭКСПОРТ ДАННЫХ =====")
            print("1. Экспорт операций в CSV")
            print("2. Экспорт операций в JSON")
            print("3. Экспорт операций в YAML")
            print("0. Назад")
            print("==========================")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.export_operations("csv")
            elif choice == "2":
                self.export_operations("json")
            elif choice == "3":
                self.export_operations("yaml")
            elif choice == "0":
                break
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.")

    def import_menu(self):
        while True:
            print("\n===== ИМПОРТ ДАННЫХ =====")
            print("1. Импорт операций из CSV")
            print("2. Импорт операций из JSON")
            print("3. Импорт операций из YAML")
            print("0. Назад")
            print("==========================")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.import_operations("csv")
            elif choice == "2":
                self.import_operations("json")
            elif choice == "3":
                self.import_operations("yaml")
            elif choice == "0":
                break
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.")

    def balance_menu(self):
        while True:
            print("\n===== УПРАВЛЕНИЕ БАЛАНСОМ =====")
            print("1. Проверить балансы счетов")
            print("2. Пересчитать балансы счетов")
            print("0. Назад")
            print("===============================")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.check_account_balances()
            elif choice == "2":
                self.recalculate_account_balances()
            elif choice == "0":
                break
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.")

    def performance_menu(self):
        while True:
            print("\n===== ПРОИЗВОДИТЕЛЬНОСТЬ =====")
            print("1. Просмотр статистики производительности")
            print("0. Назад")
            print("===============================")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.view_performance_stats()
            elif choice == "0":
                break
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.")

    # Функции для работы со счетами
    @measure_execution_time("Создание счета")
    def create_account(self):
        try:
            name = input("Введите название счета: ")
            balance_str = input("Введите начальный баланс: ")
            balance = Decimal(balance_str)

            account = self.container.bank_account_facade.create_account(name, balance)
            print(f"Счет успешно создан! ID: {account.id}")
        except ValueError as e:
            print(f"Ошибка: {e}")
        except InvalidOperation:
            print("Ошибка: Некорректная сумма баланса")

    def list_accounts(self):
        accounts = self.container.bank_account_facade.get_all_accounts()
        if not accounts:
            print("Список счетов пуст!")
            return

        print("\nСписок счетов:")
        for account in accounts:
            print(
                f"ID: {account.id}, Название: {account.name}, Баланс: {account.balance}"
            )

    def view_account(self):
        try:
            id_str = input("Введите ID счета: ")
            id = int(id_str)

            account = self.container.bank_account_facade.get_account(id)
            if not account:
                print(f"Счет с ID {id} не найден!")
                return

            print(f"\nИнформация о счете:")
            print(f"ID: {account.id}")
            print(f"Название: {account.name}")
            print(f"Баланс: {account.balance}")
        except ValueError:
            print("Ошибка: ID должен быть числом")

    @measure_execution_time("Обновление счета")
    def update_account(self):
        try:
            id_str = input("Введите ID счета: ")
            id = int(id_str)

            account = self.container.bank_account_facade.get_account(id)
            if not account:
                print(f"Счет с ID {id} не найден!")
                return

            name = input(f"Введите новое название счета [{account.name}]: ")
            if name:
                account.name = name

            self.container.bank_account_facade.update_account(account)
            print("Счет успешно обновлен!")
        except ValueError as e:
            print(f"Ошибка: {e}")

    @measure_execution_time("Удаление счета")
    def delete_account(self):
        try:
            id_str = input("Введите ID счета: ")
            id = int(id_str)

            account = self.container.bank_account_facade.get_account(id)
            if not account:
                print(f"Счет с ID {id} не найден!")
                return

            confirm = input(
                f"Вы уверены, что хотите удалить счет '{account.name}'? (y/n): "
            )
            if confirm.lower() == "y":
                self.container.bank_account_facade.delete_account(id)
                print("Счет успешно удален!")
        except ValueError:
            print("Ошибка: ID должен быть числом")

    # Функции для работы с категориями
    @measure_execution_time("Создание категории")
    def create_category(self):
        try:
            name = input("Введите название категории: ")

            print("Выберите тип категории:")
            print("1. Доход")
            print("2. Расход")
            type_choice = input("Ваш выбор: ")

            if type_choice == "1":
                type = TransactionType.INCOME
            elif type_choice == "2":
                type = TransactionType.EXPENSE
            else:
                print("Неверный выбор типа категории!")
                return

            category = self.container.category_facade.create_category(name, type)
            print(f"Категория успешно создана! ID: {category.id}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def list_categories(self):
        categories = self.container.category_facade.get_all_categories()
        if not categories:
            print("Список категорий пуст!")
            return

        print("\nСписок категорий:")
        for category in categories:
            print(
                f"ID: {category.id}, Название: {category.name}, Тип: {category.type.value}"
            )

    def view_category(self):
        try:
            id_str = input("Введите ID категории: ")
            id = int(id_str)

            category = self.container.category_facade.get_category(id)
            if not category:
                print(f"Категория с ID {id} не найдена!")
                return

            print(f"\nИнформация о категории:")
            print(f"ID: {category.id}")
            print(f"Название: {category.name}")
            print(f"Тип: {category.type.value}")
        except ValueError:
            print("Ошибка: ID должен быть числом")

    def update_category(self):
        try:
            id_str = input("Введите ID категории: ")
            id = int(id_str)

            category = self.container.category_facade.get_category(id)
            if not category:
                print(f"Категория с ID {id} не найдена!")
                return

            name = input(f"Введите новое название категории [{category.name}]: ")
            if name:
                category.name = name

            self.container.category_facade.update_category(category)
            print("Категория успешно обновлена!")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def delete_category(self):
        try:
            id_str = input("Введите ID категории: ")
            id = int(id_str)

            category = self.container.category_facade.get_category(id)
            if not category:
                print(f"Категория с ID {id} не найдена!")
                return

            confirm = input(
                f"Вы уверены, что хотите удалить категорию '{category.name}'? (y/n): "
            )
            if confirm.lower() == "y":
                self.container.category_facade.delete_category(id)
                print("Категория успешно удалена!")
        except ValueError:
            print("Ошибка: ID должен быть числом")

    # Функции для работы с операциями
    @measure_execution_time("Создание операции")
    def create_operation(self):
        try:
            # Выбор типа операции
            print("Выберите тип операции:")
            print("1. Доход")
            print("2. Расход")
            type_choice = input("Ваш выбор: ")

            if type_choice == "1":
                type = TransactionType.INCOME
            elif type_choice == "2":
                type = TransactionType.EXPENSE
            else:
                print("Неверный выбор типа операции!")
                return

            # Выбор счета
            accounts = self.container.bank_account_facade.get_all_accounts()
            if not accounts:
                print("Нет доступных счетов! Сначала создайте счет.")
                return

            print("\nДоступные счета:")
            for account in accounts:
                print(
                    f"ID: {account.id}, Название: {account.name}, Баланс: {account.balance}"
                )

            bank_account_id_str = input("Введите ID счета: ")
            bank_account_id = int(bank_account_id_str)

            # Проверка существования счета
            account = self.container.bank_account_facade.get_account(bank_account_id)
            if not account:
                print(f"Счет с ID {bank_account_id} не найден!")
                return

            # Ввод суммы
            amount_str = input("Введите сумму: ")
            amount = Decimal(amount_str)

            # Выбор категории (опционально)
            categories = [
                c
                for c in self.container.category_facade.get_all_categories()
                if c.type == type
            ]
            category_id = None

            if categories:
                print("\nДоступные категории:")
                for category in categories:
                    print(f"ID: {category.id}, Название: {category.name}")

                category_id_str = input("Введите ID категории (или оставьте пустым): ")
                if category_id_str:
                    category_id = int(category_id_str)
                    # Проверка существования категории
                    category = self.container.category_facade.get_category(category_id)
                    if not category or category.type != type:
                        print(
                            f"Категория с ID {category_id} не найдена или имеет неправильный тип!"
                        )
                        return

            # Ввод описания (опционально)
            description = input("Введите описание операции (или оставьте пустым): ")

            # Создание операции
            operation = self.container.operation_facade.create_operation(
                type, bank_account_id, amount, datetime.now(), category_id, description
            )

            print(f"Операция успешно создана! ID: {operation.id}")
        except ValueError as e:
            print(f"Ошибка: {e}")
        except InvalidOperation:
            print("Ошибка: Некорректная сумма")

    @measure_execution_time("Отображение списка операций")
    def list_operations(self):
        try:
            # Используем паттерн Команда с декоратором для измерения производительности
            command = GetOperationsCommand(self.container.operation_facade)
            decorated_command = PerformanceDecorator(
                command, "Получение списка операций", self.container.performance_tracker
            )
            operations = decorated_command.execute()

            if not operations:
                print("Список операций пуст!")
                return

            print("\nСписок операций:")
            for op in operations:
                category_name = "Без категории"
                if op.category_id:
                    category = self.container.category_repository.get_by_id(
                        op.category_id
                    )
                    if category:
                        category_name = category.name

                account_name = "Неизвестный счет"
                account = self.container.bank_account_repository.get_by_id(
                    op.bank_account_id
                )
                if account:
                    account_name = account.name

                print(
                    f"ID: {op.id}, Тип: {op.type.value}, Счет: {account_name}, "
                    f"Сумма: {op.amount}, Категория: {category_name}, "
                    f"Дата: {op.date.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                if op.description:
                    print(f"    Описание: {op.description}")
        except Exception as e:
            print(f"Ошибка при получении списка операций: {e}")

    def view_operation(self):
        try:
            id_str = input("Введите ID операции: ")
            id = int(id_str)

            operation = self.container.operation_facade.get_operation(id)
            if not operation:
                print(f"Операция с ID {id} не найдена!")
                return

            category_name = "Без категории"
            if operation.category_id:
                category = self.container.category_repository.get_by_id(
                    operation.category_id
                )
                if category:
                    category_name = category.name

            account_name = "Неизвестный счет"
            account = self.container.bank_account_repository.get_by_id(
                operation.bank_account_id
            )
            if account:
                account_name = account.name

            print(f"\nИнформация об операции:")
            print(f"ID: {operation.id}")
            print(f"Тип: {operation.type.value}")
            print(f"Счет: {account_name} (ID: {operation.bank_account_id})")
            print(f"Сумма: {operation.amount}")
            print(f"Категория: {category_name}")
            print(f"Дата: {operation.date.strftime('%Y-%m-%d %H:%M:%S')}")
            if operation.description:
                print(f"Описание: {operation.description}")
        except ValueError:
            print("Ошибка: ID должен быть числом")

    def delete_operation(self):
        try:
            id_str = input("Введите ID операции: ")
            id = int(id_str)

            operation = self.container.operation_facade.get_operation(id)
            if not operation:
                print(f"Операция с ID {id} не найдена!")
                return

            confirm = input(
                f"Вы уверены, что хотите удалить операцию с ID {id}? (y/n): "
            )
            if confirm.lower() == "y":
                self.container.operation_facade.delete_operation(id)
                print("Операция успешно удалена!")
        except ValueError:
            print("Ошибка: ID должен быть числом")

    # Функции для аналитики
    def balance_for_period(self):
        try:
            print("\nВведите начальную дату (в формате YYYY-MM-DD):")
            start_date_str = input()
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

            print("Введите конечную дату (в формате YYYY-MM-DD):")
            end_date_str = input()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59
            )

            balance = self.container.analytics_service.calculate_balance_for_period(
                start_date, end_date
            )
            print(f"\nБаланс за период с {start_date_str} по {end_date_str}: {balance}")
        except ValueError:
            print("Ошибка: некорректный формат даты")

    def group_by_category(self):
        try:
            print("\nВведите начальную дату (в формате YYYY-MM-DD):")
            start_date_str = input()
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

            print("Введите конечную дату (в формате YYYY-MM-DD):")
            end_date_str = input()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59
            )

            result = self.container.analytics_service.group_by_category(
                start_date, end_date
            )

            print(
                f"\nСводка по категориям за период с {start_date_str} по {end_date_str}:"
            )
            if not result:
                print("Нет данных за указанный период.")
                return

            for category_name, amount in result.items():
                sign = "+" if amount >= Decimal("0.0") else ""
                print(f"{category_name}: {sign}{amount}")
        except ValueError:
            print("Ошибка: некорректный формат даты")

    # Функции для экспорта данных
    def export_operations(self, format_type: str):
        operations = self.container.operation_facade.get_all_operations()
        if not operations:
            print("Нет данных для экспорта!")
            return

        operations_data = []
        for op in operations:
            category_name = "Без категории"
            if op.category_id:
                category = self.container.category_repository.get_by_id(op.category_id)
                if category:
                    category_name = category.name

            account_name = "Неизвестный счет"
            account = self.container.bank_account_repository.get_by_id(
                op.bank_account_id
            )
            if account:
                account_name = account.name

            operations_data.append(
                {
                    "id": op.id,
                    "type": op.type,
                    "account_name": account_name,
                    "account_id": op.bank_account_id,
                    "amount": op.amount,
                    "category_name": category_name,
                    "category_id": op.category_id,
                    "date": op.date,
                    "description": op.description,
                }
            )

        try:
            if format_type == "csv":
                data = self.container.csv_exporter.export_data(operations_data)
                filename = "operations.csv"
            elif format_type == "json":
                data = self.container.json_exporter.export_data(operations_data)
                filename = "operations.json"
            elif format_type == "yaml":
                data = self.container.yaml_exporter.export_data(operations_data)
                filename = "operations.yaml"
            else:
                print(f"Неподдерживаемый формат: {format_type}")
                return

            with open(filename, "w", encoding="utf-8") as file:
                file.write(data)

            print(f"Данные успешно экспортированы в {filename}")
        except Exception as e:
            print(f"Ошибка при экспорте данных: {e}")

    # Демонстрационные данные для быстрого тестирования
    def initialize_demo_data(self):
        # Создаем счета
        main_account = self.container.bank_account_facade.create_account(
            "Основной счет", Decimal("5000.0")
        )
        savings_account = self.container.bank_account_facade.create_account(
            "Сберегательный счет", Decimal("10000.0")
        )

        # Создаем категории доходов
        salary = self.container.category_facade.create_category(
            "Зарплата", TransactionType.INCOME
        )
        cashback = self.container.category_facade.create_category(
            "Кэшбэк", TransactionType.INCOME
        )

        # Создаем категории расходов
        food = self.container.category_facade.create_category(
            "Кафе", TransactionType.EXPENSE
        )
        health = self.container.category_facade.create_category(
            "Здоровье", TransactionType.EXPENSE
        )
        transport = self.container.category_facade.create_category(
            "Транспорт", TransactionType.EXPENSE
        )

        # Создаем операции
        now = datetime.now()

        # Доходы
        self.container.operation_facade.create_operation(
            TransactionType.INCOME,
            main_account.id,
            Decimal("50000.0"),
            now.replace(day=5),
            salary.id,
            "Зарплата за месяц",
        )
        self.container.operation_facade.create_operation(
            TransactionType.INCOME,
            main_account.id,
            Decimal("500.0"),
            now.replace(day=10),
            cashback.id,
            "Кэшбэк за покупки",
        )

        # Расходы
        self.container.operation_facade.create_operation(
            TransactionType.EXPENSE,
            main_account.id,
            Decimal("1500.0"),
            now.replace(day=12),
            food.id,
            "Обед в ресторане",
        )
        self.container.operation_facade.create_operation(
            TransactionType.EXPENSE,
            main_account.id,
            Decimal("3000.0"),
            now.replace(day=15),
            health.id,
            "Визит к врачу",
        )
        self.container.operation_facade.create_operation(
            TransactionType.EXPENSE,
            main_account.id,
            Decimal("500.0"),
            now.replace(day=20),
            transport.id,
            "Такси",
        )

        print("Демонстрационные данные успешно созданы!")

    @measure_execution_time("Импорт операций")
    def import_operations(self, format_type: str):
        try:
            print(f"\nВведите путь к файлу для импорта ({format_type}):")
            filepath = input()

            if not os.path.exists(filepath):
                print(f"Файл {filepath} не найден!")
                return

            with open(filepath, "r", encoding="utf-8") as file:
                data_str = file.read()

            if format_type == "csv":
                data = self.container.csv_importer.import_data(data_str)
            elif format_type == "json":
                data = self.container.json_importer.import_data(data_str)
            elif format_type == "yaml":
                data = self.container.yaml_importer.import_data(data_str)
            else:
                print(f"Неподдерживаемый формат: {format_type}")
                return

            # Перед импортом данных выводим список существующих счетов
            print("\nСуществующие счета перед импортом:")
            existing_accounts = self.container.bank_account_facade.get_all_accounts()
            for acc in existing_accounts:
                print(f"  ID: {acc.id}, Название: {acc.name}, Баланс: {acc.balance}")

            # Первый проход - собираем информацию о всех уникальных счетах
            unique_accounts = {}
            for item in data:
                if "bank_account_id" in item:
                    account_id = int(item.get("bank_account_id", 0))
                    account_name = item.get("account_name", f"Счет {account_id}")

                    # Запоминаем имя счета по ID
                    unique_accounts[account_id] = account_name

            print(f"\nУникальные счета в импортируемых данных: {len(unique_accounts)}")
            for acc_id, acc_name in unique_accounts.items():
                print(f"  ID: {acc_id}, Название: {acc_name}")

            # Создаем все необходимые счета до начала обработки операций
            created_accounts = {}
            for account_id, account_name in unique_accounts.items():
                # Проверяем, существует ли уже счет с таким ID
                existing_account = self.container.bank_account_facade.get_account(
                    account_id
                )

                if existing_account:
                    print(
                        f"Найден существующий счет: {existing_account.name} (ID: {account_id})"
                    )
                    created_accounts[account_id] = existing_account
                else:
                    # Создаем новый счет с заданным ID
                    print(f"Создаю новый счет: {account_name} (ID: {account_id})")

                    # Создаем счет с нулевым ID (как заглушку)
                    new_account = self.container.entity_factory.create_bank_account(
                        account_name
                    )

                    # Устанавливаем нужный ID и добавляем напрямую в репозиторий
                    new_account.id = account_id

                    # Важно: добавляем через репозиторий, а не через фасад!
                    # Фасад может создать новый объект и сбросить ID
                    account = self.container.bank_account_repository.add(new_account)
                    created_accounts[account_id] = account

            # Теперь обрабатываем операции, используя созданные счета
            imported_count = 0
            created_categories = {}

            for item in data:
                try:
                    account_id = int(item.get("bank_account_id", 0))

                    # Получаем созданный или существующий счет по ID
                    account = created_accounts.get(account_id)
                    if not account:
                        print(f"Ошибка: счет с ID {account_id} не найден!")
                        continue

                    # Обработка категории
                    category_id = None
                    if "category_id" in item and item["category_id"]:
                        category_id = int(item["category_id"])

                        # Проверяем, создавали ли мы уже эту категорию
                        if category_id in created_categories:
                            category = created_categories[category_id]
                        else:
                            # Проверяем, существует ли категория в БД
                            category = self.container.category_facade.get_category(
                                category_id
                            )

                            if not category:
                                # Создаем новую категорию с заданным ID
                                category_name = item.get(
                                    "category_name", f"Категория {category_id}"
                                )
                                category_type = item.get("type", TransactionType.INCOME)

                                print(
                                    f"Создаю новую категорию: {category_name} (ID: {category_id}, тип: {category_type.value})"
                                )

                                # Создаем категорию с нулевым ID (как заглушку)
                                new_category = (
                                    self.container.entity_factory.create_category(
                                        category_name, category_type
                                    )
                                )

                                # Устанавливаем нужный ID
                                new_category.id = category_id

                                # Добавляем через репозиторий
                                category = self.container.category_repository.add(
                                    new_category
                                )
                                created_categories[category_id] = category

                    # Подготовка данных для создания операции
                    operation_type = item.get("type", TransactionType.INCOME)
                    amount = Decimal(str(item.get("amount", "0")))
                    date = item.get("date", datetime.now())
                    description = item.get("description", "")

                    # Проверяем, достаточно ли средств для расходной операции
                    if (
                        operation_type == TransactionType.EXPENSE
                        and amount > account.balance
                    ):
                        # Автоматически пополняем счет
                        needed_deposit = amount - account.balance
                        account.deposit(needed_deposit)
                        print(
                            f"Автоматическое пополнение счета {account.name} (ID: {account.id}) на {needed_deposit} для операции"
                        )
                        self.container.bank_account_repository.update(account)

                    # Создаем операцию через фасад (он обновит баланс счета)
                    self.container.operation_facade.create_operation(
                        operation_type,
                        account.id,
                        amount,
                        date,
                        category_id,
                        description,
                    )
                    imported_count += 1

                except Exception as e:
                    print(f"Ошибка при импорте операции: {e}")

            # Выводим итоговую информацию
            print(f"\nИтоги импорта:")
            print(f"  Счетов: {len(created_accounts)}")
            print(f"  Категорий: {len(created_categories)}")
            print(f"  Операций: {imported_count} из {len(data)}")

            # Выводим информацию о счетах после импорта
            print("\nСчета после импорта:")
            updated_accounts = self.container.bank_account_facade.get_all_accounts()
            for acc in updated_accounts:
                print(f"  ID: {acc.id}, Название: {acc.name}, Баланс: {acc.balance}")

        except Exception as e:
            print(f"Ошибка при импорте данных: {e}")

    @measure_execution_time("Проверка балансов счетов")
    def check_account_balances(self):
        try:
            discrepancies = (
                self.container.analytics_service.recalculate_account_balances()
            )

            if not discrepancies:
                print("Балансы всех счетов корректны!")
                return

            print("\nОбнаружены несоответствия в балансах счетов:")
            for account, current_balance, calculated_balance in discrepancies:
                print(f"Счет: {account.name} (ID: {account.id})")
                print(f"  Текущий баланс: {current_balance}")
                print(f"  Расчетный баланс: {calculated_balance}")
                print(f"  Разница: {calculated_balance - current_balance}")
                print()

            print(
                "Для исправления несоответствий используйте пункт 'Пересчитать балансы счетов'"
            )
        except Exception as e:
            print(f"Ошибка при проверке балансов: {e}")

    @measure_execution_time("Пересчет балансов счетов")
    def recalculate_account_balances(self):
        try:
            fixed_accounts = self.container.analytics_service.fix_account_balances()

            if not fixed_accounts:
                print("Балансы всех счетов уже корректны!")
                return

            print("\nИсправлены балансы следующих счетов:")
            for account, old_balance, new_balance in fixed_accounts:
                print(f"Счет: {account.name} (ID: {account.id})")
                print(f"  Старый баланс: {old_balance}")
                print(f"  Новый баланс: {new_balance}")
                print(f"  Разница: {new_balance - old_balance}")
                print()
        except Exception as e:
            print(f"Ошибка при пересчете балансов: {e}")

    def view_performance_stats(self):
        report = self.container.performance_tracker.report()

        if not report:
            print("Статистика производительности недоступна!")
            return

        print("\nСтатистика производительности пользовательских операций:")
        for scenario_name, stats in report.items():
            print(f"\n{scenario_name}:")
            print(f"  Среднее время: {stats['avg_time']:.6f} сек.")
            print(f"  Минимальное время: {stats['min_time']:.6f} сек.")
            print(f"  Максимальное время: {stats['max_time']:.6f} сек.")
            print(f"  Количество выполнений: {stats['executions']}")

    def run(self):
        # Инициализация демо-данных (раскомментируйте, если нужно)
        # self.initialize_demo_data()

        while self.running:
            self.display_menu()
            choice = input("Выберите действие: ")

            if choice == "1":
                self.accounts_menu()
            elif choice == "2":
                self.categories_menu()
            elif choice == "3":
                self.operations_menu()
            elif choice == "4":
                self.analytics_menu()
            elif choice == "5":
                self.export_menu()
            elif choice == "6":
                self.import_menu()
            elif choice == "7":
                self.balance_menu()
            elif choice == "8":
                self.performance_menu()
            elif choice == "0":
                print("Выход из программы...")
                self.running = False
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.")
