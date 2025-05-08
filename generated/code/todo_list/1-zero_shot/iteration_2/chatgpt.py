"""
Console-based Todo List Application

This module implements a todo list manager using the TaskManager class.
It meets the requirements of ISO/IEC 25010 by ensuring the solution is:
- Functional: Provides methods to add, remove, search, finish, list, and clear tasks.
- Efficient: Uses dictionaries for O(1) insertions, lookups, and removals.
- Modular & Maintainable: Uses object-oriented programming with clear method interfaces.
- Secure: Validates inputs and raises appropriate built-in errors.
- Testable: Well-defined methods and clear separation of concerns.
"""

from typing import List, Dict


class TaskManager:
    """
    TaskManager manages tasks stored in-memory. Each task is represented as a
    dictionary with keys: id, task_name, task_description, and is_finished.
    """

    def __init__(self) -> None:
        """
        Initialize a new TaskManager with an empty task collection and
        an auto-incrementing task ID.
        """
        self.tasks: Dict[int, Dict] = {}
        self.next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
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
        Remove a task by its unique ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was removed; False if not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        else:
            return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description containing the search term.

        Args:
            task_term (str): The search term.

        Returns:
            List[Dict]: A list of matching tasks.

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.lower().strip()
        matching_tasks = [
            task for task in self.tasks.values()
            if term in task["task_name"].lower() or term in task["task_description"].lower()
        ]
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as finished.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if the task was marked as finished; False if task not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        else:
            return False

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.

        Returns:
            List[Dict]: A list of all tasks, each represented as a dictionary.
        """
        return [self.tasks[tid] for tid in sorted(self.tasks)]

    def clear_all(self) -> bool:
        """
        Remove all tasks.

        Returns:
            bool: True after clearing all tasks.
        """
        self.tasks.clear()
        return True


def print_task(task: Dict) -> None:
    """
    Helper function to print a task's details.
    
    Args:
        task (Dict): The task dictionary.
    """
    status = "Finished" if task["is_finished"] else "Pending"
    print(f"ID: {task['id']}, Name: {task['task_name']}, "
          f"Description: {task['task_description']}, Status: {status}")


def main() -> None:
    """
    Main function providing a console-based interface to the todo list app.
    """
    task_manager = TaskManager()

    menu = """
Todo List Application:
1. Add task
2. Remove task
3. Search tasks
4. Mark task as finished
5. Get all tasks
6. Clear all tasks
7. Exit
"""
    while True:
        print(menu)
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            # Add task
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == '2':
            # Remove task
            try:
                task_id_input = input("Enter task ID to remove: ").strip()
                task_id = int(task_id_input)
                if task_manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"Task with ID {task_id} not found.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == '3':
            # Search tasks
            try:
                term = input("Enter search term: ").strip()
                results = task_manager.search(term)
                if results:
                    print("Matching Tasks:")
                    for task in results:
                        print_task(task)
                else:
                    print("No tasks match your search.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == '4':
            # Mark task as finished
            try:
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                task_id = int(task_id_input)
                if task_manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"Task with ID {task_id} not found.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == '5':
            # Get all tasks
            tasks = task_manager.get_all()
            if tasks:
                print("All Tasks:")
                for task in tasks:
                    print_task(task)
            else:
                print("No tasks available.")

        elif choice == '6':
            # Clear all tasks
            confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirm == 'yes':
                task_manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Clear all cancelled.")

        elif choice == '7':
            # Exit
            print("Exiting the Todo List Application. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option (1-7).")


if __name__ == "__main__":
    main()
