from typing import List, Dict


class TaskManager:
    """
    A manager for handling tasks in a console-based to-do list application.

    Each task is stored with a unique id, a task name, a task description, and its completion state.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty in-memory storage and an auto-incrementing task ID.
        """
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name (str): The name of the task. Must be a non-empty string.
            task_description (str): The description of the task. Must be a non-empty string.

        Returns:
            int: The unique identifier assigned to the newly added task.

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
            "is_finished": False,
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the to-do list by its unique identifier.

        Args:
            task_id (int): The unique identifier of the task to remove.
        
        Returns:
            bool: True if the task was removed successfully, False if the task does not exist.
        
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task id must be a positive integer.")
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks that match a given search term in the task name or description.

        Args:
            task_term (str): The search term to look for in task names and descriptions.
        
        Returns:
            List[Dict]: A list of tasks (as dictionaries) that match the search criteria.
                        Each task dictionary is formatted as:
                        {"id": int, "task_name": str, "task_description": str, "is_finished": bool}
        
        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")
        search_lower = task_term.lower()
        results = [
            task.copy()
            for task in self._tasks.values()
            if search_lower in task["task_name"].lower()
            or search_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished (completed).

        Args:
            task_id (int): The unique identifier of the task to mark as finished.
        
        Returns:
            bool: True if the task was successfully marked as finished,
                  False if the task does not exist.
        
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task id must be a positive integer.")
        task = self._tasks.get(task_id)
        if task is None:
            return False
        task["is_finished"] = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks stored in the to-do list.

        Returns:
            List[Dict]: A list of all tasks, each represented as a dictionary containing:
                        "id", "task_name", "task_description", and "is_finished".
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the to-do list.

        Returns:
            bool: True after successfully clearing all tasks.
        """
        self._tasks.clear()
        return True


def main() -> None:
    """
    The main function to run the console-based to-do list application.
    Provides a simple command-line interface for users to interact with the TaskManager.
    """
    manager = TaskManager()
    print("Welcome to the Console-based To-Do List Application")
    print("Available commands: add, remove, search, finish, list, clear, exit")

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == "add":
            try:
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = manager.add(task_name, task_description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as error:
                print(f"Error: {error}")

        elif command == "remove":
            try:
                task_id_str = input("Enter task ID to remove: ").strip()
                if not task_id_str.isdigit():
                    print("Error: Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_str)
                if manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"No task found with ID {task_id}.")
            except ValueError as error:
                print(f"Error: {error}")

        elif command == "search":
            try:
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                if results:
                    print("Search results:")
                    for task in results:
                        # Format: (id, task_name, task_description, is_finished)
                        print(f"({task['id']}, {task['task_name']}, {task['task_description']}, {task['is_finished']})")
                else:
                    print("No matching tasks found.")
            except ValueError as error:
                print(f"Error: {error}")

        elif command == "finish":
            try:
                task_id_str = input("Enter task ID to mark as finished: ").strip()
                if not task_id_str.isdigit():
                    print("Error: Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_str)
                if manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"No task found with ID {task_id}.")
            except ValueError as error:
                print(f"Error: {error}")

        elif command == "list":
            tasks = manager.get_all()
            if tasks:
                print("Task List:")
                for task in tasks:
                    print(f"({task['id']}, {task['task_name']}, {task['task_description']}, {task['is_finished']})")
            else:
                print("No tasks available.")

        elif command == "clear":
            confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirm == "yes":
                manager.clear_all()
                print("All tasks cleared.")
            else:
                print("Clear operation canceled.")

        elif command == "exit":
            print("Exiting application. Goodbye!")
            break

        else:
            print("Invalid command. Available commands: add, remove, search, finish, list, clear, exit")


if __name__ == "__main__":
    main()
