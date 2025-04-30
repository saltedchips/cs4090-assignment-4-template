import pytest
from pytest_bdd import scenario, given, when, then
from src.tasks import sort_tasks_by_priority


@scenario('../task_management.feature', 'Sorting tasks by priority and ID')
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

@given("a list of unsorted tasks", target_fixture="unsorted_tasks")
def given_unsorted_tasks(sample_tasks):
    return sample_tasks

@when("the user sorts the tasks by priority", target_fixture="sorted_result")
def when_user_sorts(unsorted_tasks):
    return sort_tasks_by_priority(unsorted_tasks)

@then("the tasks should be sorted with High priority first and lower IDs first")
def then_tasks_sorted(sorted_result, sorted_tasks):
    assert sorted_result == sorted_tasks

