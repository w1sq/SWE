import pytest
from unittest.mock import MagicMock, patch

from performance import PerformanceTracker, measure_execution_time


class TestPerformanceTracker:
    def setup_method(self):
        self.tracker = PerformanceTracker()

    def test_add_execution_time(self):
        self.tracker.add_execution_time("test_scenario", 1.5)
        assert "test_scenario" in self.tracker.performance_data
        assert self.tracker.performance_data["test_scenario"] == [1.5]

        self.tracker.add_execution_time("test_scenario", 2.0)
        assert self.tracker.performance_data["test_scenario"] == [1.5, 2.0]

    @patch("time.time")
    def test_start_measuring(self, mock_time):
        mock_time.return_value = 100.0

        session_id = self.tracker.start_measuring("test_scenario")

        assert session_id == 0
        assert "test_scenario" in self.tracker.performance_data
        assert self.tracker.performance_data["test_scenario"] == [
            -100.0
        ]

    @patch("time.time")
    def test_stop_measuring(self, mock_time):
        mock_time.side_effect = [100.0, 102.5]

        session_id = self.tracker.start_measuring("test_scenario")
        execution_time = self.tracker.stop_measuring("test_scenario", session_id)

        assert execution_time == 2.5
        assert self.tracker.performance_data["test_scenario"] == [
            2.5
        ]

    def test_stop_measuring_nonexistent_scenario(self):
        with pytest.raises(ValueError):
            self.tracker.stop_measuring("nonexistent", 0)

    def test_stop_measuring_invalid_session(self):
        self.tracker.start_measuring("test_scenario")
        with pytest.raises(ValueError):
            self.tracker.stop_measuring("test_scenario", 999)

    def test_report_empty(self):
        report = self.tracker.report()
        assert report == {}

    def test_report_with_data(self):
        self.tracker.add_execution_time("scenario1", 1.5)
        self.tracker.add_execution_time("scenario1", 2.5)
        self.tracker.add_execution_time("scenario2", 3.0)

        report = self.tracker.report()

        assert len(report) == 2
        assert "scenario1" in report
        assert "scenario2" in report

        assert report["scenario1"]["avg_time"] == 2.0
        assert report["scenario1"]["min_time"] == 1.5
        assert report["scenario1"]["max_time"] == 2.5
        assert report["scenario1"]["executions"] == 2

        assert report["scenario2"]["avg_time"] == 3.0
        assert report["scenario2"]["executions"] == 1


@patch("time.time")
def test_measure_execution_time_decorator(mock_time):
    mock_time.side_effect = [100.0, 101.5]

    mock_container = MagicMock()
    mock_container.performance_tracker = MagicMock()

    class TestClass:
        def __init__(self):
            self.container = mock_container

        @measure_execution_time("test_scenario")
        def test_method(self):
            return "test result"

    test_instance = TestClass()
    result = test_instance.test_method()

    assert result == "test result"
    mock_container.performance_tracker.add_execution_time.assert_called_once_with(
        "test_scenario", 1.5
    )
