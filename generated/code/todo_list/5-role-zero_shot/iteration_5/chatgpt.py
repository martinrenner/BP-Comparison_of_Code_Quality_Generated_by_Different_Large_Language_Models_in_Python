#!/usr/bin/env python3
"""
Console-based To-Do List Application

This application implements a TaskManager class that provides functions
to add, remove, search, finish, retrieve, and clear tasks. Each task is stored
as a dictionary with the following keys:
    - id (int)
    - task_name (str)
    - task_description (str)
    - is_finished (bool)

The design follows OOP principles and adheres to software quality standards
for clarity, efficiency, and maintainability.
"""

from typing import List, Dict


class TaskManager:
    """
    Manages a collection of tasks.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty in-memory tasks storage.
        """
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task manager.

        Args:
            task_name: The name of the task.
            task_description: A detailed description of the task.

        Returns:
            The unique ID of the added task.

        Raises:
            ValueError: If the task_name or task_description is an empty string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id: The unique task ID to be removed.

        Returns:
            True if the task was successfully removed, False otherwise.

        Raises:
            ValueError: If the task_id is not a positive integer.
            KeyError: If the task with the given ID does not exist.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist.")

        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks by a term contained in the task name or description.

        Args:
            task_term: The term to search for in tasks.

        Returns:
            A list of tasks matching the search term. Each task is represented as a dictionary.

        Raises:
            ValueError: If task_term is not a string.
        """
        if not isinstance(task_term, str):
            raise ValueError("Search term must be a string.")

        # Return empty list if search term is empty or whitespace.
        term = task_term.strip().lower()
        if not term:
            return []

        matched_tasks = []
        for task in self._tasks.values():
            if term in task["task_name"].lower() or term in task["task_description"].lower():
                # Return a copy to maintain encapsulation
                matched_tasks.append(task.copy())
        return matched_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The unique task ID to be marked as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If the task with the given ID does not exist.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist.")

        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks, each represented as a dictionary.
        """
        # Return copies to ensure external code cannot modify internal state.
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the manager.

        Returns:
            True after clearing all tasks.
        """
        self._tasks.clear()
        return True


def display_task(task: Dict) -> None:
    """
    Displays a single task in a formatted way.

    Args:
        task: The task dictionary to display.
    """
    status = "Finished" if task["is_finished"] else "Pending"
    print(f"ID: {task['id']} | Name: {task['task_name']} | Description: {task['task_description']} | Status: {status}")


def main() -> None:
    """
    Console interface for the To-Do List application.
    """
    manager = TaskManager()
    menu = (
        "\nAvailable commands:\n"
        "1. add - Add a new task\n"
        "2. remove - Remove a task by ID\n"
        "3. finish - Mark a task as finished by ID\n"
        "4. search - Search tasks by term\n"
        "5. get_all - List all tasks\n"
        "6. clear_all - Remove all tasks\n"
        "7. exit - Exit the application\n"
    )

    print("Welcome to the To-Do List Application!")
    while True:
        print(menu)
        command = input("Enter a command: ").strip().lower()

        try:
            if command == "add" or command == "1":
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")

            elif command == "remove" or command == "2":
                task_id_input = input("Enter task ID to remove: ").strip()
                if not task_id_input.isdigit():
                    print("Invalid input. Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_input)
                manager.remove(task_id)
                print(f"Task with ID {task_id} removed successfully.")

            elif command == "finish" or command == "3":
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                if not task_id_input.isdigit():
                    print("Invalid input. Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_input)
                manager.finish(task_id)
                print(f"Task with ID {task_id} marked as finished.")

            elif command == "search" or command == "4":
                term = input("Enter search term: ")
                results = manager.search(term)
                if not results:
                    print("No matching tasks found.")
                else:
                    print("\nMatching tasks:")
                    for task in results:
                        display_task(task)

            elif command == "get_all" or command == "5":
                tasks = manager.get_all()
                if not tasks:
                    print("No tasks available.")
                else:
                    print("\nAll tasks:")
                    for task in tasks:
                        display_task(task)

            elif command == "clear_all" or command == "6":
                confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirmation == "yes":
                    manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear all operation canceled.")

            elif command == "exit" or command == "7":
                print("Exiting the application. Goodbye!")
                break

            else:
                print("Invalid command. Please try again.")

        except (ValueError, KeyError) as error:
            print(f"Error: {error}")


if __name__ == '__main__':
    main()
