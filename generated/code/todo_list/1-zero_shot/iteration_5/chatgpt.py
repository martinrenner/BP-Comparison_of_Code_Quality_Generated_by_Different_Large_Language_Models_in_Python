"""
Console-based Todo List App implementing the TaskManager class with ISO/IEC 25010 requirements.

This application provides the following functionalities:
    - add(task_name, task_description) -> int
    - remove(task_id) -> bool
    - search(task_term) -> list[dict]
    - finish(task_id) -> bool
    - get_all() -> list[dict]
    - clear_all() -> bool

Usage:
    Run this module and follow the interactive prompts in the console.
"""

from typing import List, Dict


class TaskManager:
    """
    TaskManager manages an in-memory todo list with functionalities to add, remove, search,
    mark tasks as finished, retrieve all tasks, and clear all tasks.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty tasks dictionary and a counter for unique task IDs.
        """
        self.tasks: Dict[int, Dict] = {}
        self.next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with the given name and description.
        
        Args:
            task_name (str): The name of the task. Must not be empty.
            task_description (str): The description of the task. Must not be empty.
        
        Returns:
            int: The unique ID assigned to the new task.
        
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty or whitespace.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty or whitespace.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task identified by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove. Must be a positive integer.
        
        Returns:
            bool: True if the task was successfully removed.
        
        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If the task does not exist.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            raise KeyError(f"Task with ID {task_id} does not exist.")
        
        del self.tasks[task_id]
        return True

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks containing the search term in their name or description.
        
        Args:
            task_term (str): The search term. Must not be empty.
        
        Returns:
            list[dict]: A list of tasks (as dicts) matching the search criteria.
        
        Raises:
            ValueError: If the search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty or whitespace.")
        
        lower_term = task_term.lower()
        results = [
            task for task in self.tasks.values()
            if lower_term in task["task_name"].lower() or lower_term in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished (completed).
        
        Args:
            task_id (int): The unique ID of the task to mark as finished.
        
        Returns:
            bool: True if the task was successfully marked as finished.
        
        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If the task does not exist.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            raise KeyError(f"Task with ID {task_id} does not exist.")

        self.tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.
        
        Returns:
            list[dict]: A list containing all tasks with their details.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Clears all tasks from the system.
        
        Returns:
            bool: True after clearing all tasks successfully.
        """
        self.tasks.clear()
        return True


def display_task(task: Dict):
    """
    Displays task details in a formatted manner.
    
    Args:
        task (dict): A dictionary containing task details.
    """
    status = "Finished" if task["is_finished"] else "Pending"
    print(f'ID: {task["id"]} | Name: {task["task_name"]} | Description: {task["task_description"]} | Status: {status}')


def print_menu():
    """
    Prints the main menu options for the console-based todo list app.
    """
    menu = """
----- Todo List App -----
1. Add Task
2. Remove Task
3. Search Tasks
4. Mark Task as Finished
5. Get All Tasks
6. Clear All Tasks
7. Exit
-------------------------
Enter your choice (1-7): """
    print(menu, end="")


def main():
    """
    Main function for running the console-based todo list application.
    """
    manager = TaskManager()

    while True:
        print_menu()
        choice = input().strip()

        if choice == "1":
            # Add Task
            try:
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = manager.add(task_name, task_description)
                print(f"Task added successfully with ID {task_id}.\n")
            except ValueError as ve:
                print(f"Error: {ve}\n")

        elif choice == "2":
            # Remove Task
            try:
                task_id_input = input("Enter the task ID to remove: ").strip()
                if not task_id_input.isdigit():
                    print("Error: Task ID must be a positive integer.\n")
                    continue
                task_id = int(task_id_input)
                manager.remove(task_id)
                print(f"Task with ID {task_id} removed successfully.\n")
            except (ValueError, KeyError) as err:
                print(f"Error: {err}\n")

        elif choice == "3":
            # Search Tasks
            try:
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                if results:
                    print("Search Results:")
                    for task in results:
                        display_task(task)
                else:
                    print("No tasks matched your search.")
                print()
            except ValueError as ve:
                print(f"Error: {ve}\n")

        elif choice == "4":
            # Mark Task as Finished
            try:
                task_id_input = input("Enter the task ID to mark as finished: ").strip()
                if not task_id_input.isdigit():
                    print("Error: Task ID must be a positive integer.\n")
                    continue
                task_id = int(task_id_input)
                manager.finish(task_id)
                print(f"Task with ID {task_id} marked as finished.\n")
            except (ValueError, KeyError) as err:
                print(f"Error: {err}\n")

        elif choice == "5":
            # Get All Tasks
            tasks = manager.get_all()
            if tasks:
                print("All Tasks:")
                for task in tasks:
                    display_task(task)
            else:
                print("No tasks available.")
            print()

        elif choice == "6":
            # Clear All Tasks
            confirm = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
            if confirm == "y":
                manager.clear_all()
                print("All tasks cleared successfully.\n")
            else:
                print("Clear all operation cancelled.\n")

        elif choice == "7":
            # Exit
            print("Exiting the Todo List App. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option (1-7).\n")


if __name__ == "__main__":
    main()
