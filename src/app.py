import streamlit as st
import pandas as pd
from datetime import datetime
from tasks import *
import sys
import os
import subprocess

DEFAULT_BACKUP_FILE = "backup.json"

def render_task(task, tasks):
    col1, col2 = st.columns([4, 1])
    with col1:
        if task["completed"]:
            st.markdown(f"~~**{task['title']}**~~")
        else:
            st.markdown(f"**{task['title']}**")
        st.write(task["description"])
        st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
    with col2:
        if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
            for t in tasks:
                if t["id"] == task["id"]:
                    t["completed"] = not t["completed"]
                    save_tasks(tasks)
                    st.rerun()
        if st.button("Delete", key=f"delete_{task['id']}"):
            tasks = [t for t in tasks if t["id"] != task["id"]]
            save_tasks(tasks)
            st.rerun()

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, "..", "tests", "results")
    os.makedirs(results_dir, exist_ok=True)

    #Run test button
    st.sidebar.markdown("Run Unit Tests")

    if st.sidebar.button("Test: pytest-cov"):
        test_file_path = os.path.join(base_dir, "..", "tests", "test_basic.py")
        output_file = os.path.join(results_dir, "test_output.txt")
        os.system(f"PYTHONPATH=.. pytest {test_file_path} --cov=src.tasks --cov-report=term > {output_file}")
        with open(output_file) as f:
            st.sidebar.text(f.read())

    if st.sidebar.button("Test: HTML Report"):
        output_file = os.path.join(results_dir, "html")
        test_file_path = os.path.join(base_dir, "..", "tests", "test_basic.py")
        os.system(f"PYTHONPATH=.. pytest {test_file_path} --cov=src.tasks --cov-report=html:{output_file}")
        st.success("Tests completed! Check the HTML report in '/tests/results/html/index.html'.")

    if st.sidebar.button("Test: Parametrize"):
        test_file_path = os.path.join(base_dir, "..", "tests", "test_advanced.py")
        os.system(f"PYTHONPATH=.. pytest {test_file_path} -k 'parametrize' --maxfail=1 --disable-warnings -q")
        st.success("Tests completed with parameterized inputs!")

    if st.sidebar.button("Test: Mocking"):
        test_file_path = os.path.join(base_dir, "..", "tests", "test_advanced.py")
        os.system(f"PYTHONPATH=.. pytest {test_file_path} -k 'mock' --maxfail=1 --disable-warnings -q")
        st.success("Mocking tests completed!")

    if st.sidebar.button("Test: TDD"):
        test_file_path = os.path.join(base_dir, "..", "tests", "test_tdd.py")
        os.system(f"PYTHONPATH=.. pytest {test_file_path} --maxfail=1 --disable-warnings -q")
        st.success("TDD tests completed!")
        


    if st.sidebar.button("Test: BDD"):
        directory = os.path.join(base_dir, "..", "tests", "feature", "steps")
        for filename in os.listdir(directory):
            if filename.endswith('.py'):
                full_path = os.path.join(directory, filename)
                subprocess.call(f'PYTHONPATH=.. pytest --maxfail=1 --disable-warnings -q {full_path}', shell=True)
        st.success("BDD tests completed!")

    if st.sidebar.button("Run Property-Based Tests"):
        st.write("Running property-based tests with Hypothesis...")
        test_file_path = os.path.join(base_dir, "..", "tests", "test_property.py")
        result = subprocess.run(
            ["pytest", test_file_path, "--maxfail=1", "--disable-warnings", "-q", "--tb=short"],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": ".."}
        )
        st.code(result.stdout)
        if result.returncode == 0:
            st.success("All property-based tests passed!")
        else:
            st.error(result)



    #Save and load backup
    st.sidebar.markdown("Save/Load Backup")
    if st.sidebar.button("Save Backup"):
        st.sidebar.write("Saving...")
        save_tasks(tasks, DEFAULT_BACKUP_FILE)

    if st.sidebar.button("Load Backup"):
        st.sidebar.write("Loading...")
        tasks = load_tasks(DEFAULT_BACKUP_FILE)

    if st.sidebar.button("Overwrite Tasks With Backup"):
        st.sidebar.write("Loading...")
        save_tasks(load_tasks(DEFAULT_BACKUP_FILE))

    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")

    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title:
            new_task = {
                "id": generate_unique_id(tasks),
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with col3:
        if st.button("Sort tasks"):
            tasks = sort_tasks_by_priority(tasks)
            save_tasks(tasks)
    
    show_completed = st.checkbox("Show Completed Tasks")
    show_diffrence = st.checkbox("Show Backup and Current Tasks Diffrence")
    
    # Apply filters
    o, s = None, None
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    if show_diffrence:
        o, s = compare_backup_to_current()
    
    # Display tasks
    if o is not None and s is not None:
        st.header("Tasks only in Current Tasks")
        for task in o:
            render_task(task, tasks)
        st.header("Tasks only in Backup Tasks")
        for task in s:
            render_task(task, tasks)
    else:
        for task in filtered_tasks:
            render_task(task, tasks)

if __name__ == "__main__":

    main()