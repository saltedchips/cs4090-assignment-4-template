Feature: Search Management

  Scenario: Search tasks by a text query in title and description
    Given a list of tasks
    And a text query
    When the user searches the tasks with the query
    Then the tasks should return a list of satisfied searches

  Scenario: Filter tasks by completion status
    Given a list of tasks
    And a completion state
    When the user filters the tasks
    Then it should return an list of tasks with the specified completion status
