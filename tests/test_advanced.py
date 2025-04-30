import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.tasks import filter_tasks_by_priority
import json

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "completed": False},
        {"id": 2, "title": "Task 2", "priority": "High", "completed": True},
        {"id": 3, "title": "Task 3", "priority": "Medium", "completed": False},
        {"id": 4, "title": "Task 4", "priority": "Low", "completed": True},
    ]

@pytest.mark.parametrize("priority,expected_count", [
    ("High", 2),  # Expected count for high-priority tasks
    ("Medium", 1),
    ("Low", 1),
])

def test_filter_tasks_by_priority_with_data(priority, expected_count, sample_tasks):
    result = filter_tasks_by_priority(sample_tasks, priority)
    assert len(result) == expected_count

def test_mock_load_tasks(mocker, sample_tasks):
    # Convert Python list of dicts to valid JSON string
    json_data = json.dumps(sample_tasks)

    # Create a mock open function with valid JSON
    mock_open = mocker.mock_open(read_data=json_data)

    # Patch the built-in open function with our mock
    mocker.patch("builtins.open", mock_open)

    # Import AFTER mocking to ensure mock is active
    from src.tasks import load_tasks

    tasks = load_tasks("dummy.json")
    assert isinstance(tasks, list)
    assert tasks[0]["id"] == 1
    assert tasks[0]["title"] == "Task 1"