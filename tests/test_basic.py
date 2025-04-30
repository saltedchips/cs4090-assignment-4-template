import pytest

# test/test_basic.py
import os
import json
import pytest
from datetime import datetime, timedelta
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.tasks import *

@pytest.fixture
def sample_tasks():
    past = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    future = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    return [
        {"id": 1, "title": "Task A", "priority": "High", "category": "Work", "completed": False, "due_date": past},
        {"id": 2, "title": "Task B", "priority": "Low", "category": "Personal", "completed": True, "due_date": past},
        {"id": 3, "title": "Urgent Bug Fix", "priority": "High", "category": "Work", "completed": False, "due_date": future},
    ]

def test_generate_unique_id(sample_tasks):
    assert generate_unique_id(sample_tasks) == 4
    assert generate_unique_id([]) == 1

def test_filter_tasks_by_priority(sample_tasks):
    result = filter_tasks_by_priority(sample_tasks, "High")
    assert len(result) == 2
    assert all(task["priority"] == "High" for task in result)

def test_filter_tasks_by_category(sample_tasks):
    result = filter_tasks_by_category(sample_tasks, "Work")
    assert len(result) == 2
    assert all(task["category"] == "Work" for task in result)

def test_search_tasks(sample_tasks):
    result = search_tasks(sample_tasks, "bug")
    assert len(result) == 1
    assert "Bug" in result[0]["title"]

    result = search_tasks(sample_tasks, "Task")
    assert len(result) == 2
    assert all("Task" in task["title"] for task in result)

def test_get_overdue_tasks(sample_tasks):
    overdue = get_overdue_tasks(sample_tasks)
    assert len(overdue) == 1
    assert overdue[0]["id"] == 1

def test_save_and_load_tasks(sample_tasks, tmp_path):
    file_path = tmp_path / "tasks.json"
    save_tasks(sample_tasks, str(file_path))
    loaded = load_tasks(str(file_path))
    assert loaded == sample_tasks

def test_filter_tasks_by_completion(sample_tasks):
    completed = filter_tasks_by_completion(sample_tasks)
    assert len(completed) == 1
    assert all(task["completed"] == True for task in completed)
    not_completed = filter_tasks_by_completion(sample_tasks, False)
    assert len(not_completed) == 2
    assert all(task["completed"] == False for task in not_completed)

def test_load_tasks_invalid_json_with_backup(sample_tasks, tmp_path):
    bad_file = tmp_path / "bad.json"
    backup_path = tmp_path / "backup.json"
    bad_file.write_text("{not valid json}")
    save_tasks(sample_tasks, str(backup_path))

    tasks = load_tasks(str(bad_file), str(backup_path))
    assert tasks == sample_tasks


def test_load_tasks_invalid_json_without_backup(tmp_path):
    bad_file = tmp_path / "bad.json"
    backup_path = tmp_path / "backup.json"
    bad_file.write_text("{not valid json}")

    tasks = load_tasks(str(bad_file), str(backup_path))
    assert tasks == []

def test_load_tasks_no_tasks_with_backup(sample_tasks, tmp_path):
    bad_file = tmp_path / "bad.json"
    backup_path = tmp_path / "backup.json"
    save_tasks(sample_tasks, str(backup_path))

    tasks = load_tasks(str(bad_file), str(backup_path))
    assert tasks == sample_tasks

def test_load_tasks_no_tasks_without_backup(tmp_path):
    bad_file = tmp_path / "bad.json"
    backup_path = tmp_path / "backup.json"

    tasks = load_tasks(str(bad_file), str(backup_path))
    assert tasks == []


def test_save_tasks(tmp_path):
    sample = [{"id": 1, "title": "Save me", "completed": False}]
    file_path = tmp_path / "tasks.json"

    save_tasks(sample, str(file_path))

    with open(file_path) as f:
        data = json.load(f)

    assert data == sample


# The following are tdd tests implemented for coverage

from src.tasks import compare_backup_to_current, sort_tasks_by_priority, default_to_backup, save_tasks

@pytest.fixture
def sample_tasks_2():
    return [
        {"id": 5, "title": "Task 5", "priority": "High", "completed": False}, # Not in backup
        {"id": 4, "title": "Task 4", "priority": "Medium", "completed": True},
        {"id": 6, "title": "Task 6", "priority": "Medium", "completed": False}, #Not in backup
        {"id": 2, "title": "Task 2", "priority": "Low", "completed": False},
        {"id": 1, "title": "Task 1", "priority": "High", "completed": True},
        {"id": 3, "title": "Task 3", "priority": "Low", "completed": True},
    ]

@pytest.fixture
def sorted_tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "completed": True},
        {"id": 5, "title": "Task 5", "priority": "High", "completed": False},
        {"id": 4, "title": "Task 4", "priority": "Medium", "completed": True},
        {"id": 6, "title": "Task 6", "priority": "Medium", "completed": False},
        {"id": 2, "title": "Task 2", "priority": "Low", "completed": False},
        {"id": 3, "title": "Task 3", "priority": "Low", "completed": True},
    ]

@pytest.fixture
def backup_tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "completed": True},
        {"id": 4, "title": "Task 4", "priority": "Medium", "completed": True},
        {"id": 2, "title": "Task 2", "priority": "Low", "completed": False},
        {"id": 3, "title": "Task 3", "priority": "Low", "completed": True},
        {"id": 5, "title": "Task 5", "priority": "Low", "completed": False}, # not in sample_tasks_2
    ]

backup_only = [{"id": 5, "title": "Task 5", "priority": "Low", "completed": False}]
sample_only = [{"id": 5, "title": "Task 5", "priority": "High", "completed": False},
        {"id": 6, "title": "Task 6", "priority": "Medium", "completed": False}]

def test_compare_backup_to_current(sample_tasks_2, backup_tasks, tmp_path):
    current_path = str(tmp_path / "current.json")
    backup_path = str(tmp_path / "backup.json")

    save_tasks(sample_tasks_2, current_path)
    save_tasks(backup_tasks, backup_path)

    s, o = compare_backup_to_current(current_path, backup_path)

    assert len(s) == 2
    assert len(o) == 1
    assert s == sample_only
    assert o == backup_only

def test_sort_tasks_by_priority(sample_tasks_2, sorted_tasks):

    s = sort_tasks_by_priority(sample_tasks_2)
    assert len(s) == 6
    assert s == sorted_tasks


def test_default_to_backup_with_backup(sample_tasks_2, backup_tasks, tmp_path):
    current_path = str(tmp_path / "current.json")
    backup_path = str(tmp_path / "backup.json")

    save_tasks(backup_tasks, backup_path)

    o = default_to_backup(current_path, backup_path)
    assert len(o) == 5
    assert o == backup_tasks


def test_default_to_backup_without_backup(sample_tasks_2, backup_tasks, tmp_path):
    current_path = str(tmp_path / "current.json")
    backup_path = str(tmp_path / "backup.json")

    o = default_to_backup(current_path, backup_path)
    assert o == []