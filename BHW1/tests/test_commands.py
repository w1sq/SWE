from decimal import Decimal
from datetime import datetime

from unittest.mock import MagicMock, patch

from facades import OperationFacade, BankAccountFacade, CategoryFacade
from performance import PerformanceDecorator
from models import Operation, TransactionType
from commands import (
    Command,
    GetOperationsCommand,
    CreateAccountCommand,
    CreateCategoryCommand,
    CreateOperationCommand,
)


class TestCommand:
    def test_get_operations_command(self):
        mock_facade = MagicMock(spec=OperationFacade)

        op1 = Operation(1, TransactionType.INCOME, 1, Decimal("100.0"), datetime.now())
        op2 = Operation(2, TransactionType.EXPENSE, 1, Decimal("50.0"), datetime.now())
        mock_facade.get_all_operations.return_value = [op1, op2]

        command = GetOperationsCommand(mock_facade)
        result = command.execute()

        mock_facade.get_all_operations.assert_called_once()

        assert len(result) == 2
        assert result[0] == op1
        assert result[1] == op2

    def test_performance_decorator_with_get_operations(self):
        mock_facade = MagicMock(spec=OperationFacade)
        mock_facade.get_all_operations.return_value = []
        base_command = GetOperationsCommand(mock_facade)

        decorator = PerformanceDecorator(base_command)

        with patch("builtins.print") as mock_print:
            result = decorator.execute()

        mock_facade.get_all_operations.assert_called_once()

        assert mock_print.call_count > 0, "No output was printed"
        assert any(
            "Время выполнения" in str(call) for call in mock_print.call_args_list
        ), "Performance timing message not found"

    @patch("time.time")
    def test_performance_decorator_time_calculation(self, mock_time):
        mock_time.side_effect = [10.0, 10.5]

        mock_command = MagicMock(spec=Command)
        mock_command.execute.return_value = "test result"

        decorator = PerformanceDecorator(mock_command)

        with patch("builtins.print") as mock_print:
            result = decorator.execute()

        mock_command.execute.assert_called_once()

        assert result == "test result"

        assert mock_print.call_count > 0, "No output was printed"

        output_str = mock_print.call_args[0][0]
        assert "0.500000 секунд" in output_str, "Timing value not found in output"

    def test_create_account_command(self):
        mock_facade = MagicMock(spec=BankAccountFacade)
        mock_account = MagicMock(id=1, name="Test Account", balance=Decimal("100.0"))
        mock_facade.create_account.return_value = mock_account

        command = CreateAccountCommand(mock_facade, "Test Account", Decimal("100.0"))
        result = command.execute()

        mock_facade.create_account.assert_called_once_with(
            "Test Account", Decimal("100.0")
        )
        assert result == mock_account

    def test_create_category_command(self):
        mock_facade = MagicMock(spec=CategoryFacade)
        mock_category = MagicMock(id=1, name="Food", type=TransactionType.EXPENSE)
        mock_facade.create_category.return_value = mock_category

        command = CreateCategoryCommand(mock_facade, "Food", TransactionType.EXPENSE)
        result = command.execute()

        mock_facade.create_category.assert_called_once_with(
            "Food", TransactionType.EXPENSE
        )
        assert result == mock_category

    def test_create_operation_command(self):
        mock_facade = MagicMock(spec=OperationFacade)
        date = datetime.now()
        mock_operation = MagicMock(
            id=1,
            type=TransactionType.INCOME,
            bank_account_id=1,
            amount=Decimal("500.0"),
            date=date,
        )
        mock_facade.create_operation.return_value = mock_operation

        command = CreateOperationCommand(
            mock_facade, TransactionType.INCOME, 1, Decimal("500.0"), date
        )
        result = command.execute()

        mock_facade.create_operation.assert_called_once_with(
            TransactionType.INCOME, 1, Decimal("500.0"), date, None, ""
        )
        assert result == mock_operation
