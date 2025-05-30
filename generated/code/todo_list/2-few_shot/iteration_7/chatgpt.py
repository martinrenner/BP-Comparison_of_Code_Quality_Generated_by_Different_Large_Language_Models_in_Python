#!/usr/bin/env python3
"""
Console-Based Todo List App

This application provides a simple console interface for managing a todo list.
It meets the ISO/IEC 25010 requirements by ensuring functionality, performance,
modularity, testability, and security in handling tasks.

Functionalities:
    - Add a new task
    - Remove an existing task
    - Search tasks by name or description
    - Mark a task as finished
    - Retrieve all the tasks
    - Clear all tasks

Usage:
    Run this script and follow the on-screen instructions.
"""

class TaskManager:
    def __init__(self):
        """
        Initializes the TaskManager with an empty task storage and ID counter.
        """
        self.tasks = {}  # Store tasks as {id: task_dict}
        self._next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a task to the todo list.

        Args:
            task_name (str): Name of the task (must be non-empty).
            task_description (str): Description of the task (must be non-empty).

        Returns:
            int: A unique task ID.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")
        
        task_id = self._next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the todo list by its ID.

        Args:
            task_id (int): The unique task ID (must be a positive integer).

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

    def search(self, task_term: str) -> list:
        """
        Searches for tasks that match the given term within their name or description.

        Args:
            task_term (str): The search term (must be non-empty).

        Returns:
            list[dict]: A list of tasks (dictionaries) that match the term.

        Raises:
            ValueError: If the search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")
        
        term_lower = task_term.lower()
        results = [
            task for task in self.tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks the specified task as finished.

        Args:
            task_id (int): The unique task ID (must be a positive integer).

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

    def get_all(self) -> list:
        """
        Retrieves all tasks with their details.

        Returns:
            list[dict]: A list of all tasks in the todo list.
        """
        # Sort tasks by their unique ID for consistency.
        return [self.tasks[tid] for tid in sorted(self.tasks.keys())]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the todo list.

        Returns:
            bool: True if all tasks were cleared successfully.
        """
        self.tasks.clear()
        return True

def display_task(task: dict):
    """
    Displays task details in a formatted output.

    Args:
        task (dict): A dictionary containing task details.
    """
    status = "Finished" if task["is_finished"] else "Pending"
    print(f"ID: {task['id']}, Name: {task['task_name']}, Description: {task['task_description']}, Status: {status}")

def print_menu():
    """
    Displays the main menu for the Todo List App.
    """
    print("\n====== Todo List App ======")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Search Tasks")
    print("4. Finish Task")
    print("5. Get All Tasks")
    print("6. Clear All Tasks")
    print("7. Exit")
    print("===========================")

def main():
    """
    Entry point for the console-based todo list application.
    """
    manager = TaskManager()

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            # Add Task
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "2":
            # Remove Task
            try:
                task_id = int(input("Enter task ID to remove: "))
                if manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "3":
            # Search Tasks
            try:
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                if results:
                    print("\nSearch Results:")
                    for task in results:
                        display_task(task)
                else:
                    print("No matching tasks found.")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "4":
            # Finish Task
            try:
                task_id = int(input("Enter task ID to mark as finished: "))
                if manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "5":
            # Get All Tasks
            tasks = manager.get_all()
            if tasks:
                print("\nAll Tasks:")
                for task in tasks:
                    display_task(task)
            else:
                print("No tasks available.")

        elif choice == "6":
            # Clear All Tasks
            confirm = input("Are you sure you want to clear all tasks? (y/N): ").strip().lower()
            if confirm == "y":
                if manager.clear_all():
                    print("All tasks cleared successfully.")
            else:
                print("Clear operation cancelled.")

        elif choice == "7":
            print("Exiting Todo List App. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
