"""
Console-based Todo List Application

This module implements a console-based todo list application using OOP.
The TaskManager class provides functionality to add, remove, search,
finish, display, and clear tasks. The application adheres to high-quality
standards inspired by ISO/IEC 25010 requirements.

Features:
    - Add a task with a name and description.
    - Remove a task by its unique ID.
    - Search for tasks by a term in the name or description.
    - Mark a task as finished.
    - Retrieve all tasks.
    - Clear all tasks.

Error Handling:
    - Validates inputs (e.g., non-empty strings, valid integer IDs).
    - Gracefully handles errors for non-existent tasks.
    
Data Storage & Efficiency:
    - Uses an in-memory dictionary for task storage for O(1) lookup, insertion,
      and deletion operations.

Usage:
    Run this file and follow the on-screen instructions to interact with the todo list.
"""

import sys


class TaskManager:
    """
    A manager for tasks in a todo list application.
    
    Attributes:
        tasks (dict): Dictionary storing tasks with task_id as keys.
        next_task_id (int): A counter for generating unique task IDs.
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task list and counter."""
        self.tasks = {}  # Mapping from task_id to task dictionary.
        self.next_task_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.
            
        Returns:
            int: The unique task ID assigned to the new task.
            
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self.next_task_id
        self.tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False
        }
        self.next_task_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed; False if the task does not exist.
            
        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Search for tasks that contain the given term in their name or description.
        
        Args:
            task_term (str): The term to search for.
            
        Returns:
            list[dict]: A list of matching tasks, each represented as a dictionary.
            
        Raises:
            ValueError: If task_term is an empty string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        results = []
        for task in self.tasks.values():
            if term in task['task_name'].lower() or term in task['task_description'].lower():
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as finished.
        
        Args:
            task_id (int): The unique ID of the task to mark as finished.
            
        Returns:
            bool: True if the task was marked as finished; False if the task does not exist.
            
        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        task = self.tasks.get(task_id)
        if task:
            task['is_finished'] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieve all tasks from the todo list.
        
        Returns:
            list[dict]: A list of all tasks, with each task represented as a dictionary.
        """
        # Returning tasks sorted by task ID for consistent order.
        return [self.tasks[tid] for tid in sorted(self.tasks)]

    def clear_all(self) -> bool:
        """
        Remove all tasks from the todo list.
        
        Returns:
            bool: True after successfully clearing all tasks.
        """
        self.tasks.clear()
        self.next_task_id = 1
        return True


def print_task(task: dict):
    """
    Pretty-print a single task.
    
    Args:
        task (dict): The task dictionary to print.
    """
    status = "Finished" if task['is_finished'] else "Not Finished"
    print(f"ID: {task['id']} | Name: {task['task_name']} | Description: {task['task_description']} | Status: {status}")


def display_tasks(task_manager: TaskManager):
    """
    Display all tasks in the console.
    
    Args:
        task_manager (TaskManager): The instance of TaskManager.
    """
    tasks = task_manager.get_all()
    if not tasks:
        print("No tasks available.")
        return
    print("Current Tasks:")
    for task in tasks:
        print_task(task)


def main():
    """
    Main loop for the console-based todo list application.
    
    Handles user input to interact with the TaskManager.
    """
    task_manager = TaskManager()

    instructions = (
        "\nCommands:\n"
        "  add         - Add a new task\n"
        "  remove      - Remove a task by its ID\n"
        "  search      - Search tasks by name/description\n"
        "  finish      - Mark a task as finished\n"
        "  get_all     - Display all tasks\n"
        "  clear_all   - Remove all tasks\n"
        "  help        - Show instructions\n"
        "  exit        - Exit the application\n"
    )

    print("Welcome to the Todo List Application!")
    print(instructions)

    while True:
        command = input("\nEnter a command: ").strip().lower()

        try:
            if command == "add":
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")

            elif command == "remove":
                try:
                    task_id_input = input("Enter task ID to remove: ").strip()
                    task_id = int(task_id_input)
                except ValueError:
                    print("Invalid input. Task ID must be an integer.")
                    continue
                if task_manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"Task with ID {task_id} does not exist.")

            elif command == "search":
                term = input("Enter search term: ").strip()
                results = task_manager.search(term)
                if results:
                    print(f"Found {len(results)} task(s):")
                    for task in results:
                        print_task(task)
                else:
                    print("No matching tasks found.")

            elif command == "finish":
                try:
                    task_id_input = input("Enter task ID to mark as finished: ").strip()
                    task_id = int(task_id_input)
                except ValueError:
                    print("Invalid input. Task ID must be an integer.")
                    continue
                if task_manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"Task with ID {task_id} does not exist.")

            elif command == "get_all":
                display_tasks(task_manager)

            elif command == "clear_all":
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirm == "yes":
                    task_manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Clear operation cancelled.")

            elif command == "help":
                print(instructions)

            elif command == "exit":
                print("Exiting the Todo List Application. Goodbye!")
                sys.exit(0)

            else:
                print("Unknown command. Type 'help' to see the list of commands.")

        except (ValueError, TypeError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
