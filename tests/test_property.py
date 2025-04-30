# test/test_property.py

from hypothesis import given, strategies as st
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.tasks import (
    filter_tasks_by_priority, filter_tasks_by_completion, sort_tasks_by_priority,
    search_tasks, get_overdue_tasks, generate_unique_id
)
from datetime import datetime, timedelta

# 1. Test: Filtering by priority retains only matching priorities
@given(
    st.lists(
        st.fixed_dictionaries({
            "id": st.integers(min_value=1),
            "title": st.text(min_size=1),
            "priority": st.sampled_from(["High", "Medium", "Low"]),
            "completed": st.booleans()
        }),
        min_size=1
    ),
    st.sampled_from(["High", "Medium", "Low"])
)
def test_filter_tasks_by_priority(tasks, target_priority):
    filtered = filter_tasks_by_priority(tasks, target_priority)
    assert all(task["priority"] == target_priority for task in filtered)


# 2. Test: Sorting by priority puts High < Medium < Low
@given(
    st.lists(
        st.fixed_dictionaries({
            "id": st.integers(min_value=1, max_value=1000),
            "priority": st.sampled_from(["High", "Medium", "Low"])
        }),
        min_size=2
    )
)
def test_sort_tasks_by_priority_order(tasks):
    sorted_tasks = sort_tasks_by_priority(tasks)
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    priorities = [priority_order[task["priority"]] for task in sorted_tasks]
    assert priorities == sorted(priorities)


# 3. Test: Completed filter returns only matching tasks
@given(
    st.lists(
        st.fixed_dictionaries({
            "id": st.integers(min_value=1),
            "completed": st.booleans()
        }),
        min_size=1
    )
)
def test_filter_tasks_by_completion(tasks):
    true_tasks = filter_tasks_by_completion(tasks, True)
    false_tasks = filter_tasks_by_completion(tasks, False)
    assert all(task["completed"] is True for task in true_tasks)
    assert all(task["completed"] is False for task in false_tasks)


# 4. Test: Search matches either title or description
@given(
    st.text(min_size=1),
    st.lists(
        st.fixed_dictionaries({
            "title": st.text(),
            "description": st.text()
        }),
        min_size=1
    )
)
def test_search_tasks_finds_query(query, tasks):
    results = search_tasks(tasks, query)
    query_lower = query.lower()
    for task in results:
        assert query_lower in task.get("title", "").lower() or query_lower in task.get("description", "").lower()


# 5. Test: Overdue tasks only include those past today's date
@given(
    st.lists(
        st.fixed_dictionaries({
            "completed": st.just(False),
            "due_date": st.dates(min_value=datetime(2000, 1, 1).date(), max_value=datetime.now().date())
                           .map(lambda d: d.strftime("%Y-%m-%d"))
        }),
        min_size=1
    )
)
def test_get_overdue_tasks(tasks):
    overdue = get_overdue_tasks(tasks)
    today = datetime.now().strftime("%Y-%m-%d")
    assert all(task["due_date"] < today and not task["completed"] for task in overdue)