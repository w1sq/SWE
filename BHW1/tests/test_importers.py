from decimal import Decimal
import json
import yaml

import pytest
from unittest.mock import patch, MagicMock
from models import TransactionType
from importers import CSVImporter, JSONImporter, YAMLImporter


class TestImporters:
    def test_csv_importer(self):
        importer = CSVImporter()
        csv_data = """id,type,account_name,account_id,amount,category_name,category_id,date,description
1,INCOME,Main Account,1,1000.0,Salary,1,2023-01-01T12:00:00,January salary"""

        result = importer.import_data(csv_data)

        assert len(result) == 1
        assert result[0]["id"] == "1"
        assert result[0]["type"] == TransactionType.INCOME
        assert result[0]["account_name"] == "Main Account"
        assert result[0]["account_id"] == "1"
        assert result[0]["amount"] == Decimal("1000.0")
        assert "date" in result[0]

    def test_json_importer(self):
        importer = JSONImporter()
        json_data = """{"operations": [
            {
                "id": "1",
                "type": "INCOME",
                "account_name": "Main Account",
                "account_id": "1",
                "amount": "1000.0",
                "category_name": "Salary",
                "category_id": "1", 
                "date": "2023-01-01T12:00:00",
                "description": "January salary"
            }
        ]}"""
        
        original_prepare_data = importer._prepare_data
        importer._prepare_data = lambda data: [
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

        result = importer.import_data(json_data)

        importer._prepare_data = original_prepare_data

        assert len(result) == 1
        assert result[0]["id"] == "1"
        assert result[0]["type"] == TransactionType.INCOME
        assert result[0]["account_name"] == "Main Account"
        assert result[0]["account_id"] == "1"
        assert result[0]["amount"] == Decimal("1000.0")

    def test_yaml_importer(self):
        importer = YAMLImporter()
        yaml_data = """operations:
  - id: "1"
    type: INCOME
    account_name: Main Account
    account_id: "1"
    amount: "1000.0"
    category_name: Salary
    category_id: "1"
    date: "2023-01-01T12:00:00"
    description: January salary
"""
        original_prepare_data = importer._prepare_data
        importer._prepare_data = lambda data: [
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

        result = importer.import_data(yaml_data)

        importer._prepare_data = original_prepare_data

        assert len(result) == 1
        assert result[0]["id"] == "1"
        assert result[0]["type"] == TransactionType.INCOME
        assert result[0]["amount"] == Decimal("1000.0")

    def test_csv_importer_empty_data(self):
        importer = CSVImporter()
        csv_data = "id,type,account_name,account_id,amount,category_name,category_id,date,description"

        result = importer.import_data(csv_data)
        assert len(result) == 0

    def test_json_importer_invalid_format(self):
        importer = JSONImporter()
        original_prepare = importer._prepare_data
        importer._prepare_data = MagicMock(side_effect=ValueError("Invalid format"))

        with pytest.raises(ValueError):
            importer.import_data('{"something_else": []}')

        importer._prepare_data = original_prepare

    def test_yaml_importer_invalid_format(self):
        importer = YAMLImporter()
        original_prepare = importer._prepare_data
        importer._prepare_data = MagicMock(side_effect=ValueError("Invalid format"))

        with pytest.raises(ValueError):
            importer.import_data("something_else: []")

        importer._prepare_data = original_prepare
