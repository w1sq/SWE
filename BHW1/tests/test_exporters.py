import json
from decimal import Decimal
from datetime import datetime

from models import TransactionType
from exporters import CSVExporter, JSONExporter


class TestCSVExporter:
    def test_export_data(self):
        exporter = CSVExporter()
        data = [
            {
                "id": 1,
                "type": TransactionType.INCOME,
                "amount": Decimal("1000.0"),
                "date": datetime(2023, 1, 1, 12, 0, 0),
            }
        ]

        result = exporter.export_data(data)

        assert "id,type,amount,date" in result
        assert "1,INCOME,1000.0,2023-01-01T12:00:00" in result


class TestJSONExporter:
    def test_export_data(self):
        exporter = JSONExporter()
        data = [
            {
                "id": 1,
                "type": TransactionType.INCOME,
                "amount": Decimal("1000.0"),
                "date": datetime(2023, 1, 1, 12, 0, 0),
            }
        ]

        result = exporter.export_data(data)
        parsed = json.loads(result)

        assert len(parsed) == 1
        assert parsed[0]["id"] == 1
        assert parsed[0]["type"] == "INCOME"
        assert parsed[0]["amount"] == "1000.0"
        assert parsed[0]["date"] == "2023-01-01T12:00:00"