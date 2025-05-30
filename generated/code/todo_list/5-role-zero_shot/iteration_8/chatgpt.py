#!/usr/bin/env python3
"""
Console-based To-Do List Application

This application implements a TaskManager class to manage tasks according
to the ISO/IEC 25010 quality standard. Each task includes an id, name,
description, and completion status. The application supports adding, removing,
searching, finishing, listing, and clearing tasks.

Author: Senior Software Developer
Date: YYYY-MM-DD
"""

from typing import List, Dict, Any


class TaskManager:
    """
    Manages tasks stored in-memory with efficient lookup and modular design.
    """

    def __init__(self) -> None:
        # Internal storage: keys are task IDs, values are task details.
        self.tasks: Dict[int, Dict[str, Any]] = {}
        # Next unique ID to be assigned to a task.
        self.next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): The name of the task; must not be an empty string.
            task_description (str): The description of the task; must not be empty.

        Returns:
            int: The unique ID assigned to the newly added task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        # Trim whitespace and validate input.
        task_name = task_name.strip()
        task_description = task_description.strip()

        if not task_name:
            raise ValueError("Task name cannot be empty.")
        if not task_description:
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task identified by its unique ID.

        Args:
            task_id (int): The ID of the task to remove. Must be a positive integer.

        Returns:
            bool: True if the task was removed successfully; False if the task does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks containing the provided term in the name or description.
        The search is case-insensitive.

        Args:
            task_term (str): The term to search for; must not be empty.

        Returns:
            List[Dict[str, Any]]: A list of tasks that match the search term.

        Raises:
            ValueError: If task_term is an empty string.
        """
        task_term = task_term.strip()
        if not task_term:
            raise ValueError("Search term cannot be empty.")

        term_lower = task_term.lower()
        matching_tasks = [
            task for task in self.tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks a given task as completed.

        Args:
            task_id (int): The ID of the task to finish. Must be a positive integer.

        Returns:
            bool: True if the task was marked as finished; False if the task does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks stored in the manager.

        Returns:
            List[Dict[str, Any]]: A list of all tasks in sorted order by their ID.
        """
        return [self.tasks[tid] for tid in sorted(self.tasks.keys())]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            bool: True upon successful deletion.
        """
        self.tasks.clear()
        self.next_id = 1  # Optionally reset task IDs.
        return True


def print_task(task: Dict[str, Any]) -> None:
    """
    Prints a single task's details in a formatted way.

    Args:
        task (Dict[str, Any]): The task dictionary to be printed.
    """
    status = "Yes" if task["is_finished"] else "No"
    print(f"ID: {task['id']} | Name: {task['task_name']} | "
          f"Description: {task['task_description']} | Finished: {status}")


def display_menu() -> None:
    """
    Displays the menu options for the console-based application.
    """
    print("\n===== To-Do List Application =====")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Search Tasks")
    print("4. Finish Task")
    print("5. Get All Tasks")
    print("6. Clear All Tasks")
    print("7. Exit")


def main() -> None:
    """
    The main function that runs the interactive console-based to-do list.
    """
    task_manager = TaskManager()

    while True:
        display_menu()
        try:
            choice = input("Enter your choice (1-7): ").strip()
            if choice == "1":
                task_name = input("Enter task name: ")
                task_description = input("Enter task description: ")
                task_id = task_manager.add(task_name, task_description)
                print(f"Task added with ID: {task_id}")

            elif choice == "2":
                id_input = input("Enter task ID to remove: ").strip()
                task_id = int(id_input)
                if task_manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"Task with ID {task_id} not found.")

            elif choice == "3":
                search_term = input("Enter search term: ")
                results = task_manager.search(search_term)
                if results:
                    print("Matching Tasks:")
                    for task in results:
                        print_task(task)
                else:
                    print("No tasks match your search.")

            elif choice == "4":
                id_input = input("Enter task ID to mark as finished: ").strip()
                task_id = int(id_input)
                if task_manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"Task with ID {task_id} not found.")

            elif choice == "5":
                all_tasks = task_manager.get_all()
                if all_tasks:
                    print("All Tasks:")
                    for task in all_tasks:
                        print_task(task)
                else:
                    print("No tasks found.")

            elif choice == "6":
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirm in ("yes", "y"):
                    task_manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear operation canceled.")

            elif choice == "7":
                print("Exiting the application. Goodbye!")
                break

            else:
                print("Invalid choice. Please choose an option between 1 and 7.")

        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
