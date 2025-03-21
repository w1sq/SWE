from container import FinanceModuleContainer
from repositories import (
    InMemoryBankAccountRepository,
    InMemoryCategoryRepository,
    InMemoryOperationRepository,
)
from validators import BankAccountValidator, CategoryValidator, OperationValidator
from facades import BankAccountFacade, CategoryFacade, OperationFacade
from analytics import AnalyticsService
from exporters import CSVExporter, JSONExporter, YAMLExporter
from importers import CSVImporter, JSONImporter, YAMLImporter
from proxy import OperationRepositoryProxy
from performance import PerformanceTracker
from factories import EntityFactory


class TestFinanceModuleContainer:
    def test_container_initialization(self):
        container = FinanceModuleContainer()

        assert isinstance(
            container.bank_account_repository, InMemoryBankAccountRepository
        )
        assert isinstance(container.category_repository, InMemoryCategoryRepository)
        assert isinstance(container.operation_repository, InMemoryOperationRepository)
        assert isinstance(
            container.operation_repository_proxy, OperationRepositoryProxy
        )

        assert isinstance(container.bank_account_validator, BankAccountValidator)
        assert isinstance(container.category_validator, CategoryValidator)
        assert isinstance(container.operation_validator, OperationValidator)

        assert isinstance(container.entity_factory, EntityFactory)

        assert isinstance(container.bank_account_facade, BankAccountFacade)
        assert isinstance(container.category_facade, CategoryFacade)
        assert isinstance(container.operation_facade, OperationFacade)

        assert isinstance(container.analytics_service, AnalyticsService)

        assert isinstance(container.csv_exporter, CSVExporter)
        assert isinstance(container.json_exporter, JSONExporter)
        assert isinstance(container.yaml_exporter, YAMLExporter)
        assert isinstance(container.csv_importer, CSVImporter)
        assert isinstance(container.json_importer, JSONImporter)
        assert isinstance(container.yaml_importer, YAMLImporter)

        assert isinstance(container.performance_tracker, PerformanceTracker)

    def test_repository_dependencies(self):
        container = FinanceModuleContainer()

        assert (
            container.operation_repository_proxy.real_repository
            is container.operation_repository
        )

        assert (
            container.bank_account_facade.repository
            is container.bank_account_repository
        )
        assert container.category_facade.repository is container.category_repository
        assert container.operation_facade.repository is container.operation_repository

        assert (
            container.bank_account_facade.validator is container.bank_account_validator
        )
        assert container.category_facade.validator is container.category_validator
        assert container.operation_facade.validator is container.operation_validator

        assert (
            container.analytics_service.operation_repository
            is container.operation_repository
        )
        assert (
            container.analytics_service.category_repository
            is container.category_repository
        )
        assert (
            container.analytics_service.account_repository
            is container.bank_account_repository
        )
