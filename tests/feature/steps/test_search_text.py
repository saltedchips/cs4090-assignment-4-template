import pytest
from pytest_bdd import scenario, given, when, then
from src.tasks import search_tasks


@scenario('../search_management.feature', 'Search tasks by a text query in title and description')
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
        {"id": 5, "title": "Task 1-1", "priority": "High", "completed": False},
        {"id": 4, "title": "Task 1-2", "priority": "Medium", "completed": True},
        {"id": 6, "title": "Task 1-3", "priority": "Medium", "completed": False},
    ]

@given("a list of tasks", target_fixture="tasks")
def given_backup_file(sample_tasks):
    return sample_tasks

@given("a text query", target_fixture="query")
def given_no_task(query="Task 1"):
    return query

@when("the user searches the tasks with the query", target_fixture="out")
def when_load_tasks(tasks, query):
    return search_tasks(tasks, query)

@then("the tasks should return a list of satisfied searches")
def then_empty_list_and_files_created(out, out_tasks):
    assert out == out_tasks
