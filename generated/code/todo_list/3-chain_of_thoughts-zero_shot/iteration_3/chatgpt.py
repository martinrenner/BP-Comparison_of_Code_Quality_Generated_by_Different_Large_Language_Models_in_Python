#!/usr/bin/env python3
"""
Console-based Todo List App that meets ISO/IEC 25010 requirements.

This module defines a TaskManager class to manage tasks and provides a console-based
interface for interacting with the todo list. It demonstrates:
    - Correctness & Efficiency: Using a hash table (dict) for quick lookups.
    - Modularity: Separation of concerns via the TaskManager class and the main CLI loop.
    - Security & Validation: Checks for empty inputs, negative IDs, and type validations.
    - Readability & Documentation: Clear docstrings and comments.
"""


class TaskManager:
    """
    TaskManager manages tasks for a todo list application.

    Each task is stored as a dictionary with the following keys:
        - id: Unique integer identifier for the task.
        - task_name: Name of the task.
        - task_description: Description of the task.
        - is_finished: Boolean indicating if the task is completed.
    """

    def __init__(self):
        """Initialize the TaskManager with an empty in-memory storage for tasks."""
        self.tasks = {}  # Dictionary to store tasks for quick lookups by ID.
        self.next_id = 1  # Auto-increment task ID generator.

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task with the given name and description.

        Args:
            task_name (str): Name of the task.
            task_description (str): Description of the task.

        Returns:
            int: Unique ID of the newly added task.

        Raises:
            ValueError: If task_name or task_description is empty or only whitespace.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.

        Args:
            task_id (int): ID of the task to be removed.

        Returns:
            bool: True if the task was successfully removed; False if the task does not exist.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        else:
            return False

    def search(self, task_term: str) -> list:
        """
        Search for tasks by matching the term in task name or description.

        Args:
            task_term (str): The search term to query tasks.

        Returns:
            list[dict]: List of tasks (as dictionaries) that match the search term.

        Raises:
            ValueError: If search term is empty or not a string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        results = [
            task.copy()  # Use copy to prevent external modifications.
            for task in self.tasks.values()
            if term in task["task_name"].lower() or term in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as finished/completed by its ID.

        Args:
            task_id (int): ID of the task to mark as finished.

        Returns:
            bool: True if the task was marked finished; False if the task does not exist.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        else:
            return False

    def get_all(self) -> list:
        """
        Retrieve all tasks.

        Returns:
            list[dict]: A list of all tasks, where each task is represented as a dictionary in the format:
                        { "id": int, "task_name": str, "task_description": str, "is_finished": bool }
        """
        # Return copies to prevent external modification.
        return [task.copy() for task in self.tasks.values()]

    def clear_all(self) -> bool:
        """
        Clear all tasks from the task manager.

        Returns:
            bool: True after successfully clearing all tasks.
        """
        self.tasks.clear()
        return True


def print_task(task: dict) -> None:
    """
    Print the details of a single task.

    Args:
        task (dict): Task dictionary with keys id, task_name, task_description, is_finished.
    """
    status = "Finished" if task["is_finished"] else "Pending"
    print(f'ID: {task["id"]} | Name: {task["task_name"]} | Description: {task["task_description"]} | Status: {status}')


def main():
    """
    The main function providing a console-based interface for the todo list application.
    """
    task_manager = TaskManager()

    menu = (
        "\nTodo List App - Menu\n"
        "1. Add Task\n"
        "2. Remove Task\n"
        "3. Search Tasks\n"
        "4. Mark Task as Finished\n"
        "5. Get All Tasks\n"
        "6. Clear All Tasks\n"
        "7. Exit\n"
        "Enter your choice (1-7): "
    )

    while True:
        choice = input(menu).strip()

        if choice == "1":
            # Add Task
            try:
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = task_manager.add(task_name, task_description)
                print(f"Task added successfully with ID: {task_id}.")
            except ValueError as ve:
                print(f"Error adding task: {ve}")

        elif choice == "2":
            # Remove Task
            try:
                task_id_str = input("Enter task ID to remove: ").strip()
                task_id = int(task_id_str)
                if task_manager.remove(task_id):
                    print(f"Task ID {task_id} removed successfully.")
                else:
                    print(f"No task found with ID {task_id}.")
            except (ValueError, TypeError) as err:
                print(f"Error removing task: {err}")

        elif choice == "3":
            # Search Tasks
            try:
                search_term = input("Enter search term: ").strip()
                results = task_manager.search(search_term)
                if results:
                    print(f"Found {len(results)} matching task(s):")
                    for task in results:
                        print_task(task)
                else:
                    print("No tasks match your search.")
            except ValueError as ve:
                print(f"Error searching tasks: {ve}")

        elif choice == "4":
            # Mark Task as Finished
            try:
                task_id_str = input("Enter task ID to mark as finished: ").strip()
                task_id = int(task_id_str)
                if task_manager.finish(task_id):
                    print(f"Task ID {task_id} marked as finished.")
                else:
                    print(f"No task found with ID {task_id}.")
            except (ValueError, TypeError) as err:
                print(f"Error updating task: {err}")

        elif choice == "5":
            # Get All Tasks
            tasks = task_manager.get_all()
            if tasks:
                print("All tasks:")
                for task in tasks:
                    print_task(task)
            else:
                print("No tasks available.")

        elif choice == "6":
            # Clear All Tasks
            confirm = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
            if confirm == "y":
                task_manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Operation cancelled.")

        elif choice == "7":
            # Exit the application
            print("Exiting Todo List App. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
