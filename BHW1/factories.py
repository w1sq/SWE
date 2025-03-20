from typing import Optional
from decimal import Decimal
from datetime import datetime

from models import BankAccount, Category, Operation, TransactionType


class EntityFactory:
    def create_bank_account(
        self, name: str, balance: Decimal = Decimal("0.0")
    ) -> BankAccount:
        return BankAccount(0, name, balance)

    def create_category(self, name: str, type: TransactionType) -> Category:
        return Category(0, name, type)

    def create_operation(
        self,
        type: TransactionType,
        bank_account_id: int,
        amount: Decimal,
        date: datetime,
        category_id: Optional[int] = None,
        description: str = "",
    ) -> Operation:
        return Operation(
            0, type, bank_account_id, amount, date, category_id, description
        )
