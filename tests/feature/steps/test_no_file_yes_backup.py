import pytest
from pytest_bdd import scenario, given, when, then
from src.tasks import default_to_backup, save_tasks, load_tasks
import os
import json


@scenario('../task_management.feature', 'Using backup when main task file is missing')
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


@pytest.fixture
def backup_tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "completed": True},
        {"id": 4, "title": "Task 4", "priority": "Medium", "completed": True},
        {"id": 2, "title": "Task 2", "priority": "Low", "completed": False},
        {"id": 3, "title": "Task 3", "priority": "Low", "completed": True},
        {"id": 5, "title": "Task 5", "priority": "Low", "completed": False}, # not in sample_tasks
    ]

@given("a backup file with tasks exists", target_fixture="backup")
def given_backup_file(tmp_path, backup_tasks):
    backup_path = str(tmp_path / "backup.json")
    save_tasks(backup_tasks, backup_path)
    return str(tmp_path / "backup.json")

@given("the main task file is missing", target_fixture="tasks")
def given_no_task(tmp_path):
    task_path = str(tmp_path / "tasks.json")
    return str(tmp_path / "tasks.json")

@when("the app loads tasks", target_fixture="loaded")
def when_load_tasks(tasks, backup):
    return load_tasks(tasks, backup)

@then("it should return the tasks from the backup")
def then_empty_list_and_files_created(loaded, backup_tasks):
    assert loaded == backup_tasks
