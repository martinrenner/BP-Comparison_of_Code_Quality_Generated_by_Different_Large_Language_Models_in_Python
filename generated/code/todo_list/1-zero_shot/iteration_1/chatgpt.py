#!/usr/bin/env python3
"""
Console-based To-Do List App implementing ISO/IEC 25010 requirements.

This module contains the TaskManager class which provides methods to add, remove,
search, finish, list, and clear tasks. It also includes a simple console-based
interface for user interaction.

Author: Your Name
Date: 2023-10-05
"""


class TaskManager:
    """
    Manages tasks for a to-do list.
    
    Each task is stored as a dictionary containing:
        - id: Unique task identifier (int)
        - task_name: Name of the task (str)
        - task_description: Description of the task (str)
        - is_finished: Completion status (bool)
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and an id counter.
        """
        self.tasks = {}  # Stores tasks keyed by their unique id for efficient lookup.
        self.next_id = 1  # Incremental counter for unique task IDs.

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name of the task. Cannot be empty.
            task_description (str): A description of the task. Cannot be empty.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

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
        Removes a task by its id.

        Args:
            task_id (int): The unique task ID to remove. Must be a positive integer.

        Returns:
            bool: True if the task was successfully removed.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If no task exists with the given id.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id not in self.tasks:
            raise KeyError(f"Task with ID {task_id} does not exist.")

        del self.tasks[task_id]
        return True

    def search(self, task_term: str) -> list:
        """
        Searches for tasks that contain the search term in their name or description.

        Args:
            task_term (str): The term to search for. Cannot be empty.

        Returns:
            list[dict]: A list of tasks (as dictionaries) that match the search term.

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = task_term.strip().lower()
        results = [
            task for task in self.tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The unique ID of the task to mark as completed.

        Returns:
            bool: True if the task was successfully marked as finished.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If no task exists with the given id.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id not in self.tasks:
            raise KeyError(f"Task with ID {task_id} does not exist.")

        self.tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> list:
        """
        Retrieves all tasks with their details.

        Returns:
            list[dict]: A list of all tasks.
        """
        # Returning tasks sorted by id for consistent ordering.
        return sorted(self.tasks.values(), key=lambda task: task["id"])

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True if all tasks were successfully cleared.
        """
        self.tasks.clear()
        # Optionally, reset the ID counter.
        self.next_id = 1
        return True


def print_task(task: dict) -> None:
    """
    Prints a single task in a formatted manner.

    Args:
        task (dict): A task dictionary containing id, task_name, task_description, and is_finished.
    """
    status = "Finished" if task["is_finished"] else "Pending"
    print(f"ID: {task['id']} | Name: {task['task_name']} | Description: {task['task_description']} | Status: {status}")


def display_all_tasks(manager: TaskManager) -> None:
    """
    Retrieves and displays all tasks from the manager.

    Args:
        manager (TaskManager): The task manager instance.
    """
    tasks = manager.get_all()
    if not tasks:
        print("No tasks found.")
    else:
        print("\nAll Tasks:")
        for task in tasks:
            print_task(task)


def main():
    """
    Main function to run the console-based To-Do List App.
    """
    manager = TaskManager()

    MENU = """
    === To-Do List App ===
    Choose an option:
      1. Add a task
      2. Remove a task
      3. Search tasks
      4. Mark a task as finished
      5. Display all tasks
      6. Clear all tasks
      7. Exit
    """

    while True:
        try:
            print(MENU)
            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                # Add a task
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")

            elif choice == "2":
                # Remove a task
                id_input = input("Enter task ID to remove: ").strip()
                try:
                    task_id = int(id_input)
                except ValueError:
                    print("Invalid input. Task ID must be an integer.")
                    continue
                manager.remove(task_id)
                print(f"Task with ID {task_id} removed successfully.")

            elif choice == "3":
                # Search tasks
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                if results:
                    print(f"\nFound {len(results)} matching task(s):")
                    for task in results:
                        print_task(task)
                else:
                    print("No matching tasks found.")

            elif choice == "4":
                # Mark a task as finished
                id_input = input("Enter task ID to mark as finished: ").strip()
                try:
                    task_id = int(id_input)
                except ValueError:
                    print("Invalid input. Task ID must be an integer.")
                    continue
                manager.finish(task_id)
                print(f"Task with ID {task_id} marked as finished.")

            elif choice == "5":
                # Display all tasks
                display_all_tasks(manager)

            elif choice == "6":
                # Clear all tasks
                confirm = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
                if confirm == "y":
                    manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif choice == "7":
                # Exit the app
                print("Exiting Todo List App. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

        except ValueError as ve:
            print(f"ValueError: {ve}")
        except KeyError as ke:
            print(f"KeyError: {ke}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    main()
