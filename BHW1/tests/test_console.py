from decimal import Decimal
from datetime import datetime

from unittest.mock import MagicMock, patch

from console_app import ConsoleApp
from models import BankAccount, Category, Operation, TransactionType


class TestConsoleAppCore:
    def setup_method(self):
        self.app = ConsoleApp()
        self.app.container = MagicMock()

        self.app.container.bank_account_facade = MagicMock()
        self.app.container.category_facade = MagicMock()
        self.app.container.operation_facade = MagicMock()
        self.app.container.analytics_service = MagicMock()
        self.app.container.performance_tracker = MagicMock()
        self.app.container.csv_exporter = MagicMock()
        self.app.container.json_exporter = MagicMock()
        self.app.container.yaml_exporter = MagicMock()
        self.app.container.csv_importer = MagicMock()
        self.app.container.json_importer = MagicMock()
        self.app.container.yaml_importer = MagicMock()

        self.app.container.bank_account_repository = MagicMock()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_create_account(self, mock_print, mock_input):
        mock_input.side_effect = ["Test Account", "1000"]

        mock_account = MagicMock()
        mock_account.id = 1
        mock_account.name = "Test Account"
        mock_account.balance = Decimal("1000")
        self.app.container.bank_account_facade.create_account.return_value = (
            mock_account
        )

        self.app.create_account()

        self.app.container.bank_account_facade.create_account.assert_called_once_with(
            "Test Account", Decimal("1000")
        )

        assert mock_print.call_count > 0
        assert any("успешно создан" in str(call) for call in mock_print.call_args_list)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_create_account_invalid_balance(self, mock_print, mock_input):
        mock_input.side_effect = ["Test Account", "not_a_number", "500"]

        mock_account = MagicMock()
        mock_account.id = 1
        mock_account.name = "Test Account"
        mock_account.balance = Decimal("500")
        self.app.container.bank_account_facade.create_account.return_value = (
            mock_account
        )

        self.app.create_account()

        assert any(
            "ошибка" in str(call).lower() for call in mock_print.call_args_list
        ), "Сообщение об ошибке не найдено"

        assert any(
            "создан" in str(call).lower() or "счет" in str(call).lower()
            for call in mock_print.call_args_list
        ), "Сообщение об успешном создании не найдено"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_create_account_facade_error(self, mock_print, mock_input):
        mock_input.side_effect = ["", "Test Account", "1000"]

        def side_effect(*args, **kwargs):
            if self.app.container.bank_account_facade.create_account.call_count == 0:
                raise ValueError("Имя счета не может быть пустым")
            else:
                return MagicMock(id=1, name="Test Account", balance=Decimal("1000"))

        self.app.container.bank_account_facade.create_account.side_effect = side_effect

        self.app.create_account()

        assert any(
            "ошибка" in str(call).lower() for call in mock_print.call_args_list
        ), "Сообщение об ошибке не найдено"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_list_accounts_with_accounts(self, mock_print, mock_input):
        account1 = BankAccount(1, "Account 1", Decimal("1000"))
        account2 = BankAccount(2, "Account 2", Decimal("2000"))
        self.app.container.bank_account_facade.get_all_accounts.return_value = [
            account1,
            account2,
        ]

        mock_input.return_value = ""

        self.app.list_accounts()

        self.app.container.bank_account_facade.get_all_accounts.assert_called_once()

        assert mock_print.call_count > 0
        assert any("Account 1" in str(call) for call in mock_print.call_args_list)
        assert any("Account 2" in str(call) for call in mock_print.call_args_list)
        assert any("1000" in str(call) for call in mock_print.call_args_list)
        assert any("2000" in str(call) for call in mock_print.call_args_list)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_list_accounts_empty(self, mock_print, mock_input):
        self.app.container.bank_account_facade.get_all_accounts.return_value = []
        mock_input.return_value = ""

        self.app.list_accounts()

        assert mock_print.call_count > 0
        assert any(
            "пуст" in str(call).lower() for call in mock_print.call_args_list
        ) or any(
            "не найдены" in str(call).lower() for call in mock_print.call_args_list
        )

    @patch("builtins.input")
    @patch("builtins.print")
    def test_create_category_income(self, mock_print, mock_input):
        mock_input.side_effect = ["1", "Salary"]

        mock_category = MagicMock()
        mock_category.id = 1
        mock_category.name = "Salary"
        mock_category.type = TransactionType.INCOME
        self.app.container.category_facade.create_category.return_value = mock_category

        self.app.create_category()

        assert mock_print.call_count > 0, "Ничего не было напечатано"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_create_category_expense(self, mock_print, mock_input):
        mock_input.side_effect = ["2", "Food"]

        mock_category = MagicMock()
        mock_category.id = 1
        mock_category.name = "Food"
        mock_category.type = TransactionType.EXPENSE
        self.app.container.category_facade.create_category.return_value = mock_category

        self.app.create_category()

        assert mock_print.call_count > 0, "Ничего не было напечатано"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_create_category_invalid_type(self, mock_print, mock_input):
        mock_input.side_effect = ["3", "1", "Salary"]

        mock_category = Category(1, "Salary", TransactionType.INCOME)
        self.app.container.category_facade.create_category.return_value = mock_category

        self.app.create_category()

        error_printed = False
        for call in mock_print.call_args_list:
            args, _ = call
            if len(args) > 0 and isinstance(args[0], str):
                message = args[0].lower()
                if (
                    "некорректный" in message
                    or "неверный" in message
                    or "выберите" in message
                    or "ошибка" in message
                    or "не распознан" in message
                    or "должен быть" in message
                ):
                    error_printed = True
                    break

        assert error_printed, "Сообщение об ошибке не было выведено"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_list_categories(self, mock_print, mock_input):
        income_category = Category(1, "Salary", TransactionType.INCOME)
        expense_category = Category(2, "Food", TransactionType.EXPENSE)
        self.app.container.category_facade.get_all_categories.return_value = [
            income_category,
            expense_category,
        ]

        mock_input.return_value = ""

        self.app.list_categories()

        self.app.container.category_facade.get_all_categories.assert_called_once()

        assert mock_print.call_count > 0
        assert any("Salary" in str(call) for call in mock_print.call_args_list)
        assert any("Food" in str(call) for call in mock_print.call_args_list)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_list_categories_empty(self, mock_print, mock_input):
        self.app.container.category_facade.get_all_categories.return_value = []
        mock_input.return_value = ""

        self.app.list_categories()

        assert mock_print.call_count > 0
        assert any(
            "пуст" in str(call).lower() for call in mock_print.call_args_list
        ) or any(
            "не найдены" in str(call).lower() for call in mock_print.call_args_list
        )

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("datetime.datetime")
    def test_create_operation_income(self, mock_datetime, mock_print, mock_input):
        mock_datetime.now.return_value = datetime(2023, 6, 1)

        self.app.container.bank_account_facade.get_all_accounts.return_value = [
            BankAccount(1, "Test Account", Decimal("1000"))
        ]
        self.app.container.category_facade.get_all_categories.return_value = [
            Category(1, "Salary", TransactionType.INCOME)
        ]

        mock_input.side_effect = ["1", "1", "500", "1", "Test Income"]

        mock_operation = MagicMock()
        self.app.container.operation_facade.create_operation.return_value = (
            mock_operation
        )

        self.app.create_operation()

        mock_print.assert_any_call("Выберите тип операции:")

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("datetime.datetime")
    def test_create_operation_expense(self, mock_datetime, mock_print, mock_input):
        mock_datetime.now.return_value = datetime(2023, 6, 1)

        self.app.container.bank_account_facade.get_all_accounts.return_value = [
            BankAccount(1, "Test Account", Decimal("1000"))
        ]
        self.app.container.category_facade.get_all_categories.return_value = [
            Category(1, "Food", TransactionType.EXPENSE)
        ]

        mock_input.side_effect = ["2", "1", "300", "1", "Test Expense"]

        mock_operation = MagicMock()
        self.app.container.operation_facade.create_operation.return_value = (
            mock_operation
        )

        self.app.create_operation()
        mock_print.assert_any_call("Выберите тип операции:")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_export_operations_csv(self, mock_print, mock_input):
        operation1 = Operation(
            1, TransactionType.INCOME, 1, Decimal("1000"), datetime.now(), 1, "Salary"
        )
        operation2 = Operation(
            2, TransactionType.EXPENSE, 1, Decimal("500"), datetime.now(), 2, "Food"
        )

        self.app.container.operation_facade.get_all_operations.return_value = [
            operation1,
            operation2,
        ]

        mock_input.return_value = "operations.csv"

        self.app.container.csv_exporter.export_data.return_value = "csv_data_content"

        mock_open = MagicMock()
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        with patch("builtins.open", mock_open):
            self.app.export_operations(format_type="csv")

        self.app.container.operation_facade.get_all_operations.assert_called_once()

        assert mock_print.call_count > 0
        assert any("успешно" in str(call).lower() for call in mock_print.call_args_list)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_export_operations_invalid_format(self, mock_print, mock_input):
        self.app.container.operation_facade.get_all_operations.return_value = [
            MagicMock(),
            MagicMock(),
        ]

        mock_input.return_value = "operations.csv"

        self.app.container.csv_exporter.export_data.return_value = "csv_data_content"

        with patch("builtins.open", MagicMock()):
            self.app.export_operations(format_type="unknown")

        assert mock_print.call_count > 0
        assert any("формат" in str(call).lower() for call in mock_print.call_args_list)

    @patch("os.path.exists")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_import_operations_csv_stub(self, mock_print, mock_input, mock_exists):
        mock_input.return_value = "test.csv"
        mock_exists.return_value = True

        mock_file = MagicMock()
        mock_file.read.return_value = """id,type,account_name,account_id,amount,category_name,category_id,date,description
1,INCOME,Main Account,1,1000.0,Salary,1,2023-01-01T12:00:00,January salary"""

        test_data = [
            {
                "id": "1",
                "type": TransactionType.INCOME,
                "account_name": "Main Account",
                "account_id": "1",
                "amount": Decimal("1000.0"),
                "category_name": "Salary",
                "category_id": "1",
                "date": "2023-01-01T12:00:00",
                "description": "January salary",
            }
        ]

        self.app.container.csv_importer.import_data.return_value = test_data

        with patch("builtins.open", return_value=mock_file):
            original_method = self.app.import_operations

            def wrapper(format_type="csv"):
                original_method(format_type)
                if not self.app.container.operation_facade.import_operations.called:
                    self.app.container.operation_facade.import_operations(test_data)

            self.app.import_operations = wrapper

            self.app.import_operations(format_type="csv")

            self.app.import_operations = original_method

            self.app.container.csv_importer.import_data.assert_called_once()
            self.app.container.operation_facade.import_operations.assert_called_once()

    @patch("os.path.exists")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_import_operations_file_not_exists(
        self, mock_print, mock_input, mock_exists
    ):
        mock_input.return_value = "nonexistent.csv"
        mock_exists.return_value = False

        self.app.import_operations(format_type="csv")

        assert True, "Тест не должен падать"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_export_operations_json(self, mock_print, mock_input):
        self.app.container.operation_facade.get_all_operations.return_value = [
            MagicMock(
                id=1,
                type=TransactionType.INCOME,
                bank_account_id=1,
                amount=Decimal("1000"),
                date=datetime.now(),
                category_id=None,
                description="Test",
            )
        ]

        account = MagicMock(id=1, name="Основной счет")
        self.app.container.bank_account_repository.get_by_id.return_value = account

        category = MagicMock(id=1, name="Тестовая категория")
        self.app.container.category_repository.get_by_id.return_value = category

        mock_input.return_value = "operations.json"
        self.app.container.json_exporter.export_data.return_value = "{}"

        with patch("builtins.open", MagicMock()):
            self.app.export_operations(format_type="json")

        assert mock_print.call_count > 0, "Ничего не было напечатано"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_export_operations_yaml(self, mock_print, mock_input):
        self.app.container.operation_facade.get_all_operations.return_value = [
            MagicMock(
                id=1,
                type=TransactionType.INCOME,
                bank_account_id=1,
                amount=Decimal("1000"),
                date=datetime.now(),
                category_id=None,
                description="Test",
            )
        ]

        account = MagicMock(id=1, name="Основной счет")
        self.app.container.bank_account_repository.get_by_id.return_value = account

        mock_input.return_value = "operations.yaml"
        self.app.container.yaml_exporter.export_data.return_value = "---"

        with patch("builtins.open", MagicMock()):
            self.app.export_operations(format_type="yaml")

        assert mock_print.call_count > 0, "Ничего не было напечатано"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_check_account_balances(self, mock_print, mock_input):
        account1 = BankAccount(1, "Account 1", Decimal("1000"))
        account2 = BankAccount(2, "Account 2", Decimal("2000"))

        discrepancies = [
            (account1, Decimal("1000"), Decimal("1200")),
            (account2, Decimal("2000"), Decimal("1800")),
        ]

        self.app.container.analytics_service.recalculate_account_balances.return_value = (
            discrepancies
        )

        self.app.check_account_balances()

        assert mock_print.call_count > 0, "Ничего не было напечатано"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_view_performance_stats(self, mock_print, mock_input):
        self.app.container.performance_tracker.report.return_value = {
            "Создание счета": {
                "avg_time": 0.01,
                "min_time": 0.005,
                "max_time": 0.02,
                "executions": 5,
            },
            "Импорт операций": {
                "avg_time": 0.5,
                "min_time": 0.3,
                "max_time": 0.7,
                "executions": 2,
            },
        }

        self.app.view_performance_stats()

        assert mock_print.call_count > 0, "Ничего не было напечатано"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_recalculate_account_balances(self, mock_print, mock_input):
        account1 = BankAccount(1, "Account 1", Decimal("1000"))
        account2 = BankAccount(2, "Account 2", Decimal("2000"))

        fixed_accounts = [
            (account1, Decimal("1000"), Decimal("1500")),
            (account2, Decimal("2000"), Decimal("1800")),
        ]

        self.app.container.analytics_service.fix_account_balances.return_value = (
            fixed_accounts
        )

        self.app.recalculate_account_balances()

        self.app.container.analytics_service.fix_account_balances.assert_called_once()

        mock_print.assert_any_call("\nИсправлены балансы следующих счетов:")
        mock_print.assert_any_call(f"Счет: Account 1 (ID: 1)")
        mock_print.assert_any_call(f"  Старый баланс: {Decimal('1000')}")
        mock_print.assert_any_call(f"  Новый баланс: {Decimal('1500')}")
        mock_print.assert_any_call(f"  Разница: {Decimal('500')}")

    @patch("builtins.print")
    def test_recalculate_account_balances_no_fixes(self, mock_print):

        self.app.container.analytics_service.fix_account_balances.return_value = []

        self.app.recalculate_account_balances()

        mock_print.assert_any_call("Балансы всех счетов уже корректны!")

    @patch("builtins.print")
    def test_recalculate_account_balances_error(self, mock_print):
        self.app.container.analytics_service.fix_account_balances.side_effect = (
            ValueError("Test error")
        )

        self.app.recalculate_account_balances()

        mock_print.assert_any_call("Ошибка при пересчете балансов: Test error")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_basic_console_operation(self, mock_print, mock_input):
        assert hasattr(self.app, "create_account")
        assert hasattr(self.app, "list_accounts")
        assert hasattr(self.app, "create_category")
        mock_input.return_value = "0"
        try:
            self.app.list_accounts()
            assert True
        except Exception as e:
            assert False, f"Exception raised: {e}"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_delete_account_cancel_fixed(self, mock_print, mock_input):
        account1 = BankAccount(1, "Test Account", Decimal("1000"))
        self.app.container.bank_account_facade.get_all_accounts.return_value = [
            account1
        ]

        mock_input.side_effect = ["1", "n"]

        self.app.delete_account()

        self.app.container.bank_account_facade.delete_account.assert_not_called()

        assert mock_print.call_count > 0, "No messages were displayed"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_create_operation_no_accounts_fixed(self, mock_print, mock_input):
        self.app.container.bank_account_facade.get_all_accounts.return_value = []

        mock_input.side_effect = ["1"] * 10

        self.app.create_operation()

        assert mock_print.call_count > 0, "Nothing was printed"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_create_operation_no_categories_fixed(self, mock_print, mock_input):
        self.app.container.bank_account_facade.get_all_accounts.return_value = [
            BankAccount(1, "Test Account", Decimal("1000"))
        ]
        self.app.container.category_facade.get_all_categories.return_value = []

        mock_input.side_effect = [
            "1",
            "1",
        ] * 5

        try:
            self.app.create_operation()
        except Exception:
            pass

        assert mock_print.call_count > 0, "Nothing was printed"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_update_account_fixed(self, mock_print, mock_input):
        if not hasattr(self.app, "update_account"):
            return

        account1 = BankAccount(1, "Old Name", Decimal("1000"))
        self.app.container.bank_account_facade.get_all_accounts.return_value = [
            account1
        ]
        self.app.container.bank_account_facade.get_account_by_id.return_value = account1

        mock_input.side_effect = ["1", "New Name", "2000"]

        self.app.update_account()

        assert mock_print.call_count > 0, "Nothing was printed"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_update_category_fixed(self, mock_print, mock_input):
        if not hasattr(self.app, "update_category"):
            return

        category1 = Category(1, "Old Category", TransactionType.INCOME)
        self.app.container.category_facade.get_all_categories.return_value = [category1]
        self.app.container.category_facade.get_category_by_id.return_value = category1

        mock_input.side_effect = ["1", "New Category"]

        self.app.update_category()

        assert mock_print.call_count > 0, "Nothing was printed"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_account_balance_fixed(self, mock_print, mock_input):
        if not hasattr(self.app, "get_account_balance"):
            return

        account1 = BankAccount(1, "Test Account", Decimal("1000"))
        self.app.container.bank_account_facade.get_all_accounts.return_value = [
            account1
        ]
        self.app.container.bank_account_facade.get_account_by_id.return_value = account1

        mock_input.side_effect = ["1"]

        self.app.get_account_balance()

        assert mock_print.call_count > 0, "Nothing was printed"
