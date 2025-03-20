from repositories import (
    InMemoryBankAccountRepository,
    InMemoryCategoryRepository,
    InMemoryOperationRepository,
)
from validators import BankAccountValidator, CategoryValidator, OperationValidator
from factories import EntityFactory
from facades import BankAccountFacade, CategoryFacade, OperationFacade
from analytics import AnalyticsService
from exporters import CSVExporter, JSONExporter, YAMLExporter
from importers import CSVImporter, JSONImporter, YAMLImporter
from proxy import OperationRepositoryProxy
from performance import PerformanceTracker


class FinanceModuleContainer:
    def __init__(self):
        # Репозитории
        self.bank_account_repository = InMemoryBankAccountRepository()
        self.category_repository = InMemoryCategoryRepository()
        self.operation_repository = InMemoryOperationRepository()
        self.operation_repository_proxy = OperationRepositoryProxy(
            self.operation_repository
        )

        # Валидаторы
        self.bank_account_validator = BankAccountValidator()
        self.category_validator = CategoryValidator()
        self.operation_validator = OperationValidator()

        # Фабрика
        self.entity_factory = EntityFactory()

        # Фасады
        self.bank_account_facade = BankAccountFacade(
            self.bank_account_repository, self.bank_account_validator
        )
        self.category_facade = CategoryFacade(
            self.category_repository, self.category_validator
        )
        self.operation_facade = OperationFacade(
            self.operation_repository,
            self.operation_validator,
            self.bank_account_repository,
        )

        # Аналитика
        self.analytics_service = AnalyticsService(
            self.operation_repository,
            self.category_repository,
            self.bank_account_repository,
        )

        # Экспортеры
        self.csv_exporter = CSVExporter()
        self.json_exporter = JSONExporter()
        self.yaml_exporter = YAMLExporter()

        # Импортеры
        self.csv_importer = CSVImporter()
        self.json_importer = JSONImporter()
        self.yaml_importer = YAMLImporter()

        # Отслеживание производительности
        self.performance_tracker = PerformanceTracker()
