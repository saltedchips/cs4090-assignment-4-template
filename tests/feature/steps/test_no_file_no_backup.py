import pytest
from pytest_bdd import scenario, given, when, then
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.tasks import default_to_backup
import os
import json


@scenario('../task_management.feature', 'Loading tasks with no file available')
def test_bdd():
    pass

@pytest.fixture
def sample_tasks():
    return [
        {"id": 5, "title": "Task 5", "priority": "High", "completed": False}, # Not in backup
        {"id": 4, "title": "Task 4", "priority": "Medium", "completed": True},
        {"id": 6, "title": "Task 6", "priority": "Medium", "completed": False}, #Not in backup
        {"id": 2, "title": "Task 2", "priority": "Low", "completed": False},
        {"id": 1, "title": "Task 1", "priority": "High", "completed": True},
        {"id": 3, "title": "Task 3", "priority": "Low", "completed": True},
    ]

@given("no existing tasks or backup file", target_fixture="path")
def given_no_files(tmp_path):
    return str(tmp_path / "tasks.json"), str(tmp_path / "backup.json")

@when("the app tries to load tasks", target_fixture="loading")
def when_loading_without_files(path):
    file_path, backup_path = path
    return default_to_backup(file_path, backup_path)

@then("it should return an empty list and create new files")
def then_empty_list_and_files_created(path, loading):
    file_path, backup_path = path
    assert loading == []
    assert os.path.exists(file_path)
    assert os.path.exists(backup_path)
