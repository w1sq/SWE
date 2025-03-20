import json
import yaml
from decimal import Decimal
from typing import List, Dict
from datetime import datetime
from abc import ABC, abstractmethod

from models import TransactionType


class DataExporter(ABC):
    def export_data(self, data: List[Dict]) -> str:
        # Шаблонный метод
        prepared_data = self._prepare_data(data)
        exported = self._export(prepared_data)
        return exported

    def _prepare_data(self, data: List[Dict]) -> List[Dict]:
        # Общая для всех обработка (например, преобразование Decimal в строки)
        prepared = []
        for item in data:
            prepared_item = {}
            for key, value in item.items():
                if isinstance(value, Decimal):
                    prepared_item[key] = str(value)
                elif isinstance(value, datetime):
                    prepared_item[key] = value.isoformat()
                elif isinstance(value, TransactionType):
                    prepared_item[key] = value.value
                else:
                    prepared_item[key] = value
            prepared.append(prepared_item)
        return prepared

    @abstractmethod
    def _export(self, data: List[Dict]) -> str:
        pass


class CSVExporter(DataExporter):
    def _export(self, data: List[Dict]) -> str:
        if not data:
            return ""

        output = []
        headers = data[0].keys()
        output.append(",".join(headers))

        for item in data:
            row = []
            for header in headers:
                row.append(str(item.get(header, "")))
            output.append(",".join(row))

        return "\n".join(output)


class JSONExporter(DataExporter):
    def _export(self, data: List[Dict]) -> str:
        return json.dumps(data, indent=2)


class YAMLExporter(DataExporter):
    def _export(self, data: List[Dict]) -> str:
        return yaml.dump(data)
