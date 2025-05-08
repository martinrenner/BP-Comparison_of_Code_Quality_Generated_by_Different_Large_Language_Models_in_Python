#!/usr/bin/env python3
"""
Console-based Todo List App based on ISO/IEC 25010 requirements.

This app implements a TaskManager class which provides the following functions:
- add(task_name: str, task_description: str) -> int
- remove(task_id: int) -> bool
- search(task_term: str) -> list[dict]
- finish(task_id: int) -> bool
- get_all() -> list[dict]
- clear_all() -> bool

Tasks are stored in memory with an auto-incremented unique identifier.
Each task is represented as a dictionary in the format:
    { "id": int, "task_name": str, "task_description": str, "is_finished": bool }
"""

class TaskManager:
    def __init__(self):
        """Initialize the TaskManager with an empty task store and id counter."""
        self.tasks = {}  # Dictionary to store tasks by their unique id for O(1) access.
        self.next_id = 1  # Auto-increment task ID

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): Name of the task. Must be non-empty.
            task_description (str): Description of the task. Must be non-empty.

        Returns:
            int: The unique ID assigned to the added task.

        Raises:
            ValueError: If task_name or task_description is empty.
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
        Removes a task by its ID.

        Args:
            task_id (int): The unique ID of the task to remove. Must be a positive integer.

        Returns:
            bool: True if the task was removed successfully, False if the task does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks whose name or description include the given search term (case-insensitive).

        Args:
            task_term (str): The term to search for. Must be a non-empty string.

        Returns:
            list[dict]: A list of dictionaries representing tasks that match the search.
                        The format of each task is: {id, task_name, task_description, is_finished}.

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term_lower = task_term.lower()
        matching_tasks = [
            task for task in self.tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The unique ID of the task to mark as completed. Must be a positive integer.

        Returns:
            bool: True if the task was marked as finished, False if the task does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks stored in the TaskManager.

        Returns:
            list[dict]: A list of all tasks in the format {id, task_name, task_description, is_finished}
        """
        # Return tasks sorted by their ID for predictability.
        return [self.tasks[task_id] for task_id in sorted(self.tasks)]

    def clear_all(self) -> bool:
        """
        Removes all tasks from the TaskManager.

        Returns:
            bool: True when all tasks have been successfully cleared.
        """
        self.tasks.clear()
        self.next_id = 1
        return True


def print_task(task: dict) -> None:
    """
    Utility function to print a task in the required format.
    
    Args:
        task (dict): A dictionary representing a task.
    """
    print(f"(ID: {task['id']}, Name: {task['task_name']}, "
          f"Description: {task['task_description']}, Finished: {task['is_finished']})")


def display_menu() -> None:
    """
    Prints the command menu.
    """
    print("\nTodo List App - Commands:")
    print("  add      -> Add a new task")
    print("  remove   -> Remove a task by ID")
    print("  search   -> Search tasks by a term")
    print("  finish   -> Mark a task as completed by ID")
    print("  list     -> List all tasks")
    print("  clear    -> Clear all tasks")
    print("  help     -> Show this menu")
    print("  exit     -> Exit the app")


def main():
    """
    Main function to run the console-based todo list application.
    """
    task_manager = TaskManager()
    print("Welcome to the Todo List App!")
    display_menu()

    while True:
        command = input("\nEnter a command (type 'help' for available commands): ").strip().lower()

        if command == "add":
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif command == "remove":
            try:
                id_str = input("Enter task ID to remove: ").strip()
                if not id_str.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(id_str)
                if task_manager.remove(task_id):
                    print(f"Task {task_id} removed successfully.")
                else:
                    print(f"Task with ID {task_id} does not exist.")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif command == "search":
            try:
                term = input("Enter search term: ").strip()
                results = task_manager.search(term)
                if results:
                    print("Matching tasks:")
                    for task in results:
                        print_task(task)
                else:
                    print("No matching tasks found.")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif command == "finish":
            try:
                id_str = input("Enter task ID to mark as finished: ").strip()
                if not id_str.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(id_str)
                if task_manager.finish(task_id):
                    print(f"Task {task_id} marked as finished.")
                else:
                    print(f"Task with ID {task_id} does not exist.")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif command == "list":
            tasks = task_manager.get_all()
            if tasks:
                print("All tasks:")
                for task in tasks:
                    print_task(task)
            else:
                print("No tasks found.")

        elif command == "clear":
            confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirmation == "yes":
                task_manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Clear operation cancelled.")

        elif command == "help":
            display_menu()

        elif command == "exit":
            print("Exiting the Todo List App. Goodbye!")
            break

        else:
            print("Invalid command. Please try again or type 'help' for available commands.")


if __name__ == '__main__':
    main()
