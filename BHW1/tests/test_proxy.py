from decimal import Decimal
from datetime import datetime

from proxy import OperationRepositoryProxy
from repositories import InMemoryOperationRepository
from models import Operation, TransactionType


class TestOperationRepositoryProxy:
    def setup_method(self):
        self.real_repository = InMemoryOperationRepository()
        self.proxy = OperationRepositoryProxy(self.real_repository)

        self.operation1 = Operation(
            0, TransactionType.INCOME, 1, Decimal("100.0"), datetime.now()
        )
        self.operation2 = Operation(
            0, TransactionType.EXPENSE, 1, Decimal("50.0"), datetime.now()
        )

        self.added_op1 = self.real_repository.add(self.operation1)
        self.added_op2 = self.real_repository.add(self.operation2)

    def test_get_all_caching(self):
        result1 = self.proxy.get_all()
        assert len(result1) == 2
        assert self.added_op1 in result1
        assert self.added_op2 in result1

        self.real_repository.delete(self.added_op2.id)

        result2 = self.proxy.get_all()
        assert len(result2) == 2

        self.proxy.is_cache_valid = False

        result3 = self.proxy.get_all()
        assert len(result3) == 1

    def test_get_by_id_caching(self):
        op1 = self.proxy.get_by_id(self.added_op1.id)
        assert op1.id == self.added_op1.id

        modified_op = Operation(
            self.added_op1.id,
            TransactionType.INCOME,
            1,
            Decimal("200.0"),
            datetime.now(),
        )
        self.real_repository.update(modified_op)

        op1_cached = self.proxy.get_by_id(self.added_op1.id)
        assert op1_cached.amount == Decimal("100.0")

    def test_add_invalidates_cache(self):
        self.proxy.get_all()
        assert self.proxy.is_cache_valid

        new_op = Operation(
            0, TransactionType.INCOME, 2, Decimal("300.0"), datetime.now()
        )
        self.proxy.add(new_op)

        assert not self.proxy.is_cache_valid

        all_ops = self.proxy.get_all()
        assert len(all_ops) == 3

    def test_update_invalidates_specific_cache(self):
        op1 = self.proxy.get_by_id(self.added_op1.id)

        op1.amount = Decimal("150.0")
        self.proxy.update(op1)

        assert f"id_{op1.id}" not in self.proxy.cache

        assert not self.proxy.is_cache_valid

    def test_delete_invalidates_specific_cache(self):
        self.proxy.get_by_id(self.added_op1.id)

        self.proxy.delete(self.added_op1.id)

        assert f"id_{self.added_op1.id}" not in self.proxy.cache

        assert not self.proxy.is_cache_valid
