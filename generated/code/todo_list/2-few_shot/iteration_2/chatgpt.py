#!/usr/bin/env python3
"""
Console-based ToDo List Application

This application implements a to-do list manager that complies with the ISO/IEC 25010 quality requirements.
It provides functions to add, remove, search, finish, retrieve all, and clear all tasks.

Usage:
    Run the script and follow the command prompts.
    Commands available:
      - add       : Add a new task.
      - remove    : Remove a task by its ID.
      - search    : Search tasks by a keyword in task name or description.
      - finish    : Mark a task as completed by its ID.
      - get_all   : Display all tasks.
      - clear_all : Remove all tasks.
      - help      : Display available commands.
      - exit      : Terminate the application.
"""

class TaskManager:
    """
    Manages tasks for a console-based to-do list application.
    
    Tasks are stored in an in-memory dictionary where each task has a unique integer ID.
    Each task is a dictionary with: id, task_name, task_description, and is_finished status.
    """
    def __init__(self):
        """
        Initializes the TaskManager with an empty task storage and initializes the ID counter.
        """
        self.tasks = {}  # Dictionary to store tasks with IDs as keys
        self.next_id = 1  # Unique ID generator for tasks

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task manager.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is empty or whitespace.
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
        Removes a task given its ID.

        Args:
            task_id (int): The unique ID of the task to be removed.

        Returns:
            bool: True if the task was removed, False if no task exists with the given ID.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            return False

        del self.tasks[task_id]
        return True

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks whose name or description includes the provided search term.
        The search is case-insensitive.

        Args:
            task_term (str): The term to search for within tasks.

        Returns:
            list[dict]: A list of tasks that match the search term in the format:
                        {'id': int, 'task_name': str, 'task_description': str, 'is_finished': bool}

        Raises:
            ValueError: If the search term is empty or whitespace.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term_lower = task_term.strip().lower()
        matching_tasks = [
            task for task in self.tasks.values()
            if term_lower in task["task_name"].lower()
            or term_lower in task["task_description"].lower()
        ]
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished/completed.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            return False

        self.tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks stored in the manager.

        Returns:
            list[dict]: A list of all tasks with details in the format:
                        {'id': int, 'task_name': str, 'task_description': str, 'is_finished': bool}
        """
        # Return tasks sorted by their ID for readability.
        return sorted(self.tasks.values(), key=lambda task: task["id"])

    def clear_all(self) -> bool:
        """
        Clears all the tasks in the task manager.

        Returns:
            bool: True after clearing all the tasks.
        """
        self.tasks.clear()
        return True

def print_task(task: dict) -> None:
    """
    Prints a single task's details in a formatted manner.

    Args:
        task (dict): A task dictionary containing details.
    """
    status = "Finished" if task["is_finished"] else "Pending"
    print(f"ID: {task['id']}, Name: {task['task_name']}, Description: {task['task_description']}, Status: {status}")

def display_all_tasks(task_manager: TaskManager) -> None:
    """
    Retrieves and displays all tasks from the task manager.

    Args:
        task_manager (TaskManager): An instance of TaskManager.
    """
    tasks = task_manager.get_all()
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print_task(task)

def print_help() -> None:
    """
    Prints the available commands for the console-based todo list app.
    """
    help_text = """
Available commands:
  add       - Add a new task
  remove    - Remove a task by its ID (Usage: remove <id>)
  search    - Search tasks by a keyword (Usage: search <term>)
  finish    - Mark a task as completed by its ID (Usage: finish <id>)
  get_all   - Display all tasks
  clear_all - Remove all tasks
  help      - Show this help message
  exit      - Exit the application
"""
    print(help_text)

def main():
    """
    The main function for the console-based todo list app.
    It processes user commands and interacts with TaskManager.
    """
    task_manager = TaskManager()
    print("Welcome to the Todo List App!")
    print_help()

    while True:
        try:
            user_input = input("Enter command: ").strip()
            if not user_input:
                continue

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()

            # Process each command
            if command == "add":
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                try:
                    task_id = task_manager.add(task_name, task_description)
                    print(f"Task added with ID: {task_id}")
                except ValueError as ve:
                    print(f"Error: {ve}")

            elif command == "remove":
                if len(parts) < 2:
                    print("Usage: remove <task_id>")
                    continue
                try:
                    task_id = int(parts[1])
                    if task_manager.remove(task_id):
                        print(f"Task {task_id} removed successfully.")
                    else:
                        print(f"Task {task_id} does not exist.")
                except ValueError:
                    print("Error: Task ID must be a positive integer.")

            elif command == "search":
                if len(parts) < 2:
                    print("Usage: search <search_term>")
                    continue
                try:
                    matching_tasks = task_manager.search(parts[1])
                    if not matching_tasks:
                        print("No matching tasks found.")
                    else:
                        print("Matching tasks:")
                        for task in matching_tasks:
                            print_task(task)
                except ValueError as ve:
                    print(f"Error: {ve}")

            elif command == "finish":
                if len(parts) < 2:
                    print("Usage: finish <task_id>")
                    continue
                try:
                    task_id = int(parts[1])
                    if task_manager.finish(task_id):
                        print(f"Task {task_id} marked as finished.")
                    else:
                        print(f"Task {task_id} does not exist.")
                except ValueError:
                    print("Error: Task ID must be a positive integer.")

            elif command == "get_all":
                display_all_tasks(task_manager)

            elif command == "clear_all":
                task_manager.clear_all()
                print("All tasks have been cleared.")

            elif command == "help":
                print_help()

            elif command == "exit":
                print("Exiting the Todo List App. Goodbye!")
                break

            else:
                print("Unknown command. Type 'help' to see available commands.")

        except Exception as e:
            # Catch-all to ensure our app does not crash unexpectedly.
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
