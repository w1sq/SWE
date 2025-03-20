from typing import Dict, List, Tuple
from decimal import Decimal
from datetime import datetime

from repositories import (
    InMemoryOperationRepository,
    InMemoryCategoryRepository,
    InMemoryBankAccountRepository,
)
from models import TransactionType, BankAccount, Operation


class AnalyticsService:
    def __init__(
        self,
        operation_repository: InMemoryOperationRepository,
        category_repository: InMemoryCategoryRepository,
        account_repository: InMemoryBankAccountRepository = None,
    ):
        self.operation_repository = operation_repository
        self.category_repository = category_repository
        self.account_repository = account_repository

    def calculate_balance_for_period(
        self, start_date: datetime, end_date: datetime
    ) -> Decimal:
        operations = self.operation_repository.get_all()
        balance = Decimal("0.0")

        for op in operations:
            if start_date <= op.date <= end_date:
                if op.type == TransactionType.INCOME:
                    balance += op.amount
                else:
                    balance -= op.amount

        return balance

    def group_by_category(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Decimal]:
        operations = self.operation_repository.get_all()
        result = {}

        for op in operations:
            if start_date <= op.date <= end_date and op.category_id:
                category = self.category_repository.get_by_id(op.category_id)
                if category:
                    if category.name not in result:
                        result[category.name] = Decimal("0.0")

                    if op.type == TransactionType.INCOME:
                        result[category.name] += op.amount
                    else:
                        result[category.name] -= op.amount

        return result

    def recalculate_account_balances(
        self,
    ) -> List[Tuple[BankAccount, Decimal, Decimal]]:
        """
        Пересчитывает балансы всех счетов на основе операций и возвращает список
        кортежей (счет, текущий_баланс, правильный_баланс) для счетов с несоответствиями
        """
        if not self.account_repository:
            raise ValueError("Account repository is not set")

        accounts = self.account_repository.get_all()
        operations = self.operation_repository.get_all()
        discrepancies = []

        # Группируем операции по счетам
        account_operations = {}
        for op in operations:
            if op.bank_account_id not in account_operations:
                account_operations[op.bank_account_id] = []
            account_operations[op.bank_account_id].append(op)

        # Проверяем каждый счет
        for account in accounts:
            calculated_balance = Decimal("0.0")

            # Учитываем все операции для этого счета
            ops = account_operations.get(account.id, [])
            for op in ops:
                if op.type == TransactionType.INCOME:
                    calculated_balance += op.amount
                else:
                    calculated_balance -= op.amount

            # Если есть расхождение, добавляем в список
            if account.balance != calculated_balance:
                discrepancies.append((account, account.balance, calculated_balance))

        return discrepancies

    def fix_account_balances(self) -> List[Tuple[BankAccount, Decimal, Decimal]]:
        """
        Исправляет балансы счетов на основе операций и возвращает список
        исправленных счетов с их старыми и новыми значениями
        """
        discrepancies = self.recalculate_account_balances()
        fixed_accounts = []

        for account, old_balance, new_balance in discrepancies:
            # Сохраняем старое значение для отчета
            fixed_accounts.append((account, old_balance, new_balance))

            # Исправляем баланс
            account.balance = new_balance
            self.account_repository.update(account)

        return fixed_accounts
