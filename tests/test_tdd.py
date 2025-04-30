import pytest
from src.tasks import compare_backup_to_current, sort_tasks_by_priority, default_to_backup, save_tasks

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
        {"id": 5, "title": "Task 5", "priority": "Low", "completed": False}, # not in sample_tasks
    ]

backup_only = [{"id": 5, "title": "Task 5", "priority": "Low", "completed": False}]
sample_only = [{"id": 5, "title": "Task 5", "priority": "High", "completed": False},
        {"id": 6, "title": "Task 6", "priority": "Medium", "completed": False}]

def test_compare_backup_to_current(sample_tasks, backup_tasks, tmp_path):
    current_path = str(tmp_path / "current.json")
    backup_path = str(tmp_path / "backup.json")

    save_tasks(sample_tasks, current_path)
    save_tasks(backup_tasks, backup_path)

    s, o = compare_backup_to_current(current_path, backup_path)

    assert len(s) == 2
    assert len(o) == 1
    assert s == sample_only
    assert o == backup_only

def test_sort_tasks_by_priority(sample_tasks, sorted_tasks):

    s = sort_tasks_by_priority(sample_tasks)
    assert len(s) == 6
    assert s == sorted_tasks


def test_default_to_backup_with_backup(sample_tasks, backup_tasks, tmp_path):
    current_path = str(tmp_path / "current.json")
    backup_path = str(tmp_path / "backup.json")

    save_tasks(backup_tasks, backup_path)

    o = default_to_backup(current_path, backup_path)
    assert len(o) == 5
    assert o == backup_tasks


def test_default_to_backup_without_backup(sample_tasks, backup_tasks, tmp_path):
    current_path = str(tmp_path / "current.json")
    backup_path = str(tmp_path / "backup.json")

    o = default_to_backup(current_path, backup_path)
    assert o == []