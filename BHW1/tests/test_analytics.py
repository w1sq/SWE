from decimal import Decimal
from datetime import datetime, timedelta

from analytics import AnalyticsService
from repositories import (
    InMemoryBankAccountRepository,
    InMemoryCategoryRepository,
    InMemoryOperationRepository,
)
from models import BankAccount, Category, Operation, TransactionType


class TestAnalyticsService:
    def setup_method(self):
        self.operation_repo = InMemoryOperationRepository()
        self.category_repo = InMemoryCategoryRepository()
        self.account_repo = InMemoryBankAccountRepository()

        self.analytics = AnalyticsService(
            self.operation_repo, self.category_repo, self.account_repo
        )

        self.account = self.account_repo.add(
            BankAccount(0, "Test Account", Decimal("0"))
        )

        self.income_category = self.category_repo.add(
            Category(0, "Salary", TransactionType.INCOME)
        )
        self.expense_category = self.category_repo.add(
            Category(0, "Food", TransactionType.EXPENSE)
        )

        self.today = datetime.now()
        self.yesterday = self.today - timedelta(days=1)
        self.tomorrow = self.today + timedelta(days=1)

        self.operation_repo.add(
            Operation(
                0,
                TransactionType.INCOME,
                self.account.id,
                Decimal("1000"),
                self.yesterday,
                self.income_category.id,
                "Yesterday income",
            )
        )

        self.operation_repo.add(
            Operation(
                0,
                TransactionType.EXPENSE,
                self.account.id,
                Decimal("300"),
                self.today,
                self.expense_category.id,
                "Today expense",
            )
        )

        self.operation_repo.add(
            Operation(
                0,
                TransactionType.INCOME,
                self.account.id,
                Decimal("500"),
                self.tomorrow,
                self.income_category.id,
                "Tomorrow income",
            )
        )

    def test_calculate_balance_for_period_all(self):
        balance = self.analytics.calculate_balance_for_period(
            self.yesterday, self.tomorrow
        )
        assert balance == Decimal("1200")

    def test_calculate_balance_for_period_partial(self):
        balance = self.analytics.calculate_balance_for_period(
            self.yesterday, self.today
        )
        assert balance == Decimal("700")

    def test_group_by_category(self):
        result = self.analytics.group_by_category(self.yesterday, self.tomorrow)

        assert result[self.income_category.name] == Decimal("1500")
        assert result[self.expense_category.name] == Decimal("-300")


class TestAnalyticsServiceExtended:
    def setup_method(self):
        self.operation_repo = InMemoryOperationRepository()
        self.category_repo = InMemoryCategoryRepository()
        self.account_repo = InMemoryBankAccountRepository()

        self.analytics = AnalyticsService(
            self.operation_repo, self.category_repo, self.account_repo
        )

        self.account1 = self.account_repo.add(
            BankAccount(0, "Account 1", Decimal("1000"))
        )
        self.account2 = self.account_repo.add(
            BankAccount(0, "Account 2", Decimal("2000"))
        )

        self.income_category = self.category_repo.add(
            Category(0, "Salary", TransactionType.INCOME)
        )
        self.expense_category = self.category_repo.add(
            Category(0, "Food", TransactionType.EXPENSE)
        )

        self.today = datetime.now()
        self.month_start = datetime(self.today.year, self.today.month, 1)
        self.prev_month_start = self.month_start - timedelta(days=self.month_start.day)

        self.operation_repo.add(
            Operation(
                0,
                TransactionType.INCOME,
                self.account1.id,
                Decimal("5000"),
                self.month_start + timedelta(days=5),
                self.income_category.id,
                "Salary current month",
            )
        )

        self.operation_repo.add(
            Operation(
                0,
                TransactionType.EXPENSE,
                self.account1.id,
                Decimal("1000"),
                self.month_start + timedelta(days=10),
                self.expense_category.id,
                "Food current month",
            )
        )

        self.operation_repo.add(
            Operation(
                0,
                TransactionType.INCOME,
                self.account1.id,
                Decimal("4500"),
                self.prev_month_start + timedelta(days=5),
                self.income_category.id,
                "Salary previous month",
            )
        )

        self.operation_repo.add(
            Operation(
                0,
                TransactionType.EXPENSE,
                self.account1.id,
                Decimal("800"),
                self.prev_month_start + timedelta(days=10),
                self.expense_category.id,
                "Food previous month",
            )
        )

    def test_recalculate_account_balances(self):
        self.account1.balance = Decimal("2000")
        self.account_repo.update(self.account1)

        discrepancies = self.analytics.recalculate_account_balances()

        assert len(discrepancies) > 0

        for account, current_balance, calculated_balance in discrepancies:
            if account.id == self.account1.id:
                assert current_balance == Decimal("2000")
                break

    def test_fix_account_balances(self):
        self.account1.balance = Decimal("2000")
        self.account_repo.update(self.account1)

        fixed = self.analytics.fix_account_balances()

        assert len(fixed) > 0

        for account, old_balance, new_balance in fixed:
            if account.id == self.account1.id:
                assert old_balance == Decimal("2000")
                break
