#!/usr/bin/env python3
"""
Console-based To-Do List Application

This module implements a TaskManager class that allows users to manage tasks
in a to-do list. The TaskManager provides methods to add, remove, search, finish,
retrieve, and clear tasks. Each task is represented as a dictionary containing:
    - id: Unique task identifier
    - task_name: Name of the task
    - task_description: Description of the task
    - is_finished: Boolean flag indicating if the task is completed

The application runs in the console and provides a menu-driven interface.
"""

from typing import List, Dict


class TaskManager:
    """
    A class to manage tasks in a to-do list.

    Attributes:
        _tasks (Dict[int, dict]): In-memory storage for tasks.
        _counter (int): A counter to generate unique task IDs.
    """

    def __init__(self) -> None:
        """
        Initializes a new TaskManager instance with an empty task store.
        """
        self._tasks: Dict[int, dict] = {}
        self._counter: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name of the task. Must not be an empty string.
            task_description (str): The task description. Must not be an empty string.

        Returns:
            int: The unique ID of the newly added task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self._counter
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False,
        }
        self._counter += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id (int): The ID of the task to remove. Must be non-negative.

        Returns:
            bool: True if the task was successfully removed; False if not found.

        Raises:
            ValueError: If task_id is negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[dict]:
        """
        Searches for tasks that contain the given search term in their name or description.

        Args:
            task_term (str): The term to search for. Must not be an empty string.

        Returns:
            List[dict]: A list of tasks matching the search criteria.

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not task_term.strip():
            raise ValueError("Search term must not be empty.")

        term_lower = task_term.strip().lower()
        results = [
            task for task in self._tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished (completed).

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task exists and was marked as finished; False otherwise.

        Raises:
            ValueError: If task_id is negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        task = self._tasks.get(task_id)
        if task is not None:
            task["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[dict]:
        """
        Retrieves all tasks.

        Returns:
            List[dict]: A list of all tasks, each represented in the format:
                        {"id": int, "task_name": str, "task_description": str, "is_finished": bool}
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Clears all tasks from the manager.

        Returns:
            bool: True after clearing all tasks.
        """
        self._tasks.clear()
        # Note: The counter is not reset to maintain unique task IDs over the lifetime.
        return True


def display_task(task: dict) -> None:
    """
    Displays a task's details formatted as: (id, task_name, task_description, is_finished)

    Args:
        task (dict): The task to display.
    """
    print(f"({task['id']}, {task['task_name']}, {task['task_description']}, {task['is_finished']})")


def main() -> None:
    """
    Main loop for the console-based to-do list application.
    Provides a menu-driven interface for task operations.
    """
    manager = TaskManager()

    menu = """
Choose an option:
1. Add a task
2. Remove a task
3. Search tasks
4. Finish a task
5. List all tasks
6. Clear all tasks
7. Exit
Enter your choice: """

    while True:
        try:
            choice = input(menu).strip()
            if choice == '1':
                # Add a task
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = manager.add(name, description)
                print(f"Task added with ID: {task_id}")

            elif choice == '2':
                # Remove a task
                task_id_input = input("Enter task ID to remove: ").strip()
                if not task_id_input.isdigit():
                    print("Invalid input. Please enter a positive integer for task ID.")
                    continue
                task_id = int(task_id_input)
                success = manager.remove(task_id)
                if success:
                    print(f"Task {task_id} removed successfully.")
                else:
                    print(f"Task {task_id} not found.")

            elif choice == '3':
                # Search tasks
                search_term = input("Enter search term: ").strip()
                results = manager.search(search_term)
                if results:
                    print("Search results:")
                    for task in results:
                        display_task(task)
                else:
                    print("No matching tasks found.")

            elif choice == '4':
                # Finish a task
                task_id_input = input("Enter task ID to finish: ").strip()
                if not task_id_input.isdigit():
                    print("Invalid input. Please enter a positive integer for task ID.")
                    continue
                task_id = int(task_id_input)
                success = manager.finish(task_id)
                if success:
                    print(f"Task {task_id} marked as finished.")
                else:
                    print(f"Task {task_id} not found.")

            elif choice == '5':
                # List all tasks
                tasks = manager.get_all()
                if tasks:
                    print("All tasks:")
                    for task in tasks:
                        display_task(task)
                else:
                    print("No tasks available.")

            elif choice == '6':
                # Clear all tasks
                confirmation = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
                if confirmation == 'y':
                    manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear operation cancelled.")

            elif choice == '7':
                # Exit the application
                print("Exiting the to-do list application. Goodbye!")
                break

            else:
                print("Invalid option. Please enter a number between 1 and 7.")

        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")


if __name__ == '__main__':
    main()
