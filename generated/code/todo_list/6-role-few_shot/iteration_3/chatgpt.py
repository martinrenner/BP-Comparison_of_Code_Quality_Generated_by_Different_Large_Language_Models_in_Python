#!/usr/bin/env python3
"""
A console-based to-do list application.

This module implements a TaskManager class that manages tasks and allows users
to add, remove, search, finish, retrieve, and clear tasks. The implementation
follows best practices for readability, modularity, and efficiency.
"""

from typing import List, Dict


class TaskManager:
    """
    Manages a collection of tasks.

    Each task is stored with a unique ID and includes:
        - id (int): Unique identifier for the task.
        - task_name (str): Name of the task.
        - task_description (str): Description of the task.
        - is_finished (bool): Status indicating if the task is completed.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty task store and a counter for unique IDs.
        """
        self._tasks: Dict[int, Dict[str, object]] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with the provided name and description.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the newly added task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was found and removed, False otherwise.

        Raises:
            ValueError: If task_id is negative.
        """
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict[str, object]]:
        """
        Searches for tasks that contain the given term in their name or description.

        Args:
            task_term (str): The term to search for within tasks.

        Returns:
            List[Dict[str, object]]: A list of tasks in dictionary form that match the search criteria.

        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = task_term.lower()
        results = [
            task for task in self._tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished/completed.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished, False otherwise.

        Raises:
            ValueError: If task_id is negative.
        """
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")
        task = self._tasks.get(task_id)
        if task:
            task["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[Dict[str, object]]:
        """
        Retrieves all tasks in the manager.

        Returns:
            List[Dict[str, object]]: A list of all tasks with their details.
        """
        # Return tasks sorted by ID for consistent ordering
        return [self._tasks[task_id] for task_id in sorted(self._tasks.keys())]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            bool: True after the tasks are successfully cleared.
        """
        self._tasks.clear()
        return True


def print_task(task: Dict[str, object]) -> None:
    """
    Prints the task details in a formatted way.

    Args:
        task (Dict[str, object]): A dictionary representing a task.
    """
    print(f"(ID: {task['id']}) {task['task_name']} - {task['task_description']} "
          f"[{'Finished' if task['is_finished'] else 'Pending'}]")


def display_all_tasks(manager: TaskManager) -> None:
    """
    Retrieves and prints all tasks using the TaskManager.

    Args:
        manager (TaskManager): The task manager instance containing tasks.
    """
    tasks = manager.get_all()
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print_task(task)


def main() -> None:
    """
    The main interactive loop for the console-based to-do list application.
    """
    manager = TaskManager()
    command_prompt = (
        "\nCommands:\n"
        "  add      - Add a task\n"
        "  remove   - Remove a task by ID\n"
        "  search   - Search tasks by term\n"
        "  finish   - Mark a task as finished\n"
        "  get_all  - List all tasks\n"
        "  clear_all- Remove all tasks\n"
        "  exit     - Exit the application\n"
        "Enter command: "
    )

    print("Welcome to the To-Do List Application!")
    while True:
        user_input = input(command_prompt).strip().lower()

        try:
            if user_input == "add":
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = manager.add(name, description)
                print(f"Task added with ID: {task_id}")

            elif user_input == "remove":
                id_input = input("Enter task ID to remove: ").strip()
                if not id_input.isdigit():
                    print("Invalid input. Task ID must be a positive integer.")
                    continue
                task_id = int(id_input)
                if manager.remove(task_id):
                    print(f"Task with ID {task_id} removed.")
                else:
                    print(f"No task found with ID {task_id}.")

            elif user_input == "search":
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                if not results:
                    print("No tasks match the search term.")
                else:
                    print("Matching tasks:")
                    for task in results:
                        print_task(task)

            elif user_input == "finish":
                id_input = input("Enter task ID to mark as finished: ").strip()
                if not id_input.isdigit():
                    print("Invalid input. Task ID must be a positive integer.")
                    continue
                task_id = int(id_input)
                if manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"No task found with ID {task_id}.")

            elif user_input == "get_all":
                display_all_tasks(manager)

            elif user_input == "clear_all":
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirm == "yes":
                    manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear all operation cancelled.")

            elif user_input == "exit":
                print("Exiting the application. Goodbye!")
                break

            else:
                print("Invalid command. Please try again.")

        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as ex:
            # General exception catch to ensure graceful failure.
            print(f"An unexpected error occurred: {ex}")


if __name__ == "__main__":
    main()
