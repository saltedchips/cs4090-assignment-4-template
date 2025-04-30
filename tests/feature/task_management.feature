Feature: Task Management

  Scenario: Sorting tasks by priority and ID
    Given a list of unsorted tasks
    When the user sorts the tasks by priority
    Then the tasks should be sorted with High priority first and lower IDs first

  Scenario: Loading tasks with no file available
    Given no existing tasks or backup file
    When the app tries to load tasks
    Then it should return an empty list and create new files

  Scenario: Using backup when main task file is missing
    Given a backup file with tasks exists
    And the main task file is missing
    When the app loads tasks
    Then it should return the tasks from the backup
