import pytest
from pytest_bdd import scenario, given, when, then
from src.tasks import filter_tasks_by_completion


@scenario('../search_management.feature', 'Filter tasks by completion status')
def test_bdd():
    pass

@pytest.fixture
def sample_tasks():
    return [
        {"id": 5, "title": "Task 1-1", "priority": "High", "completed": False},
        {"id": 4, "title": "Task 1-2", "priority": "Medium", "completed": True},
        {"id": 6, "title": "Task 1-3", "priority": "Medium", "completed": False},
        {"id": 2, "title": "Task 2-1", "priority": "Low", "completed": False},
        {"id": 1, "title": "Task 3-1", "priority": "High", "completed": True},
        {"id": 3, "title": "Task 3-2", "priority": "Low", "completed": True},
    ]

@pytest.fixture
def out_tasks():
    return [
        {"id": 4, "title": "Task 1-2", "priority": "Medium", "completed": True},
        {"id": 1, "title": "Task 3-1", "priority": "High", "completed": True},
        {"id": 3, "title": "Task 3-2", "priority": "Low", "completed": True},
    ]

@given("a list of tasks", target_fixture="tasks")
def given_backup_file(sample_tasks):
    return sample_tasks

@given("a completion state", target_fixture="state")
def given_no_task(state=True):
    return state

@when("the user filters the tasks", target_fixture="out")
def when_load_tasks(tasks, state):
    return filter_tasks_by_completion(tasks, state)

@then("it should return an list of tasks with the specified completion status")
def then_empty_list_and_files_created(out, out_tasks):
    assert out == out_tasks
