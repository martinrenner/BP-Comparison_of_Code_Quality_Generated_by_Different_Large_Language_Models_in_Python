"""
Console-based Todo List Application using a TaskManager class.

This application provides functionality to manage tasks with operations to add, remove, search,
finish, retrieve all, and clear all tasks. Each task is stored in an in-memory data structure with
a unique ID, task name, description, and completion status.

This implementation conforms to ISO/IEC 25010 quality requirements regarding functionality,
performance, modularity, security, testability, and readability.
"""

from typing import List, Dict


class TaskManager:
    """
    Manages tasks with operations to add, remove, search, finish, retrieve, and clear tasks.
    """

    def __init__(self):
        """
        Initializes a new TaskManager instance with an empty task dictionary and a counter for unique IDs.
        """
        self.tasks: Dict[int, dict] = {}
        self.next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name of the task. Must be a non-empty string.
            task_description (str): The description of the task. Must be a non-empty string.

        Returns:
            int: The unique ID of the newly added task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self.next_id
        self.tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The unique ID of the task to be removed.

        Returns:
            bool: True if the task was successfully removed, False if the task does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[dict]:
        """
        Searches tasks by name or description for a given search term (case-insensitive).

        Args:
            task_term (str): The search term to match within task names or descriptions.

        Returns:
            list[dict]: A list of task dictionaries that match the search term.

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term_lower = task_term.lower()
        matching_tasks = [
            task for task in self.tasks.values()
            if term_lower in task['task_name'].lower() or term_lower in task['task_description'].lower()
        ]
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The unique ID of the task to mark as completed.

        Returns:
            bool: True if the task was found and marked as finished, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]['is_finished'] = True
            return True
        return False

    def get_all(self) -> List[dict]:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: A list containing all task dictionaries.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True after clearing all tasks.
        """
        self.tasks.clear()
        return True


def print_menu() -> None:
    """
    Displays the main menu options for the Todo List App.
    """
    print("\n--- Todo List App Menu ---")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Search Tasks")
    print("4. Finish Task")
    print("5. Get All Tasks")
    print("6. Clear All Tasks")
    print("7. Exit")


def main() -> None:
    """
    The main function which drives the console-based Todo List App.
    """
    manager = TaskManager()

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            # Add Task
            try:
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = manager.add(task_name, task_description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '2':
            # Remove Task
            try:
                task_id_input = input("Enter task ID to remove: ").strip()
                task_id = int(task_id_input)
                if manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"No task found with ID {task_id}.")
            except (ValueError, TypeError) as e:
                print(f"Error: Please provide a valid positive integer for task ID. {e}")

        elif choice == '3':
            # Search Tasks
            try:
                search_term = input("Enter search term: ").strip()
                results = manager.search(search_term)
                if results:
                    print("Matching Tasks:")
                    for task in results:
                        finished_status = "Finished" if task['is_finished'] else "Not Finished"
                        print(f"ID: {task['id']}, Name: {task['task_name']}, Description: {task['task_description']}, Status: {finished_status}")
                else:
                    print("No matching tasks found.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '4':
            # Finish Task
            try:
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                task_id = int(task_id_input)
                if manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"No task found with ID {task_id}.")
            except (ValueError, TypeError) as e:
                print(f"Error: Please provide a valid positive integer for task ID. {e}")

        elif choice == '5':
            # Get All Tasks
            all_tasks = manager.get_all()
            if all_tasks:
                print("All Tasks:")
                for task in all_tasks:
                    finished_status = "Finished" if task['is_finished'] else "Not Finished"
                    print(f"ID: {task['id']}, Name: {task['task_name']}, Description: {task['task_description']}, Status: {finished_status}")
            else:
                print("Task list is empty.")

        elif choice == '6':
            # Clear All Tasks
            confirm = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
            if confirm == 'y':
                manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Clear all tasks operation canceled.")

        elif choice == '7':
            # Exit Application
            print("Exiting the Todo List App. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a number between 1 and 7.")


if __name__ == "__main__":
    main()
