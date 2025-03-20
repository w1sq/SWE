from abc import ABC, abstractmethod
from typing import List, Dict, Any
from decimal import Decimal
from datetime import datetime
import csv
import json
import yaml
import io
from models import TransactionType


class DataImporter(ABC):
    def import_data(self, data_str: str) -> List[Dict[str, Any]]:
        # Шаблонный метод
        raw_data = self._import(data_str)
        prepared_data = self._prepare_data(raw_data)
        return prepared_data

    def _prepare_data(self, data: List[Dict]) -> List[Dict]:
        # Общая для всех обработка (например, преобразование строк в нужные типы)
        prepared = []
        for item in data:
            prepared_item = {}
            for key, value in item.items():
                if key == "amount" and isinstance(value, str):
                    prepared_item[key] = Decimal(value)
                elif key == "date" and isinstance(value, str):
                    try:
                        prepared_item[key] = datetime.fromisoformat(value)
                    except ValueError:
                        try:
                            prepared_item[key] = datetime.strptime(
                                value, "%Y-%m-%d %H:%M:%S"
                            )
                        except ValueError:
                            prepared_item[key] = datetime.now()  # Fallback
                elif key == "type" and isinstance(value, str):
                    try:
                        prepared_item[key] = TransactionType(value)
                    except ValueError:
                        if value.upper() == "INCOME":
                            prepared_item[key] = TransactionType.INCOME
                        elif value.upper() == "EXPENSE":
                            prepared_item[key] = TransactionType.EXPENSE
                else:
                    prepared_item[key] = value
            prepared.append(prepared_item)
        return prepared

    @abstractmethod
    def _import(self, data_str: str) -> List[Dict]:
        pass


class CSVImporter(DataImporter):
    def _import(self, data_str: str) -> List[Dict]:
        result = []
        f = io.StringIO(data_str)
        reader = csv.reader(f)
        headers = next(reader)

        for row in reader:
            item = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    item[header] = row[i]
            result.append(item)

        return result


class JSONImporter(DataImporter):
    def _import(self, data_str: str) -> List[Dict]:
        return json.loads(data_str)


class YAMLImporter(DataImporter):
    def _import(self, data_str: str) -> List[Dict]:
        return yaml.safe_load(data_str)
