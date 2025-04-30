import pytest

# test/test_basic.py
import json
import pytest
from datetime import datetime, timedelta
import os
from src.tasks import (
    load_tasks, save_tasks, generate_unique_id,
    filter_tasks_by_priority, filter_tasks_by_category,
    search_tasks, get_overdue_tasks, filter_tasks_by_completion
)

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
    sample = [{"id": 1, "title": "Save me", "completed": False}]
    file_path = tmp_path / "tasks.json"

    save_tasks(sample, str(file_path))
    loaded = load_tasks(str(file_path))
    assert loaded == sample

def test_filter_tasks_by_completion(sample_tasks):
    completed = filter_tasks_by_completion(sample_tasks)
    assert len(completed) == 1
    assert all(task["completed"] == True for task in completed)
    not_completed = filter_tasks_by_completion(sample_tasks, False)
    assert len(not_completed) == 2
    assert all(task["completed"] == False for task in not_completed)

def test_load_tasks_invalid_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{not valid json}")

    tasks = load_tasks(str(bad_file))
    assert tasks == []


def test_save_tasks(tmp_path):
    sample = [{"id": 1, "title": "Save me", "completed": False}]
    file_path = tmp_path / "tasks.json"

    save_tasks(sample, str(file_path))

    with open(file_path) as f:
        data = json.load(f)

    assert data == sample

